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


import sys, fileinput, re, random, math
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

    def entropy(self,values):
        total = sum(values)
        return reduce(op.add, map(lambda x: -(x/total)*math.log(x/total), values))

    def _ncr(self,n,r):
        r = min(r, n-r)
        numerator = reduce(op.mul, xrange(n, n-r, -1), 1)
        denominator = reduce(op.mul, xrange(1, r+1), 1)
        return numerator//denominator



class GameState(GameMath):

    def __init__(self,colours,board_length):
        self.turn = 0
        self.board_length = board_length
        self.colours = colours
        self.all_actions = sorted([ item for item in it.permutations(range(colours),board_length)])
        self.all_feedbacks = self._generate_valid_feedbacks()
            # (4,0),(3,0),(2,0),(1,0),(0,0),(0,1),(0,2),(0,3),(0,4),(1,1),(2,1),(1,2),(1,3),(2,2)    ]

        printd('\tGame Stats\n{col}\tColours\n{brd}\tBoard Length\n{V}\tValid Actions',\
            col=colours,brd=board_length,V=len(self.all_actions),level=2)

        self.turn_items = [ dict(feedbacks=list(),actions=list(),valid_actions=self.all_actions) ]

    def derive_constraints(self, actions, feedback, valid_actions):
        valid_actions_sets = list()
        for turn, act in enumerate(actions):
            printd('Processing Feedback for Turn {T}',T=turn,level=4)
            printd('{A} Act\t({C},{CC}) (Correct,Colours Correct)\t\t {V} Valid Actions\n',\
                C=feedback[turn][CORRECT_PLACEMENT], CC=feedback[turn][CORRECT_COLOUR], \
                V=len(valid_actions), A=act,level=4)
            valid_actions_sets.append(\
                set(self._constrained_permutations(\
                    number_correct=feedback[turn][CORRECT_PLACEMENT],\
                    number_colours_correct=feedback[turn][CORRECT_COLOUR],\
                    action=act,\
                    valid_actions=valid_actions)))
            printd("Valid Actions Turn {T}\t\t{V}\n",T=turn,V=xstr(valid_actions_sets[turn]),level=4)

        printd('Intersection Valid Actions {inter}\n',inter=set.intersection(*valid_actions_sets), level=4)
        return set.intersection(*valid_actions_sets)

    def _constrained_permutations(self,number_correct,number_colours_correct,action,valid_actions):
        valid = list()
        for p, pitem in enumerate(valid_actions):
            nc = 0
            ncnc = 0
            for (x,y) in zip(pitem,action):
                if x == y:
                    nc += 1
                if not x == y and x in action:
                    ncnc += 1
            printd('Item:\t{item}\tFeedback:{fb}',item=pitem, fb=(nc,ncnc), level=5)
            if nc == number_correct and ncnc == number_colours_correct:
                valid.append(pitem)
        return valid

    def _generate_valid_feedbacks(self):
        units = [ item for item in it.permutations(range(self.board_length+1),2)\
            if sum(item) <= self.board_length and not(item == (3,1))
        ]
        doubles = [ (i,i) for i in range(self.board_length+1) if sum((i,i)) <= self.board_length]
        return units + doubles

    def get_turn(self):
        return self.turn

    def get_actions(self, turn=None):
        if turn is None:
            turn = self.get_turn()
        return self.turn_items[turn]['actions']

    def get_feedbacks(self, turn=None):
        if turn is None:
            turn = self.get_turn()
        return self.turn_items[turn]['feedbacks']

    def get_valid_actions(self, turn=None):
        if turn is None:
            turn = self.get_turn()
        return self.turn_items[turn]['valid_actions']

    def record_turn(self, actions, feedbacks, valid_actions):
        self.turn_items.append(dict())
        self.turn_items[self.get_turn()]['feedbacks'] = feedbacks
        self.turn_items[self.get_turn()]['actions'] = actions
        self.turn_items[self.get_turn()]['valid_actions'] = valid_actions
        printd('Submitting Turn {T}\nActions\t\t{A}\nFeedbacks\t{F}\n{N} Valid Actions Remain',\
            T=self.get_turn(),\
            A=actions,\
            F=feedbacks,\
            N=len(valid_actions))

        self.turn += 1

    def _dict_key(self,array):
        return ''.join([ str(item) for item in array])





class Player(GameState):

    def __init__(self, colours, board_length):
        GameState.__init__(self,colours,board_length)
        self.action_tree = GameTree()

    def play_turn(self):
        action = self._decide_act()
        actions = self._process_action(action)
        feedbacks = self._process_feedback()
        valid_actions = self.derive_constraints(actions, feedbacks, self.get_valid_actions(self.get_turn()-1))
        self.record_turn(actions, feedbacks, valid_actions)
        self.check_win(valid_actions)

    def _process_action(self,action):
        actions = self.get_actions(self.get_turn()-1)
        printd('\nPast Actions: {A}',A=xstr(actions), level=2)
        actions.append(action)
        printd('Current Action: {A}',A=xstr(action), level=2)
        printd('New Actions: {A}',A=xstr(actions), level=2)
        printd('Turn {T}:\tSubmitted {act}',T=self.get_turn(),act=action, level=1)
        return actions

    def _process_feedback(self):
        f = input('Please input feedback in form (#correct_place,#correct_colour): ')
        feedbacks = self.get_feedbacks(self.get_turn()-1)
        feedback = None
        if type(f) is tuple and len(f) == 2:
            feedback = (f[0],f[1])
        feedbacks.append(feedback)
        return feedbacks

    def _build_game_tree(self, tree):
        # initialise root node
        root_id = tree.add_node(parent_id=None,feedbacks=[],actions=[])
        #build subtree for each feedback option
        new_tree = self._build_game_subtree(tree, root_id)

    def _build_game_subtree(self, tree, root_node_id, feedbacks):

        for feedback in self.all_feedbacks:
            constrained_actions = self.derive_constraints()
            tree.add_node(parent_id=root_node_id,feedbacks=[feedback],actions=[])
            new_tree = self._build_game_subtree()

    def check_win(self, valid):
        if len(valid) == 1:
            printd('')

    def _decide_act(self):
        turn = self.get_turn()
        action = None
        scores = dict()
        count_valid = dict()
        if turn == 0:
            action = list(self.all_actions[random.randint(0,len(self.all_actions)-1)])
        else:
            last_feedback = self.get_feedbacks(turn-1)
            last_actions = self.get_actions(turn-1)
            last_valid_actions = self.get_valid_actions(turn-1)
            if len(last_valid_actions) > 1:
                for act in self.all_actions:
                    scores[self._dict_key(act)] = dict(counts=[])
                    for feedback in self.all_feedbacks:
                        new_actions = last_actions + [act]
                        new_feedbacks = last_feedback + [feedback]
                        constrained_actions = self.derive_constraints(new_actions, new_feedbacks, last_valid_actions)
                        if len(constrained_actions) > 0 :
                            scores[self._dict_key(act)][self._dict_key(feedback)] = len(constrained_actions)
                            scores[self._dict_key(act)]['counts'].append(len(constrained_actions))
                    scores[self._dict_key(act)]['entropy'] = self.entropy(scores[self._dict_key(act)]['counts'])
                max_key = max(scores.iterkeys(), key=(lambda key: scores[key]['entropy']))
                intial_guess = self._dict_key(last_actions[0])
                print max_key, scores[max_key]['entropy'], scores[max_key]
                action = [ int(i) for i in list(max_key)]
            else:
                action = list(last_valid_actions)
        return action

def main():
    p = Player(NUM_COLOURS,BOARD_LENGTH)

    while True:
        p.play_turn()

   
if __name__ == '__main__':
  main()


