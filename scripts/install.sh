#!/bin/bash
set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m'

# Configuration
REPO_URL="https://github.com/YOUR_USERNAME/omarchy-zellij"
INSTALL_DIR="$HOME/.config/omarchy-zellij"
HOOK_DEST="$HOME/.local/bin/omarchy-zellij-hook"
OMARCHY_HOOK="$HOME/.config/omarchy/hooks/theme-set"
ZELLIJ_THEMES_DIR="$HOME/.config/zellij/themes"
OMARCHY_THEMES_DIR="$HOME/.config/omarchy/themes"

# Banner
echo -e "${BLUE}${BOLD}"
cat << "EOF"
   ___                           _             
  / _ \ _ __ ___   __ _ _ __ ___| |__  _   _   
 | | | | '_ ` _ \ / _` | '__/ __| '_ \| | | |  
 | |_| | | | | | | (_| | | | (__| | | | |_| |  
  \___/|_| |_| |_|\__,_|_|  \___|_| |_|\__, |  
                                        |___/   
          ____     _ _ _ _       
         |_  /___ | | (_|_)      
          / // -_)| | | | |      
         /___\___||_|_|_| |      
                      |__/       
EOF
echo -e "${NC}"
echo -e "${BOLD}Zellij themes that automatically sync with Omarchy${NC}"
echo

# Check prerequisites
echo -e "${BOLD}Checking prerequisites...${NC}"

if ! command -v zellij &> /dev/null; then
    echo -e "${RED}✗${NC} Zellij is not installed"
    echo "  Install from: https://zellij.dev/"
    exit 1
fi
echo -e "${GREEN}✓${NC} Zellij is installed"

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗${NC} Python 3 is not installed"
    exit 1
fi
echo -e "${GREEN}✓${NC} Python 3 is installed"

if [[ ! -d "$HOME/.config/omarchy" ]]; then
    echo -e "${RED}✗${NC} Omarchy is not installed"
    echo "  Install from: https://github.com/basecamp/omarchy"
    exit 1
fi
echo -e "${GREEN}✓${NC} Omarchy is installed"

echo

# Clone or update repository
if [[ -d "$INSTALL_DIR" ]]; then
    echo -e "${YELLOW}Repository already exists. Updating...${NC}"
    cd "$INSTALL_DIR"
    git pull --quiet || true
else
    echo -e "Cloning repository..."
    git clone --quiet "$REPO_URL" "$INSTALL_DIR" 2>/dev/null || {
        # If git clone fails (repo doesn't exist yet), use the local scripts
        echo -e "${YELLOW}Repository not available. Using local installation...${NC}"
        mkdir -p "$INSTALL_DIR/scripts"
        
        # Assuming this script is in the scripts directory
        SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
        cp "$SCRIPT_DIR/omarchy-zellij-hook" "$INSTALL_DIR/scripts/"
        cp "$SCRIPT_DIR/convert_theme.py" "$INSTALL_DIR/scripts/"
    }
fi

# Create necessary directories
mkdir -p "$HOME/.local/bin"
mkdir -p "$ZELLIJ_THEMES_DIR"
mkdir -p "$(dirname "$OMARCHY_HOOK")"

# Install hook script
echo -e "Installing hook script..."
cp "$INSTALL_DIR/scripts/omarchy-zellij-hook" "$HOOK_DEST"
chmod +x "$HOOK_DEST"
echo -e "${GREEN}✓${NC} Hook installed to $HOOK_DEST"

# Register hook in Omarchy
echo -e "Registering hook with Omarchy..."
if [[ -f "$OMARCHY_HOOK" ]]; then
    if grep -q "omarchy-zellij-hook" "$OMARCHY_HOOK"; then
        echo -e "${YELLOW}⚠${NC} Hook already registered"
    else
        echo "$HOOK_DEST \$1" >> "$OMARCHY_HOOK"
        echo -e "${GREEN}✓${NC} Hook registered in Omarchy"
    fi
else
    cat > "$OMARCHY_HOOK" << 'EOF'
#!/bin/bash
$HOME/.local/bin/omarchy-zellij-hook $1
EOF
    chmod +x "$OMARCHY_HOOK"
    echo -e "${GREEN}✓${NC} Hook file created"
fi

# Generate themes
echo
echo -e "${BOLD}Generating Zellij themes...${NC}"

if [[ ! -d "$OMARCHY_THEMES_DIR" ]]; then
    echo -e "${YELLOW}⚠${NC} No Omarchy themes found"
    exit 0
fi

THEME_COUNT=0
for theme_path in "$OMARCHY_THEMES_DIR"/*; do
    if [[ ! -d "$theme_path" ]]; then
        continue
    fi
    
    theme_name=$(basename "$theme_path")
    kitty_conf="$theme_path/kitty.conf"
    zellij_theme="$ZELLIJ_THEMES_DIR/${theme_name}.kdl"
    
    if [[ -f "$kitty_conf" ]]; then
        if python3 "$INSTALL_DIR/scripts/convert_theme.py" "$theme_name" "$kitty_conf" > "$zellij_theme" 2>/dev/null; then
            echo -e "${GREEN}✓${NC} $theme_name"
            ((THEME_COUNT++))
        else
            echo -e "${RED}✗${NC} $theme_name (failed)"
        fi
    fi
done

echo
echo -e "${GREEN}${BOLD}Installation complete!${NC}"
echo
echo -e "Generated ${BOLD}$THEME_COUNT${NC} Zellij themes"
echo
echo -e "${BOLD}Usage:${NC}"
echo -e "  Change your Omarchy theme and Zellij will automatically sync:"
echo -e "  ${BLUE}omarchy theme tokyo-night${NC}"
echo
echo -e "${BOLD}Next steps:${NC}"
echo -e "  • Test the integration by changing themes"
echo -e "  • Check out the documentation at ${INSTALL_DIR}/README.md"
echo
