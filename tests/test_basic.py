import os, sys
import logging

logging.basicConfig(level = logging.DEBUG)

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from vmhack.vmtranslator import translate

pathToFile = "/Users/vk/software/BuildComputer/soft/nand2tetris/projects/07/StackArithmetic/SimpleAdd/SimpleAdd.vm"
translate(pathToFile)
