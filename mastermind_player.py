#!/usr/bin/env python3

### Program title here
### Last updated on ... by Ryan McKay
# Insert
# Program
# Description
# Here

# Common imports

from __future__ import division
from game_config import *
from board_tree import *


import sys, fileinput, re, random
import numpy as np
import itertools as it
import operator as op

class GameMath(object):

    def __init__(self):
        pass

    def Pboard(self, board):
        return 1/len(board)

    def _hypergeometric_pdf(self, size_variates, selection_variates):
        l = lambda x,y: x*y
        n = reduce(l, [ self._ncr(n,r) for n,r in zip(size_variates,selection_variates)])
        d = self._ncr(size_variates.sum(),selection_variates.sum())
        printd('Hypogeometric pdf\nn:{N}\td:{D}\t',N=n,D=d)
        return  n / d

    def _ncr(self,n,r):
        r = min(r, n-r)
        numerator = reduce(op.mul, xrange(n, n-r, -1), 1)
        denominator = reduce(op.mul, xrange(1, r+1), 1)
        return numerator//denominator



class GameState(GameMath):

    def __init__(self,colours,board_length):
        printd('\tGame Stats\n{col}\tColours\n{brd}\tBoard Length',col=colours,brd=board_length,level=1)
        self.turn = 0
        self.all_actions = sorted([ item for item in it.permutations(range(colours),board_length)])

        self.turn_items = [ dict(feedbacks=list(),actions=list(),valid_boards=self.all_actions) ]

    def derive_constraints(self, actions, feedback, valid_boards):
        valid_actions = list()
        valid_actions_sets = list()
        print feedback, actions
        for a, act in enumerate(actions):
            valid_actions.append(\
                self._constrained_permutations(\
                    number_correct=feedback[a][CORRECT_PLACEMENT],\
                    number_colours_correct=feedback[a][CORRECT_COLOUR],\
                    board=act,\
                    valid_boards=valid_boards))
            valid_actions_sets.append(set(valid_actions[a]))

        print np.array(valid_actions)
        printd('Intersection Valid Actions {inter}\n',inter=set.intersection(*valid_actions_sets), level=1)
        return valid_actions

    def _constrained_permutations(self,number_correct,number_colours_correct,board,valid_boards):
        valid = list()
        for p, pitem in enumerate(valid_boards):
            nc = 0
            ncnc = 0
            for (x,y) in zip(pitem,board):
                if x == y:
                    nc += 1
                if not x == y and x in board:
                    ncnc += 1
            printd('Item:\t{item}\tFeedback:{fb}',item=pitem, fb=(nc,ncnc), level=4)
            if nc == number_correct and ncnc == number_colours_correct:
                valid.append(pitem)
        return valid

    def _process_feedback(self):
        f = input('Please input feedback in form [#correct_place,#correct_colour]: ')
        feedback = None
        if type(f) is list and len(f) == 2:
            feedback = [f[0],f[1]]
        return feedback

    def get_turn(self):
        return self.turn

    def record_turn(self, action, feedback):
        current_feedback = list()
        current_actions = list()
        if self.turn > 0:
            current_feedbacks = self.turn_items[self.turn-1]['feedback']
            current_actions = self.turn_items[self.turn-1]['action']

        self.turn_items[self.turn]['feedback'] = current_feedbacks.append(feedback)
        self.turn_items[self.turn]['action'] = current_actions.append(action)
        self.turn += 1

    def _dict_key(self,array):
        return ''.join([ str(item) for item in array])



class Player(GameState):

    def __init__(self, colours, board_length):
        GameState.__init__(self,colours,board_length)
        self.action_tree = GameTree()

    def turn(self):
        action = self._decide_act()
        self._act(action)
        feedback = self._process_feedback()
        valid_actions = self.derive_constraints()
        self.record_turn(action, feedback)

    def _act(self,action):
        print 'Current Action: ' + xstr(action)
        new_actions = self.actions.append(action)
        print 'New Actions: ' + xstr(new_actions)
        printd('Turn {T}:\tSubmitted {act}',T=self.get_turn(),act=action)

    def _decide_act(self):
        if self.get_turn == 0:
            action = self.all_actions[random.randint(0,len(self.all_actions)-1)]





def main():
    g = GameState(NUM_COLOURS,BOARD_LENGTH)
    actions = [[0,1,2,3],[0,1,4,5]]
    feedback = [ { CORRECT_PLACEMENT:0, CORRECT_COLOUR:2 }, { CORRECT_PLACEMENT:2, CORRECT_COLOUR:2 } ]
    g.derive_constraints(actions, feedback, g.all_actions)


if __name__ == '__main__':
  main()

#
