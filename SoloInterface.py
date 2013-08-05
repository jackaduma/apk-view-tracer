#! python2.7
## -*- coding: utf-8 -*-

## kun for Apk View Tracing
## SoloInterface.py

import logging, time
import Logger
from DeviceManagement.Device import Device
from ViewManagement.ViewTree import ViewTree
from ViewManagement import ParseElement
from ViewController.EventController import EventController
from SystemComponent import Notification, ProgressBar, GroupView, PopupView, ActionBar

class SoloInterface():
    '''
    Solo Interface for Automated Testing
    '''
        
    Android_Class_Name_Dict = { "Button":  "android.widget.Button",
                                "CheckBox": "android.widget.CheckBox",
                                "EditText" : "android.widget.EditText",
                                "ImageButton": "android.widget.ImageButton",
                                "ImageVIew": "android.widget.ImageView",
                                "RadioButton": "android.widget.RadioButton",
                                "TextView": "android.widget.TextView",
                                "View": "android.view.View",
                                "ProgressBar": "android.widget.ProgressBar",
                                "ScrollView": "android.widget.ScrollView"}
          
    def __init__(self, device_name="emulator-5554", device_port=5554, device_address="127.0.0.1", view_server_port=4939, monkey_server_port=12345):
        '''
        Constructor
        '''
        self.class_name = "SoloInterface"
        self.m_logger = Logger.InitLog("solo-interface.log", logging.getLogger("solo-interface.thread"))
        
        self.device_name = device_name
        self.device_port = device_port
        self.device_address = device_address
        
        self.view_server_port = view_server_port
        self.monkey_server_port = monkey_server_port
        
        # object of Device
        self.device = Device(self.m_logger, self.device_name, self.device_port, self.device_address, self.view_server_port, self.monkey_server_port)        
        # init device
        self.device.open()
        
        # build View Tree
        self.vt = ViewTree(self.m_logger)
        
        self.tree_nodes_list = None
        
        # object of View Controller 
        self.event_controller = EventController(self.m_logger, self.device_name, self.device_port, self.device_address, self.monkey_server_port)
        # init event controller
        self.event_controller.open()
        
        try:
            self.device_display_width = int(self.event_controller.getDisplayWidth())
            self.device_display_height = int(self.event_controller.getDisplayHeight())
            
#            LCD density is in the build.prop:
#            adb shell getprop ro.sf.lcd_density
#            And the resolution is availble in the dumpsys of the input activity:            
#            # windows
#            adb shell dumpsys window | find "DisplayWidth"
#            # linux
#            adb shell dumpsys window | grep DisplayWidth
        except Exception, e:
            print "Failed to get device display width and height: [%s]" %str(e)
        # to 480*800 display
        # Notification (y: 0-37  / x: 8-471 )
        self.notification_height = 37
        
        self.abs_action_bar_bottom = None
    
    def setUp(self):
        data = self.device.getDumpData()
        # key point
        if None!=self.tree_nodes_list and 0!=len(self.tree_nodes_list):
            del self.tree_nodes_list     
        self.tree_nodes_list = self.vt.build(data)        
        
    def tearDown(self):
        # do nothing
        pass

    def close(self):
        # release socket connect with Monkey Server
        self.event_controller.close()       
        # release socket connect with Android View Server
        self.device.close()
        
        
#'''adb shell command'''------------------------------------------------------------------------------ 

    def installPackage(self, package_name):
        return self.device.adb_console.installPkg(package_name)
    
    def removePackage(self, package_name):
        return self.device.adb_console.removePkg(package_name)
    
    def shell(self, command):
        return self.device.adb_console.shell(command)
    
    def shellForResult(self, command):
        return self.device.adb_console.shell(command, True)
    
    def startActivity(self, uri=None, action=None, data=None, mimetype=None, categories_list=None, component=None, flags_list=None, extras_list=None):
        self.device.adb_console.startActivity(uri, action, data, mimetype, categories_list, component, flags_list, extras_list)            
        time.sleep(1)
        self.setUp()
        
    def pushFile(self, local_path, device_path):
        return self.device.adb_console.pushFile(local_path, device_path)
    
    def pullFile(self, device_path, local_path):
        return self.device.adb_console.pullFile(device_path, local_path)

#Basic Operation------------------------------------------------------------------------------ 
    def searchForViewClassName(self, class_name):
        for node in self.tree_nodes_list:
            if class_name == node.mClassName:
                return True
            
        return False
    
    def searchForText(self, text, partial_matching=True):
        if partial_matching:
            for node in self.tree_nodes_list:
                try:
                    if node.mVisible and (node.mText != None) and (node.mText.find(text)>=0):
                        return True
                except Exception, e:
                    self.m_logger.error("Current text fail to find sub string: [%s] " %e)
                    continue
        else:            
            for node in self.tree_nodes_list:
                try:
                    if node.mVisible and (node.mText != None) and (text == node.mText):
                        return True
                except Exception, e:
                    self.m_logger.error("Current text fail to match string: [%s] " %e)
                    continue        
        return False
    
    def searchForViewID(self, id):
        real_id = "id/"+id
        for node in self.tree_nodes_list:
            if real_id == node.mId:
                return True            
        return False
    
    def getCurrentViewClassName(self):
        return self.device.view_console.getFocusViewClassName()
    
    def existViewByClassName(self, class_name):
        for node in self.tree_nodes_list:
            if class_name == node.mClassName:
                return True            
        return False
    
    def existViewByText(self, text, partial_matching=True):
        if partial_matching:
            for node in self.tree_nodes_list:
                try:
                    if node.mVisible and (node.mText != None) and (node.mText.find(text)>=0):
                        return True
                except Exception, e:
                    self.m_logger.error("Current text fail to find sub string: [%s] " %e)
                    continue
        else:
            for node in self.tree_nodes_list:
                try:
                    if node.mVisible and (node.mText != None) and (text == node.mText):
                        return True
                except Exception, e:
                    self.m_logger.error("Current text fail to match string: [%s] " %e)
                    continue
        return False
    
    def existViewById(self, id):
        real_id = "id/"+id
        for node in self.tree_nodes_list:
            if real_id == node.mId:
                return True        
        return False
    
    def isVisibleById(self, id):
        real_id = "id/"+id
        for node in self.tree_nodes_list:
            if real_id == node.mId:
                return node.mVisible            
        return False
    
    def isClickableById(self, id):
        real_id = "id/"+id
        for node in self.tree_nodes_list:
            if real_id == node.mId:
                return node.mClickable
        return False
    
    def clickViewById(self, id, ReDump=True):
        if 0==len(id):
            return False
        
        real_id = "id/"+id
        for node in self.tree_nodes_list:
            if real_id == node.mId:
                if not self.event_controller.tap(node.mLocation.x, node.mLocation.y):
                    return False
                if ReDump:
                    time.sleep(2)
                    self.setUp()
                return True
            
        return False
    
    def clickViewByText(self, text, partial_matching=True):
        if 0==len(text):
            return False
        
        if partial_matching:
            for node in self.tree_nodes_list:
                try:
                    if node.mVisible and (node.mText != None) and (node.mText.find(text)>=0):
                        if not self.event_controller.tap(node.mLocation.x, node.mLocation.y):
                            return False
                        self.setUp()
                        return True
                except Exception, e:
                    self.m_logger.error("Current text fail to find sub string: [%s] " %e)
                    continue
        else:
            for node in self.tree_nodes_list:
                try:
                    if node.mVisible and (node.mText != None) and (text == node.mText):
                        if not self.event_controller.tap(node.mLocation.x, node.mLocation.y):
                            return False
                        self.setUp()
                        return True
                except Exception, e:
                    self.m_logger.error("Current text fail to match string: [%s] " %e)
                    continue
            
        return False
            
    def getTextById(self, id):
        if 0==len(id):
            return None
        
        real_id = "id/"+id
        for node in self.tree_nodes_list:
            if real_id == node.mId:
                return node.mText
            
        return None
    
    
    def clearEditTextById(self, id):
        if 0==len(id):
            return False
        
        # make the cursor can focus at this edit text
        self.clickViewById(id, False)
        self.goBack(False)
        
        real_id = "id/"+id
        for node in self.tree_nodes_list:
            if real_id == node.mId:
                length = len(node.mText)
                while 0<length:
                    self.event_controller.press("del")
                    length-=1
                
                self.setUp()
                return True
            
        return False
    
    ## another method: adb shell input text
    ## the blank '' should be replaced by ASCII code '\x20', but it can not work now.
    ## the blank '' also can be input by "adb shell input keyevent 62"  or "key down 62"
    def setEditTextById(self, id, text):
        
        if 0==len(id) or 0==len(text):
            return False
        
        # make the cursor can focus at this edit text
        self.clickViewById(id, False)
        self.goBack(False)
        
        real_id = "id/"+id
        for node in self.tree_nodes_list:
            if real_id == node.mId:
                length = len(node.mText)
                while 0<length:
                    self.event_controller.press("del")
                    length-=1
                                
                if not self.event_controller.type(text):
                    return False
                self.setUp()
                return True
            
        return False
    
    def appendEditTextById(self, id, text):
        if 0==len(id) or 0==len(text):
            return False
        
        # make the cursor can focus at this edit text
        self.clickViewById(id, False)
        self.goBack(False)
        
        real_id = "id/"+id
        for node in self.tree_nodes_list:
            if real_id == node.mId:
                if not self.event_controller.type(text):
                    return False
                self.setUp()
                return True
        
        return False
    
    '''
    this method for simple Checkbox or RadioButton
    android.widget.RadioButton
    android.widget.CheckBox
    '''
    def isCheckedById(self, id):
        view_name_list = ["android.widget.RadioButton", "android.widget.CheckBox"]
        if 0==len(id):
            return False
        
        real_id = "id/"+id
        for node in self.tree_nodes_list:
            if self.isViewType(node.mClassName, view_name_list) and (real_id==node.mId):
                element_parser = ParseElement.ParseElement(node.mElement)
                element_parser.parseElmentData() 
                return element_parser.getBoolean("isChecked()", False)
        
        return False
    
    def isCheckedByText(self, text, partial_matching=True):
        view_name_list = ["android.widget.RadioButton", "android.widget.CheckBox"]
        if 0==len(text):
            return False
        
        if partial_matching:
            for node in self.tree_nodes_list:
                try:
                    if node.mVisible and self.isViewType(node.mClassName, view_name_list) and (node.mText != None) and (node.mText.find(text)>=0):
                        element_parser = ParseElement.ParseElement(node.mElement)
                        element_parser.parseElmentData()
                        return element_parser.getBoolean("isChecked()", False)
                except Exception, e:
                    self.m_logger.error("Current text fail to find sub string: [%s] " %e)
                    continue
        else:
            for node in self.tree_nodes_list:
                try:
                    if node.mVisible and self.isViewType(node.mClassName, view_name_list) and (node.mText != None) and (text==node.mText):
                        element_parser = ParseElement.ParseElement(node.mElement)
                        element_parser.parseElmentData() 
                        return element_parser.getBoolean("isChecked()", False)
                except Exception, e:
                    self.m_logger.error("Current text fail to match string: [%s] " %e)
                    continue
        return False

#internal interface------------------------------------------------------------------------------ 
    '''
    judge whether class name belongs to view_name_list
    @param param: node.mClassName
                 list of views name
    @return: True or False
    '''
    def isViewType(self, class_name, view_name_list):
        for name in view_name_list:
            if name == class_name:
                return True
        return False
    
#Physical Button Operations------------------------------------------------------------------------------ 

    def longPressHome(self):
        if not self.event_controller.longPressByKeyCode("home"):
            return False
        self.setUp()
        return True
    
    def pressHome(self):
        if not self.event_controller.press("home"):
            return False
        self.setUp()
        return True
    
    def callMenu(self):
        if not self.event_controller.press("menu"):
            return False
        self.setUp()
        return True
    
    def goBack(self, ReDump=True):
        # another method:
        # self.device.adb_console.shell("input keyevent 4")
        if not self.event_controller.press("back"):
            return False
        if ReDump:
            self.setUp()
        return True
    
    def callDelete(self, reDump=False):
        if not self.event_controller.press("del"):
            return False
        if reDump:
            self.setUp()
        return True
    
    def callLeft(self, reDump=False):
        if not self.event_controller.press("dpad_left"):
            return False
        if reDump:
            self.setUp()
        return True
    
    def callRight(self, reDump=False):
        if not self.event_controller.press("dpad_right"):
            return False
        if reDump:
            self.setUp()
        return True
    
    def callUp(self, reDump=False):
        if not self.event_controller.press("dpad_up"):
            return False
        if reDump:
            self.setUp()
        return True
    
    def callDown(self, reDump=False):
        if not self.event_controller.press("dpad_down"):
            return False
        if reDump:
            self.setUp()
        return True
    
#Device Operation with GSM------------------------------------------------------------------------------
    def sendSMS(self, recv_num, text):
        return self.device.device_console.sendSMS(recv_num, text)
    
    def makePhoneCall(self, phone_num):
        return self.device.device_console.makePhoneCall(phone_num)
    
    def cancelPhoneCall(self, phone_num):
        return self.device.device_console.cancelPhoneCall(phone_num)

#Operation with Notification------------------------------------------------------------------------------ 
    def callNotification(self):
        if not self.event_controller.drag(100, 20, 100, 500):
            return False
        self.setUp()
        return True
    
    def clearAllNotifications(self, reDump=False):
        notifies = Notification.Notification(self.tree_nodes_list)
        location = notifies.getClearButtonLocation()
        if not self.event_controller.tap(location.x, location.y):
            return False
        if reDump:
            self.setUp()        
        return True
    
    def clickNotificationItemByText(self, text, partial_matching=True):
        if 0==len(text):
            return False
        
        notifies = Notification.Notification(self.tree_nodes_list)
        notifies.loadAllItems()
        
        if partial_matching:            
            location = notifies.getLocationByKeyWord(text)
        else:
            location = notifies.getLocationByText(text)
            
        if not self.event_controller.tap(location.x, location.y):
            return False
        self.setUp()
        return True       

#Operation with ProgressBar------------------------------------------------------------------------------  
    def getCurrentProgress(self):
        progress_bar = ProgressBar.ProgressBar(self.tree_nodes_list)
        return progress_bar.getCurrentProgress()
   
    def getProgressById(self, id):
        progress_bar = ProgressBar.ProgressBar(self.tree_nodes_list)
        return progress_bar.getProgressById(id)
    
    def getProgressByText(self, text, partial_matching=True):
        progress_bar = ProgressBar.ProgressBar(self.tree_nodes_list)
        if partial_matching:
            return progress_bar.getProgressByKeyWord(text)
        else:
            return progress_bar.getProgressByText(text)
    
#------------------------------------------------------------------------------ 
    def assertCurrentActivity(self, expectedClassName):
        try:
            curActivityClassName = self.getCurrentViewClassName()
            if curActivityClassName == expectedClassName:
                return True
            else:
                return False
        except Exception, e:
            msg = "[%s] Failed to assert current activity [%s]" %(self.class_name, str(e))
            self.m_logger.error(msg)
            return None
        
    def assertCurrentActivityNewInstance(self, expectedClassName, oldHashCode):
        try:
            curActivityClassName = self.getCurrentViewClassName()
            curActivityHashCode = self.device.view_console.getFocusViewHashCode()
            if (curActivityClassName == expectedClassName) and (curActivityHashCode != oldHashCode):
                return True
            else:
                return False
        except Exception, e:
            msg = "[%s] Failed to assert current activity new instance [%s]" %(self.class_name, str(e))
            self.m_logger.error(msg)
            return None
   
    def longPressByText(self, text, partial_matching=True):
        if 0==len(text):
            return False
        
        if partial_matching: 
            for node in self.tree_nodes_list:
                try:
                    if node.mVisible and (node.mText != None) and (node.mText.find(text)>=0):
                        location = node.mLocation
                        if not self.event_controller.longPressByLocation(location.x, location.y):
                            return False 
                        time.sleep(1)       
                        self.setUp()
                        return True
                except Exception, e:
                    self.m_logger.error("Current text fail to find sub string: [%s] " %e)
                    continue
        else:
            for node in self.tree_nodes_list:
                try:
                    if node.mVisible and (node.mText != None) and (text == node.mText):
                        location = node.mLocation
                        if not self.event_controller.longPressByLocation(location.x, location.y):
                            return False   
                        time.sleep(1)     
                        self.setUp()
                        return True
                except Exception, e:
                    self.m_logger.error("Current text fail to match string: [%s] " %e)
                    continue       
        return False

#Operation with View Group such as ListView, ScrollView, GridView, etc.------------------------------------------------------------------------------ 
    def getItemsNumber(self, groupview_id, groupview_classname=None):
        if None==groupview_id or 0==len(groupview_id):
            return None
        
        real_id = "id/" + groupview_id
        for node in self.tree_nodes_list:
            if real_id==node.mId:
                element_parser = ParseElement.ParseElement(node.mElement)
                element_parser.parseElmentData()
                if None!=groupview_classname and 0!=len(groupview_classname):
                    if groupview_classname==node.mClassName:
                        if "list:mItemCount" in element_parser.properties_dict.keys():
                            return int(element_parser.properties_dict["list:mItemCount"])
                        else:
                            return len(node.mChildNodes)
                else:
                    if "list:mItemCount" in element_parser.properties_dict.keys():
                        return int(element_parser.properties_dict["list:mItemCount"])
                    else:
                        return len(node.mChildNodes)
            
        return None
            

    def clickItemByIndex(self, groupview_id, index=0):
        if None==groupview_id or 0==len(groupview_id):
            return False
        
        if None==index or (not isinstance(index, int)):
            return False
        
        real_id = "id/" + groupview_id
        for node in self.tree_nodes_list:
            if real_id==node.mId:
                groupview = GroupView.GroupView(node)
                groupview.loadAllItems()
                item = groupview.items_list[index]
                break
        
        for location in item.properties_dict["mLocation"]:
            if self.event_controller.tap(location.x, location.y):
                self.setUp()
                return True
            
        return False
    
    def clickItemByText(self, groupview_id, text, partial_matching=True):
        if None==groupview_id or 0==len(groupview_id):
            return False
        
        if None==text or 0==len(text):
            return False
        
        groupview = None
        real_id = "id/" + groupview_id
        for node in self.tree_nodes_list:
            if real_id==node.mId:
                groupview = GroupView.GroupView(node)
                groupview.loadAllItems()
                break
                
        if not partial_matching:
            for item in groupview.items_list:
                if text in item.properties_dict["mText"]:
                    # click this item
                    for location in item.properties_dict["mLocation"]:
                        if self.event_controller.tap(location.x, location.y):
                            self.setUp()
                            return True
        else:
            for item in groupview.items_list:                
                for msg in item.properties_dict["mText"]:
                    try:
                        if (None!=msg) and (msg.find(text)>=0):
                            # click this item
                            for location in item.properties_dict["mLocation"]:
                                if self.event_controller.tap(location.x, location.y):
                                    self.setUp()
                                    return True
                    except Exception, e:
                        self.m_logger.error("Current text fail to match string: [%s] " %e)
                        continue  
                              
        return False
    
    def isItemCheckedByIndex(self, groupview_id, index=0):
        if None==groupview_id or 0==len(groupview_id):
            return False
        
        if None==index or 0==len(index):
            return False
        
        real_id = "id/" + groupview_id
        for node in self.tree_nodes_list:
            if real_id==node.mId:
                groupview = GroupView.GroupView(node)
                groupview.loadAllItems()
                item = groupview.items_list[index]
                break
            
        return item.properties["isChecked"]
    
    def isItemCheckedByText(self, groupview_id, text, partial_matching=True):
        if None==groupview_id or 0==len(groupview_id):
            return False
        
        if None==text or 0==len(text):
            return False
        
        groupview = None
        real_id = "id/" + groupview_id
        for node in self.tree_nodes_list:
            if real_id==node.mId:
                groupview = GroupView.GroupView(node)
                groupview.loadAllItems()
                break
            
        if not partial_matching:
            for item in groupview.items_list:
                if text in item.properties_dict["mText"]:
                    return item.properties_dict["isChecked"]
        else:
            for item in groupview.items_list:
                for msg in item.properties_dict["mText"]:
                    try:
                        if (None!=msg) and (msg.find(text)>=0):
                            return item.properties_dict["isChecked"]
                    except Exception, e:
                        self.m_logger.error("Current text fail to match string: [%s] " %e)
                        continue
                                        
        return False            

#Popup View Operations------------------------------------------------------------------------------ 
    def typeInPopupByIndex(self, text, index=0):
        if None == text or 0 == len(text):
            return False
             
        if None==index:
            return False
        
        popup = PopupView.PopupView(self.tree_nodes_list, self.event_controller, self.device_display_width, self.device_display_height)
        popup.loadProperties()
        if popup.typeTextByIndex(text, index):
            time.sleep(1)
            self.setUp()
            return True
        
        return False
           
    def clickInPopupById(self, id):
        if None == id or 0==len(id):
            return False
        
        popup = PopupView.PopupView(self.tree_nodes_list, self.event_controller, self.device_display_width, self.device_display_height)
        popup.loadProperties()
        if popup.clickViewById(id):
            time.sleep(1)
            self.setUp()
            return True
        else:
            return False
    
    def clickInPopupByText(self, text, partial_matching=True):
        if None == text or 0 == len(text):
            return False
        
        popup = PopupView.PopupView(self.tree_nodes_list, self.event_controller, self.device_display_width, self.device_display_height)
        popup.loadProperties()
        if popup.clickViewByText(text, partial_matching):
            time.sleep(1)
            self.setUp()
            return True
        else:
            return False
        
    def selectInVerticalPopupByText(self, text, partial_matching=True):
        if None == text or 0 == len(text):
            return False
        
        popup = PopupView.PopupView(self.tree_nodes_list, self.event_controller, self.device_display_width, self.device_display_height)
        popup.loadProperties()
        
        if popup.focusViewByText(text, partial_matching, first_direction="dpad_down"):
            if self.event_controller.press("enter"):
                time.sleep(1)
                self.setUp()
                return True 
        
        return False

    def selectInHorizontalPopupByText(self, text, partial_matching=True):
        if None == text or 0 == len(text):
            return False
        
        popup = PopupView.PopupView(self.tree_nodes_list, self.event_controller, self.device_display_width, self.device_display_height)
        popup.loadProperties()
        
        if popup.focusViewByText(text, partial_matching, first_direction="dpad_right"):
            if self.event_controller.press("enter"):
                time.sleep(1)
                self.setUp()
                return True
            
        return False
        

    
#Menu Item Operation------------------------------------------------------------------------------
    def clickMenuItemById(self, id):
        if 0==len(id):
            return False
        
        real_id = "id/"+id
        view_height = self.tree_nodes_list[0].mAbsoluteRect.mBottom - self.tree_nodes_list[0].mAbsoluteRect.mTop
        for node in self.tree_nodes_list:
            if real_id == node.mId:
                realX = node.mLocation.x                
                realY = (self.device_display_height - view_height) + node.mLocation.y
                self.m_logger.info("realX: %s   realY: %s" %(realX, realY))
                if not self.event_controller.tap(realX, realY):
                    return False

                time.sleep(1)
                self.setUp()
                return True
            
        return False
    
    def clickMenuItemByText(self, text, partial_matching=True): 
        if 0==len(text):
            return False
        
        if partial_matching:
            view_height = self.tree_nodes_list[0].mAbsoluteRect.mBottom - self.tree_nodes_list[0].mAbsoluteRect.mTop
            for node in self.tree_nodes_list:
                try:
                    if node.mVisible and (node.mText != None) and (node.mText.find(text)>=0):
                        realX = node.mLocation.x
                        realY = (self.device_display_height - view_height) + node.mLocation.y
                        self.m_logger.info("realX: %s   realY: %s" %(realX, realY))
                        if not self.event_controller.tap(realX, realY):
                            return False                        
                        time.sleep(1)
                        self.setUp()
                        return True
                except Exception, e:
                    self.m_logger.error("Current text fail to match string: [%s] " %e)
                    continue
        else:
            view_height = self.tree_nodes_list[0].mAbsoluteRect.mBottom - self.tree_nodes_list[0].mAbsoluteRect.mTop
            for node in self.tree_nodes_list:
                if node.mVisible and (node.mText != None) and (text == node.mText):
                    realX = node.mLocation.x
                    realY = (self.device_display_height - view_height) + node.mLocation.y
                    self.m_logger.info("realX: %s   realY: %s" %(realX, realY))
                    if not self.event_controller.tap(realX, realY):
                        return False                    
                    time.sleep(1)
                    self.setUp()
                    return True
            
        return False

#Scroll Operation------------------------------------------------------------------------------ 
    def scrollDownToBottom(self):
        try:
            last_node = self.tree_nodes_list[-1]
            delta_height = last_node.mAbsoluteRect.mBottom - self.device_display_height
            step_count = delta_height/100 + 1
            if not self.event_controller.drag(self.device_display_width/2, self.device_display_height/8*6, 
                                       self.device_display_width/2, self.device_display_height/8*5, steps=step_count+1):
                return False        
            self.setUp()
            return True
        except Exception, e:
            self.m_logger.error("Failed to scroll to bottom. [%s]" %str(e))
            return False        
    
    def scrollUpToTop(self):
        try:
            first_node = self.tree_nodes_list[0]           
            self.setUp()
            return True
        except Exception, e:
            self.m_logger.error("Failed to scroll to top. [%s]" %str(e))
            return False
    
    def scrollDown(self):
        pass
    
    def scrollUp(self):
        pass
    
    def scrollToRight(self):
        try:
            if not self.event_controller.drag(self.device_display_width/8*6, self.device_display_height/2, 
                                       self.device_display_width/8*2, self.device_display_height/2, steps=5):
                return False        
            self.setUp()
            return True
        except Exception, e:
            self.m_logger.error("Failed to scroll to right. [%s]" %str(e))
            return False  
    
    def scrollToLeft(self):
        try:
            if not self.event_controller.drag(self.device_display_width/8*2, self.device_display_height/2, 
                                       self.device_display_width/8*6, self.device_display_height/2, steps=5):
                return False        
            self.setUp()
            return True
        except Exception, e:
            self.m_logger.error("Failed to scroll to right. [%s]" %str(e))
            return False 
    
#Action Bar Operation------------------------------------------------------------------------------             
    def getActionBarItemsNumber(self, actionbar_id, actionbar_classname=None):
        if None==actionbar_id or 0==len(actionbar_id):
            return None
        
        real_id = "id/" + actionbar_id
        for node in self.tree_nodes_list:
            if real_id==node.mId:
                element_parser = ParseElement.ParseElement(node.mElement)
                element_parser.parseElmentData()
                if None!=actionbar_classname and 0!=len(actionbar_classname):
                    if actionbar_classname==node.mClassName:
                        if "list:mItemCount" in element_parser.properties_dict.keys():
                            return int(element_parser.properties_dict["list:mItemCount"])
                        else:
                            actionbar = ActionBar.ActionBar(node)
                            actionbar.loadAllItems()
                            return len(actionbar.items_list)
                else:
                    if "list:mItemCount" in element_parser.properties_dict.keys():
                        return int(element_parser.properties_dict["list:mItemCount"])
                    else:
                        actionbar = ActionBar.ActionBar(node)
                        actionbar.loadAllItems()
                        return len(actionbar.items_list)            
        return None

    #===========================================================================
    # this id is the id of the ActionBarContainer 
    # from right to left, default the first<0> is ActionMenuView
    #===========================================================================
    def clickActionBarByIndex(self, actionbar_id, index=0):
        if None==actionbar_id or 0==len(actionbar_id):
            return False
        
        if None==index or (not isinstance(index, int)):
            return False
        
        real_id = "id/" + actionbar_id
        item = None
        for node in self.tree_nodes_list:
            if real_id==node.mId:
                self.abs_action_bar_bottom = node.mAbsoluteRect.mBottom               
                actionbar = ActionBar.ActionBar(node)
                actionbar.loadAllItems()
                item_count = len(actionbar.items_list)
                item = actionbar.items_list[abs(index+1-item_count)]
                break
        if None == item:
            return False
        
        if self.event_controller.tap(item.mLocation.x, item.mLocation.y):
            self.setUp()
            return True
            
        return False
    
    def clickActionMenu(self, actionbar_id="abs__action_bar"):
        return self.clickActionBarByIndex(actionbar_id, 0)
    
    def clickActionMenuItemByText(self, text, partial_matching=True):
        if None == self.abs_action_bar_bottom:
            return False
        
        if 0==len(text):
            return False
        
        if partial_matching:
            for node in self.tree_nodes_list:
                try:
                    if node.mVisible and (node.mText != None) and (node.mText.find(text)>=0):
                        real_location_x = self.device_display_width - node.mLocation.x 
                        real_location_y = node.mLocation.y + self.abs_action_bar_bottom
                        if not self.event_controller.tap(real_location_x, real_location_y):
                            return False
                        self.setUp()
                        return True
                except Exception, e:
                    self.m_logger.error("Current text fail to find sub string: [%s] " %e)
                    continue
        else:
            for node in self.tree_nodes_list:
                try:
                    if node.mVisible and (node.mText != None) and (text == node.mText):
                        real_location_x = self.device_display_width - node.mLocation.x 
                        real_location_y = node.mLocation.y + self.abs_action_bar_bottom
                        if not self.event_controller.tap(real_location_x, real_location_y):
                            return False
                        self.setUp()
                        return True
                except Exception, e:
                    self.m_logger.error("Current text fail to match string: [%s] " %e)
                    continue
            
        return False
           
if __name__=="__main__":
    solo = SoloInterface(device_name="emulator-5554")  #device_name="f0b23e6e"
    solo.setUp()

#------------------------------------------------------------------------------ 
#    solo.clickViewById("btn_signin")
#    for node in solo.tree_nodes_list:
#        print node.mId
#        print node.mText
#        print "----------------"
#    solo.setEditTextById("account", "mk@126.com")
#    solo.setEditTextById("password", "11111111")
#    solo.clickViewById("cb_eula")
#    solo.clickViewById("sign_in")
#------------------------------------------------------------------------------ 
    
#    solo.event_controller.touchDown(300, 600)
#    solo.event_controller.touchMove(300, 600)
#    solo.event_controller.touchMove(300, 400)
#    solo.event_controller.touchMove(300, 200)
#    solo.event_controller.touchUp(300, 200)   
    
#    solo.event_controller.drag(300, 600, 300, 200)
#    
#    solo.setUp()
#    
#    solo.clickViewByText("Scan Now", True)
#------------------------------------------------------------------------------ 

#    solo.clickViewByText("Mobile Security")

#------------------------------------------------------------------------------
#    solo.event_controller.press("dpad_down")
#    
#    time.sleep(2)
#    solo.event_controller.press("dpad_down")
#
#    time.sleep(2)
#    solo.event_controller.press("dpad_down")
#    
#    solo.event_controller.press("enter")
#------------------------------------------------------------------------------ 
#    solo.clickItemInVerticalPopupByIndex(2)

#------------------------------------------------------------------------------ 
#    solo.clickMenuItemByText("More")
#------------------------------------------------------------------------------ 

#    solo.callMenu()
#    solo.clickMenuItemByText("Add")
#    solo.typeInPopupByIndex("renren", 0)
#    solo.typeInPopupByIndex("http://www.renren.com", 1)
#    solo.clickInPopupByText("Save", False)
#    
#    solo.longPressByText("renren", False)
#    solo.clickInPopupByText("Delete", False)
#------------------------------------------------------------------------------ 
    


#    solo.clickItemByIndex("phone_malware_list", 0)  #scan_result_installmal
#    solo.clickViewById("cancel_button")
#    solo.clickItemByText("phone_malware_list", "Threat", True)
#    solo.clickViewById("cancel_button")

#------------------------------------------------------------------------------ 

#    solo.scrollToRight()
#    solo.scrollToLeft()

#------------------------------------------------------------------------------
    
    print solo.getActionBarItemsNumber("abs__action_bar")
    solo.clickActionBarByIndex("abs__action_bar", 0)
    
    solo.clickActionMenuItemByText("Help")

#------------------------------------------------------------------------------

    solo.clickActionBarByIndex("NO_ID", 0)
    solo.clickViewByText("Help")
        
    solo.close()
    print"success to end"
    
    
