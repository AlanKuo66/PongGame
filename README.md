# PongGame
I have been learning Python for 1 week. This is my first python game. (for Python Learning).
The original source code of pong comes from TokyoEdTech's "[Simple Pong in Python 3 for Beginners](http://christianthompson.com/sites/default/files/Pong/pong.py)".
My father helped to add many new features and refactor the source code for me. 

## Demo
![Pong Demo](/demo/pong.gif?raw=true "Pong Demo")

Sound Video:

https://user-images.githubusercontent.com/88357844/127956942-de214c92-bb5a-48b3-a1f9-e2a5f4cfe101.mp4

## Features

- Use Turtle graphics for Game Render
- Support multiple balls
- Improve collision detection
- Support audio support
- Funny cheating key
- Add new ball speed and reflect control

## Audio Support and Issues

- Support audio modules: [SimpleAudio](https://github.com/hamiltron/py-simple-audio), [Pydub](https://github.com/jiaaro/pydub) and [Pygame](https://github.com/pygame/pygame)
- Play multiple audio tracks simultaneously
- SimpleAudio audio playback issue:
  - System will throw errors randomly if we try to playback multiple sounds
  - This error always raises a native exception when Turtle Graphics Screen is updated
  - Pydub uses SimpleAudio to render audio, so we will encounter the same problems as SimpleAudio
- Pygame works perfectly with multiple audio tracks, so I use the pygame mixer as my default audio rendering 

## Controls

- Select Audio Render
  - PyGame (default), PLAY_LIB_PYGAME = True
  - PyDub, PLAY_LIB_PYDUB= True
  - SimpleAudio, If no PyGame and no PyDub
- Select Ball Numbers
  - BALL_NUM = 5, (Maximum)
- Paddles Size
  - PAD_1_H = 101
  - PAD_2_H = 101

## Programming
I use Visual Sutdio 2019 Python to maintain the project. You can edit and run the code by opening the .sln file.
Use pip to install all relevant packages to run the project.
For other editors, you can use your favorite Python (such as Visual Studio Code) to run pong.py. 

## License

- Audio files is from [Freesound](https://freesound.org)
- Original **Pong.py** is from TokyoEdTech's "[Simple Pong in Python 3 for Beginners](http://christianthompson.com/sites/default/files/Pong/pong.py)"
- There is No License for this pony game.



