#!/usr/bin/python
import sys, webbrowser, BaseHTTPServer, urlparse, cgi, urllib2
from SimpleHTTPServer import SimpleHTTPRequestHandler
from BaseHTTPServer import BaseHTTPRequestHandler
from os import curdir, sep


servername = ''

class GetHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            content=''
            filepathlower = self.path.lower()
            filepath = "/w"+self.path
            if filepath == "/w/":
                #Send the default page
                filepath = "/w/index.html"
                filepathlower = filepath
            if filepathlower.startswith("../"):
                self.send_error(404,"Please do not try to attack me, I'm here to help you instead!" )
                return
            if filepathlower.endswith(".html"):
                content='text/html'
                f = open(curdir + sep + filepath)
            if filepathlower.endswith(".css"):
                content='text/css'
                f = open(curdir + sep + filepath)
            if filepathlower.endswith(".js"):
                content='application/x-javascript'
                f = open(curdir + sep + filepath)
            if filepathlower.endswith(".jpg"):
                content='image/jpeg'
                f = open(curdir + sep + filepath, 'rb')
            if filepathlower.endswith(".gif"):
                content='image/gif'
                f = open(curdir + sep + filepath, 'rb')
            if filepathlower.endswith(".png"):
                content='image/png'
                f = open(curdir + sep + filepath, 'rb')
            if content != '':
                if content.startswith("text") or (content == 'application/x-javascript'):
                    print "Server processing!"
                    source = server_process(f.read())
                else:
                    source = f.read()
                self.send_response(200)
                self.send_header('Content-type',content)
                self.end_headers()
                self.wfile.write(source)
                f.close()
            else:
                self.send_error(404,"File type not supported" )
            return
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)
    def do_POST(self):
        # Parse the form data posted
        form = cgi.FieldStorage(
            fp=self.rfile, 
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })

        # Begin the response
        self.send_response(200)
        self.end_headers()

        # Echo back information about what was posted in the form
        for field in form.keys():
            result=''
            if field == 'xfs':
                xfs_url=form[field].value
                result=test_xfs(xfs_url)
            self.wfile.write(result)
        return
def server_process(source):
    content = source
    #Server Vars
    port=get_port()
    content = content.replace("<SERVER_NAME>",servername)
    content = content.replace("<SERVER_PORT>",str(port))
    return content
def test_xfs(url):
    try:
        request = urllib2.Request(url)
        request.add_header('User-Agent', 'PoC Creator')
        response = urllib2.urlopen(request)
        xframe=str(response.info().getheader('X-Frame-Options'))
        if (xframe.lower()=='deny') or (xframe.lower()=='sameorigin'):
            return 'X-Frame-Options:'+xframe
        else:
            print 'XFS Confirmed in ',url
            return 'true'
    except:
        return 'error'
def get_port():
    if sys.argv[1:]:
        port = int(sys.argv[1])
    else:
        port = 8000
    return port
def Get_Info(self):
    parsed_path = urlparse.urlparse(self.path)
    message_parts = [
            'CLIENT VALUES:',
            'client_address=%s (%s)' % (self.client_address,
                                        self.address_string()),
            'command=%s' % self.command,
            'path=%s' % self.path,
            'real path=%s' % parsed_path.path,
            'query=%s' % parsed_path.query,
            'request_version=%s' % self.request_version,
            '',
            'SERVER VALUES:',
            'server_version=%s' % self.server_version,
            'sys_version=%s' % self.sys_version,
            'protocol_version=%s' % self.protocol_version,
            '',
            'HEADERS RECEIVED:',
            ]
    for name, value in sorted(self.headers.items()):
        message_parts.append('%s=%s' % (name, value.rstrip()))
    message_parts.append('')
    message = '\r\n'.join(message_parts)
    return message

if __name__ == '__main__':
    HandlerClass = SimpleHTTPRequestHandler
    ServerClass  = BaseHTTPServer.HTTPServer
    Protocol     = "HTTP/1.0"

    port = get_port()
    server_address = ('127.0.0.1', port)
    
    HandlerClass.protocol_version = Protocol
#    httpd = ServerClass(server_address, HandlerClass)
    httpd = ServerClass(server_address, GetHandler)
    sa = httpd.socket.getsockname()
    servername="localhost"
    print "Serving HTTP on", sa[0], "port", sa[1], "..."
    url="http://localhost:"+str(port)
    webbrowser.open(url, 0, True)
    httpd.serve_forever()
