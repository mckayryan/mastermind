
from __future__ import division

import sys, fileinput, re, random
import numpy as np
import itertools as it
import operator as op

from game_config import *

CURRENT = -1

class TreeNode(object):

    def __init__(self,parent_id,feedbacks,actions):
        self.id = self._generate_id(parent_id,feedbacks[CURRENT])
        self.parent = parent_id
        self.feedbacks = feedbacks
        self.actions = actions
        self.valid_actions = None
        self.child_nodes = None

    def _generate_id(self,parent_id,feedback):
        return xstr(parent_id) + '|' + self._dict_key(feedback)

    def _dict_key(self,array):
        return ''.join([ str(item) for item in array])

    def write_child_node_ids(self,child_feedbacks):
        self.child_nodes = [ self._generate_id(self.id,feedback) for feedback in child_feedbacks ]
        return self.child_nodes

    def assign_valid_actions(self,valid_actions):
        self.valid_actions = valid_actions

    def get_id(self):
        return self.id

    def get_feedbacks(self):
        return self.feedbacks

    def get_actions(self):
        return self.actions

    def get_children(self):
        return self.child_nodes

    def get_parent(self):
        return self.parent

    def get_valid_actions(self):
        return xstr(self.valid_actions)

    def __str__(self):
        to_print = ["*** Node ",xstr(self.id),' ***\n',
                    'Parent\t\t',xstr(self.parent),'\n',
                    'Valid Actions\t',xstr(self.valid_actions),'\n',
                    'Child Nodes\t',xstr(self.child_nodes),'\n',
                    'Actions\n',xstr(self.actions),'\n',
                    'Feedbacks\n',xstr(self.feedbacks),'\n']
        return ''.join(to_print)


class GameTree(object):

    def __init__(self):
        self.nodes = dict()
        root = None

    def add_node(self,parent_id,feedbacks,actions):
        new_node = TreeNode(parent_id,feedbacks,actions)
        self.nodes[new_node.get_id()] = new_node
        if parent_id == None:
            root = new_node.get_id()
        return new_node.get_id()

    def add_node_children(self,node_id,child_feedbacks,child_actions):
        child_ids = self.nodes[node_id].write_child_node_ids(child_feedbacks)
        for i, child in enumerate(child_feedbacks):
            feedbacks = self.nodes[node_id].get_feedbacks() + [child]
            actions = child_actions[i]
            # get valid actions for child
            self.add_node(node_id,feedbacks,actions)
        return child_ids

    def print_node_contents(self,node_id):
        print self.nodes[node_id]

    def get_tree(self):
        return self.nodes

    def get_node_children(self, node_id):
        return self.nodes[node_id].get_children()

    def get_sub_tree_ids(self,sub_tree_root_id):
        if sub_tree_root_id in self.nodes.keys():
            children = self.get_node_children(sub_tree_root_id)
            ids = [sub_tree_root_id]
            if children is not None:
                for child in children:
                    ids += self.get_sub_tree_ids(child)
            return ids
        else:
            printd('Node {n} is not present in tree!',n=sub_tree_root_id)

    def remove_node(self,node_id):
        parent_id = self.nodes[node_id].get_parent()
        if parent_id is not None:
            self.nodes[parent_id].child_nodes.remove(node_id)
            self.root = None
        del self.nodes[node_id]

    def prune_sub_tree(self,sub_tree_root_id):
        node_ids = self.get_sub_tree_ids(sub_tree_root_id)
        # make sure leaves are at the bottom
        node_ids.sort(key=lambda x: -len(x))
        for node_id in node_ids:
            self.remove_node(node_id)

    def __str__(self):
        print self.nodes


def main():
    pass

if __name__ == '__main__':
  main()
