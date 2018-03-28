#!/usr/bin/env python3

### Program title here
### Last updated on ... by Ryan McKay
# Insert
# Program
# Description
# Here

# Common imports
from __future__ import division

import game_config.py

import sys, fileinput, re, random
import numpy as np

def printd(string, level=0, **kwargs):
    if DEBUG_LEVEL >= level:
        print(string.format(**kwargs))

class Game(object):

    def __init__(self):
        self.turn = 0
        self.board_length = BOARD_LENGTH
        self.turns = list()
        self.board = list()
        self._beginGame()

    def submitTurn(self,submission):
        if self._isSubmissionValid(submission):
            self.turns.append(Turn(submission))
            if _isCorrectGuess(self.turns[-1].getNumCorrect()):
                printd('Your Guess is correct!\nYou won in {n} turns!!',0,n=self.turns[-1].getNumCorrect())
            else:
                feedback = self.turns[-1]._getFeedback()
        else:


    def _isCorrectGuess(self,num_correct):
        return num_correct == BOARD_LENGTH

    def _beginGame(self):
        self.board = [ random.randrange(0,NUM_COLOURS) for i in range(BOARD_LENGTH) ]
        self.turn = 1

    def _isSubmissionValid(self, player_guess):
        is_valid = False
        if isinstance(player_guess, SUBMIT_TURN_TYPE):
            printd('Submitted player guess must be of type {correct_type}, not {submitted_type}', 0 correct_type=SUBMIT_TURN_TYPE, submitted_type=type(player_guess))
        elif len(player_guess) != BOARD_LENGTH:
            printd('Submitted player guess must be of length {correct_type}, not {submitted_type}', 0 correct_type=BOARD_LENGTH, submitted_type=len(player_guess))
        else:
            is_valid = True

        return is_valid

class Turn(Game):

    def __init__(self,submission):
        self.guess = submission
        self.are_correct = self._areCorrect()
        self.are_matching_colour = self._areMatchingColours()

    def _areCorrect(self):
        return [ self.guess[i] == self.board[i] for i in range(BOARD_LENGTH) ]

    def _areMatchingColours(self):
        return [ min(self.board.count(colour),self.guess.count(colour)) for colour in range(NUM_COLOURS) ]

    def getNumCorrect(self):
        return sum(self.are_correct())

    def getNumMatchingColour(self):
        return sum(self.are_matching_colour())

    def getFeedback(self):
        feedback = list()
        feedback.append([ CORRECT_PLACEMENT for i in range(self.getNumCorrect()) ])
        return feedback.append([ CORRECT_COLOUR for i in range(self.getNumMatchingColour() - self.getNumCorrect()) ])
