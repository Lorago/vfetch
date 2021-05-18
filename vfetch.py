#!/usr/bin/env python3

from xdg.BaseDirectory import xdg_config_home
from enum import Enum
import subprocess
import platform
import distro
import json
import re
import os
import wmctrl

colors = [
    # Regular colors.
    "\u001b[30m",
    "\u001b[31m",
    "\u001b[32m",
    "\u001b[33m",
    "\u001b[34m",
    "\u001b[35m",
    "\u001b[36m",
    "\u001b[37m",

    # Bright colors.
    "\u001b[30;1m",
    "\u001b[31;1m",
    "\u001b[32;1m",
    "\u001b[33;1m",
    "\u001b[34;1m",
    "\u001b[35;1m",
    "\u001b[36;1m",
    "\u001b[37;1m",

    # Reset.
    "\u001b[0m"
]

decorations = [
    "\u001b[1m", # Bold.
    "\u001b[4m", # Underline.
    "\u001b[7m"  # Reversed.
]

# Creates a copy of the specified string with color and decorations added.
def colored(string, colorIndex, decorationIndices=[]):
    newString = colors[colorIndex]
    for decorationIndex in decorationIndices:
        newString += decorations[decorationIndex]
    newString += string + colors[len(colors)-1]
    return newString

# Enum for the different data types.
class Type(str, Enum):
    os = 'os'
    kernel = 'kernel'
    wm = 'wm'
    packages = 'packages'
    uptime = 'uptime'
    shell = 'shell'
    terminal = 'terminal'
    battery = 'battery'
    usage =  'usage'

# Enum for the different align modes.
class AlignMode(str, Enum):
    spaces = 'spaces'
    center = 'center'

# Loads the settings from the configuration file.
# First checks for a configuration file in ~/.config/vfetch/vfetch.conf,
# else it defaults to the configuration file in the same folder as the script.
def loadSettings():
    try:
        file = open(xdg_config_home + '/vfetch/vfetch.conf', 'r')
    except FileNotFoundError:
        file = open(os.path.dirname(os.path.realpath(__file__)) + '/vfetch.conf', 'r')
    content = file.read()
    settings = json.loads(content)
    file.close()
    return settings

# Prints string without ending with a new line.
def printn(string):
    print(string, end="")

# Prints string at a specified position.
def printAt(string, *position):
    if len(position) == 1:
        x = position[0][0]
        y = position[0][1]
    else:
        x = position[0]
        y = position[1]
    printn("\x1b7\x1b[%d;%df%s\x1b8" % (y+1, x+1, string))

# Prints the data lines.
def printLines(lines, colorIndex, offsetX, offsetY, alignMode, alignSpace):
    longestName = 0
    dataPosition = 0

    if alignMode is AlignMode.spaces:
        for line in lines:
            position = len(line[0]) + alignSpace
            if position > dataPosition:
                dataPosition = position
    else:
        # Finds the length of the longest name.
        longestName = len(max(lines, key = lambda data: len(data[0]))[0])

    y = 0
    x = offsetX
    # Prints the lines and formats them accordingly.
    for line in lines:
        if alignMode is AlignMode.spaces:
            printAt(line[1], x + dataPosition, y+offsetY)
        elif alignMode is AlignMode.center:
            line[0] = ' ' * (longestName - len(line[0])) + line[0]

        printAt(colored(line[0], colorIndex, [0]), x, y+offsetY)
        if alignMode is AlignMode.center:
            printAt(' ~ ' + line[1], x+len(line[0]), y+offsetY)
        y += 1

# Sets the cursor position.
def setCursorPosition(*position, newLine=False):
    if len(position) == 1:
        x = position[0][0]
        y = position[0][1]
    else:
        x = position[0]
        y = position[1]
    string = '\033[%d;%dH' % (y, x)
    if newLine:
        print(string)
    else:
        printn(string)

# Runs the specified terminal command.
def termRun(command, arguments):
    # output = subprocess.run([command, arguments], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #Their is also a method popen().read() of os library that do exactly the same thing
    output = os.popen("{} {}".format(command , arguments)).read()
    return output

# Prints ascii image.
def printAscii(position, asciiImage):
    setCursorPosition(position)
    lines = asciiImage.split('\n')
    for line in lines:
        print(line)

# Gets the operating system.
def getOS(architecture=False, removeLinux=False):
    os = distro.linux_distribution()[0]
    if removeLinux:
        os = re.sub('linux', '', os, flags=re.IGNORECASE)
    os = os.rstrip()
    if architecture:
        os += ' ' + platform.machine()
    return os

# Gets the kernel.
def getKernel(fullName=True):
    kernel = platform.release()
    if not fullName:
        kernel = kernel.split('-')[0]
    return kernel

# Gets the window manager.
def getWM():
    try:
        return wmctrl.os.environ.get('DESKTOP_SESSION')
    except:
        pass
    try:
        return wmctrl.os.environ.get('XDG_SESSION_DESKTOP')
    except:
        return None

# Gets the number of packages.
def getPackages(displayPackageManager=False):
    try:
        packages = termRun('pacman', '-Qq')
        string = str(len(packages.split('\n')))
        if displayPackageManager:
            string += ' (pacman)'
        return string
    except:
        return None

# Gets the machine uptime.
def getUptime():
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])
        hours = uptime_seconds / 3600
        minutes = (hours - int(hours)) * 60
        hours = int(hours)
        minutes = int(minutes)
        string = ''
        if hours != 0:
            string += str(hours) + 'h '
        if minutes != 0 or hours == 0:
            string += str(minutes) + 'm'
    return string

# Gets the data for the specified data type.
def getData(type, settings):
    data = {
        Type.os: getOS(settings['displayArchitecture'], settings['removeLinux']),
        Type.kernel: getKernel(settings['kernelFullName']),
        Type.wm: getWM(),
        Type.packages: getPackages(settings['displayPackageManager']),
        Type.uptime: getUptime(),
        Type.terminal: termRun("echo" , "$TERM"), #getting current activate terminal
        Type.shell: getShell(),#get default terminal
        Type.battery: getBattery(),#get current battery status
        Type.usage: getCurrentBatteryConsumption() #get current battery usage in mW
    }.get(type, None)

    if data is None:
        return None

    name = {
        Type.os: [ 'OS', '' ],
        Type.kernel: [ 'Kernel', '' ],
        Type.wm: [ 'WM', '缾' ],
        Type.packages: [ 'Packages', '' ],
        Type.uptime: [ 'Uptime', '' ],
        Type.terminal: ['Terminal' , ''],
        Type.shell: ['Shell' , ''],
        Type.battery: ['Battery' , ''],
        Type.usage: ['Usage' , '']
    }.get(type, None)[int(settings['iconMode'])]

    if settings['lowercase']:
        name = name.lower()
        data = data.lower()

    return [name, data]

# Gets the size of the specified ascii image.
def asciiSize(asciiImage):
    x = 0
    split = asciiImage.split('\n')
    for line in split:
        if len(line) > x:
            x = len(line)
    return [x, len(split)]

# Trims the specified ascii image of empty lines and trailing whitespaces.
def trimAscii(asciiImage):
    lines = asciiImage.split('\n')
    string = ''
    for line in lines:
        trimmedString = line.rstrip()
        if len(trimmedString) != 0:
            string += trimmedString + '\n'
    string = string[:-1] # Removes last newline.
    return string

# Loads the ascii image at the specified path.
def loadAsciiImage(path):
    file = open(path, 'r')
    asciiImage = trimAscii(file.read())
    file.close()
    return asciiImage


#get Terminal
def getShell():
    res = termRun("echo" , "$SHELL")
    resp = re.search(r"/.+/(.+)" , res)
    return resp.group(1)

#Get battery data
BattPath = "/sys/class/power_supply/BAT0/"

def getBattery():
    fullBatteryCapacityPath , currentBatteryPath = [BattPath+"energy_full" , BattPath+"energy_now"]
    with open(fullBatteryCapacityPath , "r") as f:
        fullBatteryCapacity = int(f.read())
    with open(currentBatteryPath , "r") as f:
        currentBattery = int(f.read())
    batteryPercent = (currentBattery/fullBatteryCapacity)*100
    return f"{int(batteryPercent)}%"

def getCurrentBatteryConsumption():
    with open(BattPath+"power_now") as f:
        currentPowerUsage = int(f.read())
    return f"{currentPowerUsage/1000000:.2f}mW"

settings = loadSettings()

displayAscii = settings['displayAscii']
offset = settings['offset']

# Loads the data lines. If the data is invalid (None) it does not get added.
lines = []
for dataType in settings['data']:
    data = getData(dataType, settings)
    if data is not None:
        lines.append(data)

# Loads the ascii image if the option is set for it.
if displayAscii:
    asciiImage = loadAsciiImage(settings['asciiImage'])
    size = asciiSize(asciiImage)
    offset[0] += size[0]
    finalPosition = [0, size[1]]
else:
    finalPosition = [0, len(lines)+offset[1]]

# Makes the prompt after the script finishes have a blank line before it.
finalPosition[1] += 1

os.system('clear')

if displayAscii:
    printAscii([0,0], asciiImage)

alignMode = AlignMode(settings['alignMode'])

printLines(lines, settings['colorIndex'], offset[0], offset[1], alignMode, settings['alignSpace'])

# Sets the final cursor position for the prompt to end up at.
setCursorPosition(finalPosition, newLine=True)
