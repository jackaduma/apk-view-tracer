#! python2.7
## -*- coding: utf-8 -*-

#===============================================================================
# @author: kun
#===============================================================================

from EventController import EventController 

class Controller():
    '''
    Controller
    '''
    
    def __init__(self, logger, device_name, device_address="127.0.0.1", monkey_server_port=12345):
        self.m_logger = logger
        self.device_name = device_name
        
        self.event_controller = EventController(self.m_logger, device_address, monkey_server_port)
        
    def open(self):
        if self.event_controller.open():
            return True
        else:
            return False
    
    def close(self):
        self.event_controller.close()
        
    
    def clickByID(self, view_id):
        pass
    
    def clickByText(self, text):
        pass
    
    def clickByIndex(self, index):
        pass   
    
    def callNotification(self):
        self.event_controller.drag(100, 20, 100, 500)

#------------------------------------------------------------------------------ 
#    Physical Buttons
#------------------------------------------------------------------------------     
    def longClickHome(self):
        pass
    
    def goBack(self):
        self.monkeyrunner_device.clickBackButton()
    
    def callMenu(self):
        self.monkeyrunner_device.clickMenuButton()
    
    def down(self):
        pass
    
    def up(self):
        pass
    
    def left(self):
        pass
    
    def right(self):
        pass
    
    