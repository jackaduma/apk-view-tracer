#! python2.7
## -*- coding: utf-8 -*-

## kun for Apk View Tracing
## MonkeyRunnerImpl.py

## run mode
## java -jar $(jython.jar file path) $(python script file)

## adb shell monkey <...>

## start monkey server
## adb forward tcp:1080 tcp:1080
## adb shell monkey --port 1080

import os, sys
curDir = os.getcwd()
parent_path = os.path.abspath(os.path.join(os.getcwd(), os.path.pardir))
if curDir not in sys.path:
    sys.path.append(curDir)
if parent_path not in sys.path:
    sys.path.append(parent_path)
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice, MonkeyImage, MonkeyView
from com.android.monkeyrunner.recorder import MonkeyRecorder
import Logger
import logging

class MonkeyRunnerImpl():
    def __init__(self, logger, device_name=None):
        self.class_name = "MonkeyRunnerImpl"
        ## command map
        self.CMD_MAP = {"TOUCH": lambda dev, arg: dev.touch(**arg),
                        "DRAG": lambda dev, arg: dev.drag(**arg),
                        "PRESS": lambda dev, arg: dev.press(**arg),
                        "TYPE": lambda dev, arg: dev.type(**arg),
                        "SLEEP": lambda dev, arg: MonkeyRunner.sleep(**arg)
                        }

        self.PhysicalButton={"HOME": "KEYCODE_HOME", 
                             "SEARCH": "KEYCODE_SEARCH", 
                              "MENU": "KEYCODE_MENU", 
                              "BACK": "KEYCODE_BACK", 
                              "POWER": "KEYCODE_POWER",
                              "DPAD_UP": "DPAD_UP", 
                              "DPAD_DOWN": "DPAD_DOWN", 
                              "DPAD_LEFT": "DPAD_LEFT", 
                              "DPAD_RIGHT": "DPAD_RIGHT", 
                              "DPAD_CENTER": "DPAD_CENTER", 
                              "ENTER": "enter"
                            }
        self.action_type_list=["DOWN", "UP", "DOWN_AND_UP"]
        self.action_down = "DOWN"
        self.action_up = "UP"
        self.action_down_and_up = "DOWN_AND_UP"
        
        self.m_logger = logger
                
        if None!=device_name:
            self.device = MonkeyRunner.waitForConnection(deviceId=device_name)
        else:
            self.device = MonkeyRunner.waitForConnection()
            
#------------------------------------------------------------------------------ 
# basic operation, include press, touch, drag, type, etc.
           
    def press(self, key_code, action_type):
        try:
            self.device.press(key_code, action_type)
            return True
        except Exception, e:
            msg = "[%s] Failed to press: [%s]" %(self.class_name, str(e))
            self.m_logger.error(msg)
            return False
        
    def clickPowerButton(self):
        try:
            self.device.press("KEYCODE_POWER", "DOWN_AND_UP")
            return True
        except Exception, e:
            msg = "[%s] Failed to click power button: [%s]" %(self.class_name, str(e))
            self.m_logger.error(msg)
            return False
    
    def clickHomeButton(self):
        try:
            self.device.press("KEYCODE_HOME", "DOWN_AND_UP")
            return True
        except Exception, e:
            msg = "[%s] Failed to click Home button: [%s]" %(self.class_name, str(e))
            self.m_logger.error(msg)
            return False
    
    def clickMenuButton(self):
        try:
            self.device.press("KEYCODE_MENU", "DOWN_AND_UP")
            return True
        except Exception, e:
            print "[%s] Failed to click Menu button: [%s]" %(self.class_name, str(e))
            return False
    
    def clickBackButton(self):
        try:
            self.device.press("KEYCODE_BACK", "DOWN_AND_UP")
            return True
        except Exception, e:
            msg = "[%s] Failed to click Back button: [%s]" %(self.class_name, str(e))
            self.m_logger.error(msg)
            return False
    
    def clickSearchButton(self):
        try:
            self.device.press("KEYCODE_SEARCH", "DOWN_AND_UP")
            return True
        except Exception, e:
            msg = "[%s] Failed to click Search button: [%s]" %(self.class_name, str(e))
            self.m_logger.error(msg)
            return False
    
    #- Simulates a drag gesture (touch, hold, and move) on this device's screen.
    def drag(self, fromX, fromY, toX, toY, duration=0.1, steps=2):
        try:
            self.device.drag((fromX, fromY), (toX, toY), duration, steps)
            return True
        except Exception, e:
            msg = "[%s] Failed to drag: [%s]" %(self.class_name, str(e))
            self.m_logger.error(msg)
            return False
    
    def touch(self, targetX, targetY, action_type):
        try:
            self.device.touch(targetX, targetY, action_type)
            return True
        except Exception, e:
            msg = "[%s] Failed to touch: [%s]" %(self.class_name, str(e))
            self.m_logger.error(msg)
            return False
        
    def clickByLocation(self, x, y):
        return self.touch(x, y, "DOWN_AND_UP")
    
    # implement by using android's bug
    def longClickByLocation(self, x, y):
        try:
            self.device.drag(x, y, x, y, 10, 1)
            return True
        except Exception, e:
            msg = "[%s] Failed to long click by Location: [%s]" %(self.class_name, str(e))
            self.m_logger.error(msg)
            return False
        
#------------------------------------------------------------------------------ 
# system operation, include reboot, sleep, wake
#------------------------------------------------------------------------------ 

    def shell(self, command):
        try:
            return self.device.shell(command)
        except Exception, e:
            msg = "[%s] Failed to execute shell [%s]: [%s]" %(self.class_name, command, str(e))
            self.m_logger.error(msg)
            return None   

    def sleep(self, time_sec):
        try:
            MonkeyRunner.sleep(time_sec)
            return True
        except Exception, e:
            msg = "[%s] Failed to sleep [%s]" %(self.class_name, str(e))
            self.m_logger.error(msg)
            return False
    
    # Reboots the specified device into a specified bootloader
    # @args: the bootloader to reboot into: bootloader, recovery, or None 
    def reboot(self, into):
        try:
            self.device.reboot(into)
            return True
        except Exception, e:
            msg = "[%s] Failed to reboot device: [%s]" %(self.class_name, str(e))
            self.m_logger.error(msg)
            return False
    
    def installPkg(self, local_apk_path):
        try:
            install_status = self.device.installPackage(local_apk_path)
            if install_status!=True:
                msg = "[%s] Something went wrong with the installation: [%s]" %(self.class_name, str(install_status))
                self.m_logger.error(msg)
                return False
            return True
        except Exception, e:
            msg = "[%s] Failed to install package [%s]" %(self.class_name, str(e))
            self.m_logger.error(msg)
            return False
    
    def startActivity(self, package_name, activity_name):
        runComponent = package_name + "/" + activity_name
        try:
            self.device.startActivity(component = runComponent)
            return True
        except Exception, e:
            msg = "[%s] Failed to start activity [%s]" %(self.class_name, str(e))
            self.m_logger.error(msg)
            return False
     
    # Deletes the specified package from this device, including its data and cache.
    def removePkg(self, package_name):
        try:
            self.device.removePackage(package_name)
            return True
        except Exception, e:
            msg = "[%s] Failed to remove package [%s]" %(self.class_name, str(e))
            self.m_logger.error(msg)
            return False
    
    # Wakes the screen of this device.
    def wake(self):
        try:
            self.device.wake()
            return True
        except Exception, e:
            msg = "[%s] Failed to wake [%s]" %(self.class_name, str(e))
            self.m_logger.error(msg)
            return False
        
    def instrument(self, str_className, dict_args):
        try:
            self.device.instrument(str_className, dict_args)
            return True
        except Exception, e:
            msg = "[%s] Failed to instrument [%s]" %(self.class_name, str(e))
            self.m_logger.error(msg)
            return False
        
#------------------------------------------------------------------------------ 
# screen shot and comparison 
#------------------------------------------------------------------------------ 
    def snapShot(self, file_dir, file_name):
        try:
            result = self.device.takeSnapshot()
            file_path = file_dir + os.sep + file_name + ".png"
            result.writeToFile(file_path, "png")
            return True
        except Exception,e:
            msg = "[%s] Failed to snap shot [%s]" %(self.class_name, str(e))
            self.m_logger.error(msg)
            return False 
            
    def sameAs(self, otherImage, percent):
        try:
            result = self.device.takeSnapshot()
            return result.sameAs(otherImage, percent) # otherImage should be a MonkeyImage type
        except Exception,e:
            msg = "[%s] Failed to same as [%s]" %(self.class_name, str(e))
            self.m_logger.error(msg)
            return None
    
    #===========================================================================
    # Sends the characters contained in message to this device, 
    # as if they had been typed on the device's keyboard. 
    # This is equivalent to calling press() for each keycode in message 
    # using the key event type DOWN_AND_UP.    
    #===========================================================================
    def typeText(self, message):
        try:
            self.device.type(message)
            return True
        except Exception, e:
            msg = "[%s] Failed to type message [%s]" %(self.class_name, str(e))
            self.m_logger.error(msg)
            return False
               
#===============================================================================
# # Left: newLeft = (Root Node)->mLeft + (ParentNode)->mLeft + ... + self->mLeft
# # Right: newRight = newLeft + (self->mRight - self->mLeft)
# # Top : newTop = (Root Node)->mTop + (ParentNode)->mTop + ... + self->mTop
# # Bottom: newBottom = newTop + (self->mBottom - self->mTop)
#===============================================================================
def clickEvent_Point(monkey_runner_impl):
    ## calculate (digit 7 : 80/370)
    print "begin"
    monkey_runner_impl.touch(59, 406, "DOWN_AND_UP")
    monkey_runner_impl.touch(59, 277, "DOWN_AND_UP")
    print "end"        
    monkey_runner_impl.sleep(1)

    ## Notification (y: 0-37  / x: 8-471 )
    print "begin"
    monkey_runner_impl.touch(471, 37, "DOWN_AND_UP")
    print "end"
    MonkeyRunner.sleep(1)
    
    monkey_runner_impl.press("KEYCODE_MENU", "DOWN_AND_UP");
    monkey_runner_impl.sleep(1)
    
    monkey_runner_impl.press("KEYCODE_BACK", "DOWN_AND_UP");
    
    monkey_runner_impl.clickPowerButton()
    monkey_runner_impl.clickHomeButton()

def touchEventByViewFile(view_file_name, monkey_runner_impl):
    pass

def touchEventByViewPointList(view_point_list,monkey_runner_impl):
    for view_point in view_point_list:
        monkey_runner_impl.touch(view_point[0],view_point[1],"DOWN_AND_UP")
        MonkeyRunner.sleep(0.7)

def dragEventByViewPointList(view_point_list, monkey_runner_impl):
    print str(monkey_runner_impl.device.getProperty('display.width'))
    print str(monkey_runner_impl.device.getProperty('display.height'))
    monkey_runner_impl.drag(350, 370, 50, 370)
    

def main():
    logger = Logger.InitLog("test.log", logging.getLogger("test.thread"))
    monkey_runner_impl = MonkeyRunnerImpl(logger)
      
    clickEvent_Point(monkey_runner_impl) ## this is just for testing
    
if __name__ == "__main__":
    main()
    
    