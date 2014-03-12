#!/usr/bin/python
#@author = Mario Robles

import sys,urllib2

def test_xfs(url,headers):
    results = {'poc':'','message':'','action':'','data':''}
    try:
        request = urllib2.Request(url)
        print 'Sending Request'
        for header in headers:
            if header == 'user-agent':
                print header+': '+headers[header]
                request.add_header(header, headers[header])
        response = urllib2.urlopen(request)
        print "Response received"
        xframe=str(response.info().getheader('X-Frame-Options'))
        print 'Verify X-Frame-Options Header: '+xframe
        if (xframe.lower()=='deny') or (xframe.lower()=='sameorigin'):
            results['poc'] = 'false' # true | false | error 
            results['message'] = 'Not vulnerable: X-Frame-Options:'+xframe+' will prevent the browser to display the site within any iFrame or Frame set'
            print results['poc']+': '+results['message']
            return results
        else:
            results['poc'] = 'true' # true | false | error 
            results['message'] = 'XFS Confirmed in '+url
            results['action'] = 'go_payload'
            results['data'] = ''
            print results['poc']+': '+results['message']
            return results
    except:
        results['poc'] = 'error'
        results['message'] = "Unexpected error:"+str(sys.exc_info()[0])
        print results['poc']+': '+results['message']
        return results

def run(action,url,headers,cookies,data):
    print 'Cross-Frame Scripting (XFS) validator by Roblest.com'
    if (action=='xfs1'):
        return test_xfs(url,headers)
    else:
        return 'Action: '+action+' not found'