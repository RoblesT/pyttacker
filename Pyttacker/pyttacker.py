#!/usr/bin/python
import webbrowser, sys, os
from modules import webhandler

def get_port():
    if sys.argv[1:]:
        port = int(sys.argv[1])
    else:
        port = 8080
    return port

if __name__ == '__main__':
    print '      __________'
    print '     /    ____  \   ___    _____________________       _______   __    _________________    '
    print '    /    /\__/  /\  \  \  /  __    __    ____   \     /   ___ \ |  |  /  _    ________  \   '
    print '   /     ______/ /   \  \/  /  |  |  |  |   /    \   /  /    \| |  | /  / |  |____ ___\  \  '
    print '  /    /\______\/     \    /   |  |  |  |  /  /\  \ |  |        |  |/  /  |   ___/ \   __/  '
    print ' /____/ /              /  /    |  |  |  | /  /  \  \_\  \____/\_|  |\  \  |  |____  \  \    '
    print ' \____\/              /__/     |__|  |__|/__/    \_________________| \__\ |_______\  \__\   '
    print ''
    print ' Python Attacker and PoC Creator '
    print ' '
    print '*******************************************************************************************'
    print '* Initial process                                                                         *'
    print '*******************************************************************************************'
    #Load Plugins
    plugins_path=os.path.dirname(os.path.abspath(__file__))+'/plugins/'
    print "Plugins location:"+plugins_path
    
    #plugin_list=plugins.import_plugins(plugins_path)
    
    #Arg handling
    port = get_port()
    
    #Open System default Browser
    url="http://127.0.0.1:"+str(port)
    webbrowser.open(url, 0, True)
    
    #Start Pyttacker Server
    while True:
        try:
            wh = webhandler
            wh.start('127.0.0.1', port,plugins_path)
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