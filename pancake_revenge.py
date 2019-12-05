#!/usr/bin/env python
import itertools
from six.moves import input as raw_input
import os
import sys
import traceback


class PancakeStack(object):
    """ The object which will represent an actual ++++--+-+-+---+++ pancake stack 
        all of the validity checking will have been performed by the time this object
        is created. """
    def __init__(self, stack_str):
        self._stack = stack_str
        self._flips = 0

    @staticmethod
    def is_valid_stack(stack_str):
        """ check if the stack_str string contains only '+' and/or '-' """
        return all(c == '+' or c == '-' for c in stack_str)

    def get_happy_pancake_stack_count(self):
        """ After an hour of manipulating +-- strings it finally sunk in that I was basically dealing with
            a set of 1 and 0 and I didn't really need to manipulate the string to all +++ if I could 
            figure out the flip count by evaluating the string """
        # this simply takes all the runs out of the string (i.e. ----++++--- transforms to -+-)
        consolidated_stack = ''.join(c for c, _ in itertools.groupby(self._stack))
        # the following three lines are what tripped me up for another 1/2 hour but running it on
        # the google code jam sample output files I saw the trend where I was off by one.
        self._flips = len(consolidated_stack) - 1
        if consolidated_stack[-1] == "-":
            self._flips += 1
        return self._flips


def _is_integer(s):
    """ safely checking the string for whether its an integer -- skip the try/except method """
    s = str(s)
    if s[0] in ('-', '+'):
        return s[1:].isdigit()
    return s.isdigit()

def _is_help(s):
    """ checks whether there is a first arg and whether its asking for help """
    return len(s) == 0 or s.startswith('-h') or s.startswith('--h') or s.startswith('-?') or s.startswith('--?')

def _parse_args():
    """ This will parse the incoming arguments for the count and the various number of pancake stacks """
    arg = raw_input()
    if _is_help(arg):
        return _print_usage()
    if not _is_integer(arg):
        print('ERROR: first parameter should be the count of pancake stacks')
        return _print_usage()

    count = int(arg)
    if count < 1 or count > 100:
        print('ERROR: the pancake stack count must be an integer from 1-100')
        return _print_usage()

    pancake_stacks = []
    for i in range(count):
        arg = raw_input()
        if not PancakeStack.is_valid_stack(arg):
            print('ERROR: the pancake stack "%s" is invalid and should only contain \'+\' and \'-\' characters' % arg)
            return _print_usage()
        pancake_stacks.append(PancakeStack(arg))

    # We have already checked the size above and have error-ed out if an invalid pancake stack is encountered
    assert len(pancake_stacks) == count
    return pancake_stacks

def _print_usage():
    print('Pancake Revenge v0.1')
    print('%s <pancake stack count> <pancake stack> [<pancake stack> ...]' % sys.argv[0])
    print(' The app takes a number from 1-100 which indicates how many stacks of pancakes')
    print('  will follow. The stacks will be a string of \'+\' and/or \'-\' with a minimum')
    print('  length of 1 and a maximum length of 100. The stacks can delimited either by a')
    print('  space or by a newline character. The output will be the number of flips/rotations')
    print('  it took for each stack to transition to all \'+\'.')

    print('\nExample:')
    print('%s < input.txt' % sys.argv[0])
    print('Case #1: 1')
    print('Case #2: 1')
    print('Case #3: 2')
    return None

def make_pancake_stack_happy(pancake_stack):
    """ this is where the magic happens and the pancake stack goes from -+-+-+- to +++++++ and it returns the number
        of flips it went through to make that magic happen. """
    return pancake_stack.get_happy_pancake_stack_count()

def make_pancake_stacks_happy(pancake_stacks):
    """ this is simply the outer function which iterates over the pancake stacks and displays the output after
        making the magic happen """
    for i, pancake_stack in enumerate(pancake_stacks, 1):
        flips = make_pancake_stack_happy(pancake_stack)
        print('Case #%d: %d' % (i, flips))

def main():
    pancake_stacks = _parse_args()
    if not pancake_stacks:
        return 1
    try:
        make_pancake_stacks_happy(pancake_stacks)
        return 0
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback, file=sys.stderr)
        return 1

if __name__ == '__main__':
    sys.exit(main())
