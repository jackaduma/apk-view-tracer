#! python2.7
## -*- coding: utf-8 -*-

## kun for Apk View Tracing
## HierarchyViewerImpl.py

from MonkeyRunnerImpl import MonkeyRunnerImpl      
        
class HierarchyViewer():
    def __init__(self, logger, monkey_runner_impl):
        self.class_name = "HierarchyViewer"
        self.m_logger = logger
        
        try:
            self.hierarchy_viewer = monkey_runner_impl.device.getHierarchyViewer()
            return True
        except Exception, e:
            msg = "[%s] Failed to init [%s]" %(self.class_name, str(e))
            self.m_logger.error(msg)
            return False
    
#------------------------------------------------------------------------------ 
# special functions:
#------------------------------------------------------------------------------ 
    def getFocusedWindowClassName(self):
        try:
            return self.hierarchy_viewer.getFocusedWindowName()
        except Exception, e:
            msg = "[%s] Failed to get focused window's class name: [%s]" %(self.class_name, str(e))
            self.m_logger.error(msg)
            return None
    
    def getTextById(self, str_id):
        try:
            view_node = self.hierarchy_viewer.findViewById(str_id)
            return self.hierarchy_viewer.getText(view_node)
        except Exception, e:
            msg = "[%s] Failed to get Text by Id: [%s]" %(self.class_name, str(e))
            self.m_logger.error(msg)
            return None
    
    def getVisibleById(self, str_id):
        try:
            view_node = self.hierarchy_viewer.findViewById(str_id)
            return self.hierarchy_viewer.visible(view_node)
        except Exception, e:
            msg = "[%s] Failed to get Visible by Id: [%s]" %(self.class_name, str(e))
            self.m_logger.error(msg)
            return None
    
    def getAbsolutePositionOfViewById(self, str_id):
        try:
            view_node = self.hierarchy_viewer.findViewById(str_id)
            return self.hierarchy_viewer.getAbsolutePositionOfView(view_node)
        except Exception, e:
            msg = "[%s] Failed to get Absolute position of view by Id: [%s]" %(self.class_name, str(e))
            self.m_logger.error(msg)
            return None
    
    def getAbsoluteCenterOfViewById(self, str_id):
        try:
            view_node = self.hierarchy_viewer.findViewById(str_id)
            return self.hierarchy_viewer.getAbsoluteCenterOfView(view_node)
        except Exception, e:
            msg = "[%s] Failed to get Absolute center of view by Id: [%s]" %(self.class_name, str(e))
            self.m_logger.error(msg)
            return None    
        
if __name__ == "__main__":
    monkey_runner_impl = MonkeyRunnerImpl()
    hierarchy_viewer = HierarchyViewer(monkey_runner_impl)
    print hierarchy_viewer.getFocusedWindowClassName()