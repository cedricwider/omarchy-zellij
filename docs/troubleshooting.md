# Troubleshooting Guide

Common issues and their solutions for omarchy-zellij.

## Theme Not Changing

### Symptom
When you change the Omarchy theme, Zellij doesn't update.

### Diagnosis

1. **Check if the hook is installed:**
   ```bash
   ls -la ~/.local/bin/omarchy-zellij-hook
   ```

2. **Check if the hook is registered:**
   ```bash
   cat ~/.config/omarchy/hooks/theme-set
   ```
   Should contain: `~/.local/bin/omarchy-zellij-hook $1`

3. **Test the hook manually:**
   ```bash
   ~/.local/bin/omarchy-zellij-hook tokyo_night
   ```

4. **Check if config was updated:**
   ```bash
   grep "^theme" ~/.config/zellij/config.kdl
   ```

### Solutions

- **Hook not installed:** Run the installer again
- **Hook not executable:** `chmod +x ~/.local/bin/omarchy-zellij-hook`
- **Hook not registered:** Edit `~/.config/omarchy/hooks/theme-set` and add the hook line

## Theme File Not Found

### Symptom
Error message: "Error: Theme directory not found"

### Diagnosis

Check if the theme exists:
```bash
ls ~/.config/omarchy/themes/
ls ~/.config/zellij/themes/
```

### Solutions

1. **Regenerate themes:**
   ```bash
   cd ~/.config/omarchy-zellij
   bash scripts/install.sh
   ```

2. **Generate specific theme:**
   ```bash
   python3 ~/.config/omarchy-zellij/scripts/convert_theme.py \
       "theme-name" \
       ~/.config/omarchy/themes/theme-name/kitty.conf \
       > ~/.config/zellij/themes/theme-name.kdl
   ```

## Colors Look Wrong

### Symptom
Theme applies but colors don't match expectations.

### Diagnosis

1. **Check source colors:**
   ```bash
   cat ~/.config/omarchy/themes/THEME_NAME/kitty.conf
   ```

2. **Check generated theme:**
   ```bash
   cat ~/.config/zellij/themes/THEME_NAME.kdl
   ```

### Solutions

1. **Regenerate theme** (in case of corruption):
   ```bash
   python3 ~/.config/omarchy-zellij/scripts/convert_theme.py \
       "THEME_NAME" \
       ~/.config/omarchy/themes/THEME_NAME/kitty.conf \
       > ~/.config/zellij/themes/THEME_NAME.kdl
   ```

2. **Manually adjust colors:**
   ```bash
   nvim ~/.config/zellij/themes/THEME_NAME.kdl
   ```
   Zellij will auto-reload on save.

## Hook Runs But Nothing Happens

### Symptom
Hook executes without errors but theme doesn't change.

### Diagnosis

1. **Check Zellij is running:**
   ```bash
   ps aux | grep zellij
   ```

2. **Check config line number:**
   ```bash
   grep -n "^theme" ~/.config/zellij/config.kdl
   ```
   Note the line number.

### Solutions

If the theme line is not on line 372, update the hook script:

```bash
nvim ~/.local/bin/omarchy-zellij-hook
```

Change line 22 to use the correct line number, or use a more flexible approach:

```bash
# Replace line 22 with:
sed -i "s/^theme .*/theme \"$THEME\"/" "$ZELLIJ_CONF"
```

This will find and replace any line starting with `theme` regardless of line number.

## Permission Denied

### Symptom
Error: "Permission denied" when running hooks or scripts.

### Solutions

Make scripts executable:
```bash
chmod +x ~/.local/bin/omarchy-zellij-hook
chmod +x ~/.config/omarchy/hooks/theme-set
chmod +x ~/.config/omarchy-zellij/scripts/*.sh
chmod +x ~/.config/omarchy-zellij/scripts/*.py
```

## Python Script Fails

### Symptom
Theme generation fails with Python errors.

### Diagnosis

1. **Check Python version:**
   ```bash
   python3 --version
   ```
   Should be 3.6 or later.

2. **Test the converter manually:**
   ```bash
   python3 ~/.config/omarchy-zellij/scripts/convert_theme.py \
       "test" \
       ~/.config/omarchy/themes/nord/kitty.conf
   ```

### Solutions

- **Python too old:** Upgrade Python 3
- **Missing dependencies:** No external dependencies required
- **Syntax error:** Re-download the script from the repository

## Zellij Doesn't Auto-Reload

### Symptom
Config file updates but Zellij doesn't reflect changes.

### Diagnosis

Check if Zellij is watching config:
```bash
# In a Zellij session, manually reload:
# Press Ctrl+o then r
```

### Solutions

1. **Restart Zellij session:**
   ```bash
   # Exit all panes
   # Start new session
   zellij
   ```

2. **Force config reload:**
   - Press `Ctrl+o` (session mode)
   - Then press `r` (reload)

## PATH Issues

### Symptom
"command not found: omarchy-zellij-hook"

### Diagnosis

Check if `~/.local/bin` is in PATH:
```bash
echo $PATH | grep ".local/bin"
```

### Solutions

Add to your shell configuration:

**Bash (~/.bashrc):**
```bash
export PATH="$HOME/.local/bin:$PATH"
```

**Fish (~/.config/fish/config.fish):**
```fish
set -gx PATH $HOME/.local/bin $PATH
```

**Zsh (~/.zshrc):**
```zsh
export PATH="$HOME/.local/bin:$PATH"
```

Then reload:
```bash
source ~/.bashrc  # or restart terminal
```

## Omarchy Hook Not Firing

### Symptom
Omarchy changes theme but hook never runs.

### Diagnosis

1. **Check hook file exists:**
   ```bash
   ls -la ~/.config/omarchy/hooks/theme-set
   ```

2. **Check hook is executable:**
   ```bash
   test -x ~/.config/omarchy/hooks/theme-set && echo "executable" || echo "not executable"
   ```

3. **Test hook manually:**
   ```bash
   bash ~/.config/omarchy/hooks/theme-set tokyo_night
   ```

### Solutions

- **Make executable:** `chmod +x ~/.config/omarchy/hooks/theme-set`
- **Fix shebang:** Ensure first line is `#!/bin/bash`
- **Check syntax:** Run `bash -n ~/.config/omarchy/hooks/theme-set`

## Multiple Hooks Conflict

### Symptom
You have multiple hooks (tmux, zellij, etc.) and they interfere.

### Solution

Omarchy hooks can have multiple commands. Edit `~/.config/omarchy/hooks/theme-set`:

```bash
#!/bin/bash

# Run all hooks
~/.local/bin/omarchy-tmux-hook $1
~/.local/bin/omarchy-zellij-hook $1
# Add more hooks here
```

## Still Having Issues?

If none of these solutions work:

1. **Check logs:** Look for error messages when running hooks manually
2. **Reinstall:** Remove everything and run the installer again
3. **Report bug:** Create an issue on GitHub with:
   - Error messages
   - Output of diagnostic commands
   - Your OS and shell version
   - Zellij and Omarchy versions

## Diagnostic Script

Run this script to gather debugging information:

```bash
#!/bin/bash
echo "=== Omarchy-Zellij Diagnostic ==="
echo
echo "Zellij version:"
zellij --version
echo
echo "Python version:"
python3 --version
echo
echo "Hook script exists:"
ls -la ~/.local/bin/omarchy-zellij-hook
echo
echo "Hook registered:"
cat ~/.config/omarchy/hooks/theme-set
echo
echo "Generated themes:"
ls -1 ~/.config/zellij/themes/ | wc -l
echo
echo "Current theme in config:"
grep "^theme" ~/.config/zellij/config.kdl
echo
echo "PATH includes ~/.local/bin:"
echo $PATH | grep -q ".local/bin" && echo "Yes" || echo "No"
```

Save as `diagnostic.sh`, make executable (`chmod +x diagnostic.sh`), and run it.
