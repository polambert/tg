
# tg
tg is a python utility for setting up small graphical interfaces in the terminal.

It is not as complex as curses, and should primarily be used for game development, graphing, or other smaller programs.

## Features
- Draw lines, blocks, circles, and rectangles.
- Draw characters on the screen
- Change the color of whatever you want

## Not yet added
- Filling in shapes
- Gradients
- Keyboard input, although this can be done manually pretty easily

## Usage
```
from tg import Window

window = Window()

window.clear()
window.backspace()

window.circle(40, 40, 10, (0, 255, 0), (0, 150, 0))

window.display()
```

There are other drawing functions available, such as rect(), write(), line(), and dot(). You can also browse through `tg.py`.
