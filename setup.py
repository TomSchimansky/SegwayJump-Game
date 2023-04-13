from setuptools import setup

APP = ['main.py']

APP_NAME = "SegwayJump"

ICON_FILES = ["assets/icons/icon.png"]

HIGHSCORE_FILES = ["assets/highscores/highscores.json"]

LEVEL_FILES = ["assets/levels/levels.json"]

FONT_FILES = ["assets/fonts/Chalkboard_Bold.ttf"]

SOUND_FILES = ["assets/sounds/sfx_die.wav",
               "assets/sounds/ambient_background_music_cicada_3301.wav",
               "assets/sounds/blup.wav",
               "assets/sounds/button_27.wav",
               "assets/sounds/jump_Sound.wav",
               "assets/sounds/ding_sound.wav",
               "assets/sounds/powerup.wav"]

IMAGE_FILES = ["assets/images/banner.png",
               "assets/images/coin_1.png",
               "assets/images/coin_10.png",
               "assets/images/coins.png",
               "assets/images/endbutton.png",
               "assets/images/finish.png",
               "assets/images/floatingplatform.png",
               "assets/images/floatingplatformsocket.png",
               "assets/images/jumpboost.png",
               "assets/images/level_list.png",
               "assets/images/levelmenu.png",
               "assets/images/menubutton.png",
               "assets/images/middleplatform.png",
               "assets/images/movingfloatingplatform.png",
               "assets/images/movingplatform.png",
               "assets/images/movingsocketplatform.png",
               "assets/images/pause.png",
               "assets/images/platform.png",
               "assets/images/play.png",
               "assets/images/player_jump_1.png",
               "assets/images/player_jump_2.png",
               "assets/images/player_left_1.png",
               "assets/images/player_left_2.png",
               "assets/images/player_left_3.png",
               "assets/images/speeddrop.png",
               "assets/images/startbutton.png",
               "assets/images/steelplate_1.png",
               "assets/images/steelplate_2.png",
               "assets/images/steelplate_3.png",
               "assets/images/steelplate_4.png"]

OPTIONS = {'argv_emulation': True,
           'iconfile': 'assets/icons/icon.icns',
           'includes': ['pygame'],
           'excludes': ['opencv', 'numpy', 'scipy'],
           'plist': {
               'CFBundleName': APP_NAME,
               'CFBundleDisplayName': APP_NAME,
               'CFBundleGetInfoString': "SegwayJump game made with pygame",
               'CFBundleIdentifier': "com.TomSchimansky.SegwayJump",
               'CFBundleVersion': "4.0.0",
               'CFBundleShortVersionString': "4.0.0",
               'NSHumanReadableCopyright': u"Copyright © 2018, Tom Schimansky, All Rights Reserved"
              }}

# compile to .app for macOS with py2app:
setup(name=APP_NAME,
      app=APP,
      author='Tom Schimansky',
      data_files=[("assets/images", IMAGE_FILES),
                  ("assets/sounds", SOUND_FILES),
                  ("assets/fonts", FONT_FILES),
                  ("assets/icons", ICON_FILES),
                  ("assets/highscores", HIGHSCORE_FILES),
                  ("assets/levels", LEVEL_FILES)],
      options={'py2app': OPTIONS},
      setup_requires=['py2app'])
