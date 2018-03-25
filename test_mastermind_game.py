#!/usr/bin/env python3

### Program title here
### Last updated on ... by Ryan McKay
# Insert
# Program
# Description
# Here

from mastermind_game import Game
from mastermind_game import Turn

def printd(string, level=0, **kwargs):
    if DEBUG_LEVEL >= level:
        print(string.format(**kwargs))

def print_test_turn_details(test_number, test_component, tests_passed, tests_failed):
    printd('Testing')

def test_turn():
    printd('Begin Testing Class Turn')
    g = Game()
    g.board = [1,1,1,1]
    test_num = 0
    turns = list()
    test_results = list()
    test_results.append(dict(_areCorrect=0,_areMatchingColours=0,getFeedback=0))
    # Test 1
    turns.append(Turn([5,5,5,5]))
    if turns[test_num]._areCorrect() == 0 then test_results[test_num]['_areCorrect'] = 1
    if turns[test_num]._areMatchingColours() == 0 then test_results[test_num]['_areMatchingColours'] = 1
    if turns[test_num].getFeedback() == [] then test_results[test_num]['getFeedback'] = 1




def test_game():
    pass

def main():
    new_game = Game()


if __name__ == '__main__':
  main()
