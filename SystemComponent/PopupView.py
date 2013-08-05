#! python2.7
## -*- coding: utf-8 -*-

#===============================================================================
# @author: kun
#===============================================================================

import os, sys
from ast import parse
current_path = os.getcwd()
parent_path = os.path.abspath(os.path.join(os.getcwd(), os.path.pardir))
if current_path not in sys.path:
    sys.path.append(current_path)
if parent_path not in sys.path:
    sys.path.append(parent_path)

from ViewManagement.ParseElement import ParseElement

class PopupView():
    '''
    Popup View
    '''
    
    def __init__(self, tree_nodes_list, event_controller, device_width, device_height, notification_height=37):
        self.class_name = "Popup View"
        
        self.tree_nodes_list = tree_nodes_list
        self.event_controller = event_controller
        
        self.device_width = device_width
        self.device_height = device_height
        
        self.view_height = self.tree_nodes_list[0].mAbsoluteRect.mBottom - self.tree_nodes_list[0].mAbsoluteRect.mTop
        # to 480*800 display
        # Notification (y: 0-37  / x: 8-471 )
        self.notification_height = notification_height # this is not inexact
        
        self.focusable_view_list = []
        self.next_direction_list = []
        self.pre_direction_list = []
        self.currentFocusIndex = None        
    
    def loadProperties(self):
        index = 0
        for node in self.tree_nodes_list:
            if node.mVisible:
                if self.isListView(node):
                    for child in node.mChildNodes:
                        self.focusable_view_list.append(child)
                else:
                    element_parser = ParseElement(node.mElement)
                    element_parser.parseElmentData()
                    if "focus:isFocusable()" in element_parser.properties_dict.keys():
                        if element_parser.getBoolean("focus:isFocusable()", False):
                            self.focusable_view_list.append(node)
                            if element_parser.getBoolean("focus:isFocused()", False):  # or ["focus:hasFocus()"]
                                self.currentFocusIndex = index
                            index += 1
                                
        total = len(self.focusable_view_list)
        for i in range(total):
            if i == total-1:
                self.next_direction_list.append(None)
            else:                    
                if self.focusable_view_list[i].mLocation.y == self.focusable_view_list[i+1].mLocation.y:
                    self.next_direction_list.append("dpad_right")
                else:
                    self.next_direction_list.append("dpad_down")
                    
        for i in range(total):
            if 0 == i:
                self.pre_direction_list.append(None)
            else:
                if self.focusable_view_list[i].mLocation.y == self.focusable_view_list[i-1].mLocation.y:
                    self.pre_direction_list.append("dpad_left")
                else:
                    self.pre_direction_list.append("dpad_up")
                    
    #===========================================================================
    # listview : list:recycleOnMeasure()=4,true
    #            list:mNextSelectedPosition=2,-1 
    #            list:mSelectedPosition=2,-1 
    #            list:mItemCount=1,2
    #            focus:getDescendantFocusability()=24,FOCUS_BEFORE_DESCENDANTS+
    # list item : list:layout_forceAdd=5,false 
    #             list:layout_recycledHeaderFooter=5,false 
    #             list:layout_viewType=1,0
    #===========================================================================
    def isListView(self, node):
        element_parser = ParseElement(node.mElement)
        element_parser.parseElmentData()
        if "list:mItemCount" in element_parser.properties_dict.keys():
            return True
        else:
            return False
                    
    def getRealLocation(self, x, y):
        realX = x # this is not inexact
        
        deltaY = (self.device_height - self.notification_height - self.view_height) / 2
        
        realY = self.notification_height + deltaY + y
        
        return realX, realY
    
    def focusNext(self, first_direction="dpad_right"):
        if None == self.currentFocusIndex:
            self.event_controller.press(first_direction)
            self.currentFocusIndex = 0
        
        direction = self.next_direction_list[self.currentFocusIndex]
        self.event_controller.press(direction)
        self.currentFocusIndex += 1
            
    
    def focusPrevious(self, first_direction="dpad_left"):
        if None == self.currentFocusIndex:
            self.event_controller.press(first_direction)
            self.currentFocusIndex = 0
            
        direction = self.pre_direction_list[self.currentFocusIndex]
        self.event_controller.press(direction)
        self.currentFocusIndex -= 1
                    
    def focusHead(self, first_direction="dpad_right"):
        if None == self.currentFocusIndex:
            self.focusNext(first_direction)
            return True
        
        if 0 == self.currentFocusIndex:
            return True
        
        while 0<self.currentFocusIndex:
            self.focusPrevious()
        return True
    
    def focusTail(self, first_direction="dpad_right"):
        if None == self.currentFocusIndex:
            self.focusPrevious()
        
        tail_index = len(self.focusable_view_list)    
        while self.currentFocusIndex<tail_index:
            self.focusNext(first_direction)            
        return True
    
    def focusViewByIndex(self, index, first_direction="dpad_right"):
        if None == index:
            return False
        
        if None == self.currentFocusIndex:
            self.focusHead(first_direction)
        
        delta = index - self.currentFocusIndex
        
        if 0 == delta:
            return True
        elif delta > 0:
            while delta>0:
                self.focusNext(first_direction)
                delta -= 1
        elif delta < 0:
            while delta<0:
                self.focusPrevious()
                delta += 1
        return True
        
    def focusViewById(self, id):
        if None == id or 0 ==len(id):
            return False
        
        real_id = "id/" + id
        for node in self.focusable_view_list:
            if real_id == node.mId:
                pass
    
    def focusViewByText(self, text, partial_matching=True, first_direction="dpad_right"):
        if (None == text) or (0==len(text)):
            return False
        
        index = 0
        if partial_matching:
            for node in self.focusable_view_list:
                if node.mVisible and (None!=node.mText) and (node.mText.find(text)>=0):
                    self.focusViewByIndex(index, first_direction)
                index += 1
        else:
            for node in self.focusable_view_list:
                if node.mVisible and (None!=node.mText) and (text == node.mText):
                    self.focusViewByIndex(index, first_direction)
                index += 1
                
        return True
    
    #===========================================================================
    # # other method
    # def typeTextByIndex(self, text, index):
    #    self.focusViewByIndex(index)
    #    view_text_length = len(self.focusable_view_list[index].mText)
    #    if view_text_length>=0:
    #        element_parser = ParseElement(self.focusable_view_list[index].mElement)
    #        element_parser.parseElmentData()
    #        if "text:getSelectionEnd()" in element_parser.properties_dict.keys(): # or "text:getSelectionStart()"
    #            cursor_location = element_parser.getInt("text:getSelectionEnd()", 0)
    #            if view_text_length == cursor_location:
    #                self.event_controller.type(text)
    #            elif cursor_location<view_text_length:
    #                delta = view_text_length - cursor_location
    #                while delta>0:
    #                    self.event_controller.press("dpad_right")
    #                    delta -= 1
    #                self.event_controller.type(text)
    #===========================================================================                    

    def typeTextByIndex(self, text, index):
        
        self.focusViewByIndex(index)
        
        view_text_length = len(self.focusable_view_list[index].mText)
        if view_text_length>0:
            element_parser = ParseElement(self.focusable_view_list[index].mElement)
            element_parser.parseElmentData()
            if "text:getSelectionEnd()" in element_parser.properties_dict.keys(): # or "text:getSelectionStart()"
                cursor_location = element_parser.getInt("text:getSelectionEnd()", 0)
                if view_text_length == cursor_location:
                    self.event_controller.type(text)
                elif cursor_location<view_text_length:
                    delta = view_text_length - cursor_location
                    while delta>0:
                        self.event_controller.press("dpad_right")
                        delta -= 1
                    while view_text_length>0:
                        self.event_controller.press("del")
                        view_text_length -= 1
                    self.event_controller.type(text)
                    return True
        else:
            self.event_controller.type(text)
            return True
        
        return False
                    
        
    def clickViewById(self, id):
        if None==id or 0==len(id):
            return False
        
        real_id = "id/" + id
        for node in self.focusable_view_list:
            if real_id == node.mId:
                real_location = self.getRealLocation(node.mLocation.x, node.mLocation.y)
                self.event_controller.tap(int(real_location[0]), int(real_location[1]))
                return True
    
    def clickViewByText(self, text, partial_matching=True):
        if None == text or 0 == len(text):
            return False
        
        if partial_matching:
            for node in self.focusable_view_list:
                if node.mVisible and (None != node.mText) and (node.mText.find(text)>=0):
                    real_location = self.getRealLocation(node.mLocation.x, node.mLocation.y)
                    self.event_controller.tap(int(real_location[0]), int(real_location[1]))
                    return True                    
        else:
            for node in self.focusable_view_list:
                if node.mVisible and (None != node.mText) and (text == node.mText):
                    real_location = self.getRealLocation(node.mLocation.x, node.mLocation.y)
                    self.event_controller.tap(int(real_location[0]), int(real_location[1]))
                    return True
                     
    
    def clickViewByIndex(self, index):
        self.focusViewByIndex(index)
        self.event_controller.press("enter")    

if __name__=="__main__":
    pass

