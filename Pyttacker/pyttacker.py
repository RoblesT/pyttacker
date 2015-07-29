#!/usr/bin/python
import modules, webbrowser, sys, os, threading, socket, getpass
from modules import webhandler

def get_port():
    try:
        port = 9090
        if sys.argv[1:]:
            port = int(sys.argv[1])
    except:
        print "Wrong Port provided, only Integer values are accepted"
    return port
def start_webserver():
    #Start Pyttacker Server
    global password,myip, port, plugins_path
    try:
        
        if myip != '':
            modules.webhandler.start(myip, port,plugins_path)
    except Exception, e:
        print 'Errors while starting the Web Server: ', str(e)

def stop_server():
    if web_server.isAlive():
        web_server._Thread__stop()

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8",80))
    myip = s.getsockname()[0]
    s.close()
    return myip

if __name__ == '__main__':
    print '      __________'
    print '     /    ____  \   ___    _____________________       _______   __    _________________    '
    print '    /    /\__/  /\  \  \  /  __    __    ____   \     /   ___ \ |  |  /  _    ________  \   '
    print '   /     ______/ /   \  \/  /  |  |  |  |   /    \   /  /    \| |  | /  / |  |____ ___\  \  '
    print '  /    /\______\/     \    /   |  |  |  |  /  /\  \ |  |        |  |/  /  |   ___/ \   __/  '
    print ' /____/ /              /  /    |  |  |  | /  /  \  \_\  \____/\_|  |\  \  |  |____  \  \    '
    print ' \____\/              /__/     |__|  |__|/__/    \_________________| \__\ |_______\  \__\   '
    print ''
    print ' OWASP Python Attacker and PoC Creator '
    print '                                                                      mario.robles@owasp.org'
    print '*******************************************************************************************'
    print '* Initial process                                                                         *'
    print '*******************************************************************************************'
    #Load Plugins
    plugins_path=os.path.dirname(os.path.abspath(__file__))+'/plugins/'
    print "Plugins location:"+plugins_path
    
    #plugin_list=plugins.import_plugins(plugins_path)
    
    #Arg handling
    port = get_port()
    myip = get_ip()
    
    #Open System default Browser
    url="http://"+myip+":"+str(port)
    webbrowser.open(url, 0, True)
    process_started = False

    
    #Start Pyttacker Server
    while True:
        try:
            if not process_started:
                web_server = threading.Thread(target=start_webserver)  
                web_server.start()
                process_started = True
            print 'URL: '+url+':'+port+'/'
            print ''
            print 'Use this interface for management commands'
            print 'Type: q = Shutdown the server and close Pyttacker'
            msg = raw_input('Command:')
            if msg == 'q':
                stop_server()
                print 'Ok, Bye, thank you for using Pyttacker!!'
                exit()
                
        except Exception, e:
            print 'Something wrong happened, make sure the port is not used by other service: ', str(e)
            print 'Select a new port number (1000 - 65535) or type "q" to exit:'
            msg = raw_input('Port:')
            if msg == 'q':
                print "Ok bye"
                exit()
            else:
                port = int(msg)
                wh = None