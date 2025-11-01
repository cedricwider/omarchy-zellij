#!/usr/bin/env python3
import sys
import re

def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def format_rgb(rgb):
    """Format RGB tuple as space-separated string"""
    return f"{rgb[0]} {rgb[1]} {rgb[2]}"

def parse_kitty_conf(file_path):
    """Parse kitty.conf file and extract colors"""
    colors = {}
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # Match foreground/background
            if line.startswith('foreground'):
                colors['fg'] = hex_to_rgb(line.split()[-1])
            elif line.startswith('background'):
                colors['bg'] = hex_to_rgb(line.split()[-1])
            # Match color0-color15
            elif match := re.match(r'color(\d+)\s+#?([0-9A-Fa-f]{6})', line):
                num = int(match.group(1))
                rgb = hex_to_rgb(match.group(2))
                if num == 0:
                    colors['black'] = rgb
                elif num == 1:
                    colors['red'] = rgb
                elif num == 2:
                    colors['green'] = rgb
                elif num == 3:
                    colors['yellow'] = rgb
                elif num == 4:
                    colors['blue'] = rgb
                elif num == 5:
                    colors['magenta'] = rgb
                elif num == 6:
                    colors['cyan'] = rgb
                elif num == 7:
                    colors['white'] = rgb
                elif num == 8:
                    colors['bright_black'] = rgb
                elif num == 11:
                    colors['bright_yellow'] = rgb
                elif num == 9:
                    colors['bright_red'] = rgb
                elif num == 14:
                    colors['bright_cyan'] = rgb
                elif num == 10:
                    colors['bright_green'] = rgb
                elif num == 12:
                    colors['bright_blue'] = rgb
    
    return colors

def generate_zellij_theme(theme_name, colors):
    """Generate zellij theme KDL file content"""
    fg = format_rgb(colors.get('fg', (255, 255, 255)))
    bg = format_rgb(colors.get('bg', (0, 0, 0)))
    red = format_rgb(colors.get('red', (255, 0, 0)))
    green = format_rgb(colors.get('green', (0, 255, 0)))
    yellow = format_rgb(colors.get('yellow', (255, 255, 0)))
    blue = format_rgb(colors.get('blue', (0, 0, 255)))
    magenta = format_rgb(colors.get('magenta', (255, 0, 255)))
    cyan = format_rgb(colors.get('cyan', (0, 255, 255)))
    black = format_rgb(colors.get('black', (0, 0, 0)))
    white = format_rgb(colors.get('white', (255, 255, 255)))
    bright_black = format_rgb(colors.get('bright_black', colors.get('black', (50, 50, 50))))
    
    return f"""themes {{
    {theme_name} {{
        // Basic UI text components
        text_unselected {{
            base {fg}
            background {bg}
            emphasis_0 {cyan}
            emphasis_1 {white}
            emphasis_2 {green}
            emphasis_3 {yellow}
        }}
        
        text_selected {{
            base {bg}
            background {fg}
            emphasis_0 {cyan}
            emphasis_1 {white}
            emphasis_2 {green}
            emphasis_3 {yellow}
        }}
        
        // Ribbon components (tabs, status bar sections)
        ribbon_unselected {{
            base {fg}
            background {bright_black}
            emphasis_0 {green}
            emphasis_1 {blue}
            emphasis_2 {cyan}
            emphasis_3 {magenta}
        }}
        
        ribbon_selected {{
            base {bg}
            background {fg}
            emphasis_0 {red}
            emphasis_1 {green}
            emphasis_2 {cyan}
            emphasis_3 {yellow}
        }}
        
        // Table components
        table_title {{
            base {yellow}
            background {bg}
            emphasis_0 {cyan}
            emphasis_1 {white}
            emphasis_2 {green}
            emphasis_3 {red}
        }}
        
        table_cell_unselected {{
            base {fg}
            background {bg}
            emphasis_0 {blue}
            emphasis_1 {green}
            emphasis_2 {cyan}
            emphasis_3 {magenta}
        }}
        
        table_cell_selected {{
            base {bg}
            background {green}
            emphasis_0 {white}
            emphasis_1 {yellow}
            emphasis_2 {cyan}
            emphasis_3 {red}
        }}
        
        // List components
        list_unselected {{
            base {fg}
            background {bg}
            emphasis_0 {green}
            emphasis_1 {cyan}
            emphasis_2 {blue}
            emphasis_3 {magenta}
        }}
        
        list_selected {{
            base {bg}
            background {cyan}
            emphasis_0 {white}
            emphasis_1 {yellow}
            emphasis_2 {green}
            emphasis_3 {red}
        }}
        
        // Frame components (pane borders)
        frame_unselected {{
            base {bright_black}
            background {bg}
            emphasis_0 {green}
            emphasis_1 {cyan}
            emphasis_2 {blue}
            emphasis_3 {fg}
        }}
        
        frame_selected {{
            base {cyan}
            background {bg}
            emphasis_0 {yellow}
            emphasis_1 {white}
            emphasis_2 {green}
            emphasis_3 {red}
        }}
        
        frame_highlight {{
            base {yellow}
            background {bg}
            emphasis_0 {cyan}
            emphasis_1 {white}
            emphasis_2 {green}
            emphasis_3 {red}
        }}
        
        // Exit code indicators
        exit_code_success {{
            base {green}
            background {bg}
            emphasis_0 0 0 0
            emphasis_1 0 0 0
            emphasis_2 0 0 0
            emphasis_3 0 0 0
        }}
        
        exit_code_error {{
            base {red}
            background {bg}
            emphasis_0 0 0 0
            emphasis_1 0 0 0
            emphasis_2 0 0 0
            emphasis_3 0 0 0
        }}
        
        // Multiplayer user colors
        multiplayer_user_colors {{
            player_1 {cyan}
            player_2 {green}
            player_3 {yellow}
            player_4 {magenta}
            player_5 {blue}
            player_6 {red}
            player_7 {format_rgb(colors.get('bright_blue', colors.get('blue', (100, 100, 255))))}
            player_8 {format_rgb(colors.get('bright_cyan', colors.get('cyan', (100, 255, 255))))}
            player_9 {format_rgb(colors.get('bright_green', colors.get('green', (100, 255, 100))))}
            player_10 {fg}
        }}
    }}
}}
"""

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: convert_theme.py <theme_name> <kitty.conf_path>")
        sys.exit(1)
    
    theme_name = sys.argv[1]
    kitty_conf_path = sys.argv[2]
    
    colors = parse_kitty_conf(kitty_conf_path)
    print(generate_zellij_theme(theme_name, colors))
