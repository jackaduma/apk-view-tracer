#! python2.7
## -*- coding: utf-8 -*-

#===============================================================================
# @author: kun
# @date: 2012-07-01
# @file name: testHome.py
#===============================================================================

import os,sys
current_path = os.getcwd()
parent_path = os.path.abspath(os.path.join(os.getcwd(), os.path.pardir))
if current_path not in sys.path:
    sys.path.append(current_path)
if parent_path not in sys.path:
    sys.path.append(parent_path)
    
python_sys_path_list = ['C:\\Python27\\Lib\\idlelib', 'C:\\Python27\\lib\\site-packages\\setuptools-0.6c11-py2.7.egg', 
                        'C:\\Python27\\lib\\site-packages\\selenium-2.15.0-py2.7.egg', 'C:\\Python27\\lib\\site-packages\\rdflib-3.1.0-py2.7.egg', 
                        'C:\\Python27\\lib\\site-packages\\openpyxl-1.5.8-py2.7.egg', 'C:\\Windows\\system32\\python27.zip', 'C:\\Python27\\DLLs', 
                        'C:\\Python27\\lib', 'C:\\Python27\\lib\\plat-win', 'C:\\Python27\\lib\\lib-tk', 'C:\\Python27', 
                        'C:\\Users\\kun_ma\\AppData\\Roaming\\Python\\Python27\\site-packages', 'C:\\Python27\\lib\\site-packages', 
                        'C:\\Python27\\lib\\site-packages\\win32', 'C:\\Python27\\lib\\site-packages\\win32\\lib', 
                        'C:\\Python27\\lib\\site-packages\\Pythonwin']
    
from SystemComponent.Home import Home
from ViewManagement.ViewTree import ViewTree

def testHome():
    vt = ViewTree()
    tree_nodes_list = vt.build()
    home = Home(tree_nodes_list)
    elements_list = home.getElementList()
    
    for element in elements_list:
        print element.mText
        
if __name__ == "__main__":
    print sys.path
    for dir_path in python_sys_path_list:
        sys.path.append(dir_path)
        
    print sys.path
    
    testHome()