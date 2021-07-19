import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

global basepath
BASEPATH = os.path.dirname(os.path.realpath(__file__))

import glob

import pygame
import engine

WIDTH = 512
HEIGHT = 512
DIMENSION = 8

SQUARE_SIZE = HEIGHT // DIMENSION

MAX_FPS = 24

global IMAGES
IMAGES = {}

def load_images():
    os.chdir(os.path.join(BASEPATH, "assets"))
    for file in glob.glob("*"):
        name = file.split(".")[0]
        IMAGES[name] = pygame.image.load(os.path.join(BASEPATH, os.path.join("assets", file)))

load_images()