import colorsys

# Check color space values

class check:

    # HSL

    def hsl(h: float, s: float, l: float):

        # Usage

        '''Checks if the given HSL Color is valid
        Example -> check.hsl(30, 100, 50) will return True'''

        # Main

        if (h >= 0 and h <= 360) and (s >= 0 and s <= 100) and (l >= 0 and l <= 100):
            return True
        else:
            return False

    # HSV

    def hsv(h: float, s: float, v: float):

        # Usage

        '''Checks if the given HSV Color is valid
        Example -> check.hsv(30, 100, 100) will return True'''

        # Main

        if (h >= 0 and h <= 360) and (s >= 0 and s <= 100) and (v >= 0 and v <= 100):
            return True
        else:
            return False

    # Hex

    def hex(hex: str):

        # Usage
    
        '''Checks if the given Hex Color is valid
        Example -> check.hex('#FF8000') will return True'''

        # Main
    
        if len(hex.lstrip('#')) in (6, 3):
            try:
                int(str(hex.lstrip('#')), 16)
            except ValueError:
                return False
            else:
                return True
        else:
            return False

    # CMYK

    def cmyk(c: int, m: int, y: int, k: int):

        # Usage

        '''Checks if the given CMYK Color is valid
        Example -> check.cmyk(0, 50, 100, 0) will return True'''

        # Main

        if c in range(0,101) and m in range(0,101) and y in range(0,101) and k in range(0,101):
            return True
        else:
            return False

    # RGB
    
    def rgb(r: int, g: int, b: int):

        # Usage

        '''Checks if the given RGB Color is valid
        Example -> check.rgb(255, 128, 0) will return True'''

        # Main

        if r in range(0,256) and g in range(0,256) and b in range(0,256):
            return True
        else:
            return False

# Validate color space values

class validate:

    # HSL

    def hsl(h: float, s: float, l: float):

        # Usage

        '''Looks for errors in the given HSL Color
        Example -> validate.hsl(400, 100, 50) will raise a ValueError
        As H is not in the range of numbers 0 to 360'''

        # Main

        if not (h >= 0 and h <= 360):
            raise ValueError('H must be in the range of numbers 0 to 360')
        if not (s >= 0 and s <= 100):
            raise ValueError('S must be in the range of numbers 0 to 100')
        if not (l >= 0 and l <= 100):
            raise ValueError('L Must be in The range of numbers 0 to 100')
        else:
            raise SyntaxError('No error was found in the given HSL Color')
            
    # HSV

    def hsv(h: float, s: float, v: float):
    
        # Usage

        '''Looks for errors in the given HSV Color
        Example -> validate.hsv(400, 100, 100) will raise a ValueError
        As H is not in the range of numbers 0 to 360'''

        # Main

        if not (h >= 0 and h <= 360):
            raise ValueError('H must be in the range of numbers 0 to 360')
        if not (s >= 0 and s <= 100):
            raise ValueError('S must be in the range of numbers 0 to 100')
        if not (v >= 0 and v <= 100):
            raise ValueError('V Must be in The range of numbers 0 to 100')
        else:
            raise SyntaxError('No error was found in the given HSV Color')

    # Hex

    def hex(hex: str):
    
        # Usage

        '''Looks for errors in the given Hex Color
        Example -> validate.hex('#GG8000') will raise a ValueError
        As it should only contain letters A to F But it Contains the letter G'''

        # Main

        if len(hex.lstrip('#')) in (6, 3):
            try:
                int(str(hex.lstrip('#')), 16)
            except ValueError:
                raise ValueError('Hex should only contain numbers 0 to 9 and letters A to F') from None
            else:
                raise SyntaxError('No error was found in the given Hex Color')
        else:
            raise ValueError('Length of hex must be of 6 or 3 characters')

    # CMYK

    def cmyk(c: int, m: int, y: int, k: int):
    
        # Usage
    
        '''Looks for errors in the given CMYK Color
        Example -> validate.cmyk(0, 150, 100, 0) will raise a ValueError
        As M is not in the range of numbers 0 to 100'''

        # Main

        if c not in range(0,101):
            raise ValueError('C must be in the range of numbers 0 to 100')
        if m not in range(0,101):
            raise ValueError('M must be in the range of numbers 0 to 100')
        if y not in range(0,101):
            raise ValueError('Y must be in the range of numbers 0 to 100')
        if k not in range(0,101):
            raise ValueError('K must be in the range of numbers 0 to 100')
        else:
            raise SyntaxError('No Error Was Found in The Given CMYK Color')

    # RGB

    def rgb(r: int, g: int, b: int):
    
        # Usage

        '''Looks for errors in the given RGB Color
        Example -> validate.rgb(300, 128, 0) will raise a ValueError
        As R is not in the range of numbers 0 to 255'''

        # Main

        if r not in range(0,256):
            raise ValueError('R must be in the range of numbers 0 to 255')
        if g not in range(0,256):
            raise ValueError('G must be in the range of numbers 0 to 255')
        if b not in range(0,256):
            raise ValueError('B must be in the range of numbers 0 to 255')
        else:
            raise SyntaxError('No error was found in the given RGB Color')

# Convert color space values to RGB and back

class convert:

    # HSL to RGB

    def hsl_to_rgb(h: float, s: float, l: float):

        # Usage

        '''Converts the given HSL color to RGB Color
        Example -> convert.hsl_to_rgb(30, 100, 50) will return (255, 128, 0)'''

        # Main

        if check.hsl(h, s, l) == True:
            r, g, b = tuple((i * 255) for i in colorsys.hls_to_rgb(h / 360, l / 100, s / 100))
            return (round(r), round(g), round(b))
        else:
            validate.hsl(h, s, l)

    # HSV to RGB
            
    def hsv_to_rgb(h: float, s: float, v: float):

        # Usage

        '''Converts the given HSV Color to RGB Color
        Example -> convert.hsv_to_rgb(30, 100, 100) will return (255, 128, 0)'''

        # Main

        if check.hsv(h, s, v) == True:
            r, g, b = tuple((i * 255) for i in colorsys.hsv_to_rgb(h / 360, s / 100, v / 100))
            return (round(r), round(g), round(b))
        else:
            validate.hsv(h, s, v)

    # Hex to RGB

    def hex_to_rgb(hex: str):

        # Usage

        '''Converts the given hex color to RGB Color
        Example -> convert.hex_to_rgb('#FF8000') will return (255, 128, 0)'''

        # Main

        if check.hex(hex) == True:
            if len(hex.lstrip('#')) == 6:
                r, g, b = tuple(int(hex.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))
                return (r, g, b)
            if len(hex.lstrip('#')) == 3:
                r, g, b = tuple(int(hex.lstrip('#')[i] * 2, 16) for i in (0, 1, 2))
                return (r, g, b)
        else:   
            validate.Hex(hex)

    # CMYK to RGB

    def cmyk_to_rgb(c: int, m: int, y: int, k: int):

        # Usage

        '''Converts the given CMYK Color to RGB Color
        Example -> convert.cmyk_to_rgb(0, 50, 100, 0) will return (255, 128, 0)'''

        # Main

        if check.cmyk(c, m, y, k) == True:
            r, g, b = tuple(255 - (min(1, i/100 * (1 - k/100) + k/100) * 255) for i in (c, m, y))
            return (round(r), round(g), round(b))
        else:
            validate.cmyk(c, m, y, k)

    # RGB to HSL

    def rgb_to_hsl(r: int, g: int, b: int):

        # Usage

        '''Converts the given RGB Color to HSL Color
        Example -> convert.rgb_to_hsl(255, 128, 0) will return (30, 100, 50)'''

        # Main
        
        if check.rgb(r, g, b) == True:
            h = 360 * colorsys.rgb_to_hls(r / 255, g / 255, b / 255)[0]
            s = 100 * colorsys.rgb_to_hls(r / 255, g / 255, b / 255)[2]
            l = 100 * colorsys.rgb_to_hls(r / 255, g / 255, b / 255)[1]
            return (h, s, l)
        else:
            validate.rgb(r, g, b)

    # RGB to HSV

    def rgb_to_hsv(r: int, g: int, b: int):

        # Usage

        '''Converts the given RGB Color to HSV Color
        Example -> convert.rgb_to_hsv(255, 128, 0) will return (30, 100, 100)'''

        # Main

        if check.rgb(r, g, b) == True:
            h = 360 * colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)[0]
            s = 100 * colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)[1]
            v = 100 * colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)[2]
            return (h, s, v)
        else:
            validate.rgb(r, g, b)

    # RGB to Hex
    
    def rgb_to_hex(r: int, g: int, b: int):

        # Usage

        '''Converts the given RGB Color to Hex Color
        Example -> convert.rgb_to_hex(255, 128, 0) will return ('#FF8000')'''

        # Main

        if check.rgb(r, g, b) == True:
            hex = '#{:02x}{:02x}{:02x}'.format(r, g, b).upper()
            return (hex)
        else:
            validate.rgb(r, g, b)

    # RGB to CMYK

    def rgb_to_cmyk(r: int, g: int, b: int):

        # Usage

        '''Converts the given RGB Color to CNYK Color
        Example -> convert.rgb_to_cmyk(255, 128, 0) will return (0, 50, 100, 0)'''

        # Main

        if check.rgb(r, g, b) == True:
            if (r == 0) and (g == 0) and (b == 0):
                c, m, y, k = (0, 0, 0, 100)
                return(c, m, y, k)
            c, m, y = tuple(100 * (1 - i / 255 - min(1 - r / 255, 1 - g / 255, 1 - b / 255)) for i in (r, g, b))
            k = 100 * min(1 - r / 255, 1 - g / 255, 1 - b / 255)
            return (round(c), round(m), round(y), round(k))
        else:
            validate.rgb(r, g, b)
