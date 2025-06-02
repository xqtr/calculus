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

NAME="Calculus"
VER="1.0.1"
OLD=0
MAX_HISTORY=100
readline.set_history_length(MAX_HISTORY)

# --- Tab Completion Setup ---
COMMANDS = [
    'sin', 'cos', 'tan', 'sqrt', 'curt', 'log2', 'log', 'log10', 'exp', 'radians', 'degrees',
    'oct', 'crc32', 'md5', 'sha256', 'px2cm', 'cm2px', 'dpi_presets', 'now','leap','date','time'
    'shl', 'shr', 'len','length', 'repeat', 'wavelength', 'base64','decodebase64',
    'hex2rgb', 'rgb2hex', 'rgb2hsl', 'hsl2rgb', 'roman', 'weekday','random',
    'convert','res','tau','phi', 'tool','command','operation','convert','pixel',
    'quit', 'exit', 'help','big','clear','monthdays','addpercent','subpercent'
]

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

def showhelp(cat):
    print('---- ')
    if cat == 'pixel':
        print('  Pixel Conversion')
        print('    Functions')
        print('      px2cm(pixels[,resolution]) : convert pixels to cm')
        print('      cm2px(pixels[,resolution]) : convert cm to pixels')
        print('      dpi_presets')
        print('    Examples:')
        print('    ')
        print('      px2cm(300)                     # 300px to cm (default 96 DPI)')
        print("      px2cm(300, 'print')            # 300px to cm at 300 DPI")
        print('      px2cm(500, 144)                # Custom DPI value')
        print('      cm2px(10)                      # 10cm to pixels (96 DPI)')
        print("      cm2px(10, 'retina')            # 10cm at 220 DPI")
        print('      dpi_presets()                  # Show available presets')
    
    elif cat == 'convert':
        print('  Functions:')
        print('             roman : convert integer to roman string')
        print('  Conversions:')
        print('    Supported Units:')
        print('    Length: m, km, cm, mm, mi, yd, ft, in')
        print('    Weight: kg, g, mg, lb, oz')
        print('    Temperature: C, F, K')
        print('    Time: s, min, hr, day')
        print('    Digital: b, kb, mb, gb, tb')
        print('')    
        print('    Examples:')
        print('    10kg in lb, 100c to f, 0k to c, 1mb to kb, 1day to hour')
    elif cat == 'operation':
        print('  Supported Operations:')
        print('           +,-,*,/ : add, subtrack, multiply, devide (float)')
        print('                // : integer devision')
        print('              ^,** : power')
        print('                 % : percentage ex. 100*10%')
        print('               sin : sine')
        print('               cos : cosine')
        print('               tan : tangent')
        print('              sqrt : square root')
        print('                   : for other roots do: number ^ (1/Nth _root)')
        print('                   : ex. cubic root of 27: 27 ^ (1/3)')
        print('    log,log2,log10 : logarithms')
        print('               exp : returns E raised to the power of x')
        print('           radians : converts a degree value into radians')
        print('           degrees : converts an angle from radians to degrees')
        print('                pi : pi constant')
        print('               phi : golden ratio')    
        print("                 e : euler's number")
        print('               res : previous result')
        print('               oct : return octal number')
        print('            random : return a random integer from 0 to parameter')
        print('        addpercent : adds the percentage value to number')
        print('        subpercent : subtracts the percentage value to number')
    elif cat == 'command':
        print('  Commands:')
        print('      cl,clear,cls : clear screen')
        print('              c,ce : clear stored value')
        print('     quit,exit,q,x : exit program')
    elif cat == 'time':
        print('  Time:')
        print('    Functions:')
        print('                time : returns current time')
        print('                date : returns current date')
        print('                leap : checks if given year is leap')
        print('             weekday : returns name of given date')
        print('           monthdays : returns number of days in month')
        print('  Examples:')
        print("    weekday(date)")
        print("    weekday('2025-05-14')")
        print("    leap(2025)")
        print("    monthdays('2025-10-22')")
    elif cat == 'tool':
        print('  Tools:')
        print('    Functions:')
        print('    crc32,md5,sha256 : return hash number of string')
        print('                     : ex. crc32("hello")')
        print('             shr,shl : shift bitwise left or right')
        print('                     : ex. shl(4, 2)')
        print('      repeat(char,n) : repeat char/string n times')
        print('         len(string) : returns length of string')
        print('    hex2rgb(#FFFFFF) : hex to RGB value')
        print('              base64 : encode string to base64')
        print('        decodebase64 : decode string to base64')
        print('    rgb2hex(byte,byte,byte) : RGB to HEX value')
        print('    rgb2hsl(byte,byte,byte) : RGB to HSL value')
        print('    hsl2rgb(byte,byte,byte) : HSL to RGB value')
        print('  Examples:')
        print("    repeat('*', 40)  # Create a visual separator")
        print("    repeat('na', 10) + ' Batman!'  # Fun with strings")
        print("    repeat(hex(16), 5)  # Combine with other functions")
        print("    hex2rgb('#FF5733')")
        print("    rgb2hsl(0, 255, 0)")
        print("    hsl2rgb(240, 100, 50)")
    else:
        print(f'{NAME} v{VER}')
        print('  Type...')
        print('         help tool : for tool commands')
        print('      help convert : for conversion functions')
        print('    help operation : for mathematical operations')
        print('      help command : for program commands')
        print('        help pixel : pixel conversion functions')
        print('         help time : time/calendar functions')
        print(' ')
        print('Up/Down keys navigate through command history')
        print('Press TAB for command auto-completion')
        print('Use syntax like: +10, *2 etc. to calculate with last result')
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
            raise ValueError(f"Unsupported character: '{char}'")

    return '\n'.join(lines)

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
        raise ValueError(f"Unsupported unit conversion: {from_unit} to {to_unit}")

def parse_conversion(expr):
    """Parse conversion expressions like '5km to mi'."""
    parts = re.split(r'\s+(?:to|in)\s+', expr, flags=re.IGNORECASE)
    if len(parts) != 2:
        raise ValueError("Use format '5km to mi' or '5km in mi'")
    
    # Extract value and from unit
    value_part = parts[0]
    match = re.match(r'([-+]?\d*\.?\d+)\s*([a-zA-Z]+)', value_part)
    if not match:
        raise ValueError("Could not parse value and unit")
    
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
            raise ValueError("Unknown unit. Use 'Hz' or 'MHz'.")
    elif isinstance(freq_input, (int, float)):
        # Assume Hz if it's a big number, MHz if it's small
        if freq_input > 1e6:
            freq_hz = freq_input
        else:
            freq_hz = freq_input * 1e6
    else:
        raise TypeError("Input must be a string, int, or float.")

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
        raise ValueError("max_num must be a positive integer")
    
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
        raise ValueError("Repeat count must be a non-negative integer")
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
        raise ValueError("Hex color must be 6 characters long")
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

def evaluate_expression(expr):
    """Evaluate a mathematical expression safely."""
    global OLD
    try:
         # Try unit conversion first (e.g., "5km to mi")
        if re.search(r'\s+(?:to|in)\s+', expr, flags=re.IGNORECASE):
            return parse_conversion(expr)
        
        if expr.lower().startswith('help'):
            s = expr.lower().strip().split()
            if len(s) == 1:
                showhelp('')
                return OLD
            else:
                if s[1].startswith('tool'):
                    showhelp('tool')
                    return OLD
                elif s[1].startswith('convert'):
                    showhelp('convert')
                    return OLD
                elif s[1].startswith('command'):
                    showhelp('command')
                    return OLD
                elif s[1].startswith('operation'):
                    showhelp('operation')
                    return OLD
                elif s[1].startswith('pixel'):
                    showhelp('pixel')
                    return OLD
                else:
                    showhelp('')
                    return OLD
            
        if expr.lower() in ['c','ce']:
            OLD = 0
            result = 0
            return result
        elif expr.lower() in ['cls','clear','cl']:
            os.system('clear')
            return OLD
        
        # if line begins with a calc, add the old number
        expr = expr.replace(" ","")
        if expr[:1] in ['+','-','*','/','^']:
            expr = str(OLD) + expr
        
        # Replace common constants and functions
        expr = expr.replace('^', '**')
        expr = expr.replace('%', '*0.01')
       
        # Check for invalid characters for security

        if not re.match(r'^[\d\s+\-*/.()^%&|~<>#xboabcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ,_"\']+$', expr):
            raise ValueError("Expression contains invalid characters")
            
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
            'time' : time.strftime('%H:%M', time.localtime()),
            'leap' : is_leap,
            'weekday' : weekday_name,
            'random' : random_int,
            'monthdays' : monthdays,
            'addpercent' : addpercent,
            'subpercent' : subpercent
        })
        
        print('# '+expr)
        return result
    except Exception as e:
        return f"Error: {str(e)}"
        
def format_result(result):
    """Enhanced output formatting with color and prime support."""
    global OLD
    try:
        output = []
        
        
        if isinstance(result, str):
            return f"{result}"
        
        # Handle color tuples
        if isinstance(result, tuple) and len(result) in (3, 4):
            if all(isinstance(x, int) and 0 <= x <= 255 for x in result[:3]):
                if len(result) == 3:  # RGB/HSL
                    output.append(f"RGB: {result}")
                    output.append(f"Hex: {rgb2hex(*result)}")
                    hsl = rgb2hsl(*result)
                    output.append(f"HSL: {hsl}°")
                return '\n'.join(output)
        
        # Handle numbers
        if isinstance(result, (int, float)):
            is_integer = isinstance(result, int) or result.is_integer()
            output.append(f"= {result}")
            OLD=result
            if is_integer:
                num = int(result)
                output.extend([
                    f"| {hex(num)}",
                    f"| {bin(num)}",
                    f"| {oct(num)}",
                    f"| Bits {num.bit_length()}"
                ])
            else:
                output.append("")
        
        return ' '.join(output) if output else str(result)
    except Exception as e:
        return f"Format error: {str(e)}"

def main():
    old=0
    if len(sys.argv) > 1:
        # Evaluate expression from command line argument
        expr = ' '.join(sys.argv[1:])
        result = evaluate_expression(expr)
        print(f"{expr} = {result}")
    else:
        # Interactive mode
        readline.set_completer_delims(' \t\n')  # Don't break completion on these
        print("'help' for help,  'quit' to exit")
        print("String values must be quoted with ' or \"")
        while True:
            try:
                expr = input("> ").strip()
                if expr.lower() in ('quit', 'exit', 'q', 'bye', 'stop', 'x'):
                    break
                if expr:
                    result = evaluate_expression(expr)
                    print(format_result(result))
            except (KeyboardInterrupt, EOFError):
                print("\nExiting...")
                break
            except Exception as e:
                print(f"Error: {str(e)}")

if __name__ == "__main__":
    # Initialize tab completion
    readline.parse_and_bind("tab: complete")
    readline.set_completer(completer)
    main()
