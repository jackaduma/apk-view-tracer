#! python2.7
## -*- coding: utf-8 -*-

#===============================================================================
# @author: kun
#===============================================================================

import os,sys
current_path = os.getcwd()
parent_path = os.path.abspath(os.path.join(os.getcwd(), os.path.pardir))
if current_path not in sys.path:
    sys.path.append(current_path)
if parent_path not in sys.path:
    sys.path.append(parent_path)
    
from ViewManagement import ParseElement

class ProgressBar():
    '''
    ProgressBar
    '''
    
    def __init__(self, tree_nodes_list):
        self.tree_nodes_list = tree_nodes_list
        self.ProgressBar_ClassName = "android.widget.ProgressBar"    
    
    '''
    @return: percent value
    '''
    def getCurrentProgress(self):
        for node in self.tree_nodes_list:
            if node.mClassName==self.ProgressBar_ClassName:
                element_parser = ParseElement.ParseElement(node.mElement)
                element_parser.parseElmentData()
                if element_parser.getBoolean(element_parser.properties_dict["progress:isIndeterminate()"], True):
                    continue
                max_value = element_parser.getInt(element_parser.properties_dict["progress:getMax()"], 100)
                current_value = element_parser.getInt(element_parser.properties_dict["progress:getProgress()"], 0)
                second_value = element_parser.getInt(element_parser.properties_dict["progress:getSecondaryProgress()"], 0)
                
                percent = float(current_value)/float(max_value) * 100
                if percent>0 and percent<=100:
                    return percent
                
                percent = float(second_value)/float(max_value) * 100
                if percent>0 and percent<=100:
                    return percent
                
        return None            
                 
    '''
    @return: percent value
    '''    
    def getProgressById(self, id):
        if 0==len(id):
            return None
        
        real_id = "id/"+id
        for node in self.tree_nodes_list:
            if (node.mClassName==self.ProgressBar_ClassName) and (real_id==node.mId):
                element_parser = ParseElement.ParseElement(node.mElement)
                element_parser.parseElmentData()
                if element_parser.getBoolean(element_parser.properties_dict["progress:isIndeterminate()"], True):
                    continue
                max_value = element_parser.getInt(element_parser.properties_dict["progress:getMax()"], 100)
                current_value = element_parser.getInt(element_parser.properties_dict["progress:getProgress()"], 0)
                second_value = element_parser.getInt(element_parser.properties_dict["progress:getSecondaryProgress()"], 0)
                
                percent = float(current_value)/float(max_value) * 100
                if percent>0 and percent<=100:
                    return percent
                
                percent = float(second_value)/float(max_value) * 100
                if percent>0 and percent<=100:
                    return percent  
            
        return None
    
    
    '''
    @return: percent value
    '''
    def getProgressByText(self, text):
        if 0==len(text):
            return None

        for node in self.tree_nodes_list:
            try:
                if node.mVisible and (node.mClassName==self.ProgressBar_ClassName) and (node.mText != None) and (text==node.mText):
                    element_parser = ParseElement.ParseElement(node.mElement)
                    element_parser.parseElmentData()
                    if element_parser.getBoolean(element_parser.properties_dict["progress:isIndeterminate()"], True):
                        continue
                    max_value = element_parser.getInt(element_parser.properties_dict["progress:getMax()"], 100)
                    current_value = element_parser.getInt(element_parser.properties_dict["progress:getProgress()"], 0)
                    second_value = element_parser.getInt(element_parser.properties_dict["progress:getSecondaryProgress()"], 0)
                    
                    percent = float(current_value)/float(max_value) * 100
                    if percent>0 and percent<=100:
                        return percent
                    
                    percent = float(second_value)/float(max_value) * 100
                    if percent>0 and percent<=100:
                        return percent
            except Exception, e:
                self.m_logger.error("Current text fail to match string: [%s] " %e)
                continue
            
        return None
    
    def getProgressByKeyWord(self, key_word):
        if 0==len(key_word):
            return None

        for node in self.tree_nodes_list:
            try:
                if node.mVisible and (node.mClassName==self.ProgressBar_ClassName) and (node.mText != None) and (node.mText.find(key_word)>=0):
                    element_parser = ParseElement.ParseElement(node.mElement)
                    element_parser.parseElmentData()
                    if element_parser.getBoolean(element_parser.properties_dict["progress:isIndeterminate()"], True):
                        continue
                    max_value = element_parser.getInt(element_parser.properties_dict["progress:getMax()"], 100)
                    current_value = element_parser.getInt(element_parser.properties_dict["progress:getProgress()"], 0)
                    second_value = element_parser.getInt(element_parser.properties_dict["progress:getSecondaryProgress()"], 0)
                    
                    percent = float(current_value)/float(max_value) * 100
                    if percent>0 and percent<=100:
                        return percent
                    
                    percent = float(second_value)/float(max_value) * 100
                    if percent>0 and percent<=100:
                        return percent
            except Exception, e:
                self.m_logger.error("Current text fail to find sub string: [%s] " %e)
                continue
            
        return None        
    
    
    