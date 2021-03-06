![](documentation/segway_jump_overview.png)
This is a complete example of a game made with python and pygame. It contains a start, menu and splash-screen with music and sound-effects.

To start the game you need python3 with pygame installed. Then you can do:
```
python3 main.py
```

### Create standalone application
To create a standalone application use py2app or py2exe, and make sure you got the exact same library versions as in my requirements.txt.

For macOS you need py2app:
```
python3 setup.py py2app
```
For windows you need to use py2exe instead.

To keep application size as small as possible, make sure you create a virtual environment where you install only the necessary libraries.
