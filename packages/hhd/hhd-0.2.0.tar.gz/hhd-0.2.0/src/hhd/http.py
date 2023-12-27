import json
import logging
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Condition, Thread
from typing import Any, Mapping
from urllib.parse import parse_qs, urlparse

from .plugins import Config, Emitter, HHDSettings

logger = logging.getLogger(__name__)

STANDARD_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Credentials": "true",
    "WWW-Authenticate": "Bearer",
}

ERROR_HEADERS = {**STANDARD_HEADERS, "Content-type": "text / plain"}
AUTH_HEADERS = ERROR_HEADERS
OK_HEADERS = {**STANDARD_HEADERS, "Content-type": "text / json"}


def parse_path(path: str) -> tuple[list, dict[str, list[str]]]:
    try:
        url = urlparse(path)
        if url.path:
            segments = url.path[1:].split("/")
        else:
            segments = []

        params = {k: v for k, v in parse_qs(url.query).items() if v}
        return segments, params
    except Exception:
        return [], {}


class RestHandler(BaseHTTPRequestHandler):
    settings: HHDSettings
    cond: Condition
    conf: Config
    profiles: Mapping[str, Config]
    emit: Emitter
    token: str | None

    def set_response(self, code: int, headers: dict[str, str] = {}):
        self.send_response(code)
        for title, head in headers.items():
            self.send_header(title, head)
        self.end_headers()

    def is_authenticated(self):
        if not self.token:
            return True

        auth = self.headers["Authorization"]
        if not auth:
            return False

        if not isinstance(auth, str):
            return False

        if not auth.lower().startswith("bearer "):
            return False

        return auth.lower()[len("Bearer ") :] == self.token

    def send_authenticate(self):
        if self.is_authenticated():
            return True

        self.set_response(401, {"Content-type": "text / plain"})
        self.wfile.write(
            f"Handheld Daemon Error: Authentication is on and you did not supply the proper bearer token.".encode()
        )

        return False

    def send_json(self, data: Any):
        self.set_response_ok()
        self.wfile.write(json.dumps(data).encode())

    def set_response_ok(self):
        self.set_response(200, STANDARD_HEADERS)

    def send_not_found(self, error: str):
        self.set_response(400, ERROR_HEADERS)
        self.wfile.write(b"Handheld Daemon Error (404, invalid endpoint):\n")
        self.wfile.write(error.encode())

    def send_error(self, error: str):
        self.set_response(404, ERROR_HEADERS)
        self.wfile.write(b"Handheld Daemon Error:\n")
        self.wfile.write(error.encode())

    def handle_profile(
        self, segments: list[str], params: dict[str, list[str]], content: Any | None
    ):
        if not segments:
            return self.send_not_found(
                f"No endpoint provided for '/profile/...', (e.g., list, get, set, apply)"
            )

        with self.cond:
            match segments[0]:
                case "list":
                    self.send_json(list(self.profiles))
                case "get":
                    if "profile" not in params:
                        return self.send_error(f"Profile not specified")
                    profile = params["profile"][0]
                    if profile not in self.profiles:
                        return self.send_error(f"Profile '{profile}' not found.")
                    self.send_json(self.profiles[profile].conf)
                case "set":
                    if "profile" not in params:
                        return self.send_error(f"Profile not specified")
                    if not content:
                        return self.send_error(f"Data for the profile not sent.")

                    profile = params["profile"][0]
                    self.emit(
                        {"type": "profile", "name": profile, "config": Config(content)}
                    )
                    # Wait for the profile to be processed
                    self.cond.wait()

                    # Return the profile
                    if profile in self.profiles:
                        self.send_json(self.profiles[profile].conf)
                    else:
                        self.send_error(f"Applied profile not found (race condition?).")
                case "apply":
                    if "profile" not in params:
                        return self.send_error(f"Profile not specified")

                    profiles = params["profile"]
                    for p in profiles:
                        if p not in self.profiles:
                            return self.send_error(f"Profile '{p}' not found.")

                    self.emit([{"type": "apply", "name": p} for p in profiles])
                    # Wait for the profile to be processed
                    self.cond.wait()
                    # Return the profile
                    self.send_json(self.conf.conf)

    def v1_endpoint(self, content: Any | None):
        segments, params = parse_path(self.path)
        if not segments:
            return self.send_not_found(f"Empty path.")

        if segments[0] != "v1":
            return self.send_not_found(
                f"Only v1 endpoint is supported by this version of hhd (requested '{segments[0]}')."
            )

        if len(segments) == 1:
            return self.send_not_found(f"No command provided")

        command = segments[1].lower()
        match command:
            case "profile":
                self.handle_profile(segments[2:], params, content)
            case "settings":
                self.set_response_ok()
                with self.cond:
                    self.wfile.write(json.dumps(self.settings).encode())
            case "state":
                self.set_response_ok()
                with self.cond:
                    if content:
                        self.emit({"type": "state", "config": Config(content)})
                        self.cond.wait()
                    self.wfile.write(json.dumps(self.conf.conf).encode())
            case other:
                self.send_not_found(f"Command '{other}' not supported.")

    def do_GET(self):
        if not self.send_authenticate():
            return

        self.v1_endpoint(None)

    def do_POST(self):
        if not self.send_authenticate():
            return

        content_length = int(self.headers["Content-Length"])
        content = self.rfile.read(content_length)
        try:
            content_json = json.loads(content)
        except Exception as e:
            return self.send_error(
                f"Parsing the POST content as json failed with the following error:\n{e}"
            )
        self.v1_endpoint(content_json)

    def log_message(self, format: str, *args: Any) -> None:
        pass


class HHDHTTPServer:
    def __init__(
        self,
        localhost: bool,
        port: int,
        token: str | None,
    ) -> None:
        self.localhost = localhost
        self.port = port

        # Have to subclass to create closure
        class NewRestHandler(RestHandler):
            pass

        cond = Condition()
        NewRestHandler.cond = cond
        NewRestHandler.token = token
        self.cond = cond
        self.handler = NewRestHandler
        self.https = None
        self.t = None

    def update(
        self,
        settings: HHDSettings,
        conf: Config,
        profiles: Mapping[str, Config],
        emit: Emitter,
    ):
        with self.cond:
            self.handler.settings = settings
            self.handler.conf = conf
            self.handler.profiles = profiles
            self.handler.emit = emit
            self.cond.notify_all()

    def open(self):
        self.https = HTTPServer(
            ("127.0.0.1" if self.localhost else "", self.port), self.handler
        )
        self.t = Thread(target=self.https.serve_forever)
        self.t.start()

    def close(self):
        if self.https and self.t:
            with self.cond:
                self.cond.notify_all()
            self.https.shutdown()
            self.t.join()
            self.https = None
            self.t = None
