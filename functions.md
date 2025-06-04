### Pixel Conversion

**Functions**

To use the DPI presets as variables, like: px2cm(200,'retina'), put the variable string inside quotes.

- px2cm(pixels[,resolution])  : convert pixels to cm
- cm2px(pixels[,resolution])  : convert cm to pixels
- dpi_presets                 : show pixel constants

**Examples**

- px2cm(300)                     # 300px to cm (default 96 DPI)
- px2cm(300, 'print')            # 300px to cm at 300 DPI")
- px2cm(500, 144)                # Custom DPI value
- cm2px(10)                      # 10cm to pixels (96 DPI)
- cm2px(10, 'retina            # 10cm at 220 DPI")
- dpi_presets()                  # Show available presets


### Unit conversion functions

**Functions**

- roman(integer)              : convert integer to roman string
- hex(integer)                : convert to hexademical number
- oct(number)                 : convert to octal number

Most conversions are done writing sentences like:
- 10kg in lb
- 100c to f
- 0k to c
- 1mb to kb
- 1day to hour

You can use either 'in' or 'to' in the sentence. For example, both lines below are the same
- 100c to f
- 100c in f

**Supported Units**

- Length: m, km, cm, mm, mi, yd, ft, in
- Weight: kg, g, mg, lb, oz
- Temperature: C, F, K
- Time: s, min, hr, day
- Digital: b, kb, mb, gb, tb
            
**Examples**

10kg in lb, 100c to f, 0k to c, 1mb to kb, 1day to hour
            
                      
### Mathematical Operations

- +,-,*,/                     : add, subtrack, multiply, devide (float)
- //                          : integer division
- ^,**                        : power
- sin(angle)                  : sine
- cos(angle)                  : cosine
- tan(angle)                  : tangent
- sqrt(number)                : square root
- curt(number)                : cubic root                                
- log(number)                 : logarithms
- log2(number)                : logarithms
- log10(number)               : logarithms
- exp(number)                 : returns E raised to the power of number
- radians(number)             : converts a degree value into radians
- degrees(number)             : converts an angle from radians to degrees
- oct(integer)                : return octal number
- random(max_number)          : return a random integer from 0 to parameter
- addpercent(value,percent)   : adds the percentage value to number
                                addpercent(100,24) = 124
- subpercent(value,percent)   : subtracts the percentage value to number
                                subpercent(100,24) = 76
- prime(number)               : returns 0/1 if number is prime                                  
                                  
**Constants**                                  

- pi                          : pi constant 
- phi                         : golden ratio    
- e                           : euler''s number
- res                         : previous result


### Commands

- cl,clear,cls                : clear screen
- c,ce                        : clear stored value
- store(number), ss(number)   : store value to variable
- restore(var), rs(number)    : restore value from variable
                                in an empty line you can also use @name for quickness
- set(name,string)            : use to store strings, USE QUOTES!
- var                         : show all stored variables
- ls,list                     : list .calc files in current dir.
- reset                       : clear all stored variables
- file(filename)              : execute given file, no need for extension
- print(string), write(string): output given string
                                You can use brackets to insert stored variables
                                and also colors. Examples:
                                print("The year is {y}")
                                print("{red}Merry {green}Christmass")

- pause                       : wait for enter, only for use in script files
- quit,exit,q,x               : exit program


          
### Time

**Functions**

In the functions below, always use quote to insert a date string!
You can use bracket, to input variable values to these functions also.
See the examples below.

- time                        : returns current time
- date                        : returns current date
- leap(year)                  : checks if given year is leap returns 1 or 0
- weekday("yyyy-mm-dd")       : returns name of given date
- monthdays("yyyy-mm-dd")     : returns number of days in given month
- cal(yyyy,mm)                : returns month calendar
- adddays("yyyy-mm-dd",num)   : add <num> days and return date
- dayofyear("yyyy-mm-dd")     : returns the number of day of the year
- weeknumber("yyyy-mm-dd")    : returns number of week
- weekend("yyyy-mm-dd")       : return 0/1 if date is on weekend
- date2unix("yyyy-mm-dd")     : convert date string to UNIX timestamp
- unix2date(timestamp)        : convert UNIX time to readable date
- unix2gregorian(timestamp)   : get Gregorian calendar components
- unix2julian(timestamp)      : convert to Julian Date

- daysbetween("yyyy-mm-dd"."yyyy-mm-dd") : returns how many days between to dates

**Examples**

-weekday("2025-05-14")
-leap(2025)
-monthdays("2025-10-22")
-cal() or cal(2025,10)
-weekend("{y}-{m}-{d}") # suppose y,m,d are stored variables 


### Tools

**Functions**

- crc32(string)               : return hash number of string
- md5(string)                 : return hash number of string
- sha256(string)              : return hash number of string
- shr(num,times)              : shift bitwise right
- shl(num,times)              : shift bitwise left
- repeat(char,n)              : repeat char/string n times
- len(string)                 : returns length of string
- hex2rgb(#FFFFFF)            : hex to RGB value
- rgb2hex(byte,byte,byte)     : RGB to HEX value
- rgb2hsl(byte,byte,byte)     : RGB to HSL value
- hsl2rgb(byte,byte,byte)     : HSL to RGB value
- base64(string)              : encode string to base64
- decodebase64(string)        : decode string to base64

**Examples**
- repeat('*', 40)  # Create a visual separator
- set('nana',repeat('na',10))
- print("{nana} Batman")
- repeat(hex(16), 5)  # Combine with other functions
- hex2rgb("#FF5733")
- rgb2hsl(0, 255, 0)")
- hsl2rgb(240, 100, 50)")
- shl(4, 2)
