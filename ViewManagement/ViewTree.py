#! python2.7
## -*- coding: utf-8 -*-

## kun for Apk View Tracking
## ViewTree.py

import copy
from TreeType import CRect,CTreeNode,CPoint
from ParseElement import ParseElement
from ViewState import ViewState

class ViewTree():
    '''
    View Tree
    '''
    
    def __init__(self, logger):
        self.m_logger = logger
    
    def getStructure(self, dump_data):
        list_data = dump_data.split("\n")
    
        # pop the last element "DONE"
        list_data.remove("DONE")
    
        elements_list=[]
        blanks_list=[]
        for element in list_data:        
            index = 0
            count = 0
            while " " == element[index]:
                index = index + 1
                count = count + 1   
            #===================================================================
            # # another method which can get blanks count in head of element
            # tag_list = element.split(" ")
            # head_tag = tag_list[0]
            # while (0 == len(head_tag)):
            #     count += 1
            #===================================================================
            
            blanks_list.append(count)
            elements_list.append(element)
        
        return elements_list,blanks_list

    def buildTree(self, elements_list, blanks_list):
        tree_nodes_list=[]
        
        root_node= CTreeNode()
        root_node.mParentNode=None    
    
        total_count = len(blanks_list)
    
        depth = 0
        pre_depth = depth-1
        for x in range(total_count):
            index = x        
            blanks_count = blanks_list[index]
            depth = blanks_count
            
            node = CTreeNode()
            ## set node depth in this tree
            node.mTreeDepth = blanks_count 
            
            if 0 == blanks_count:
                root_node.mElement = elements_list[index]
                root_node.mDepth = 0
                tree_nodes_list.append(root_node)
                
            else:
                pre_index = x-1
                pre_depth = blanks_list[pre_index]
                pre_depth = tree_nodes_list[pre_index].mDepth
                
                node.mElement = elements_list[index]
                node.mDepth = blanks_count
    
                delta_depth = (depth - pre_depth)
                if (1 == delta_depth):
                    ## 本节点是上一个节点的子节点
                    ## current node is a child node of last node
                    node.mParentNode = tree_nodes_list[pre_index]
                    tree_nodes_list.append(node)
                elif (0 == delta_depth):
                    ## 等深度， 取上一个的父节点作为自己的父节点
                    ## these two nodes have same depth, so that they have same parent node
                    node.mParentNode = tree_nodes_list[pre_index].mParentNode
                    tree_nodes_list.append(node)
                elif (0 > delta_depth):
                    ## 向上递归寻找和自己等深度的节点
                    ## Recurse down to up, seek the node which has same depth
                    new_delta_depth = delta_depth
                    new_pre_depth = pre_depth
                    new_pre_index = pre_index
                    while True:
                        if 0==new_delta_depth:
                            node.mParentNode = tree_nodes_list[new_pre_index].mParentNode
                            tree_nodes_list.append(node)
                            break
                        else:
                            new_pre_index -= 1
                            new_pre_depth = tree_nodes_list[new_pre_index].mDepth
                            new_delta_depth = depth - new_pre_depth
                else:
                    raise Exception, "Raise an Exception when Build Elements Tree!"
                    break           
    
        return tree_nodes_list
    
    
    ## Left: newLeft = (Root Node)->mLeft + (ParentNode)->mLeft + ... + self->mLeft
    ## Right: newRight = newLeft + (self->mRight - self->mLeft)
    ## Top : newTop = (Root Node)->mTop + (ParentNode)->mTop + ... + self->mTop
    ## Bottom: newBottom = newTop + (self->mBottom - self->mTop)
    def getAbsoluteRect(self, node):
        absoluteRect = CRect()
        
        temp_rect = CRect()    
        current_node = CTreeNode()
        current_node = copy.deepcopy(node)
        temp_rect=current_node.mRect

        while True:        
            parent_node = CTreeNode()        
            
            if None == current_node.mParentNode:
                break
            else:
                parent_node = current_node.mParentNode
                temp_rect.mLeft += (parent_node.mRect.mLeft - parent_node.mScrollX)
                temp_rect.mTop += (parent_node.mRect.mTop - parent_node.mScrollY)
                current_node = parent_node
    
        temp_rect.mRight = temp_rect.mLeft + (node.mRect.mRight - node.mRect.mLeft)
        temp_rect.mBottom = temp_rect.mTop + (node.mRect.mBottom - node.mRect.mTop)    
        absoluteRect=temp_rect
        
        return absoluteRect
    
    def getViewCenterPoint(self, node):
        width = node.mAbsoluteRect.mRight - node.mAbsoluteRect.mLeft
        height = node.mAbsoluteRect.mBottom - node.mAbsoluteRect.mTop
        location = CPoint()
        location.x = node.mAbsoluteRect.mLeft + width/2
        location.y = node.mAbsoluteRect.mTop + height/2    
        return location
    
    def getChildNodesList(self, tree_nodes_list, tree_node):
        child_nodes_list = []
        start_flag = False
        end_flag = False
        for node in tree_nodes_list:
            if end_flag:
                break
            
            if node.mHashCode == tree_node.mHashCode:
                start_flag = True
            
            if (node.mDepth == (tree_node.mDepth+1)) and start_flag:
                child_nodes_list.append(node)
                
            if (node.mDepth == tree_node.mDepth) and start_flag and (node.mHashCode!=tree_node.mHashCode):
                end_flag = True

        return child_nodes_list
    
    def setNodeValue(self, node):
        element = node.mElement
        if None == element:
            msg = "Failed to set Node Value because Error in Node!"
            self.m_logger.error(msg)
            return False
        
        element_parser = ParseElement(node.mElement)
        element_parser.parseElmentData()
        node.mClassName = element_parser.getClassName()
        node.mHashCode = element_parser.getHashCode()
        node.mId = element_parser.getID()
        node.mText = element_parser.getText()
        
        active_state = ViewState(node)
        node.mVisible = element_parser.getVisible()
        node.mClickable = element_parser.getClickable()
        node.mActive = active_state.getActiveState()        
        
        node.mRect = element_parser.getRectArea()
        node.mScrollX = element_parser.scrollX
        node.mScrollY = element_parser.scrollY
        node.mAbsoluteRect = self.getAbsoluteRect(node)
        node.mLocation = self.getViewCenterPoint(node)
        
        

    
    
    def build(self, data):
        elements_list, blanks_list = self.getStructure(data)    
        
        tree_nodes_list = self.buildTree(elements_list, blanks_list)
    
        for node in tree_nodes_list:
            ## set node value from root node to child node
            self.setNodeValue(node)
            node.mChildNodes = self.getChildNodesList(tree_nodes_list, node)
            self.m_logger.info("*************************************************************************")  
            self.m_logger.info("mClassName: %s" %node.mClassName)
            self.m_logger.info("mTreeDepth: %s" %node.mTreeDepth)
            self.m_logger.info("mId: %s " %node.mId)
            self.m_logger.info("mText: %s" %node.mText)
            self.m_logger.info("mActive: %s" %node.mActive)
            self.m_logger.info("mRect.(mTop, mBottom, mLeft, mRight): %s %s %s %s" %(node.mRect.mTop, node.mRect.mBottom, node.mRect.mLeft, node.mRect.mRight))
            self.m_logger.info("mAbsoluteRect: %s %s %s %s" %(node.mAbsoluteRect.mTop, node.mAbsoluteRect.mBottom, node.mAbsoluteRect.mLeft, node.mAbsoluteRect.mRight))
            self.m_logger.info("*************************************************************************")

        return tree_nodes_list

if __name__=="__main__":
    vt = ViewTree()

