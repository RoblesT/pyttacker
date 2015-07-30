#!/usr/bin/python
import sys, BaseHTTPServer, urlparse, cgi, urllib2, threading, socket, platform, os
from SimpleHTTPServer import SimpleHTTPRequestHandler
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
from Queue import Queue
from SocketServer import TCPServer
from os import curdir, sep
import plugins

current_target=''
xml_plugins =[]
server_port=8000
server_name='localhost'
httpd = None

class GetHandler(BaseHTTPRequestHandler):

    def __ext_filter(self, filename):
        if not '?' in filename:
            ext = filename[filename.rfind('.'):].lower()
            if (ext == ".html"):
                return 'text/html'
            elif (ext == ".css"):
                return 'text/css'
            elif (ext == ".js"):
                return 'application/x-javascript'
            elif (ext == ".jpg"):
                return 'image/jpeg'
            elif (ext == ".gif"):
                return 'image/gif'
            elif (ext == ".png"):
                return 'image/png'
            else:
                return ''
        else:
            return ''
        
    def do_GET(self):
        global httpd
        try:
            content = self.__ext_filter(self.path)
            filepath = self.parse_path(self.path.lower())
            print 'Requested:'+filepath
            if filepath == "/w/":
                #Send the default page
                filepath = "/w/index.html"
                content = self.__ext_filter(filepath)
            if filepath.startswith("../"):
                self.send_response(404)
                self.end_headers()
                print ('Error:',404,"Please don't try to attack me, I'm here to help you instead!" )
                self.wfile.write("<h1>Pyttacker Server</h1>Error:404 FPlease don't try to attack me, I'm here to help you instead!")
                return
            if (content == 'text/html') or (content == 'text/css') or (content == 'application/x-javascript'):
                f = open(curdir + sep + filepath)
            elif (content == 'image/jpeg') or (content == 'image/gif') or (content == 'image/png'):
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
                web_command = filepath.replace('/w/','')
                #Work in progress here for command processing, for now just Quit call
                if web_command == 'cmd=quit':
                    print '[!] Shutting down Web server'
                    httpd.server_close()
                else:
                    self.send_response(404)
                    self.end_headers()
                    print 'Error:',404,"File type not supported:",self.path
                    self.wfile.write('<h1>Pyttacker Server</h1>Error:404 File type not supported:'+cgi.escape(self.path))
            return
        except IOError:
            self.send_response(404)
            self.end_headers()
            print 'Error:',404,'File Not Found: ',self.path
            self.wfile.write('<h1>Pyttacker Server</h1>Error:404 File Not Found:'+cgi.escape(self.path))
    
    def do_POST(self):
        # Parse the form data posted
        form = cgi.FieldStorage(
            fp=self.rfile, 
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })

        # Module manager
        results = {'poc':'','message':'','action':'','data':''}
        plugin_id=''
        action=''
        url=''
        cookies=''
        headers=''
        postdata=''
        pocid=''
        global current_target
        for field in form.keys():
            if field == 'plugin':
                plugin_id=form[field].value
            elif field == 'action':
                action=form[field].value
            elif field == 'url':
                url=form[field].value
            elif field == 'cookies':
                cookies=form[field].value
            elif field == 'headers':
                headers=form[field].value
            elif field == 'postdata':
                postdata=form[field].value
            elif field == 'pocid':
                pocid=form[field].value
        if headers=='':
            headers=self.headers
        if action == 'you_ok?':
            self.send_response(200)
            self.end_headers()
            self.wfile.write('yes')
            return
        try:
            if (plugin_id != '') and (action!=''):
                for pi in plugins.get_xml():
                    if (pi.get('id') == plugin_id):
                        if (action == 'get_info'):
                            print 'Get Plugin info for:'+plugin_id
                            results['poc']='true'
                            results['data']='name<:>'+str(pi.get('name'))+'<;>description<:>'+str(pi.get('description'))+'<;>author<:>'+str(pi.get('author'))
                            if (pi.get('mod') != None and pi.get('mod') != ''):
                                print pi.get('mod')
                                client_action='pyttacker'
                            else:
                                client_action='go'
                            for poc in pi.findall('poc'):
                                #Carefully take care of the payload
                                payload=str(poc.get('payload'))
                                if (payload != 'None'):
                                    payload = server_process(payload)
                                    payload = escape(payload)
                                else:
                                    payload=''
                                results['action']+=str(poc.get('id'))+'<:>'+str(poc.get('name'))+'<:>'+client_action+'<:>'+payload+'<;>'
                        else:
                            print 'Performing action '+action+' in Plugin:'+plugin_id
                            if (url!=''):
                                for poc in pi.findall('poc'):
                                    if str(poc.get('id'))==action:
                                        results=plugins.run_module(plugin_id, action, url, headers, cookies, postdata)
                                        if (results['action']=='go_payload'):
                                            current_target=url
                                            print 'Target: ',current_target
            else:
                print 'Error: Plugin ID and Action are required fields'
            if results['poc'] != '':
                self.send_response(200)
                self.end_headers()
                self.wfile.write('poc<=>'+results['poc']+'<|>message<=>'+results['message']+'<|>action<=>'+results['action']+'<|>data<=>'+results['data'])
            else:
                self.send_response(500)
                self.end_headers()
                self.wfile.write('Error: 500 Function or method not implemented: ')
                print 'Error:',500,'Function or method not implemented: ',plugin_id
        except Exception as inst:
            self.send_response(500)
            self.end_headers()
            self.wfile.write('Error: 500 Exception: ')
            print 'Error:',500,'Exception: ',inst
    def parse_path(self,fpath):
        sections=fpath.split('/')
        finalpath=''
        if len(sections) > 1:
            if sections[1] != '':
                for pi in plugins.get_xml():
                    if (pi.get('id') == sections[1]):
                        finalpath = '/plugins'+fpath
        if finalpath =='':
            finalpath = '/w'+fpath
        return finalpath
    def stop(self):
        self._stop.set()
        
def escape(source):
    return cgi.escape(source,True).encode('ascii', 'xmlcharrefreplace')

def server_process(source):
    global server_name, server_port
    content = source
    #Server Vars
    plugin_list=plugins.get_pluginlist()
    html_pluginlist=plugins.get_html_pluginlist()
    
    content = content.replace("<SERVER_NAME>",server_name)
    content = content.replace("<SERVER_PORT>",str(server_port))
    content = content.replace("%baseurl%",'http://'+server_name+':'+str(server_port))
    content = content.replace("%plugin_list%",plugin_list)
    content = content.replace("%html_pluginlist%",html_pluginlist)
    content = content.replace("%target%",current_target)
    return content

def start(server,port,plugins_path):
    global xml_plugins, server_port, server_name, httpd
    HandlerClass = SimpleHTTPRequestHandler
    ServerClass  = BaseHTTPServer.HTTPServer
    Protocol     = "HTTP/1.0"
    xml_plugins = plugins.import_plugins(plugins_path)
    server_port=port
    server_name=server
    
    server_address = (server, port)
    
    HandlerClass.protocol_version = Protocol
    httpd = ThreadedServer(server_address, GetHandler)
    info = httpd.socket.getsockname()
    print "******************************************************************************"
    print "Pyttacker Server started on", info[0], "port", info[1]
    print "******************************************************************************"
    httpd.serve_forever()
    exit()

def __init__():
    global current_target
    current_target=''
    
class ThreadPoolMixIn(ThreadingMixIn):
    '''
    use a thread pool instead of a new thread on every request
    '''
    numThreads = 20
    allow_reuse_address = True  # seems to fix socket.error on server restart

    def serve_forever(self):
        '''
        Handle one request at a time until doomsday.
        '''
        # set up the threadpool
        self.requests = Queue(self.numThreads)

        for x in range(self.numThreads):
            t = threading.Thread(target = self.process_request_thread)
            t.setDaemon(1)
            t.start()

        # server main loop
        while True:
            self.handle_request()
            
        self.server_close()

    
    def process_request_thread(self):
        '''
        obtain request from queue instead of directly from server socket
        '''
        while True:
            ThreadingMixIn.process_request_thread(self, *self.requests.get())

    
    def handle_request(self):
        '''
        simply collect requests and put them on the queue for the workers.
        '''
        try:
            request, client_address = self.get_request()
        except socket.error:
            return
        if self.verify_request(request, client_address):
            self.requests.put((request, client_address))
    
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""
    pass

class ThreadedServer(ThreadPoolMixIn, TCPServer):
    pass
