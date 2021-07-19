from generate2 import load, generate
import os
path = os.path.dirname(os.path.realpath(__file__))
load(path + "/messages.txt")
generate()