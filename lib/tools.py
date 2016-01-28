#useful functions

import os


def cls():
    """clear the screen for windows,mac,linus"""
    os.system('cls' if os.name=='nt' else 'clear')

def pri_input(txt=""):
    """print and wait for input"""
    print(txt)
    input("press enter")
