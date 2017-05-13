#!/usr/bin/python
import modules, webbrowser, sys, os, threading, socket, time

web_server = None


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


def port_open(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
        return True
    except:
        return False
    
def start():
    global web_server, myip, port
    try:
        if not port_open(myip, port):
            web_server = threading.Thread(target=start_webserver)  
            web_server.start()
            return True
        else:
            return False
    except Exception:
        return False
        
if __name__ == '__main__':
    print '      __________'
    print '     /    ____  \   ___    _____________________       _______   __   ___________________    '
    print '    /    /\__/  /\  \  \  /  __    __    ____   \     /   ___ \ |  | /  ___    ________  \   '
    print '   /     ______/ /   \  \/  /  |  |  |  |   /    \   /  /    \| |  |   /   |  |____ ___\  \  '
    print '  /    /\______\/     \    /   |  |  |  |  /  /\  \ |  |        |  |\  \   |   ___/ \   __/  '
    print ' /____/ /              /  /    |  |  |  | /  /  \  \_\  \____/\_|  | \  \  |  |____  \  \    '
    print ' \____\/              /__/     |__|  |__|/__/    \_________________|  \__\ |_______\  \__\   '
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
    
    #Server Information
    port = get_port()
    myip = get_ip()
    
    process_started = False
    
    #Start Pyttacker Server
    while not process_started:
        process_started = start()
        if not process_started:
            print '[X] Make sure the port '+str(port)+' is not used by other service: '
            print '[!] Select a new port number (1000 - 65535) or type "q" to exit:'
            msg = raw_input('Port:')
            if msg == 'q':
                print "Ok bye"
                exit()
            else:
                try:
                    tport = int(msg)
                    if tport >= 1000 and tport < 65535:
                        port = tport
                except:
                    print '[X] The port must be an integer value'
        else:
            #Open System default Browser
            url="http://"+myip+":"+str(port)
            print '[!] Opening Web Browser'
            webbrowser.open(url, 0, True)

    #Start command handler
    while True:
        try:
            #print "[!] If your browser didn't started check the Pop Up settings and use the following URL: "+url+'/'
            #print ''
            #print '[!] Use this interface for management commands'
            #print 'Type: q = Shutdown the server and close Pyttacker'
            #msg = raw_input('pyttacker:')
            #if msg == 'q':
            #    stop_server()
            #    print 'Ok, Bye, thank you for using Pyttacker!!'
            #    exit()
            if not port_open(myip, port):
                print '[!] Web Server is closed'
                print '*'*60
                print 'Big thanks for supporting Pyttacker!'
                print '*'*60
                stop_server()
                exit()
            time.sleep(1)
        except Exception, e:
            print str(e)
