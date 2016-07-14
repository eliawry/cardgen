from PIL import Image

import os
import random

NUM_FRAMES = 32
# random utilities. At the top bc this is for pasting into ipython bc
# i am a bum
# i'm only even writing helper functions cause i'm out of private
# repos on girhub and i don't want you to judge me
def file_for(suit, value, ext='png'):
    """because string formatting is for suckers"""
    return suit + value + '.' + ext

def dir_for(suit, value):
    # lol why this. #enterprise af
    return suit + value

def iterdeck():
    """an iterator that yields all of the card combos"""
    for suit in "cdhs":
        for value in ['A', '2', '3', '4', '5', '6',
                      '7', '8', '9', '10', 'J', 'K', 'Q']:
            yield (suit, value)


def compose_cards():
    # for this to work, you must have cards named 'c.png' with clubs on a
    # transparent background and so on.
    # Additionally, you have to have cards without suit markings but
    # with numbers
    # This will generate a full deck of cards with the suit marking
    # imposed on the numbered backgrounds.

    for suit, value in iterdeck():
        background = Image.open(value + ".png")
        overlay = Image.open(suit + ".png")

        background = background.convert("RGBA")
        overlay = overlay.convert("RGBA")

        background.paste(overlay, (0, 0), overlay)

        background.save(file_for(suit, value))

def up_down_fade(background, back_pixels, front_pixels, folder):
    """An in-place fade of the back to the front, saving in the folder"""
    for iteration in xrange(background.size[1] / 64 + 1):
        for i in xrange(background.size[0]):
            for j in xrange(background.size[1]):
                if j <= iteration * 64:
                    back_pixels[i, j] = front_pixels[i, j]
        background.save(folder + '/' + str(iteration).zfill(4) + '.png')


def left_right_fade(background, back_pixels, front_pixels, folder):
    """An in-place fade of the left to the right, saving in the folder"""
    for iteration in xrange(background.size[1] / 64 + 1):
        for i in xrange(background.size[1]):
            for j in xrange(background.size[0]):
                if j <= iteration * 64:
                    back_pixels[j, i] = front_pixels[j, i]
        background.save(folder + '/' + str(iteration).zfill(4) + '.png')


def random_fade(background, back_pixels, front_pixels, folder):
    """A random fade of the card, a few pixels at a time"""
    x = background.size[0]
    y = background.size[1]
    l = range(x * y)
    random.shuffle(l)
    frame_to_render = {i : l[i] % NUM_FRAMES for i in xrange(x*y)}

    for iteration in xrange(NUM_FRAMES):
        for i in xrange(background.size[0]):
            for j in xrange(background.size[1]):
                if frame_to_render[i * background.size[1] +  j ] <= iteration:
                    back_pixels[i, j] = front_pixels[i, j]
        background.save(folder + '/' + str(iteration).zfill(4) + '.png')

def make_gifs():
    """Generate a gif for each card"""
    # now we want to simulate flipping the card in some way
    for suit, value in iterdeck():
        background = Image.open("back.png")
        overlay = Image.open(file_for(suit, value))
        try:
            os.mkdir(dir_for(suit, value))
        except:
            print "Warning: overwriting the last thing in /%s" % dir_for(suit, value)
        back_pixels = background.load()
        front_pixels = overlay.load()
        r = random.choice(range(3))
        if r == 1:
            up_down_fade(background, back_pixels, front_pixels, dir_for(suit, value))
        elif r == 2:
            left_right_fade(background, back_pixels, front_pixels, dir_for(suit, value))
        else:
            random_fade(background, back_pixels, front_pixels, dir_for(suit, value))
        os.system("convert -delay 10 -loop 1 %s/*.png %s.gif" % (dir_for(suit, value), dir_for(suit, value)))
