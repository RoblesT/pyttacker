#!/usr/bin/python
import os.path, imp
import xml.etree.ElementTree as ET

xml_plugins = []
mods = []

def __import_module(name,fpath):
    print "Importing module: " + name[:-3]
    module_desc = imp.find_module(name[:-3], [fpath]) 
    module = imp.load_module(name[:-3], *module_desc)
    setattr(module, 'name', name[:-3])
    mods.append(module)

def run_module(name,action,url,headers,cookies,postdata):
    
    if len(mods) > 0:
        for module in mods:
            if (module.name == name):
                print '******************************************************************************'
                print 'Running Module:"'+module.name+'" Action:'+action
                print '******************************************************************************'
                return module.run(action,url,headers,cookies,postdata)
    results = {'poc':'','message':'No module found','action':'','data':''}
    return results
    
def find_duplicates(idp,name):
    for pi in xml_plugins:
        if (pi.get('id') == idp) or (pi.get('name') == name):
            return False
    return True

def get_xml():
    return xml_plugins
def get_pluginlist():
    list=''
    for pi in xml_plugins:
        list+= 'id='+pi.get('id')+','
    return list
def get_html_pluginlist():
    list=''
    for pi in xml_plugins:
        list+= "<option value='"+pi.get('id')+"'>"+pi.get('name')+"</option>"
    return list
def import_plugins(fpath):
    print 'Loading Plugins'
    for filename in os.listdir(fpath):
        if (filename.endswith(".xml")):
            print "Loading "+filename
            xmlplugin=ET.parse(fpath+filename)
            root = xmlplugin.getroot()
            #Validations
            addit = True
            if (root.get('name') != '') and (root.get('name') != None):
                print 'Plugin Name:'+root.get('name')
                if (root.get('id') != '') and (root.get('id') != None):
                    print 'Plugin ID:'+root.get('id')
                    if (root.get('mod') != '') and (root.get('mod') != None):
                        if (os.path.isdir(fpath+root.get('id'))):
                            if (os.path.isfile(fpath+root.get('id')+'/'+root.get('mod'))):
                                print 'Module Name:'+root.get('mod')+' Verified!'
                                __import_module(root.get('mod'),fpath+root.get('id'))
                            else:
                                addit = False
                                print 'Error: Module not found:'+fpath+root.get('id')+'/'+root.get('mod')
                        else:
                            addit = False
                            print 'Error: Folder "'+fpath+root.get('id')+'" not found'
                            print 'Make sure the plugin data is stored in the folder name is equal to the plugin id :'+root.get('id')
                else:
                    addit = False
                    print 'Error: The id is required'
            else:
                addit = False
                print 'Error: The name is required'
            if (addit):
                if (find_duplicates(root.get('id'),root.get('name'))):
                    print 'Plugin successfully loaded'
                    xml_plugins.append(root)
                else:
                    print 'Error: Plugin name or id is duplicated and will be skipped'
            else:
                print 'Error: Plugin skipped'
    print 'Plugins process completed'