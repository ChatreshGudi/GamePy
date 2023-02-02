from Game import *
from colors import *
import time 

win = Window(500, 500)

trial = Scene(win, white, "Trial")

# trial.setBG(white)
# trial.se

btn = Button(trial, 20, 20, 100, 100, green, 5, (50, 50, 255), 15)
btn.hover_config['bg'] = white
# input = InputBox(win, 200, 200, 50, 30)
print(win.scenes)

def do():
    print('Click!')
    time.sleep(1)
    
@win.run
def main():
    btn.onClick(do)