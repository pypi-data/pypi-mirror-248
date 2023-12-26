from base64 import b64encode
from http import HTTPStatus
from logging import Logger
import http.server
import socketserver
from socketserver import BaseRequestHandler
from urllib.parse import urlparse, parse_qs
from simpleworkspace.logproviders import DummyLogger, StdoutLogger
import ssl
import subprocess
from simpleworkspace.utility.linq import LINQ


class BasicRequestHandler(http.server.SimpleHTTPRequestHandler):
    """
    Class should always be derived and supplied into BasicServer

    Methods that may be overridden:
    - OnRequest()       , this is the main start point for the implementer and may be overriden to suite api needs.
    - GetPage_Index()   , placeholder/boilerplate function runs on entry path '/' with empty query      (if OnRequest is not overriden)
    - OnRequest_Action(), placeholder/boilerplate function that triggers when action param is specified (if OnRequest is not overriden)
    """

    # just to update intellisense
    server = None  # type: BasicServer

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Signals:
        class StopRequest(Exception):
            pass

    # override, original writes to standard outputs, which fails if app is pyw
    def log_message(self, format, *args):
        self.server.logger.debug(f"{self.address_string()} - {format % args}")

    def SendResponse_Raw(self, data: str, statusCode=HTTPStatus.OK, contentType="text/html", customHeaders: dict[str, str] = {}):
        self.send_response(statusCode.value)
        customHeaders["Content-type"] = contentType  # incase of duplicate, contentType param is preffered
        for key, value in customHeaders.items():
            self.send_header(key, value)
        self.end_headers()
        self.wfile.write(data.encode())
        return

    def _Routine_BasicAuth(self):
        if self.server.Config.Authentication._BasicKey is None:
            return # no auth configured

        if self.headers.get("Authorization") == self.server.Config.Authentication._BasicKey:
            return

        self.SendResponse_Raw("Authorization required.", HTTPStatus.UNAUTHORIZED, customHeaders={"WWW-Authenticate": 'Basic realm="Login Required"'})
        raise self.Signals.StopRequest()

    def BeforeRequest(self, method:str, path:str, query:dict[str,str]):
        pass

    def _DefaultBeforeRequest(self, method:str, path:str, query:dict[str,str]):
        # when basic auth is enabled, checks if current client is authorized
        self._Routine_BasicAuth()  # throws a stoprequest exception if not passed

    def OnRequest(self, method:str, path:str, query:dict[str,str]):
        '''This can be overriden freely, below is simply implementing boilerplate code'''
        if(method == 'GET'):
            if(path == '/' and len(query) == 0):
                self.GetPage_Index()
            elif("action" in query):
                data = query['data'] if 'data' in query else None
                return self.OnRequest_Action(query['action'], data)
        
    def GetPage_Index(self):
        '''boilerplate method'''
        #self.SendResponse_Raw(sw.io.file.Read("./index.html"))

    def OnRequest_Action(self, action: str, data: str=None):
        '''boilerplate method'''

    def handle_one_request(self):
        """Handle a single HTTP request.

        You normally don't need to override this method; see the class
        __doc__ string for information on how to handle specific HTTP
        commands such as GET and POST.

        """
        try:
            self.raw_requestline = self.rfile.readline(65537)
            if len(self.raw_requestline) > 65536:
                self.requestline = ""
                self.request_version = ""
                self.command = ""
                self.send_error(HTTPStatus.REQUEST_URI_TOO_LONG)
                return
            if not self.raw_requestline:
                self.close_connection = True
                return
            if not self.parse_request():
                # An error code has been sent, just exit
                return
            
            parsedUrl = urlparse(self.path)
            query_components = parse_qs(parsedUrl.query)
            for key in query_components.keys():
                query_components[key] = query_components[key][0] #only keep the first matching query key, discard duplicates for simplicity
            try:
                self._DefaultBeforeRequest(self.command, parsedUrl.path, query_components)
                self.BeforeRequest(self.command, parsedUrl.path, query_components)
                self.OnRequest(self.command, parsedUrl.path, query_components)
            except self.Signals.StopRequest:
                pass  # a graceful request cancellation

            self.wfile.flush()  # actually send the response if not already done.
        except TimeoutError as e:
            # a read or a write timed out.  Discard this connection
            self.server.logger.exception("Request timed out")
            self.close_connection = True
            return

class _BasicServerConfiguration:
    class _Authentication:
        _BasicKey:str = None
    class _SSL:
        _Filepath_Certificate:str = None
        _Filepath_Privatekey:str = None
    
    def __init__(self):
        self.Port: int = None
        self.Host:str = ''
        self.Authentication = self._Authentication()
        self.SSL = self._SSL()


class BasicServer(socketserver.ThreadingTCPServer):
    def __init__(self, port: int, requestHandler: BaseRequestHandler):
        self.Config = _BasicServerConfiguration()
        self.logger = DummyLogger.GetLogger()

        super().__init__(("", port), requestHandler, bind_and_activate=False)

    def UseLogger(self, logger: Logger):
        self.logger = logger

    def UseAuthorization_Basic(self, username: str, password: str):
        """Uses http basic auth before any request is accepted, one of username or password can be left empty"""
        self.Config.Authentication._BasicKey = "Basic " + b64encode(f"{username}:{password}".encode()).decode()

    def GenerateSelfSignedSSLCertificates(self, certificateOutPath = 'cert.crt', PrivateKeyOutPath = 'cert.key'):
        if(not certificateOutPath.endswith(".crt")) or (not PrivateKeyOutPath.endswith('.key')):
            raise Exception("wrong file extensions used for certs")
        result = subprocess.run(
            ["openssl", 
                "req", "-x509", ""
                "-newkey", "rsa:4096", 
                "-keyout", PrivateKeyOutPath, "-out", certificateOutPath, 
                "-days", str(365), 
                "-nodes",
                "-subj", "/C=US/CN=*"
            ],text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if result.returncode != 0:  # something went bad
            raise Exception(result.stderr, result.stdout)

    def UseSSL(self, certificatePath: str, PrivateKeyPath: str):
        self.Config.SSL._Filepath_Certificate = certificatePath
        self.Config.SSL._Filepath_Privatekey = PrivateKeyPath

    def serve_forever(self, poll_interval: float = 0.5) -> None:
        if self.Config.SSL._Filepath_Certificate is not None:
            self.socket = ssl.wrap_socket(self.socket,certfile=self.Config.SSL._Filepath_Certificate, keyfile=self.Config.SSL._Filepath_Privatekey, server_side=True)
        try:
            self.server_bind()
            self.server_activate()
        except:
            self.server_close()
            raise

        self.logger.info(f"Server started at port {self.server_address[1]}")
        return super().serve_forever(poll_interval)

# #BasicRequestHandler would be overriden for implementer
# server = BasicServer(1234, BasicRequestHandler)
# server.UseLogger(StdoutLogger.GetLogger())
# server.UseAuthorization_Basic("admin", "123")
# server.serve_forever()
