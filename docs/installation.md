# Installation Guide

This guide provides detailed installation instructions for omarchy-zellij.

## Prerequisites

Before installing, ensure you have:

- **Omarchy** installed and configured
  - Install from: https://github.com/basecamp/omarchy
- **Zellij** installed and configured
  - Install from: https://zellij.dev/
- **Python 3.x** (3.6 or later)
- **Bash shell**

Verify your installation:

```bash
# Check Zellij
zellij --version

# Check Python
python3 --version

# Check Omarchy
ls ~/.config/omarchy
```

## Quick Installation

The easiest way to install is using the automated installation script:

```bash
curl -fsSL https://raw.githubusercontent.com/cedricwider/omarchy-zellij/main/scripts/install.sh | bash
```

### What the installer does:

1. ✅ Checks prerequisites
2. ✅ Clones the repository to `~/.config/omarchy-zellij`
3. ✅ Installs the hook script to `~/.local/bin/omarchy-zellij-hook`
4. ✅ Registers the hook in Omarchy's theme-set file
5. ✅ Generates Zellij themes for all available Omarchy themes
6. ✅ Sets proper permissions

## Manual Installation

If you prefer to install manually or want to understand what's happening:

### Step 1: Clone the Repository

```bash
git clone https://github.com/cedricwider/omarchy-zellij.git ~/.config/omarchy-zellij
```

### Step 2: Install the Hook Script

```bash
cp ~/.config/omarchy-zellij/scripts/omarchy-zellij-hook ~/.local/bin/
chmod +x ~/.local/bin/omarchy-zellij-hook
```

### Step 3: Register the Hook

Create or edit `~/.config/omarchy/hooks/theme-set`:

```bash
#!/bin/bash
~/.local/bin/omarchy-zellij-hook $1
```

Make it executable:

```bash
chmod +x ~/.config/omarchy/hooks/theme-set
```

### Step 4: Generate Zellij Themes

```bash
mkdir -p ~/.config/zellij/themes

for theme_dir in ~/.config/omarchy/themes/*; do
    theme_name=$(basename "$theme_dir")
    if [[ -f "$theme_dir/kitty.conf" ]]; then
        python3 ~/.config/omarchy-zellij/scripts/convert_theme.py \
            "$theme_name" \
            "$theme_dir/kitty.conf" \
            > ~/.config/zellij/themes/${theme_name}.kdl
    fi
done
```

## Verification

Test that the installation worked:

```bash
# 1. Test the hook manually
~/.local/bin/omarchy-zellij-hook tokyo_night

# 2. Check if the theme was set in Zellij config
grep "^theme" ~/.config/zellij/config.kdl

# 3. List generated themes
ls ~/.config/zellij/themes/
```

## Updating

To update to the latest version:

```bash
cd ~/.config/omarchy-zellij
git pull
bash scripts/install.sh
```

## Uninstallation

To completely remove the integration:

```bash
# Remove the hook script
rm ~/.local/bin/omarchy-zellij-hook

# Remove the cloned repository
rm -rf ~/.config/omarchy-zellij

# Edit the Omarchy hook file
nano ~/.config/omarchy/hooks/theme-set
# Remove the line: ~/.local/bin/omarchy-zellij-hook $1

# Optional: Remove generated themes
rm -rf ~/.config/zellij/themes/*.kdl
```

## Troubleshooting Installation

### Hook script not found

If you get "command not found" errors:

1. **Check if `~/.local/bin` is in your PATH:**
   ```bash
   echo $PATH | grep ".local/bin"
   ```

2. **Add it to your PATH** if missing (add to your shell config):
   ```bash
   # For bash (~/.bashrc)
   export PATH="$HOME/.local/bin:$PATH"
   
   # For fish (~/.config/fish/config.fish)
   set -gx PATH $HOME/.local/bin $PATH
   ```

3. **Reload your shell:**
   ```bash
   source ~/.bashrc  # or restart your terminal
   ```

### Python not found

If Python 3 is not found:

```bash
# Check if python3 is installed
which python3

# If not, install it:
# Ubuntu/Debian
sudo apt install python3

# Fedora/CentyOS
sudo dnf install python3

# Arch
sudo pacman -S python
```

### Permission denied errors

If you get permission errors:

```bash
# Make scripts executable
chmod +x ~/.local/bin/omarchy-zellij-hook
chmod +x ~/.config/omarchy/hooks/theme-set
```

## Next Steps

Once installed:

1. **Test the integration** by changing themes:
   ```bash
   omarchy theme tokyo-night
   ```

2. **Read the documentation:**
   - [How It Works](how-it-works.md)
   - [Troubleshooting](troubleshooting.md)

3. **Customize** (optional):
   - Edit theme files in `~/.config/zellij/themes/`
   - Modify the hook script for custom behavior
