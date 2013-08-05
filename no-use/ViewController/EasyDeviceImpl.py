#! python2.7
## -*- coding: utf-8 -*-

## kun for Apk View Tracing
## EasyDeviceImpl.py


import os, sys
curDir = os.getcwd()
sys.path.append(curDir)
from com.android.monkeyrunner.easy import By, EasyMonkeyDevice
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice, MonkeyImage
from MonkeyRunnerImpl import MonkeyRunnerImpl

class EasyDevice():
    def __init__(self, logger, monkey_runner_impl):
        self.easy_device = EasyMonkeyDevice(monkey_runner_impl.device)
        self.action_type_dict = {"DOWN_AND_UP": MonkeyDevice.DOWN_AND_UP,
                                 "DOWN": MonkeyDevice.DOWN,
                                 "UP": MonkeyDevice.UP}
        self.class_name = "EasyDevice"
        self.m_logger = logger

#------------------------------------------------------------------------------ 
# special functions:
#------------------------------------------------------------------------------ 
    def getFocusedWindowClassName(self):
        try:
            return self.easy_device.getFocusedWindowId()
        except Exception, e:
            msg = "[%s] Failed to get focused window class name: [%s]" %(self.class_name, str(e))
            self.m_logger.error(msg)
            return None
    
    def getVisibleById(self, str_id):
        try:
            return self.easy_device.visible(By.id("id/" + str_id))
        except Exception, e:
            msg = "[%s] Failed to get visible by Id: [%s] " %(self.class_name, str(e))
            self.m_logger.error(msg)
            return None
    
    def getLocationById(self, str_id):
        try:
            return self.easy_device.locate(By.id("id/" + str_id))
        except Exception, e:
            msg = "[%s] Failed to get Location by Id: [%s]" %(self.class_name, str(e))
            self.m_logger.error(msg)
            return None
    
    def getTextById(self, str_id):
        try:
            return self.easy_device.getText(By.id("id/" + str_id))
        except Exception, e:
            msg = "[%s] Failed to get Text by Id: [%s]" %(self.class_name, str(e))
            self.m_logger.error(msg)
            return None
    
    def getElementCenterById(self, str_id):
        try:
            return self.easy_device.getElementCenter(By.id("id/" + str_id))
        except Exception, e:
            msg = "[%s] Failed to get element center by Id: [%s]" %(self.class_name, str(e))
            self.m_logger.error(msg)
            return None
        
    def getExistById(self, str_id):
        try:
            return self.easy_device.exists(By.id("id/" + str_id))
        except Exception, e:
            msg = "[%s] Failed to get exist by Id: [%s]" %(self.class_name, str(e))
            self.m_logger.error(msg)
            return None
            
    def touchById(self, str_id, action_type="DOWN_AND_UP"):
        try:
            return self.easy_device.touch(By.id("id/" + str_id), self.action_type_dict[action_type])
        except Exception, e:
            msg = "[%s] Failed to touch by Id: [%s]" %(self.class_name, str(e))
            self.m_logger.error(msg)
            return None
    
    def typeInViewById(self, str_id, str_msg):
        try:
            self.easy_device.type(By.id("id/" + str_id), str_msg)
            return True
        except Exception, e:
            msg = "[%s] Failed to type in view [%s]" %(self.class_name, str(e))
            self.m_logger.error(msg)
            return False
        
    
if __name__ == "__main__":
    # testing
    monkey_runner_impl = MonkeyRunnerImpl()
    easy_device = EasyDevice(monkey_runner_impl)
    print easy_device.getVisibleById("del")
    print easy_device.getLocationById("del")
    print easy_device.touchById("del")
