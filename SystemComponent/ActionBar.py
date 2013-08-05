#! python2.7
## -*- coding: utf-8 -*-
'''
Created on 2012-11-14

@author: kun_ma
'''

class ActionBar(object):
    '''
    ActionBar
    '''


    def __init__(self, bar_node):
        '''
        Constructor
        '''
        self.class_name = "ActionBar"
        self.node = bar_node
        
        self.items_list = []
#        self.icons_list = []
        
    def loadAllItems(self):
        if None==self.node.mChildNodes or 0==len(self.node.mChildNodes):
            return False
        
        self.getChildProperties(self.node)
        
        return True

    def isLeafNode(self, node):
        if None==node:
            return True  ## ???
        
        if None==node.mChildNodes or 0==len(node.mChildNodes):
            return True
        else:
            return False      

    def getChildProperties(self, node):
        if None == node:
            return 
        
        if (None==node.mChildNodes) or (0==len(node.mChildNodes)):
            return
        
        for child in node.mChildNodes:
            if self.isLeafNode(child):
                if child.mVisible and child.mClickable: 
                    self.items_list.append(child)
            else:
                self.getChildProperties(child)
            
        
        
    
    def getLocationByIndex(self, index):
        pass
        