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


import sys, fileinput, re, random
import numpy as np
import itertools as it
import operator as op

PRIOR_COUNT = 2



def printd(string, level=0, **kwargs):
    if DEBUG_LEVEL >= level:
        print(string.format(**kwargs))

class GameState(object):

    def __init__(self,colours,board_length):
        printd('\tGame Stats\n{col}\tColours\n{brd}\tBoard Length',col=colours,brd=board_length,level=1)
        self.turn = 0
        self.possible_boards = sorted([ item for item in it.permutations(range(colours),board_length)])

        self.boardP = dict()
        for item in self.possible_boards:
            self.boardP[self._dict_key(item)] = 1/len(self.possible_boards)

        printd('{N}\tPossible Boards\n{P}\tPrior Probability',N=len(self.possible_boards),P=1/len(self.possible_boards),level=1)

        self.turn_items = dict(feedback=np.array([]),actions=np.array([]),valid_boards=self.possible_boards)

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


    def processFeedback(self):
        f = input('Please input feedback in form [#correct_place,#correct_colour]: ')
        feedback = None
        if type(f) is list and len(f) == 2:
            feedback = dict(CORRECT_PLACEMENT=f[0],CORRECT_COLOUR=f[1])
        return feedback

    def _dict_key(self,array):
        return ''.join([ str(item) for item in array])





class GameMath(object):

    def __init__(self):
        pass

    def _hypogeometric_pdf(self, num_variates, size_variates, selection_variates):
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




class Player(GameState, GameMath):

    def __init__(self, colours, board_length):
        GameState.__init__(self,colours,board_length)




    def turn(self):
        # Update Probabilities
        if not (self.feedback == []).all():
            self._updateBoardP()

        # decide action
        action = [1,2,3,4]

        self._act(action)
        self._processFeedback()

    def act(self,action):
        self.actions.append(action)
        # Submit turn somehow
        printd('Turn {T}:\tSubmitted {act}',T=self.turn,act=action)

    def _updateBoardP(self):
        pass





    def _updateP(self):
        self.P = np.divide(self.counts,self.counts.sum(axis=0))
        self._checkP()
        printd('Updated Probabilities Turn {C}:\n{prob}\n',C=self.turn,prob=self.P)

    def _updateCounts(self,action,feedback):
        correct = feedback[0]
        colour = feedback[1]
        for pos in range(len(action)):
            self.counts[pos,action[pos]] += correct
            for act in action:
                if act not in [action[pos],BOARD_LENGTH]:
                    self.counts[pos,action[act]] += (colour/(BOARD_LENGTH-1))

        printd('Updated Counts Turn {C}:\n{counts}\n',C=self.turn,counts=self.counts)

    def _checkP(self):
        if not (self.P.sum(axis=0) == [1]*NUM_COLOURS).all():
            print "Probabilities don't sum to 1!!"
            print self.P



def main():
    g = GameState(NUM_COLOURS,BOARD_LENGTH)
    actions = [[0,1,2,3],[1,2,4,5]]
    #,[1,4,5]]
    feedback = [ { CORRECT_PLACEMENT:2, CORRECT_COLOUR:0 }, { CORRECT_PLACEMENT:1, CORRECT_COLOUR:3 } ]
    # , dict(CORRECT_PLACEMENT=1,CORRECT_COLOUR=2)
    g.derive_constraints(actions, feedback, g.possible_boards)


if __name__ == '__main__':
  main()
