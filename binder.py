from pynput import keyboard
from pynput.keyboard import Key, Controller
from copy import deepcopy
import sys
import datetime
import time
inkey = Controller()

recording = False
triggered = False
direction = 'right'

current = []
startTimer = datetime.datetime.now()
lastpress = 'right'

#list of scripts
scripts = []

#oppening local scripts
f = open('altscript.txt','r').read()[1:-1].split('], [')
for i in range(len(f)):
    scripts.append([])
    for j in f[i].split(', '):
        if(j[0]=='\''):
            scripts[len(scripts)-1].append(j[1:-1])
        else:
            scripts[len(scripts)-1].append(j)

for i in range(len(scripts)):
    scripts[i][2]= int(scripts[i][2])
current = scripts
print(current)
def onRecordStart():
    global current
    current = []
    global startTimer
    startTimer = datetime.datetime.now()
    print('Started! '+ str(startTimer))

def onRecordPress(key):
    global startTimer
    currentTimer = datetime.datetime.now() - startTimer
    current.append([key,'down',int(currentTimer.total_seconds() * 1000)])
    startTimer = datetime.datetime.now()

def onRecordRelease(key):
    global startTimer
    currentTimer = datetime.datetime.now() - startTimer
    current.append([key,'up',int(currentTimer.total_seconds() * 1000)])
    startTimer = datetime.datetime.now()

def onRecordStop():
    print('stopped')
    print(current)

def onRecording():
    print('recording')


def startPlayer():

    playercurrent = []
    print('Playback: '+direction+'x'+lastpress)
    playercurrent = deepcopy(current)
    if (direction != lastpress):
        for i in range(len(playercurrent)):
            if (playercurrent[i][0]=='right'):
                playercurrent[i][0] = 'left'
            else :
                if (playercurrent[i][0]=='left'):
                    playercurrent[i][0] = 'right'

    for i in playercurrent:
        time.sleep(i[2]/1000)
        if(not movementKey(i[0])):
            if(i[1]=='down'):
                inkey.press(i[0])
            else:
                inkey.release(i[0])
        else:
            if(i[1]=='down'):
                inkey.press(movementSwitcher(i[0]))
            else:
                inkey.release(movementSwitcher(i[0]))
        

def inKeyRange(key):
    if (key == 'z' or key == 'x' or key == 'c' or key == 'v' or key == 'x' or key == 'up' or key == 'down' or key == 'left' or key == 'right'):
        return True
    else:
        return False

def movementSwitcher(key):
    if (key == 'up'):
        return keyboard.Key.up
    if (key == 'down'):
        return keyboard.Key.down
    if (key == 'left'):
        return keyboard.Key.left
    if (key == 'right'):
        return keyboard.Key.right
def movementKey(key):
    if (key == 'up' or key == 'down' or key == 'left' or key == 'right'):
        return True
    else:
        return False

def getPress(key):
    global recording,triggered,direction
    if (key == 'q' and not recording):
        direction = lastpress
        print('Script is facing: '+direction)
        recording = True
        print('Triggered, waiting for action.')
    else:
        if (key == 'q' and recording):
            recording = False
            triggered = False
            onRecordStop()
    if(key == 'alt'):
        startPlayer()
        
    if (inKeyRange(key) and not triggered and recording):
        triggered = True
        onRecordStart()
    
    if(inKeyRange(key) and triggered and recording):
        onRecordPress(key)
    


def getRelease(key):
    global recording,triggered
    if(inKeyRange(key) and recording and triggered):
        onRecordRelease(key)


def on_press(key):
    global lastpress
    try:
        getPress(key.char)
    except AttributeError:
        if(key == keyboard.Key.alt_l):getPress('alt')
        if(key == keyboard.Key.up):getPress('up')
        if(key == keyboard.Key.down):getPress('down')
        if(key == keyboard.Key.left):
            lastpress = 'left'
            getPress('left')
        if(key == keyboard.Key.right):
            lastpress = 'right'
            getPress('right')
        if(key == keyboard.Key.esc):sys.exit()

def on_release(key):
    try:
        getRelease(key.char)
    except AttributeError:
        if(key == keyboard.Key.up):getRelease('up')
        if(key == keyboard.Key.down):getRelease('down')
        if(key == keyboard.Key.left):getRelease('left')
        if(key == keyboard.Key.right):getRelease('right')
        if(key == keyboard.Key.alt):getRelease('alt')

    

# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
