"""Internet requesting access methods"""


class _bm:
    from http.client import HTTPSConnection, HTTPConnection, InvalidURL, RemoteDisconnected
    from ssl import SSLCertVerificationError, SSLContext
    from json import dumps, loads, JSONDecodeError
    from gzip import decompress, BadGzipFile
    from os.path import abspath, exists
    from shutil import copyfileobj
    from logging import getLogger
    from typing import Any, Union
    from base64 import b64encode
    from socket import gaierror
    from os import remove

    from ..errors import (ConnectionError, ConnectionTimeoutExpired, InvalidWifiConnection,
                          StatusCodeError, SSLCertificateFailed, RequestRedirectError,
                          RequestCodecError)
    from ..info import _loadConfig, version
    from ..sys.info import platform

    class FileDescriptorOrPath:
        pass
    
    class url_response:
        pass

    class HTTP_Port:
        pass

    class advContext():
        def __init__(self, redirectLimit: int, extraLogs: bool, SSLContext):
            self.redirectLimit: int = redirectLimit
            self.extraLogs:    bool = extraLogs
            self.SSLContext         = SSLContext

    logger = getLogger('tooltils.requests')

import tooltils.requests.urllib as urllib


status_codes:    dict[int, str] = _bm.StatusCodeError.status_codes
"""List of official valid HTTP response status codes (100-511)"""
defaultVerificationMethod: bool = bool(_bm._loadConfig('requests')['defaultVerificationMethod'])
redirectLimit:              int = _bm._loadConfig('requests')['redirectLimit']

def where() -> urllib._bm.certifs:
    """Return default certificate file and path locations used by Python"""

    return urllib.where()

def connected() -> bool:
    """Get the connectivity status of the currently connected wifi network"""
    
    return urllib.connected()

def ctx(verify: bool=True, cert: str=None) -> _bm.SSLContext:
    """Create a custom SSLContext instance"""

    return urllib.ctx(verify, cert)

def prep_url(url: str, 
             data: dict=None,
             https: bool=True,
             order: bool=False
             ) -> str:
    """Configure a URL making it viable for requests"""

    return urllib.prep_url(url, data, https, order)

def verifiable() -> bool:
    """Determine whether requests can be verified with a valid ssl 
    certificate on the current connection"""

    return urllib.verifiable()

def advancedContext(redirectLimit: int=redirectLimit, 
                    extraLogs: bool=False, 
                    SSLContext: _bm.SSLContext=ctx()) -> _bm.advContext:
    """Create an advanced context intended to be used for extended functionality with requesting"""

    if type(redirectLimit) is not int:
        raise TypeError('RedirectLimit must be a valid \'int\' instance')
    elif redirectLimit < 1:
        raise ValueError('RedirectLimit must be bigger than 1')
    if type(SSLContext) is not _bm.SSLContext and SSLContext is not None:
        raise TypeError('SSLContext must be a valid \'ssl.SSLContext\' instance')
    
    return _bm.advContext(redirectLimit, bool(extraLogs), SSLContext)

class request():
    """Initiate and send a request to a url"""

    def __init__(self, 
                 url: str,
                 method: str,
                 port: _bm.HTTP_Port=None,
                 https: bool=True,
                 verify: bool=defaultVerificationMethod,
                 redirects: bool=True,
                 auth: tuple=None,
                 data: dict=None,
                 headers: dict=None,
                 cookies: dict=None,
                 cert: _bm.FileDescriptorOrPath=None, 
                 file_name: _bm.FileDescriptorOrPath=None,
                 write_binary: bool=False,
                 override: bool=False,
                 timeout: int=15, 
                 encoding: _bm.Union[str, tuple]=('utf-8', 'ISO-8859-1'),
                 mask: bool=False,
                 agent: str=None,
                 advContext: _bm.advContext=None,
                 _redirectData: dict=None):
        self._setVariables(url, method, port, https, verify, redirects,
                           auth, data, headers, cookies, cert, file_name, 
                           write_binary, override, timeout, encoding, mask, 
                           agent, advContext, _redirectData)
        
        self._prepare()

        _bm.logger.debug('Setting up http{}/1.1 {} request to <{}:{}>'.format(
                         's' if self.verified else '', self.method, self.url.split('/')[2], self.port))

        if self.port != 80 and self.port != 443:
            _bm.logger.debug('Request is not using port 80 or 443, it may fail')
        
    def __str__(self):
        return '<{} {} {}>'.format(self.method, 
                                   self._url[0] if self.method != 'DOWNLOAD' else self.file_name,
                                   '[Unsent]' if not self.sent else f'[{self.code}]')

    def read(self) -> _bm.Any:
        """Read the request file and return the raw data"""

        return self.raw

    def readlines(self) -> list:
        """Read the request file and return the data as a list split at every newline"""

        return self.text.splitlines()

    def _setVariables(self, url: str, method: str, port: int, https: bool, 
                      verify: bool, redirects: bool, auth: tuple, data: dict, 
                      headers: dict, cookies: dict, cert: str, file_name: str, 
                      write_binary: bool, override: bool, timeout: int, 
                      encoding: _bm.Union[str, tuple], mask: bool, 
                      agent: str, advContext, _redirectData):
        self.write_binary: bool = bool(write_binary)
        self.redirects:    bool = bool(redirects)
        self.override:     bool = bool(override)
        self.verified:     bool = bool(verify)
        self.https:        bool = bool(https)
        self.mask:         bool = bool(mask)
        self.sent:         bool = False
        self.cookies:      dict = urllib._bm.propertyTest(cookies, (dict), 'Cookies')
        self.sent_headers: dict[str, str] = urllib._bm.propertyTest(headers, (dict), 'Headers')
        self._redirectData:          dict = _redirectData

        self.url:   str = prep_url(url, https=self.https)
        self._url:  str = self.url.replace('https://' if self.https else 'http://', '').split('/')
        self._page: str = '/' + '/'.join(self._url[1:])

        if type(method) is str:
            if method.upper() not in ('GET', 'POST', 'PUT', 'DOWNLOAD',
                                      'HEAD', 'PATCH', 'DELETE'):
                raise ValueError('Invalid http method \'{}\''.format(method))
            else:
                self.method: str = method.upper()
            
            if method.upper() == 'DOWNLOAD':
                self._method: str = 'GET'
            else:
                self._method: str = method.upper()
        else:
            raise TypeError('Method must be a valid \'str\' instance')
        
        if data is not None and type(data) is not dict:
            raise TypeError('Data must be a valid \'dict\' instance')
        else:
            self.data: dict = data

        if cert is None:
            self.cert: str = where().cafile
        else:
            if type(cert) is not str:
                raise TypeError('Certificate must be a valid \'str\' instance')
            elif not _bm.exists(cert) or cert.split('.')[-1] != 'pem':
                raise FileNotFoundError('Invalid certificate file path')
            elif verify:
                self.cert: str = cert
            else:
                self.cert: str = where().cafile

        if auth is None:
            self.auth = None
        elif len(auth) != 2:
            raise ValueError('Invalid authentication details')
        elif type(auth) is not tuple and type(auth) is not list:
            raise TypeError('Authentiction must be a valid \'tuple\' instance')
        else:
            self.auth: tuple = tuple(auth)

        if type(timeout) is not int and type(timeout) is not float:
            raise TypeError('Timeout must be a valid \'int\' instance')
        elif timeout > 999 or timeout < 1:
            raise ValueError('Timeout cannot be bigger than 999 or smaller than 0 seconds')
        else:
            self.timeout: int = int(timeout)

        if file_name is None:
            if self.method == 'DOWNLOAD':
                if (override and _bm.exists(self.url.split('/')[-1])) or (not _bm.exists(self.url.split('/')[-1])):
                    self.file_name: str = self.url.split('/')[-1]
                elif not override and _bm.exists(self.url.split('/')[-1]):
                    raise FileExistsError('Destination file already exists')
                else:
                    self.file_name: str = self.url.split('/')[-1]
            else:
                self.file_name = None
        elif type(file_name) != str:
            raise TypeError('File_name must be a valid \'str\' instance')
        else:
            if (override and _bm.exists(file_name)) or (not _bm.exists(file_name)):
                self.file_name: str = file_name
            elif not override and _bm.exists(file_name):
                raise FileExistsError('Destination file already exists')

        if mask:
            if _bm.platform.lower() == 'windows':
                self.agent: str = 'Mozilla/5.0 (Windows NT 10.0; ' + \
                                  'rv:10.0) Gecko/20100101 Firefox/10.0'
            elif _bm.platform.lower() == 'macos':
                self.agent: str = f'Mozilla/5.0 (Macintosh; Intel Mac OS ' + \
                                   '10.15; rv:10.0) Gecko/20100101 Firefox/10.0'
            else:
                self.agent: str = 'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) ' + \
                                  'Gecko/20100101 Firefox/10.0'

        if agent is None:
            self.agent: str = f'Python-tooltils/{_bm.version}'
        elif type(agent) is not str:
            raise TypeError('Agent must be a valid \'str\' instance')
        else:
            self.agent: str = agent

        if not isinstance(encoding, (str, tuple)):
            raise TypeError('Encoding must be a valid \'str\' or \'tuple\' instance')
        elif type(encoding) is str:
            self.encoding: str = encoding
        elif type(encoding) is tuple:
            self.encoding: tuple = encoding

        if port is None:
            if self.https:
                self.port: int = 443
            else:
                self.port: int = 80
        elif type(port) is not int:
            raise TypeError('Port must be a valid \'int\' instance')
        else:
            self.port: int = port

        if advContext is None:
            self.advContext         = None
            self.redirectLimit: int = _bm._loadConfig('requests')['redirectLimit']
            self.extraLogs:    bool = False
            self.SSLContext         = None
        elif type(advContext) is not _bm.advContext:
            raise TypeError('AdvContext must be a valid \'tooltils.requests.advContext\' instance')
        else:
            self.advContext         = advContext
            self.redirectLimit: int = advContext.redirectLimit
            self.extraLogs:    bool = advContext.extraLogs
            self.SSLContext         = advContext.SSLContext
    
    def _prepare(self):
        self._data = None

        if self.extraLogs:
            _bm.logger.debug('Preparing request')

        if self.method in ('POST', 'PUT') and self.data:
            self._data: dict = _bm.dumps(self.data).encode()
            self.sent_headers.update({"Content-Length": str(len(self._data))})

            if self.extraLogs:
                _bm.logger.debug('Adding Content-Length to headers')

        self.sent_headers.update({"Connection": "close", "User-Agent": self.agent, 
                                  "Accept": "*/*", "Accept-Encoding": "gzip, deflate"})

        if self.extraLogs:
            _bm.logger.debug(f'Adding headers: {self.sent_headers}')

        if self.https:
            if self.SSLContext:
                _ctx = self.SSLContext

                if self.extraLogs:
                    _bm.logger.debug('Using custom SSLContext request instance')
            else:
                _ctx = ctx(self.verified, self.cert)

                if self.extraLogs:
                    _bm.logger.debug('Using request created SSLContext instance')

            self._req = _bm.HTTPSConnection(self._url[0], self.port, timeout=self.timeout, context=_ctx)
        else:
            self._req = _bm.HTTPConnection(self._url[0], self.port, timeout=self.timeout)
        
        if self.extraLogs:
            _bm.logger.debug('Created request reference')
    
    def send(self) -> _bm.url_response:
        """Send the request"""

        if self.sent:
            raise _bm.ConnectionError('The request has already been sent')

        _headers: dict = self.sent_headers
        error          = None

        for i in list(self.cookies.keys()):
            _headers.update('Cookie', f'{str(i)}={str(self.cookies[i])}')
        
        if self.auth:
            _headers.update({"Authorization": "Basic {}".format(
                     _bm.b64encode(f'{self.auth[0]}:{self.auth[1]}'.encode()).decode("ascii"))})
        
        if self.extraLogs:
            _bm.logger.debug('Adding cookies to request headers')
            _bm.logger.debug('Adding authorisation to request headers')

        try:
            if self.extraLogs:
                _bm.logger.debug('Sending request to the server')
            
            _bm.logger.debug(f'Sending headers: {self.sent_headers}')

            if self.data:
                _bm.logger.debug(f'Sending data with length: {len(self._data)}')

            self._req.request(self._method, self._page, self._data, _headers)
            
            rdata = self._req.getresponse()

            if self.extraLogs:
                _bm.logger.debug('Obtained response from server')

            if rdata.status >= 400:
                if rdata.status not in list(_bm.StatusCodeError.status_codes.keys()):
                    error = _bm.StatusCodeError(reason=f'{rdata.status} - Unofficial http status code')
                else:
                    error = _bm.StatusCodeError(rdata.status)
            else:
                # test for redirect

                redirectDir:   str = rdata.getheader('location')
                redirectData: dict = self._redirectData

                if self.redirects and redirectDir is not None:
                    if redirectData:
                        if redirectData['redirected'] >= redirectData['limit']:
                            error = _bm.RequestRedirectError('Request url redirected too many times')
                        else:
                            redirectData['redirected'] += 1
                    
                        if redirectDir in redirectData['redirectList']:
                            error = _bm.RequestRedirectError('Redirect loop detected')
                        else:
                            redirectData['redirectList'].append(redirectDir)
                    else:
                        redirectData: dict = {"redirected": 1, "redirectList": [redirectDir],
                                              "limit": self.redirectLimit}
                    
                    if error is None:
                        if self.extraLogs:
                            _bm.logger.debug('Request was redirected')
                        
                        return request(redirectDir, self.method, self.port, self.https, 
                                       self.verified, self.redirects, self.auth, self.data,
                                       self.sent_headers, self.cookies, self.cert, 
                                       self.file_name, self.write_binary, self.override, 
                                       self.timeout, self.encoding, self.mask, self.agent,
                                       self.advContext, redirectData).send()
        except _bm.RemoteDisconnected:
            error = _bm.ConnectionError('The server ended the connection without a response')
        except _bm.SSLCertVerificationError:
            error = _bm.SSLCertificateFailed()
        except _bm.gaierror:
            if connected():
                error = _bm.StatusCodeError(404)
            else:
                error = _bm.InvalidWifiConnection()
            
            _bm.logger.debug('tooltils.requests.connected() was called by tooltils.requests.request() and may update the cache')
        except OSError as err:
            if 'Errno 65' in str(err):
                error = ValueError('Invalid URL')
            else:
                error = err
        except _bm.InvalidURL as err:
            if 'nonnumeric port' in str(err):
                error = ValueError('You may not include a colon in the URL object (this includes ports)')
            elif 'control characters':
                error = ValueError('Invalid URL (contains non-transmissible characters)')
            else:
                error = err
        
        self.sent: bool = True

        if error:
            _bm.logger.debug('Request to <{}:{}> failed due to: {}'.format(self.url.split('/')[2], 
                                                                           self.port, type(error).__name__))

            if self.port != 80 and self.port != 443:
                _bm.logger.debug('Request may have failed due to the port not being set to 80 or 443')

            raise error

        self.rdata              = rdata
        self.code:          int = rdata.status
        self.reason:        str = _bm.StatusCodeError.status_codes[self.code]
        self.status_code:   str = f'{self.code} {self.reason}'
        self.resp_headers: dict = {}
        self.path               = None

        for i in rdata.getheaders():
            self.resp_headers.update({i[0]: i[1]})

        if self.extraLogs:
            _bm.logger.debug('Obtained request response headers')
        
        if self.method == 'HEAD':
            self.text = None
            self.raw  = None
            self.json = None

            return self

        self.raw = rdata.read()

        try:
            self.text = _bm.decompress(self.raw)
        except _bm.BadGzipFile:
            _bm.logger.debug('Request response body was not gzipped')

        if type(self.encoding) is str:
            try:
                self.text: str = self.raw.decode(self.encoding)
            except UnicodeDecodeError:
                pass
        else:
            for i in self.encoding:
                try:
                    self.text: str = self.raw.decode(i)

                    break
                except UnicodeDecodeError:
                    pass
        
        if not self.write_binary and type(self.text) is not str:
            raise _bm.RequestCodecError('None of the specified encodings were able to decipher the ' + 
                                        'request response body', self.encoding)

        if self.method == 'DOWNLOAD':
            if _bm.exists(self.file_name):
                _bm.remove(self.file_name)
            
            # test if the file_name is sanitary
            
            try:
                with open(self.file_name, 'a+') as _f:
                    pass

                _bm.remove(self.file_name)
            except OSError:
                raise FileNotFoundError('Unable to locate valid file_name descriptor from request url')

            if self.write_binary:
                with open(self.file_name, 'wb+') as _f:
                    _bm.copyfileobj(rdata, _f)
            else:
                with open(self.file_name, 'a+') as _f:
                    _f.write(self.text)

            self.path: str = _bm.abspath(self.file_name)

        try:
            self.json: dict = _bm.loads(self.text)
        except _bm.JSONDecodeError:
            self.json = None

            _bm.logger.debug('Request response body is not json')

        _bm.logger.debug(f'Server replied with [{self.status_code}]')
        _bm.logger.debug('Connection to server has been discarded')
        
        return self

def get(url: str,
        port: _bm.HTTP_Port=None,
        https: bool=True,
        verify: bool=defaultVerificationMethod,
        redirects: bool=True,
        auth: tuple=None,
        data: dict=None,
        headers: dict=None,
        cookies: dict=None,
        cert: _bm.FileDescriptorOrPath=None, 
        timeout: int=15, 
        encoding: _bm.Union[str, tuple]=('utf-8', 'ISO-8859-1'),
        mask: bool=False,
        agent: str=None,
        advContext: _bm.advContext=None,
        ) -> _bm.url_response:
    """Send a GET request"""

    return request(url, 'GET', port, https, verify, redirects,
                   auth, data, headers, cookies, cert, None, 
                   None, None, timeout, encoding, mask, 
                   agent, advContext).send()

def post(url: str,
         port: _bm.HTTP_Port=None,
         https: bool=True,
         verify: bool=defaultVerificationMethod,
         redirects: bool=True,
         auth: tuple=None,
         data: dict=None,
         headers: dict=None,
         cookies: dict=None,
         cert: _bm.FileDescriptorOrPath=None, 
         timeout: int=15, 
         encoding: _bm.Union[str, tuple]=('utf-8', 'ISO-8859-1'),
         mask: bool=False,
         agent: str=None,
         advContext: _bm.advContext=None,
         ) -> _bm.url_response:
    """Send a POST request"""

    return request(url, 'POST', port, https, verify, redirects,
                   auth, data, headers, cookies, cert, None, 
                   None, None, timeout, encoding, mask, 
                   agent, advContext).send()

def download(url: str,
             port: _bm.HTTP_Port=None,
             https: bool=True,
             verify: bool=defaultVerificationMethod,
             redirects: bool=True,
             auth: tuple=None,
             data: dict=None,
             headers: dict=None,
             cookies: dict=None,
             cert: _bm.FileDescriptorOrPath=None, 
             file_name: _bm.FileDescriptorOrPath=None,
             write_binary: bool=False,
             override: bool=False,
             timeout: int=15, 
             encoding: _bm.Union[str, tuple]=('utf-8', 'ISO-8859-1'),
             mask: bool=False,
             agent: str=None,
             advContext: _bm.advContext=None,
             ) -> _bm.url_response:
    """Download a file onto the disk"""

    return request(url, 'DOWNLOAD', port, https, verify, redirects,
                   auth, data, headers, cookies, cert, file_name, 
                   write_binary, override, timeout, encoding, mask, 
                   agent, advContext).send()

def head(url: str,
         port: _bm.HTTP_Port=None,
         https: bool=True,
         verify: bool=defaultVerificationMethod,
         redirects: bool=True,
         auth: tuple=None,
         data: dict=None,
         headers: dict=None,
         cookies: dict=None,
         cert: _bm.FileDescriptorOrPath=None, 
         timeout: int=15, 
         encoding: _bm.Union[str, tuple]=('utf-8', 'ISO-8859-1'),
         mask: bool=False,
         agent: str=None,
         advContext: _bm.advContext=None,
         ) -> _bm.url_response:
    """Send a HEAD request"""

    return request(url, 'HEAD', port, https, verify, redirects,
                   auth, data, headers, cookies, cert, None, 
                   None, None, timeout, encoding, mask, 
                   agent, advContext).send()
def put(url: str,
        port: _bm.HTTP_Port=None,
        https: bool=True,
        verify: bool=defaultVerificationMethod,
        redirects: bool=True,
        auth: tuple=None,
        data: dict=None,
        headers: dict=None,
        cookies: dict=None,
        cert: _bm.FileDescriptorOrPath=None, 
        timeout: int=15, 
        encoding: _bm.Union[str, tuple]=('utf-8', 'ISO-8859-1'),
        mask: bool=False,
        agent: str=None,
        advContext: _bm.advContext=None,
        ) -> _bm.url_response:
    """Send a PUT request"""

    return request(url, 'PUT', port, https, verify, redirects,
                   auth, data, headers, cookies, cert, None, 
                   None, None, timeout, encoding, mask, 
                   agent, advContext).send()

def patch(url: str,
          port: _bm.HTTP_Port=None,
          https: bool=True,
          verify: bool=defaultVerificationMethod,
          redirects: bool=True,
          auth: tuple=None,
          data: dict=None,
          headers: dict=None,
          cookies: dict=None,
          cert: _bm.FileDescriptorOrPath=None, 
          timeout: int=15, 
          encoding: _bm.Union[str, tuple]=('utf-8', 'ISO-8859-1'),
          mask: bool=False,
          agent: str=None,
          advContext: _bm.advContext=None,
          ) -> _bm.url_response:
    """Send a PATCH request"""

    return request(url, 'PATCH', port, https, verify, redirects,
                   auth, data, headers, cookies, cert, None, 
                   None, None, timeout, encoding, mask, 
                   agent, advContext).send()

def delete(url: str,
           port: _bm.HTTP_Port=None,
           https: bool=True,
           verify: bool=defaultVerificationMethod,
           redirects: bool=True,
           auth: tuple=None,
           data: dict=None,
           headers: dict=None,
           cookies: dict=None,
           cert: _bm.FileDescriptorOrPath=None, 
           timeout: int=15, 
           encoding: _bm.Union[str, tuple]=('utf-8', 'ISO-8859-1'),
           mask: bool=False,
           agent: str=None,
           advContext: _bm.advContext=None,
           ) -> _bm.url_response:
    """Send a DELETE request"""

    return request(url, 'DELETE', port, https, verify, redirects,
                   auth, data, headers, cookies, cert, None, 
                   None, None, timeout, encoding, mask, 
                   agent, advContext).send()
