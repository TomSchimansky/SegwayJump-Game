"""
compilation worked with:
python 3.6.10
pygame==1.9.6
argv_emulation': False (!)

zsh: python3.6 setup.py py2app --packages=pygame
"""


from setuptools import setup

APP = ['main.py']

APP_NAME = "Segway Jump"

ICON_FILES = ["assets/icons/icon.txt"]

HIGHSCORE_FILES = ["assets/highscore_files/highscore.txt"]

FONT_FILES = ["assets/fonts/Chalkboard_Bold.ttf"]

SOUND_FILES = ["assets/sounds/sfx_die.wav",
               "assets/sounds/Ambient Background Music - Cicada 3301.wav",
               "assets/sounds/Blup.wav",
               "assets/sounds/button-27.wav",
               "assets/sounds/JumpSound.wav",
               "assets/sounds/Ding - Sound.wav",
               "assets/sounds/powerup.wav"]

IMAGE_FILES = ["assets/images/banner.txt",
               "assets/images/coin1.txt",
               "assets/images/coins.txt",
               "assets/images/endbutton.txt",
               "assets/images/floatingplatform.txt",
               "assets/images/middleplatform.txt",
               "assets/images/movingfloatingplatform.txt",
               "assets/images/movingplatform.txt",
               "assets/images/movingsocketplatform.txt",
               "assets/images/platform.txt",
               "assets/images/playerleft1.txt",
               "assets/images/playerleft2.txt",
               "assets/images/playerleft3.txt",
               "assets/images/playerleft4.txt",
               "assets/images/playerleft5.txt",
               "assets/images/startbutton.txt",
               "assets/images/speeddrop.txt",
               "assets/images/startbutton.txt",
               "assets/images/jumpboost.txt",
               "assets/images/levels.txt",
               "assets/images/finish.txt",
               "assets/images/menubutton.txt",
               "assets/images/steelplate1.txt",
               "assets/images/steelplate2.txt",
               "assets/images/steelplate3.txt",
               "assets/images/steelplate4.txt",
               "assets/highscore_files/highscore.txt"]

OPTIONS = {'argv_emulation': False,
           'iconfile': 'assets/icons/SegwayJumpIcon.icns',
           'plist': {
               'CFBundleName': APP_NAME,
               'CFBundleDisplayName': APP_NAME,
               'CFBundleGetInfoString': "Jump with Segway",
               'CFBundleIdentifier': "com.TomSchimansky.SegwayJump",
               'CFBundleVersion': "3.2.0",
               'CFBundleShortVersionString': "3.2.0",
               'NSHumanReadableCopyright': u"Copyright © 2018, Tom Schimansky, All Rights Reserved"
              }}

setup(
    name=APP_NAME,
    app=APP,
    author='Tom Schimansky',
    data_files=[("assets/images", IMAGE_FILES),
                ("assets/sounds", SOUND_FILES),
                ("assets/fonts", FONT_FILES),
                ("assets/icons", ICON_FILES),
                ("assets/highscore_files", HIGHSCORE_FILES)],
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
