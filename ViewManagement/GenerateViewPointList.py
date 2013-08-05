#! python2.7
## -*- coding: utf-8 -*-

## kun for apk view tracing
## GenerateViewPointList.py

from ViewTree import ViewTree

class GenerateViewPointList():
    ## class variables
    ## Action List and Map which ensure action sequence
    click_action_list=[]
    touch_action_list=[]
    drag_action_list=[]
    Action_Sequence_Map = {"click": click_action_list,
                           "touch": touch_action_list,
                           "drag": drag_action_list}
    def __init__(self):
        pass 

    def getViewCenterPoint(self, node):
        width = node.mAbsoluteRect.mRight - node.mAbsoluteRect.mLeft
        height = node.mAbsoluteRect.mBottom - node.mAbsoluteRect.mTop
        pointX = node.mAbsoluteRect.mLeft + width/2
        pointY = node.mAbsoluteRect.mTop + height/2    
        return pointX,pointY    
    
    def generateViewPointList(self, tree_nodes_list):
        view_point_list=[]
        
        for node in tree_nodes_list:
            if node.mActive:
                view_point_list.append(self.getViewCenterPoint(node))

        return view_point_list

    ## return list in memory
    def generateActionList(self, view_point_list):
        action_sequence_list=[]
    
        return action_sequence_list
    

def main():
    vt = ViewTree()
    tree_nodes_list = vt.build()
    view_generator = GenerateViewPointList()
    view_point_list = view_generator.generateViewPointList(tree_nodes_list)
    view_generator.generateActionList(view_point_list)


if __name__=="__main__":
    main()
