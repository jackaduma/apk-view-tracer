#! python2.7
## -*- coding: utf-8 -*-

#===============================================================================
# @author: kun
# @date: 2012-06-28
#===============================================================================

class Home():
    '''
    Physical Home Button
    '''
    
    def __init__(self, tree_nodes_list):
        self.tree_nodes_list = tree_nodes_list    
    
    def getElementList(self):
        elements_list = []
        
        for node in self.tree_nodes_list:
            if node.mActive:
                elements_list.append(node)
                
        return elements_list
    
    def getLocationByText(self, text):
        elements_list = self.getElementList()
        
        for element in elements_list:
            if text == element.mText:
                return element.mLocation
            
        return None
    
    def getLocationByKeyText(self, key_text):
        elements_list = self.getElementList()
        
        for element in elements_list:
            if 0 <= element.mText.find(key_text):
                return element.mLocation
        
        return None
    
    