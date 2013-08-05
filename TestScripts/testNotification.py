#! python2.7
## -*- coding: utf-8 -*-

#===============================================================================
# @author: kun
# @date: 2012-06-29
#===============================================================================

import os,sys
current_path = os.getcwd()
parent_path = os.path.abspath(os.path.join(os.getcwd(), os.path.pardir))
if current_path not in sys.path:
    sys.path.append(current_path)
if parent_path not in sys.path:
    sys.path.append(parent_path)
from ViewController.MonkeyRunnerImpl import MonkeyRunnerImpl
import time


from SystemComponent.Notification import Notification
from ViewManagement.ViewTree import build

def testNotification():
    tree_nodes_list = build()
    notification = Notification(tree_nodes_list)
    
    print "carrier info: %s" %notification.getCarrierInfo()
    clear_location = notification.getClearButtonLocation()
    print "clear button location: (%s, %s)" %(clear_location.x, clear_location.y)
    
    print  "Ongoing items: "
    elements_list = notification.getOngoingViewNodes()
    for element in elements_list:
        print element.mId
        print notification.getTextList(element)
     
    print "Notifications items: "   
    elements_list = notification.getNotificationViewNodes()    
    for element in elements_list:
        print element.mId
        print notification.getTextList(element)

def touchEventByViewPointList(view_point_list,monkey_runner_impl):
    for view_point in view_point_list:
        monkey_runner_impl.touch(view_point[0], view_point[1], "DOWN_AND_UP")
        
    monkey_runner_impl.touch(428, 74, "DOWN_AND_UP")
        
def dragNotification(monkey_runner_impl):
    ## Notification (y: 0-37  / x: 8-471 )
    print "begin drag Notification"
    monkey_runner_impl.drag(fromX= 200, fromY = 22, toX = 200, toY = 600)
    print "end drag Notification"
    
def longClickHome(monkey_runner_impl):
    print "begin long click home button"
    monkey_runner_impl.press("HOME", "DOWN")
    
    print "begin long click home button"

def main():
    monkey_runner_impl = MonkeyRunnerImpl()
    
    view_file_dir = os.getcwd() + os.sep + "view_file"
    view_file_path = view_file_dir + os.sep + "click.vf"
    view_file = open(view_file_path, "r")
    view_point_list=[]
    for eachline in view_file:
        l = eachline.strip("\n").split("|")
        t = (int(l[0],10),int(l[1],10))
        view_point_list.append(t)
      

    touchEventByViewPointList(view_point_list,monkey_runner_impl)

#    dragNotification(monkey_runner_impl)
    
    
if __name__ == "__main__":
    #main()    
    testNotification()