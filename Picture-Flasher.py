# -*- coding: utf-8 -*-
# Picture-Flasher (a plugin for Anki)
# Authors:
#   Emanuel Rylke, ema-fox@web.de
#   D_Malik, malik6174@gmail.com
# Version 2
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

"""
A simple plugin that flashes pictures on-screen to reinforce reviews.

Before using:
- Get pictures from someplace. I downloaded pictures off reddit using the script at https://github.com/dpbrown/RedditImageGrab
- Change all lines (in the plugin source) marked with "CHANGEME" according to your preferences.

For more details, see the post at For more details, see the post at http://lesswrong.com/r/discussion/lw/frc/two_anki_plugins_to_reinforce_reviewing/
"""

from anki.hooks import addHook
from aqt import mw
from random import random, choice
from aqt.qt import QSplashScreen, QPixmap, QTimer
from os import listdir

#------ begin configuration ------#
pictureDirectory = "/home/name/Pictures/" #CHANGEME to the directory where you're storing your pictures. NB: This MUST end with a trailing slash.

flashTime = 700 #CHANGEME to change how long pictures stay on the screen. The number is time in milliseconds.

#flashPosition = [20, 1050] #CHANGEME if you want the picture to be shown at a specific location. The numbers are x- and y-coordinates.

    #CHANGEME: The next lines are a python dictionary associating deck names with probabilities of pictures being shown.
    #Eg, when using the deck "brainscience", you will get a picture after 30% of cards. When using a deck without a listed name, "other" is used.
    #Change this according to your decks. Decks with shorter, easier cards need lower probabilities.
deckPicsProbabilities = {
    "rocketsurgery"    :   0.3,
    "brainscience"     :   0.5,
    "other"            :   0.6,
    }
#------- end configuration -------#

pics = listdir(pictureDirectory)

def showPics():
    if mw.col.decks.current()['name'] in deckPicsProbabilities:
        picsProbability = deckPicsProbabilities[mw.col.decks.current()['name']]
    else:
        picsProbability = deckPicsProbabilities["other"]
        
    if random() < picsProbability:
        mw.splash = QSplashScreen(QPixmap(pictureDirectory + choice(pics)))
        try:
            mw.splash.move(flashPosition[0], flashPosition[1])
        except NameError:
            pass
        mw.splash.show()
        QTimer.singleShot(flashTime, mw.splash.close)

addHook("showQuestion", showPics)
