# Cursor controls

class cursor:

    # Up

    def up(cells: int):

        # Usage

        '''Moves the cursor upwards by the number of cells given
        Example -> control.cursor.up(1)
        To move the cursor upward by 1 cell'''

        # Main

        if cells > -1:
            return '\033[' + str(cells) + 'A'
        else:
            raise ValueError('Number of cells must be a positive integer')

    # Down
            
    def down(cells: int):

        # Usage

        '''Moves the cursor downwards by the number of cells given
        Example -> control.cursor.down(1)
        To move the cursor downward by 1 cell'''

        # Main

        if cells > -1:
            return '\033[' + str(cells) + 'B'
        else:
            raise ValueError('Number of cells must be a positive integer')

    # Forward
  
    def forward(cells: int):
            
        # Usage
        
        '''Moves the cursor forwards by the number of cells given
        Example -> control.cursor.forward(1)
        To move cursor forward by 1 cell.'''

        # Main

        if cells > -1:
            return '\033[' + str(cells) + 'C'
        else:
            raise ValueError('Number of cells must be a positive integer')

    # Backward

    def backward(cells: int):
            
        # Usage
        
        '''Moves the cursor backwards by the number of cells given
        Example -> Control.Cursor.Backward(1)
        To move cursor backward by 1 cell'''

        # Main

        if cells > -1:
            return '\033[' + str(cells) + 'D'
        else:
            raise ValueError('Number of cells must be a positive integer')

    # NextLine

    def nextline(lines: int):
            
        # Usage
        
        '''Moves the cursor down by the number of lines given
        Example -> control.cursor.nextline(1)
        To move cursor down by 1 line'''

        # Main
        
        if lines > -1:
            return '\033[' + str(lines) + 'E'
        else:
            raise ValueError('Number of lines must be a positive integer')

    # PreviousLine

    def previousline(lines: int):
            
        # Usage

        '''Moves the cursor up by the number of lines given
        Example -> control.cursor.previousline(1)
        To move cursor up by 1 line'''

        # Main

        if lines > -1:
            return '\033[' + str(lines) + 'F'
        else:
            raise ValueError('Number of lines must be a positive integer')

    # HorizontalAbsolute

    def horizontalabsolute(column: int):

        # Usage

        '''Moves the cursor to the given column
        Example -> control.cursor.horizontalabsolute(1)
        To move cursor to the first column'''

        # Main

        if column > -1: 
            return '\033[' + str(column) + 'G'
        else:
            raise ValueError('Number of column must be a positive integer')

    # Position

    def position(row: int, column: int):
            
        # Usage

        '''Moves the cursor to the intersection of the given row and the column
        Example -> control.cursor.position(5, 5)
        To move cursor to the intersection of the fifth row and the fifth column'''

        # Main

        if row > -1 and column > -1:
            return '\033[' + str(row) + ';' + str(column) + 'H'
        else:
            raise ValueError('Number of row and column must be a positive integer')
            
# Erasing Controls

class clear:

    # Screen

    def screen(mode: int):
            
        # Usage

        '''Clears a part of the screen as per the given mode
        Mode 0 - The screen is cleared from the cursor to end of the screen
        Mode 1 - The screen is cleared from the cursor to beginning of the screen
        Mode 2 - Entire screen is cleared and the cursor moves to the upper left
        Mode 3 - Screen is cleared and all lines saved in ScrollBack buffer are deleted'''

        # Main

        if mode in range(0,3):
            return '\033[' + str(mode) + 'J'
        else:
            raise ValueError('Mode must be in numbers 0, 1, 2 and 3')

    # Line

    def line(mode: int):
            
        # Usage

        '''Clears a part of the line as per the given mode
        Mode 0 - The line is cleared from the cursor to end of the line
        Mode 1 - The line is cleared from the cursor to beginning of the line
        Mode 2 - Entire line is cleared but cursor position does not change'''

        # Main

        if mode in range(0,2):
            return '\033[' + str(mode) + 'K'
        else:
            raise ValueError('Mode must be in numbers 0, 1 and 2')

# Scrolling Controls

class scroll:

    # Up

    def up(lines: int):
            
        # Usage

        '''Scrolls the whole page up by the number of lines
        New lines are added at the bottom
        Example -> control.scroll.up(1)
        To move cursor up by the first line'''

        # Main

        if lines > -1:
            return '\033[' + str(lines) + 'S'
        else:
            raise ValueError('Number of lines must be a positive integer')

    # Down

    def down(lines: int):
            
        # Usage

        '''Scrolls the whole page down by the number of lines
        New lines are added at The top
        Example -> control.scroll.down(1)
        To move cursor down by the first line'''

        # Main

        if lines > -1:
            return '\033[' + str(lines) + 'T'
        else:
            raise ValueError('Number of lines must be a positive integer')
