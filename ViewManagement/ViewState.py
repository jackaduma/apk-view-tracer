#! python2.7
## -*- coding: utf-8 -*-

## kun for Apk View Tracing
## ViewState.py

import copy
from ParseElement import ParseElement

class ViewState():
    def __init__(self, node):
        self.node = node
        self.element_data = node.mElement
        self.element_parser = ParseElement(self.element_data)
        self.element_parser.parseElmentData()
        self.ViewGroup_ClassName_list = ["android.widget.ListView", 
                                         "android.widget.GridView", 
                                         "android.widget.RadioGroup",
                                         "android.widget.Spinner",
                                         "android.widget.Gallery"]
    
    ## The Visible state of parent node decide the Visible state of child node
    ## 应该是遍历所有的父节点的，但是下面的setNodeValue()函数是从root node开始，从上往下填值的，所以可以只判断自己和直接父节点的状态即可
    def getVisibleState(self):        
        if None == self.node.mParentNode:
            return self.element_parser.getVisible()
        else:
            parent_element_parser = ParseElement(self.node.mParentNode.mElement)
            parent_element_parser.parseElmentData()
            return (self.element_parser.getVisible() and parent_element_parser.getVisible())
    
    # 遍历所有父节点的方法
    # What does this method can do?  
    def getVisibleState_All(self):
        bResult = None
        temp_node = copy.deepcopy(self.node)        
        while (None != temp_node.mParentNode):
            temp_element_parser = ParseElement(temp_node.mElement)
            temp_element_parser.parseElmentData()
            bResult = temp_element_parser.getVisible() and temp_element_parser.getVisible()
            temp_node = temp_node.mParentNode
        return bResult
    
    ## Some Views 本身的 isClickable()=false, but its parent node 的 isClickable()=true
    ## so, these Views should be clickable
    ## for example, ListView, GridView,  etc. container View
    ## 但是如果，RadioGroup下包含了TextView和一些RadioButton,这个TextView是不可点击的吗？ 
    def getClickableState(self):
        parent_node = self.node.mParentNode
        
        if None == parent_node:
            return self.element_parser.getClickable()
                    
        parent_element_parser = ParseElement(parent_node.mElement)
        parent_element_parser.parseElmentData()
        parent_ClassName = parent_element_parser.getClassName()
        if parent_ClassName in self.ViewGroup_ClassName_list:
            return parent_element_parser.getClickable()
        else:
            return self.element_parser.getClickable()        
            
    
    ## mActive = False means it can not handle events
    ## mActive = True means it can handle events
    def getActiveState(self):
        try:
            if self.element_parser.getWillNotDraw():
                msg = "Will Not Draw!"
                return False
            if not self.getVisibleState():
                msg = "Not Visible!"
                return False
            if not self.getClickableState():
                msg = "Not Clickable!"
                return False
            if not self.element_parser.getDRAWN():
                msg = "Not Drawn!"
                return False
            else:
                return True
        except Exception,e:
            msg = "Failed to get Active State of Element! %s" %str(e)
            print msg
            return False

