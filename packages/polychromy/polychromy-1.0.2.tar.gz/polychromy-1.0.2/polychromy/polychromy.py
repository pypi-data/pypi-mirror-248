import os
import re
import sys
import json
from textlinebreaker import split_line

# Create a class for color
class Color:
    def __init__(self, name, hex, rgb, xterm, fg, bg, alt):

        self.name = name
        self.hex = hex
        self.rgb = rgb
        self.xterm = xterm
        self.fg = fg
        self.bg = bg
        self.alt = alt


# Show example of color
def main():
    show()


# Import colors from json file
def _import_colors():

    data_path = os.path.join(os.path.dirname(__file__), 'data', 'colors.json')
    with open(data_path, 'r') as file:
        json_colors = json.load(file)

    # Create instances of Color class for each color
    colors = {}
    for color_name, color_details in json_colors.items():
        colors[color_name] = Color(
            name=color_name,
            hex=color_details["hex"],
            rgb=color_details["rgb"],
            xterm=color_details["xterm"],
            fg=color_details["fg"],
            bg=color_details["bg"],
            alt=color_details["alt"]
        )

    return colors


# Print a square in the given color with
# name, xterm, hex, and rgb values of the given color 
def show(color_in="", colors = _import_colors()):

    # Check if any argument is passed to the function
    if color_in != "":
        pass
    
    # If no argument is passed to the function it checks if any argument was given launching the program
    # If no argument was given then it uses a random color
    elif len(sys.argv) == 1:
        color_in = colors["Pale Turquoise"].rgb

    # If an argument was given it uses it as the given color
    else:
        color_in = sys.argv[1]

    # Get the details about the given color
    color_name, alt_names, color_x, color_hex, color_rgb, color_fg, color_bg, unknown = _get_color(color_in)

    # Set the text and background colors for the output
    if unknown:
        if unknown == "ANSI":
            rgb_out = color_rgb
            color_rgb = color_x
            color_x = ""
            if color_rgb in (10,40,41,42,44,45,100,104,105):
                text_color = 37
            else:
                text_color = 30
        else:
            rgb_out = color_rgb
            color_rgb = colors["Light Gray"].rgb
            text_color = "255;0;0"

    # Set a complementary color code for the text
    else:
        if color_bg == "0":
            rgb_out = ""
            text_color = "37"
            color_rgb = "0"
        else:
            r,g,b = color_rgb.split(";")
            rgb_out = f"{r},{g},{b}"
            cr = abs(int(r)-255)
            if 100<cr<150:
                cr =  255
            cg = abs(int(g)-255)
            if 100<cg<150:
                cg =  255
            cb = abs(int(b)-255)
            if 100<cb<150:
                cb =  255
            text_color = f"{cr};{cg};{cb}"

    # Create the output text
    text = []
    l = 0
    for line in split_line(f"{color_name}",30,"centre"):
        text.append(line)
        l += 1
    text.append("{:^30}".format(""))
    if alt_names:
        text.append("{:<30}".format(f"Other names: "+ "{:.>17}".format(f" {alt_names}")))
        text.append("{:^30}".format(""))
        l += 2
    if color_fg:
        text.append("{:^30}".format(f"ANSI Color Codes"))
        text.append("{:^30}".format("Foreground: " + "{:.>18}".format(f" {color_fg}")))
        text.append("{:^30}".format("Background: " + "{:.>18}".format(f" {color_bg}")))
        l += 3
    for i in range(7-l):
        text.append("{:^30}".format(""))
    text.append("{:<30}".format(f"Xterm Number: " + "{:.>16}".format(f" {color_x}")))
    text.append("{:^30}".format(f""))
    text.append("{:<30}".format(f"Hex triplet: " + "{:.>17}".format(f" {color_hex}")))
    text.append("{:^30}".format(f""))
    text.append("{:<30}".format(f"sRGB: " + "{:.>24}".format(f" {rgb_out}")))

    # Retrieve terminal width and set up frame size
    adjustment = " " * int(((os.get_terminal_size().columns) - (40)) / 2)
    or_line = "═" * 38
    filling = " " * 38
    side_space = " " * 4

    syscol = f"x{color_x}"
    if color_in == syscol:
        color_rgb = syscol

    # Print color details
    display_menu  = "\n" + adjustment + colorate(f"╔{or_line}╗", text_color, color_rgb) + "\n"
    display_menu  += adjustment + colorate(f"║{filling}║", text_color, color_rgb) + "\n"
    for item in text:
        display_menu  += adjustment + colorate(f"║{side_space + item + side_space}║", text_color, color_rgb) + "\n"
    display_menu  += adjustment + colorate(f"║{filling}║", text_color, color_rgb) + "\n"
    display_menu  += adjustment + colorate(f"╚{or_line}╝", text_color, color_rgb) + "\n"

    print(display_menu)


# This function return a given string with escape codes
# to print it in the given foreground and background colors.
def colorate(txt,fg_col=37,bg_col=0):
    
    # Check validity of the given colors
    fg_color = _valid_color(fg_col)
    bg_color = _valid_color(bg_col, False)
    
    # If foreground color is equal to the reset code
    # Remove foreground color code
    if (fg_color == "\033[0m") and (fg_color != bg_color):
        fg_color = ""

    # Return string with color codes and reset code at the end
    return f"{bg_color}{fg_color}{txt}\033[0m"


# Check validity of color
def _valid_color(color, text=True):
    
    palette = _get_color(color) # [0]=name, [1]=alt_name, [2]=color_x, [3]=color_hex, [4]=color_rgb, [5]=color_fg, [6]=color_bg, [7]=unknown

    if isinstance(color,int):
        color = str(color)
    
    if palette[7]:
        if text:
            return "\033[37m"
        else:
            return "\033[0m"
    elif color==palette[5] or color==palette[6]:
        if text:
            return f"\033[{palette[5]}m"
        else:
            return f"\033[{palette[6]}m"
    elif color[1:] == palette[2]:
        if text:
            return f"\033[38;5;{palette[2]}m"
        else:
            return f"\033[48;5;{palette[2]}m"
    else:
        if text:
            return f"\033[38;2;{palette[4]}m"
        else:
            return f"\033[48;2;{palette[4]}m"


# Get and return details about a given color
def _get_color(color, all_colors = _import_colors()):

    unknown = False

    # Check if the input is a valid ANSI color code.
    if matches := re.search("^([0-9]{1,3})$", str(color)):

        try:
            color_name = next((col_name for col_name, color_obj in all_colors.items() if color_obj.fg == str(color)))
        except:
            try:
                color_name = next((col_name for col_name, color_obj in all_colors.items() if color_obj.bg == str(color)))
            except:
                return _invalid_range()
             
    # Check if the color name is in the list of colors
    elif color.title() in all_colors.keys():
        color_name = color.title()

    # Check if the Xterm Number is valid
    elif matches := re.search("^[xX]([0-9]{1,3})$", color):
        color = int(matches.group(1))
        if 0 <= color < 256:
            color_name = next((col_name for col_name, color_obj in all_colors.items() if color_obj.xterm == str(color)))
        else:
            return _invalid_range()

    # Check if the RGB color code is valid and in the list of colors
    elif matches := re.search("^([0-9]*;[0-9]*;[0-9]*)$", color):

        r,g,b = color.split(";")

        if (0<=int(r)<=255) and (0<=int(g)<=255) and (0<=int(b)<=255):

            try:
                #color_name = list(all_colors.keys())[list(map(lambda x: x['rgb'], all_colors.values())).index(matches.group(1))]
                color_name = next((col_name for col_name, color_obj in all_colors.items() if color_obj.rgb == matches.group(1)))#, None)
            except:
                return _no_name(matches.group(1))
            
        # Return an error message for an invalid color code
        else:
            return _invalid_range()
                
    # Check if the HEX color code is valid and in the list of colors
    elif matches := re.search("^(#[0-9A-Za-z]{6})$", color):
        color = matches.group(1).upper()
        try:
            #color_name = list(all_colors.keys())[list(map(lambda x: x['hex'], all_colors.values(color))).index()]
            color_name = next((col_name for col_name, color_obj in all_colors.items() if color_obj.hex == color))#, None)
        except:
            if matches := re.search("^(#[0-9A-F]{6})$", color):
                return _no_name(matches.group(1))
            
            # Return an error message for an invalid color range
            else:
                return _invalid_range()

    # Return an error message for an unknown color name
    else:
        name = f"Color '{color.title()}' Unknown"
        alt_name = ""
        color_x = "???"
        color_hex = "#??????"
        color_rgb = "???,???,???"
        color_fg = ""
        color_bg = ""
        unknown = True
        return name, alt_name, color_x, color_hex, color_rgb, color_fg, color_bg, unknown

    name = color_name
    
    # Get alternative names
    alt_name = all_colors[color_name].alt

    # Get the xterm, HEX, and RGB values of the given color
    color_x =  all_colors[color_name].xterm
    color_hex = all_colors[color_name].hex
    color_rgb = all_colors[color_name].rgb
    color_fg = all_colors[color_name].fg
    color_bg = all_colors[color_name].bg

    return name, alt_name, color_x, color_hex, color_rgb, color_fg, color_bg, unknown


# Return a window message for a non recorded valid color
def _no_name(color):
    name = "Name Unknown"
    
    try:
        r,g,b = color.split(";")
    except:
        r = int(color[1:3],16)
        g = int(color[3:5],16)
        b = int(color[5:7],16)

    alt_name = ""
    color_x = ""
    color_hex = f"#{hex(int(r))[2:].zfill(2)}{hex(int(g))[2:].zfill(2)}{hex(int(b))[2:].zfill(2)}"
    color_rgb = f"{r};{g};{b}"
    color_fg = None
    color_bg = None
    
    return name, alt_name, color_x, color_hex, color_rgb, color_fg, color_bg, False


# Return a window message for an invalide color range
def _invalid_range():
    name = "Invalid Color Range!"
    alt_name = "0, 30-37, 40-47, 90-97, 100-107"
    color_x = "0-255"
    color_hex = "#000000-FFFFFF"
    color_rgb = "0;0;0-255;255;255"
    color_fg = None
    color_bg = None
    
    return name, alt_name, color_x, color_hex, color_rgb, color_fg, color_bg, True


if __name__ == "__main__":
    main()
