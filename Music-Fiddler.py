# -*- coding: utf-8 -*-
# Music-Fiddler (a plugin for Anki)
# coded by D_Malik, malik6174@gmail.com
# Version 1
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

"""
A simple plugin that fiddles with computer volume to reinforce quick reviewing.

Before using:
- Ensure that the "amixer" command works on your computer. If it doesn't, you're going to need to modify the code somehow. Don't ask me how. If someone knows how to code this so it doesn't depend on this, and puts the better version online, they are awesome and they should feel awesome.
- Change all lines marked with "CHANGEME" according to your preferences.
"""

from aqt import mw
from aqt.utils import showInfo
from os import system
from aqt.qt import *
from anki.hooks import addHook

def resetMusicTimer():
    "Boosts volume back up and starts the music timer."
    #CHANGEME: The next lines are a python dictionary associating deck names with times (in milliseconds) between volume-decrements.
    #Eg, when using the deck "brainscience", volume will decrement every 5 seconds. When using a deck without a listed name, "other" is used.
    #Change this according to your decks. Decks with shorter, easier cards need less time.
    deckMusicTimes = {
                 "brainscience"  :   5000,
                 "rocketsurgery" :   3000,
                 "other"         :   2000,
                 }
    if mw.col.decks.current()['name'] in deckMusicTimes:
        mw.musicTimeToDecrement = deckMusicTimes[mw.col.decks.current()['name']]
    else:
        mw.musicTimeToDecrement = deckMusicTimes["other"]
    boostMusicVolume()
    mw.musicTimer = QTimer(mw)
    mw.musicTimer.setSingleShot(True)
    mw.musicTimer.start(mw.musicTimeToDecrement)
    mw.connect(mw.musicTimer, SIGNAL("timeout()"), decrementMusicVolume)
    #showInfo(mw.state)

def changeMusicVolume(change):
    "Changes volume according to string; can be either absolute ('40') or change ('2%-')."
    system("amixer set Master " + change) #CHANGEME somehow, if amixer doesn't work 

def boostMusicVolume():
    #showInfo("boosted") #To test changes, you can uncomment this line.
    changeMusicVolume("100")
    #CHANGEME: Set to however high you want your volume to go each time it's boosted back. Can be either abs
    #Protip: your music-playing program might have its own "volume multiplier" that you can adjust easily.

def killMusicVolume():
    #showInfo("killed") #To test changes, you can uncomment this line.
    changeMusicVolume("10")
    #CHANGEME: Set to how low volume should go when it dies, eg due to undoing a card.

def decrementMusicVolume():
    "When reviewing, decrements volume, then sets a timer to call itself. When not reviewing, kills volume and stops timer."
    if mw.state == "review":
        #showInfo("music volume goes down") #To test changes, you can uncomment this line.
        changeMusicVolume("2%-") #CHANGEME if you prefer smaller or bigger volume jumps.
        mw.musicTimer.start(mw.musicTimeToDecrement) #(start the timer again)
    else:
    	killMusicVolume()
        mw.musicTimer = None #(kill the timer if you're not reviewing)

addHook("showQuestion", resetMusicTimer)
