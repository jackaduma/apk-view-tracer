#! python2.7
## -*- coding: utf-8 -*-

## kun for Apk View Tracing
## IChimpDeviceImpl.py

import os, sys
curDir = os.getcwd()
sys.path.append(curDir)
from com.android.monkeyrunner import MonkeyRunner
from MonkeyRunnerImpl import MonkeyRunnerImpl

class IChimpDevice():
    def __init__(self, logger, monkey_runner_impl):
        self.class_name = "IChimpDevice"
        self.m_logger = logger
        
        self.ichimp_device = monkey_runner_impl.device.getImpl()
        
        self.action_type_dict = {"DOWN": MonkeyRunner.DOWN,
                                 "UP": MonkeyRunner.UP,
                                 "DOWN_AND_UP": MonkeyRunner.DOWN_AND_UP
                                 }
        

#------------------------------------------------------------------------------ 
# special functions:
#------------------------------------------------------------------------------         
    def getFocusedWindowClassName(self):
        HV = self.ichimp_device.getHierarchyViewer()
        try:
            return HV.getFocusedWindowName()
        except Exception, e:
            msg = "[%s] Failed to get focused window's class name: [%s]" %(self.class_name, str(e))
            self.m_logger.error(msg)
            return None

    def typeOnFocusedWindow(self, str_msg):
        try:
            self.ichimp_device.type(str_msg)
            return True
        except Exception, e:
            msg = "[%s] Failed to type on focused window: [%s]" %(self.class_name, str(e))
            self.m_logger.error(msg)
            return False


#------------------------------------------------------------------------------ 
# common functions:
#------------------------------------------------------------------------------     
    def press(self, str_key_code, action_type="DOWN_AND_UP"):
        try:
            self.ichimp_device.press(str_key_code, self.action_type_dict[action_type])
            return True
        except Exception, e:
            msg = "[%s] Failed to press: [%s]" %(self.class_name, str(e))
            self.m_logger.error(msg)
            return False
        
    def touch(self, intX, intY, action_type="DOWN_AND_UP"):
        try:
            self.ichimp_device.touch(intX, intY, self.action_type_dict[action_type])
            return True
        except Exception, e:
            msg = "[%s] Failed to touch: [%s]" %(self.class_name, str(e))
            self.m_logger.error(msg)
            return False
        
    def drag(self, int_fromX, int_fromY, int_toX, int_toY, int_duration, long_steps):
        try:
            self.ichimp_device.drag(int_fromX, int_fromY, int_toX, int_toY, int_duration, long_steps)
            return True
        except Exception, e:
            msg = "[%s] Failed to drag: [%s]" %(self.class_name, str(e))
            self.m_logger.error(msg)
            return False

    def installPkg(self, str_package_name):
        try:
            return self.ichimp_device.installPackage(str_package_name)
        except Exception, e:
            msg = "[%s] Failed to install package: [%s]" %(self.class_name, str(e))
            self.m_logger.error(msg)
            return None
    
    def removePkg(self, str_package_name):
        try:
            return self.ichimp_device.removePackage(str_package_name)
        except Exception, e:
            msg = "[%s] Failed to remove package: [%s]" %(self.class_name, str(e))
            self.m_logger.error(msg)
            return None
        
    def shell(self, command):
        try:
            self.ichimp_device.shell(command)
            return True
        except Exception, e:
            msg =  "[%s] Failed to execute shell [%s]: [%s]" %(self.class_name, command, str(e))
            self.m_logger.error(msg)
            return False
    
if __name__ == "__main__":
    monkey_runner_impl = MonkeyRunnerImpl()
    ichimp_device = IChimpDevice(monkey_runner_impl)
    ichimp_device.getFocusedWindowClassName()