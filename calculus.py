#!/usr/bin/env python3
#!/usr/bin/env python3

import sys
import os
import re
import math
import readline
import hashlib
import binascii
import colorsys
import calendar
import base64
import time
import datetime
import random
import argparse

NAME="Calculus"
VER="1.0.2"
OLD=0
MAX_HISTORY=100
readline.set_history_length(MAX_HISTORY)
ECHO = 1
STORE = {}

COLORS = {
    'black': '\033[30m',
    'red': '\033[31m',
    'green': '\033[32m',
    'yellow': '\033[33m',
    'blue': '\033[34m',
    'magenta': '\033[35m',
    'cyan': '\033[36m',
    'white': '\033[37m',
    'reset': '\033[0m',
    'bold': '\033[1m',
    'underline': '\033[4m'
}

NOCOLORS = {
    'black': '',
    'red': '',
    'green': '',
    'yellow': '',
    'blue': '',
    'magenta': '',
    'cyan': '',
    'white': '',
    'reset': '\033[0m',
    'bold': '\033[1m',
    'underline': '\033[4m'
}

CL = {}

# --- Tab Completion Setup ---
STRING_FUNCTIONS = [
        'md5', 'sha256', 'crc32', 'hex2rgb', 'rgb2hex', 
        'rgb2hsl', 'hsl2rgb', 'len', 'length', 'repeat',
        'base64', 'decodebase64', 'weekday', 'monthdays','ask',
        'ss','rs','store','restore','file','print','write'
    ]
COMMANDS = [
    'sin', 'cos', 'tan', 'sqrt', 'curt', 'log2', 'log', 'log10', 'exp', 'radians', 'degrees',
    'oct', 'px2cm', 'cm2px', 'dpi_presets', 'now','leap','date','time'
    'shl', 'shr', 'wavelength', 'ss','rs',
    'roman', 'random', 'var', 'remove','list','ls',
    'convert','res','tau','phi', 'tool','command','operation','convert','pixel',
    'quit', 'exit', 'help','big','clear', 'addpercent','subpercent','prime'
]

def getfiles():
    files = []
    for filename in os.listdir('.'):
        if filename.endswith('.calc'):
            files.append(filename)
    return files

COMMANDS.extend(STRING_FUNCTIONS)
COMMANDS.extend(getfiles())

# store values to variables

def ask(prompt="", var_type="auto"):
    """
    Get user input with type conversion and validation
    
    Args:
        prompt (str): Message to display
        var_type (str): 'auto', 'int', 'float', or 'str'
    
    Returns:
        User input converted to specified type
    
    Usage:
        x = input("Enter a number: ")
        y = input("Enter text: ", "str")
        z = input("Enter integer: ", "int")
    """
    
    try:
        # Get input
        user_input = input(prompt)
        
        # Handle empty input
        if not user_input.strip():
            raise ValueError("Input cannot be empty")
        
        # Automatic type detection
        if var_type == "auto":
            if user_input.isdigit():
                return int(user_input)
            try:
                return float(user_input)
            except ValueError:
                return str(user_input)
        
        # Specific type conversion
        elif var_type == "int":
            return int(user_input)
        elif var_type == "float":
            return float(user_input)
        elif var_type == "str":
            return str(user_input)
        else:
            raise ValueError(f"Unknown type: {var_type}")
            
    except ValueError as e:
        print(f"Invalid input: {e}")
        if var_type != "auto":
            print(f"Expected type: {var_type}")
                
def ss(k):
    """ Store last result to a variable """
    global OLD,STORE,ECHO
    STORE[k]=OLD
    if ECHO:
        print(f"{CL['white']}{k} {CL['yellow']}= {CL['green']}{OLD}")
    return OLD
    
def rs(k):
    """ restores value from stored position """
    #global STORE, OLD
    if k in STORE:
        a = STORE[k]
        return a
    else:
        return None
        
def show_all():
    #global STORE
    """Display all stored values"""
    return '\n'.join(
        f"{var}: {val:.6g}" if isinstance(val, float) else f"{var}: {val}"
        for var, val in sorted(STORE.items())
        if not var.startswith('_')  # Skip internal variables
        )

def clearvars():
    """ clear all stored variables """
    global STORE
    STORE.clear()
    print(f"{CL['bold']}{CL['yellow']}All variables cleared.{CL['reset']}")

def auto_quote(expr):
    """
    Automatically adds quotes to unquoted string arguments for specific functions
    """
    # List of functions that expect string arguments
    
    
    # Find all function calls in the expression
    for func in STRING_FUNCTIONS:
        pattern = re.compile(rf'{func}\(([^"\'][^),]*)\)')
        matches = pattern.findall(expr)
        for arg in matches:
            # Don't quote if it's already quoted or a number/variable
            if not (arg.startswith(('"', "'")) or 
                    arg.replace('.','',1).isdigit() or
                    arg in COMMANDS or
                    any(op in arg for op in '+-*/%^()')):
                expr = expr.replace(f'{func}({arg})', f'{func}("{arg}")')
    return expr

def completer(text, state):
    """Auto-complete function for readline."""
    options = [cmd for cmd in COMMANDS if cmd.startswith(text.lower())]
    if state < len(options):
        return options[state]
    return None
    
# Common DPI values (dots per inch)
DPI_PRESETS = {
    'screen': 96,         # Standard screen DPI
    'print': 300,         # Standard print DPI
    'retina': 220,        # High-DPI displays
    'photo': 254          # Photo printing standard
}

# --- Unit Conversion Constants ---
CONVERSIONS = {
    # Length
    'm': 1.0,
    'km': 1000.0,
    'cm': 0.01,
    'mm': 0.001,
    'mi': 1609.344,
    'yd': 0.9144,
    'ft': 0.3048,
    'in': 0.0254,
    
    # Weight
    'kg': 1.0,
    'g': 0.001,
    'mg': 0.000001,
    'lb': 0.453592,
    'oz': 0.0283495,
    
    # Temperature
    'c': ('c', 'k', lambda x: x + 273.15, lambda x: x - 273.15),
    'f': ('f', 'c', lambda x: (x - 32) * 5/9, lambda x: x * 9/5 + 32),
    'k': ('k', 'c', lambda x: x - 273.15, lambda x: x + 273.15),
    
    # Time
    'sec': 1.0,
    'min': 60.0,
    'hour': 3600.0,
    'day': 86400.0,
    
    # Digital Storage
    'b': 1.0,
    'kb': 1024.0,
    'mb': 1024**2,
    'gb': 1024**3,
    'tb': 1024**4,
}

def pline(cmd,text,pad=6):
    print(f"{' '*pad}{CL['bold']}{CL['white']}{cmd.strip().ljust(25)} {CL['cyan']}: {CL['reset']}{CL['white']}{text.strip().ljust(40)}")

def title(text,color='yellow',pad=4):
    print(f"{' '*pad}{CL['bold']}{CL[color]}{text.strip()}{CL['reset']}")

def showhelp(cat):
    print('---- ')
    if cat == 'pixel':
        title('Pixel Conversion',pad=2)
        title('Functions')
        pline('px2cm(pixels[,resolution])','convert pixels to cm')
        pline('cm2px(pixels[,resolution])','convert cm to pixels')
        pline('dpi_presets','show pixel constants')
        title("Examples")
        print('      px2cm(300)                     # 300px to cm (default 96 DPI)')
        print("      px2cm(300, 'print')            # 300px to cm at 300 DPI")
        print('      px2cm(500, 144)                # Custom DPI value')
        print('      cm2px(10)                      # 10cm to pixels (96 DPI)')
        print("      cm2px(10, 'retina')            # 10cm at 220 DPI")
        print('      dpi_presets()                  # Show available presets')
    
    elif cat == 'convert':
        title('Unit conversion functions',pad=2)
        title('  Functions:')
        pline('             roman','convert integer to roman string')
        title('  Conversions:')
        print('    Supported Units:')
        pline('    Length',' m, km, cm, mm, mi, yd, ft, in')
        pline('    Weight',' kg, g, mg, lb, oz')
        pline('    Temperature',' C, F, K')
        pline('    Time',' s, min, hr, day')
        pline('    Digital',' b, kb, mb, gb, tb')
        print('')    
        title('    Examples:')
        print('    10kg in lb, 100c to f, 0k to c, 1mb to kb, 1day to hour')
    elif cat == 'operation':
        title('  Supported Operations:')
        pline('           +,-,*,/ ',' add, subtrack, multiply, devide (float)')
        pline('                // ',' integer devision')
        pline('              ^,** ',' power')
        pline('                 % ',' percentage ex. 100*10%')
        pline('               sin ',' sine')
        pline('               cos ',' cosine')
        pline('               tan ',' tangent')
        pline('              sqrt ',' square root')
        pline('                   ',' for other roots do: number ^ (1/Nth _root)')
        pline('                   ',' ex. cubic root of 27: 27 ^ (1/3)')
        pline('    log,log2,log10 ',' logarithms')
        pline('               exp ',' returns E raised to the power of x')
        pline('           radians ',' converts a degree value into radians')
        pline('           degrees ',' converts an angle from radians to degrees')
        pline('                pi ',' pi constant')
        pline('               phi ',' golden ratio')    
        pline('                 e ',' euler''s number')
        pline('               res ',' previous result')
        pline('               oct ',' return octal number')
        pline('            random ',' return a random integer from 0 to parameter')
        pline('        addpercent ',' adds the percentage value to number')
        pline('        subpercent ',' subtracts the percentage value to number')
        pline('             prime ',' returns 0/1 if number is prime')
    elif cat == 'command':
        title('  Commands:')
        pline('      cl,clear,cls ',' clear screen')
        pline('              c,ce ',' clear stored value')
        pline('         store,ss ',' store value to variable')
        pline('        restore,rs ',' restore value from variable')
        pline('var ',' show all stored variables')
        pline('ls,list ','list .calc files in current dir.')
        pline('             reset ',' clear all stored variables')
        pline('file','execute given file')
        pline('print,write','output given string')
        pline('pause','wait for enter, only for use in files')
        pline('     quit,exit,q,x ',' exit program')
        title('  Examples:')
        print("      file(orthodoxeaster) or file(orthodoxeaster.calc)")
        print("      print('...this variable {x}')")
        print("      store(modulo) or ss(x) or @x")
    elif cat == 'time':
        title('Time',pad=2)
        title('    Functions:')
        pline('                time ',' returns current time')
        pline('                date ',' returns current date')
        pline('                leap ',' checks if given year is leap')
        pline('             weekday ',' returns name of given date')
        pline('           monthdays ',' returns number of days in month')
        pline('                 cal ',' returns month calendar')
        title('  Examples:')
        print("    weekday(date)")
        print("    weekday('2025-05-14')")
        print("    leap(2025)")
        print("    monthdays('2025-10-22')")
        print("    cal() or cal(2025,10)")
    elif cat == 'tool':
        title('Tools',pad=2)
        title('    Functions:')
        pline('    crc32,md5,sha256 ',' return hash number of string')
        pline('                   . ',' ex. crc32("hello")')
        pline('             shr,shl ',' shift bitwise left or right')
        pline('                   . ',' ex. shl(4, 2)')
        pline('      repeat(char,n) ',' repeat char/string n times')
        pline('         len(string) ',' returns length of string')
        pline('    hex2rgb(#FFFFFF) ',' hex to RGB value')
        pline('              base64 ',' encode string to base64')
        pline('        decodebase64 ',' decode string to base64')
        pline('    rgb2hex(byte,byte,byte) ',' RGB to HEX value')
        pline('    rgb2hsl(byte,byte,byte) ',' RGB to HSL value')
        pline('    hsl2rgb(byte,byte,byte) ',' HSL to RGB value')
        title('  Examples:')
        print("    repeat('*', 40)  # Create a visual separator")
        print("    repeat('na', 10) + ' Batman!'  # Fun with strings")
        print("    repeat(hex(16), 5)  # Combine with other functions")
        print("    hex2rgb('#FF5733')")
        print("    rgb2hsl(0, 255, 0)")
        print("    hsl2rgb(240, 100, 50)")
    else:
        print(f'{CL["green"]}{NAME} {CL["cyan"]}v{VER} {CL["reset"]}>github.com/xqtr/calculus')
        title('  Type: ',pad=2)
        pline('         help tool ',' for tool commands')
        pline('      help convert ',' for conversion functions')
        pline('    help operation ',' for mathematical operations')
        pline('      help command ',' for program commands')
        pline('        help pixel ',' pixel conversion functions')
        pline('         help time ',' time/calendar functions')
        print(f'{CL["reset"]}')
        print('Up/Down keys navigate through command history')
        print('Press TAB for command auto-completion')
        print('Use syntax like: +10, *2 etc. to calculate with last result')
        print('Quotes for string values are optional ex. hex2rgb(ffaabb) or hex2rgb("ffaabb")')
    print('---- ')
    
def big_numbers(text: str) -> str:
    """Returns a multi-line ASCII representation of digits + '.', '+', and '-' characters."""

    digits = {
        '0': [" @@@ ",
              "@   @",
              "@   @",
              "@   @",
              " @@@ "],
        '1': ["  @  ",
              " @@  ",
              "  @  ",
              "  @  ",
              "@@@@@"],
        '2': [" @@@ ",
              "@   @",
              "   @ ",
              "  @  ",
              "@@@@@"],
        '3': [" @@@ ",
              "    @",
              " @@@ ",
              "    @",
              " @@@ "],
        '4': ["@  @ ",
              "@  @ ",
              "@@@@@",
              "   @ ",
              "   @ "],
        '5': ["@@@@@",
              "@    ",
              "@@@@ ",
              "    @",
              "@@@@ "],
        '6': [" @@@ ",
              "@    ",
              "@@@@ ",
              "@   @",
              " @@@ "],
        '7': ["@@@@@",
              "   @ ",
              "  @  ",
              " @   ",
              "@    "],
        '8': [" @@@ ",
              "@   @",
              " @@@ ",
              "@   @",
              " @@@ "],
        '9': [" @@@ ",
              "@   @",
              " @@@@",
              "    @",
              " @@@ "],
        '.': ["     ",
              "     ",
              "     ",
              "  @@ ",
              "  @@ "],
        '+': ["     ",
              "  @  ",
              " @@@ ",
              "  @  ",
              "     "],
        '-': ["     ",
              "     ",
              " @@@ ",
              "     ",
              "     "]
    }

    lines = ['' for _ in range(5)]

    for char in text:
        if char in digits:
            for i in range(5):
                lines[i] += digits[char][i] + '  '
        else:
            raise ValueError(f"{CL['red']}Unsupported character{CL['reset']}: '{char}'")

    return '\n'.join(lines)
    
def listfiles():
    """
    List all .calc files in current directory with metadata
    
    Returns:
        list: Sorted list of dicts with file info
        Format: {
            'name': filename,
            'size': size in KB,
            'modified': last modified date
        }
    """
    #files = []
    for filename in os.listdir('.'):
        if filename.endswith('.calc'):
            filepath = os.path.join('.', filename)
            stat = os.stat(filepath)
            #files.append({'name': filename,'size': f"{stat.st_size / 1024:.2f} KB",'modified': datetime.datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M')})
            print(f"{filename:<40} {stat.st_size / 1024:>5.2f} KB {datetime.datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M'):>18}")
    
    # Sort by modification time (newest first)
    #return sorted(files, key=lambda x: x['modified'], reverse=True)    

# calendar functions

def is_leap(year):
    """Check leap year"""
    return int(calendar.isleap(year))

def weekday_name(date_str):
    """Get weekday name for date (YYYY-MM-DD)"""
    year, month, day = map(int, date_str.split('-'))
    return str(calendar.day_name[calendar.weekday(year, month, day)])
    
def monthdays(sdate):
    year, month, day = map(int, sdate.split("-"))
    return calendar.monthrange(year, month)[1]
    
def cal(year=None, month=None):
    """
    Display a formatted month calendar.
    
    Args:
        year (int): 4-digit year (default: current year)
        month (int): 1-12 (default: current month)
    
    Returns:
        str: Formatted calendar string
    
    Example:
        >>> print(cal(2023, 8))
        >>> print(cal())  # Current month
    """
    now = datetime.datetime.now()
    year = year if year is not None else now.year
    month = month if month is not None else now.month

    # Validate inputs
    if not (1 <= month <= 12):
        raise ValueError("Month must be 1-12")
    if not (0 < year < 10000):
        raise ValueError("Year must be 1-9999")

    # Generate calendar with custom formatting
    cal_text = calendar.month(year, month)
    
    # Enhanced formatting
    border = "-" * 20
    header = f"{calendar.month_name[month]} {year}".center(20)
    
    return f"\n{border}\n{header}\n{border}\n{cal_text}{border}\n"

# --- Unit Conversion Functions ---

def roman(num):
    """Convert integer to Roman numerals (up to 3999)"""
    val = [1000,900,500,400,100,90,50,40,10,9,5,4,1]
    syb = ["M","CM","D","CD","C","XC","L","XL","X","IX","V","IV","I"]
    roman = ""
    for i in range(len(val)):
        count = num // val[i]
        roman += syb[i] * count
        num -= val[i] * count
    return roman
    
def convert(value, from_unit, to_unit):
    """Handle unit conversions including temperature."""
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()
    
    # Temperature conversion
    if from_unit in ('c', 'f', 'k') and to_unit in ('c', 'f', 'k'):
        if from_unit == to_unit:
            return value
        
        # Convert to Celsius first if needed
        if from_unit != 'c':
            temp_info = CONVERSIONS[from_unit]
            value = temp_info[2](value)
        
        # Convert from Celsius to target
        if to_unit != 'c':
            temp_info = CONVERSIONS[to_unit]
            value = temp_info[3](value)
        
        return value
    
    # Regular conversion
    try:
        return value * (CONVERSIONS[from_unit] / CONVERSIONS[to_unit])
    except KeyError:
        raise ValueError(f"{CL['red']}Unsupported unit conversion{CL['reset']}: {from_unit} to {to_unit}")

def parse_conversion(expr):
    """Parse conversion expressions like '5km to mi'."""
    parts = re.split(r'\s+(?:to|in)\s+', expr, flags=re.IGNORECASE)
    if len(parts) != 2:
        raise ValueError("Use format '5km to mi' or '5km in mi'")
    
    # Extract value and from unit
    value_part = parts[0]
    match = re.match(r'([-+]?\d*\.?\d+)\s*([a-zA-Z]+)', value_part)
    if not match:
        raise ValueError("{CL['red']}Could not parse value and unit{CL['reset']}")
    
    value = float(match.group(1))
    from_unit = match.group(2).lower()
    to_unit = parts[1].lower()
    
    return convert(value, from_unit, to_unit)
    
# frequency functions

def wavelength(freq_input):
    """
    Calculates wavelength (in meters) from a given frequency.

    Accepts:
    - Strings with units: 'MHz', 'Hz'
    - Integers or floats (assumes Hz if >1e6, otherwise MHz)

    Returns:
    - Wavelength in meters (float)
    """

    # Speed of light in m/s
    c = 3e8

    # Parse input
    if isinstance(freq_input, str):
        freq_input = freq_input.strip().lower()
        if 'mhz' in freq_input:
            value = float(freq_input.replace('mhz', '').strip())
            freq_hz = value * 1e6
        elif 'hz' in freq_input:
            value = float(freq_input.replace('hz', '').strip())
            freq_hz = value
        else:
            raise ValueError(f"{CL['red']}Unknown unit. Use 'Hz' or 'MHz'.{CL['reset']}")
    elif isinstance(freq_input, (int, float)):
        # Assume Hz if it's a big number, MHz if it's small
        if freq_input > 1e6:
            freq_hz = freq_input
        else:
            freq_hz = freq_input * 1e6
    else:
        raise TypeError(f"{CL['red']}Input must be a string, int, or float.{CL['reset']}")

    # Calculate wavelength
    wavelength = c / freq_hz
    return f'{wavelength} m'

# --- Pixel Conversion Functions ---
def pixels_to_cm(pixels, dpi='screen'):
    """Convert pixels to centimeters."""
    dpi_value = DPI_PRESETS.get(dpi.lower(), dpi) if isinstance(dpi, str) else dpi
    inches = pixels / float(dpi_value)
    return inches * 2.54  # 1 inch = 2.54 cm

def cm_to_pixels(cm, dpi='screen'):
    """Convert centimeters to pixels."""
    dpi_value = DPI_PRESETS.get(dpi.lower(), dpi) if isinstance(dpi, str) else dpi
    inches = cm / 2.54
    return round(inches * float(dpi_value))

def show_dpi_presets():
    """List available DPI presets."""
    return "\n".join(f"{name}: {dpi} DPI" for name, dpi in DPI_PRESETS.items())

# math functions

def is_prime(n):
    """Check if a number is prime."""
    if n < 2: return 0
    if n == 2: return 1
    if n % 2 == 0: return 0
    for i in range(3, int(n**0.5)+1, 2):
        if n % i == 0:
            return 0
    return 1
    
def curt(data):
    """Cubic root of number"""
    return data ** (1/3)
    
def random_int(max_num):
    """
    Returns a random integer between 1 and max_num (inclusive).
    
    Parameters:
        max_num (int): The maximum value to generate (must be positive)
    
    Returns:
        int: Random number between 1 and max_num
    
    Examples:
        >>> random_int(10)  # Possible output: 7
        >>> random_int(100) # Possible output: 42
    """
    if not isinstance(max_num, int) or max_num < 1:
        raise ValueError(f"{CL['red']}max_num must be a positive integer{CL['reset']}")
    
    return random.randint(1, max_num)
    
def addpercent(val,p):
    try:
        return f'= {val + (val * p / 100)} perc: {val * p / 100}'
    except:
        return -1

def subpercent(val,p):
    try:
        return f'= {val - (val * p / 100)} perc: {val * p / 100}'
    except:
        return -1

# string functions    
def slen(data):
    """Calculate length of string"""
    if isinstance(data, int):
        data = str(data)
    return len(data)
    
def repeat(s, n):
    """Repeat a string or character n times."""
    if not isinstance(n, int) or n < 0:
        raise ValueError(f"{CL['red']}Repeat count must be a non-negative integer{CL['reset']}")
    if not isinstance(s, str):
        s = str(s)
    return s * n
    
# hash functions
def crc32(data):
    """Calculate CRC32 checksum."""
    if isinstance(data, int):
        data = str(data)
    return binascii.crc32(data.encode()) & 0xffffffff

def md5(data):
    """Calculate MD5 hash."""
    if isinstance(data, int):
        data = str(data)
    return hashlib.md5(data.encode()).hexdigest()

def sha256(data):
    """Calculate SHA256 hash."""
    if isinstance(data, int):
        data = str(data)
    return hashlib.sha256(data.encode()).hexdigest()
    
def encode_base64(text):
    return base64.b64encode(text.encode()).decode()

def decode_base64(encoded):
    return base64.b64decode(encoded).decode()
    
# --- Color Conversion Functions ---
def hex2rgb(hex_color):
    """Convert hex color to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    if len(hex_color) != 6:
        raise ValueError(f"{CL['red']}Hex color must be 6 characters long{CL['reset']}")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb2hex(r, g, b):
    """Convert RGB to hex color."""
    return "#{:02x}{:02x}{:02x}".format(r, g, b)

def rgb2hsl(r, g, b):
    """Convert RGB to HSL."""
    r, g, b = r/255, g/255, b/255
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return (round(h*360, 2), round(s*100, 2), round(l*100, 2))

def hsl2rgb(h, s, l):
    """Convert HSL to RGB."""
    r, g, b = colorsys.hls_to_rgb(h/360, l/100, s/100)
    return (round(r*255), round(g*255), round(b*255))
    
def write(*args, **kwargs):
    """
    Enhanced write function with:
    - Variable interpolation
    - Multiple arguments concatenation
    - Color formatting
    - Expression evaluation
    - Error handling
    """
    global CL, STORE, OLD
    
    # Prepare variables
    context = {
        **STORE,
        **CL,
        'res': OLD,
        'date': datetime.datetime.now().strftime('%Y-%m-%d'),
        'time': datetime.datetime.now().strftime('%H:%M:%S'),
        'pi': math.pi,
        'e': math.e,
    }
    
    # Process each argument
    processed_args = []
    for arg in args:
        try:
            # Handle string formatting
            if isinstance(arg, str):
                # First format with stored variables
                formatted = arg.format(**context)
                # Then evaluate expressions in braces
                while True:
                    try:
                        new_formatted = formatted.format(**context)
                        if new_formatted == formatted:
                            break
                        formatted = new_formatted
                    except:
                        break
                processed_args.append(formatted)
            else:
                processed_args.append(str(arg))
        except Exception as e:
            processed_args.append(f"[Error formatting: {str(e)}]")
    
    # Combine all parts
    output = ' '.join(processed_args)
        
    #print(output)
    return output

def evaluate_expression(expr):
    """Evaluate a mathematical expression safely."""
    global OLD,ECHO
    try:
         # Try unit conversion first (e.g., "5km to mi")
        if re.search(r'\s+(?:to|in)\s+', expr, flags=re.IGNORECASE):
            return parse_conversion(expr)
            
        # Auto-quote string arguments before evaluation
        expr = auto_quote(expr)
        expression = expr.lower()        
        if expression.startswith('ask'):
            return ask(expr[5:-2])
        if expression.startswith('@'):
            ss(expr[1:])
            return OLD
        if expr.lower().startswith('!'):
            rs(expr[1:])
            return STORE[expr[1:]]
        
        if expression.startswith('help'):
            s = expression.split()
            if len(s) == 1:
                showhelp('')
                return OLD
            else:
                showhelp(s[1])
                return OLD
        
        if expression.startswith('ls') or expression.startswith('list'):
            listfiles()
            return OLD
        
        if expression.startswith('echo'):
            ECHO = 1
            return OLD
        if expression.startswith('noecho'):
            ECHO = 0
            return OLD
            
        if expression in ['c','ce']:
            OLD = 0
            result = 0
            return result
        elif expression in ['cls','clear','cl']:
            os.system('clear')
            return OLD
        elif expression in ['reset']:
            clearvars()
            return OLD
        
        # if line begins with a calc, add the old number
        #expr = expr.replace(" ","")
        if expr[:1] in ['+','-','*','/','^']:
            expr = str(OLD) + expr
        
        # Replace common constants and functions
        expr = expr.replace('^', '**')
        #expr = expr.replace('%', '*0.01')
       
        # Check for invalid characters for security

        if not re.match(r'^[\d\s+\-*/.()^%&|~<>{}#xboabcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ,_"\']+$', expr):
            raise ValueError(f"{CL['red']}Expression contains invalid characters{CL['reset']}")
            
        # Evaluate the expression
        result = eval(expr, {'__builtins__': None}, {
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'sqrt': math.sqrt,
            'log': math.log,
            'log10': math.log10,
            'log2': math.log2,
            'exp': math.exp,
            'radians': math.radians,
            'degrees': math.degrees,
            'pi': math.pi,
            'phi': 1.61803398874989484820,
            'tau':math.tau,
            'crc32': crc32, 'md5': md5, 'sha256': sha256,
            'oct': oct,
            'curt': curt,
            'res': OLD,
            'shl': lambda x, y: x << y,  # Left shift
            'shr': lambda x, y: x >> y,  # Right shift
            'e': math.e,
            'big': big_numbers(str(OLD)),
            'b': big_numbers(str(OLD)),
            'hex2rgb': hex2rgb,
            'rgb2hex': rgb2hex,
            'rgb2hsl': rgb2hsl,
            'hsl2rgb': hsl2rgb,
            'len': slen,
            'length': slen,
            'repeat': repeat,
            'px2cm': pixels_to_cm,
            'cm2px': cm_to_pixels,
            'dpi_presets': show_dpi_presets(),
            'DPI_SCREEN': 96,
            'DPI_PRINT': 300,
            'wavelength': wavelength,
            'roman': roman,
            'base64': encode_base64,
            'decodebase64': decode_base64,
            'now'  : datetime.datetime.now(),
            'date' : datetime.datetime.now().strftime('%Y-%m-%d'),
            'year' : int(datetime.datetime.now().strftime('%Y')),
            'month' : int(datetime.datetime.now().strftime('%m')),
            'time' : time.strftime('%H:%M', time.localtime()),
            'leap' : is_leap,
            'weekday' : weekday_name,
            'random' : random_int,
            'monthdays' : monthdays,
            'addpercent' : addpercent,
            'subpercent' : subpercent,
            'cal' : cal,
            'prime' : is_prime,
            'ss' : ss,
            'rs' : rs,
            'store' : ss,
            'restore' : rs,
            'var' : show_all(),
            'vars' : show_all(),
            'file' : executefile,
            'write': write,
            'print': write            
        })
        
        #print('# '+expr)
        return result
    except Exception as e:
        return f"{CL['red']}Error{CL['reset']}: {str(e)}"
        
def format_result(result):
    """Enhanced output formatting with color and prime support."""
    global OLD,CL
    try:
        output = []
        
        
        if isinstance(result, str):
            return f"{result}"
        
        # Handle color tuples
        if isinstance(result, tuple) and len(result) in (3, 4):
            if all(isinstance(x, int) and 0 <= x <= 255 for x in result[:3]):
                if len(result) == 3:  # RGB/HSL
                    output.append(f"RGB: {result}")
                    #output.append(f"Hex: {rgb2hex(*result)}")
                    hsl = rgb2hsl(*result)
                    #output.append(f"HSL: {hsl}°")
                return '\n'.join(output)
        
        # Handle numbers
        if isinstance(result, (int, float)):
            is_integer = isinstance(result, int) or result.is_integer()
            OLD=result
            
            output.append(f"{CL['green']}= {CL['white']}{result}")
            if is_integer:
                num = int(result)
                output.extend([
                    f"{CL['reset']}{CL['white']}| {CL['cyan']}{hex(num)}",
                    f"{CL['reset']}{CL['white']}| {CL['bold']}{CL['white']}{bin(num)}",
                    f"{CL['reset']}{CL['white']}| {CL['bold']}{CL['blue']}{oct(num)}",
                    f"{CL['reset']}{CL['white']}| Bits {num.bit_length()}"
                ])
            else:
                output.append("")
        
        return ' '.join(output) if output else str(result)

    except Exception as e:
        return f"{CL['red']}Format error{CL['reset']}: {str(e)}"
        
def process_file(filename, verbose=False):
    """
    Process a file containing one calculator command per line
    
    Args:
        filename (str): Path to the input file
        verbose (bool): Whether to print processing details
        
    Returns:
        dict: Results of all commands with line numbers
    """
    global ECHO
    results = {}
    filename = filename.strip()
    
    if not os.path.isfile(filename):
        if os.path.isfile(filename+'.calc'):
            filename = filename+'.calc'
        else:
            return None
    
    try:
        with open(filename, 'r') as f:
            for line_num, line in enumerate(f, 1):
                # Clean and validate the line
                line = line.strip()
                if not line:
                    continue  # Skip empty lines and comments
                    
                if line.startswith('#'):
                    #print(line)
                    continue
                elif line.startswith('pause'):
                    print("Press [ENTER] to continue...")
                    input()
                    continue
                    
                
                #if verbose and ECHO == 1:
                    #print(f"\nProcessing line {line_num}: {line}")
                 #   print(f"{line_num}: {line}")
                
                # Process the command
                try:
                    result = evaluate_expression(line)
                    formatted = format_result(result)
                    results[line_num] = {
                        'command': line,
                        'result': formatted,
                        'success': True
                    }
                    
                    if verbose and ECHO == 1:
                        print(formatted)
            
                except Exception as e:
                    results[line_num] = {
                        'command': line,
                        'error': str(e),
                        'success': False
                    }
                    
                    if verbose:
                        print(f"Error: {e}")
    
    except FileNotFoundError:
        raise ValueError(f"File not found: {filename}")
    except Exception as e:
        raise ValueError(f"Error processing file: {str(e)}")
    
    return results

def executefile(filename):
    try:
        results = process_file(filename,True)
        errors = {k:v for k,v in results.items() if not v['success']}
        if errors:
            print("\nErrors occurred:")
            for line_num, data in errors.items():
                print(f"Line {line_num}: {data['command']}")
                print(f"  Error: {data['error']}")
        return
    except ValueError as e:
        print(str(e))
        return

def main():
    global CL,ECHO
    args = parse_args()
    
    if args.no_color:
        CL=NOCOLORS
    else:
        CL=COLORS
    
    if args.file:
        try:
            results = process_file(args.file, args.verbose)
            if not args.verbose:
                # Only show errors in non-verbose mode
                errors = {k:v for k,v in results.items() if not v['success']}
                if errors:
                    print("\nErrors occurred:")
                    for line_num, data in errors.items():
                        print(f"Line {line_num}: {data['command']}")
                        print(f"  Error: {data['error']}")
            return
        except ValueError as e:
            print(str(e))
            return
    
    if args.expression:
        expr = ' '.join(args.expression)
        result = evaluate_expression(expr)
        print(format_result(result))
        return
        
    # Interactive mode
    readline.set_completer_delims(' \t\n')  # Don't break completion on these
    print(f"{CL['yellow']}'help' for help,  'quit' to exit{CL['reset']}")
    while True:
        try:
            expr = input(f"{CL['yellow']}>{CL['reset']} ").strip()
            if expr.lower() in ('quit', 'exit', 'q', 'bye', 'stop', 'x'):
                break
            if expr:
                result = evaluate_expression(expr)
                if ECHO: print(format_result(result))
        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")
            break
        except Exception as e:
            print(f"{CL['red']}Error{CL['reset']}:{CL['bold']} {str(e)}{CL['reset']}")
                
def parse_args():
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(description=f'{NAME} v{VER} - Powerful Command-line Calculator')
    parser.add_argument('--no-color', action='store_true', 
                       help='disable colored output')
    parser.add_argument('--file', type=str, help='process commands from a file')
    parser.add_argument('--verbose', action='store_true', help='show detailed processing')
    parser.add_argument('expression', nargs='*', 
                       help='optional expression to evaluate')
    return parser.parse_args()

if __name__ == "__main__":
    # Initialize tab completion
    readline.parse_and_bind("tab: complete")
    readline.set_completer(completer)
    main()
