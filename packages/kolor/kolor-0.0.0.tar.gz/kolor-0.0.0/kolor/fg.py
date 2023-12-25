from .helper import *

# Colors
                                 
black          =   '\033[30m'
red            =   '\033[31m'
green          =   '\033[32m'
yellow         =   '\033[33m'
blue           =   '\033[34m'
magenta        =   '\033[35m'
cyan           =   '\033[36m'
grey           =   '\033[37m'
darkgrey       =   '\033[90m'
lightred       =   '\033[91m'
lightgreen     =   '\033[92m'
lightyellow    =   '\033[93m'
lightblue      =   '\033[94m'
lightmagenta   =   '\033[95m'
lightcyan      =   '\033[96m'
white          =   '\033[97m'

# 256 Color mode

def color256(number: int):

    # Usage

    '''Prints text with a colored foreground of your given Color Number
    Note -> Number must be in the range of numbers 0 to 255
    Example -> fg.color256(10) for a light green foreground'''

    # Main
        
    if number in range(0,256):
        return '\033[38;5;' + str(number) + 'm'
    else:
        raise ValueError('Number must be in the range of numbers 0 to 255')

# HSL

def hsl(h: float, s: float, l: float):

    # Usage

    '''Prints text with a colored foreground of your given HSL Color
    Note -> H must be in numbers 0 to 360 and S, L must be in numbers 0 to 100
    Example -> fg.hsl(30, 100, 50) for an orange foreground'''

    # Main
            
    if check.hsl(h, s, l) == True:
        r, g, b = tuple(int(i) for i in convert.hsl_to_rgb(h, s, l))
        return '\033[38;2;' + str(r) + ';' + str(g) + ';' + str(b) + 'm'
    else:
        validate.hsl(h, s, l)
        
# HSV

def hsv(h: float, s: float, v: float):

    # Usage

    '''Prints text with a colored foreground of your given HSV Color
    Note -> H must be in numbers 0 to 360 and S, V must be in numbers 0 to 100
    Example -> fg.hsv(30, 100, 100) for an orange foreground'''
        
    # Main
            
    if check.hsv(h, s, v) == True:
        r, g, b = tuple(int(i) for i in convert.hsv_to_rgb(h, s, v))
        return '\033[38;2;' + str(r) + ';' + str(g) + ';' + str(b) + 'm'
    else:
        validate.hsv(h, s, v)
            
# Hex

def hex(hex: str):

    # Usage

    '''Prints text with a colored foreground of your given Hex Color
    Note -> Hex should be in numbers 0 to 9 and letters A to F
    Example -> fg.hex('#FF8000') for an orange foreground'''

    # Main

    if check.hex(hex) == True:
        r, g, b = tuple(int(i) for i in convert.hex_to_rgb(hex))
        return '\033[38;2;' + str(r) + ';' + str(g) + ';' + str(b) + 'm'
    else:   
        validate.hex(hex)

# CMYK

def cmyk(c: int, m: int, y: int, k: int):

    # Usage

    '''Prints text with a colored foreground of your given CMYK Color
    Note -> CMYK must be in the range of numbers 0 to 100
    Example -> fg.cmyk(0, 50, 100, 0) for an orange foreground'''

    # Main
            
    if check.cmyk(c, m, y, k) == True:
        r, g, b = tuple(int(i) for i in convert.cmyk_to_rgb(c, m, y, k))
        return '\033[38;2;' + str(r) + ';' + str(g) + ';' + str(b) + 'm'
    else:
        validate.cmyk(c, m, y, k)
            
# RGB

def rgb(r: int, g: int, b: int):

    # Usage

    '''Prints text with a colored foreground of your given RGB Color.
    Note -> RGB must be in the range of numbers 0 to 255.
    Example -> fg.rgb(255, 128, 0) for an orange foreground.'''

    # Main
    
    if check.rgb(r, g, b) == True:
        return '\033[38;2;' + str(r) + ';' + str(g) + ';' + str(b) + 'm'
    else:
        validate.rgb(r, g, b)
