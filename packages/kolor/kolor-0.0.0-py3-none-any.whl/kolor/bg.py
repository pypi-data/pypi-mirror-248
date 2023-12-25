from .helper import *

# Colors

black          =   '\033[40m'
red            =   '\033[41m'
green          =   '\033[42m'
yellow         =   '\033[43m'
blue           =   '\033[44m'    
magenta        =   '\033[45m'
cyan           =   '\033[46m'
grey           =   '\033[47m'
darkgrey       =   '\033[100m'
lightred       =   '\033[101m'
lightgreen     =   '\033[102m'
lightyellow    =   '\033[103m'
lightblue      =   '\033[104m'
lightmagenta   =   '\033[105m'
lightcyan      =   '\033[106m'
white          =   '\033[107m'

# 256 Color mode

def color256(number: int):

    # Usage

    '''Prints text with a colored background of your given Color Number
    Note -> Number must be in the range of numbers 0 to 255
    Example -> bg.color256(10) for a light green background'''

    # Main
            
    if number in range(0,256):
        return '\033[48;5;' + str(number) + 'm'
    else:
        raise ValueError('Number must be in the range of numbers 0 to 255')

# HSL

def hsl(h: float, s: float, l: float):

    # Usage

    '''Prints text with a colored background of your given HSL Color
    Note -> H must be in numbers 0 to 360 and S, L must be in numbers 0 to 100
    Example -> bg.hsl(30, 100, 50) for an orange background'''

    # Main
            
    if check.hsl(h, s, l) == True:
        r, g, b = tuple(int(i) for i in convert.hsl_to_rgb(h, s, l))
        return '\033[48;2;' + str(r) + ';' + str(g) + ';' + str(b) + 'm'
    else:
        validate.hsl(h, s, l)
            
# HSV

def hsv(h: float, s: float, v: float):

    # Usage

    '''Prints text with a colored background of your given HSV Color
    Note -> H must be in numbers 0 to 360 and S, V must be in numbers 0 to 100
    Example -> bg.hsv(30, 100, 100) for an orange background'''

    # Main
            
    if check.hsv(h, s, v) == True:
        r, g, b = tuple(int(i) for i in convert.hsv_to_rgb(h, s, v))
        return '\033[48;2;' + str(r) + ';' + str(g) + ';' + str(b) + 'm'
    else:
        validate.hsv(h, s, v)

# Hex

def hex(hex: str):

    # Usage

    '''Prints text with a colored background of your given Hex Color
    Note -> Hex should be in numbers 0 to 9 and letters A to F
    Example -> bg.hex('#FF8000') for an orange background'''

    # Main

    if check.hex(hex) == True:
        r, g, b = tuple(int(i) for i in convert.hex_to_rgb(hex))
        return '\033[48;2;' + str(r) + ';' + str(g) + ';' + str(b) + 'm'
    else:   
        validate.hex(hex)

# CMYK

def cmyk(c: int, m: int, y: int, k: int):

    # Usage

    '''Prints text with a colored background of your given CMYK Color
    Note -> CMYK must be in the range of numbers 0 to 100
    Example -> bg.cmyk(0, 50, 100, 0) for an orange background'''

    # Main

    if check.cmyk(c, m, y, k) == True:
        r, g, b = tuple(int(i) for i in convert.cmyk_to_rgb(c, m, y, k))
        return '\033[48;2;' + str(r) + ';' + str(g) + ';' + str(b) + 'm'
    else:
        validate.cmyk(c, m, y, k)
                
# RGB

def rgb(r: int, g: int, b: int):

    # Usage

    '''Prints text with a colored background of your given RGB Color.
    Note -> RGB must be in the range of numbers 0 to 255.
    Example -> bg.rgb(255, 128, 0) for an orange background.'''

    # Main
        
    if check.rgb(r, g, b) == True:
        return '\033[48;2;' + str(r) + ';' + str(g) + ';' + str(b) + 'm'
    else:
        validate.rgb(r, g, b)
