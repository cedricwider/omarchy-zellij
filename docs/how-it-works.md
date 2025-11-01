# How It Works

This document explains the technical architecture and inner workings of omarchy-zellij.

## Architecture Overview

```mermaid
flowchart TD
    A[Omarchy Theme Manager] -->|theme change event<br/>tokyo_night| B[~/.config/omarchy/hooks/theme-set]
    B -->|calls hook| C[~/.local/bin/omarchy-zellij-hook]
    C -->|• Convert snake_case to kebab-case<br/>• Validate theme exists<br/>• Update config| D[~/.config/zellij/config.kdl]
    D -->|auto-reloads| E[Zellij - New Theme Applied!]
    
    style A fill:#4A90E2
    style E fill:#7ED321
    style C fill:#F5A623
```

## Components

### 1. Omarchy Hook System

Omarchy provides a hook system that allows external scripts to respond to events. Hooks are shell scripts placed in `~/.config/omarchy/hooks/`.

When you run `omarchy theme tokyo-night`, Omarchy:
1. Changes its internal theme state
2. Executes `~/.config/omarchy/hooks/theme-set tokyo_night`
   - Note: theme name is passed in **snake_case** (underscores)

### 2. The Hook Script (`omarchy-zellij-hook`)

Located at `~/.local/bin/omarchy-zellij-hook`, this bash script handles the theme synchronization.

**Key operations:**

1. **Name conversion:** `tokyo_night` → `tokyo-night`
   - Uses bash parameter expansion: `${THEME_SNAKE//_/-}`
   
2. **Validation:** Ensures theme directory exists
   - Prevents errors from typos or missing themes
   
3. **Config update:** Uses `sed` to replace the theme line
   - Updates the `theme` directive in Zellij's config.kdl

### 3. The Theme Converter (`convert_theme.py`)

This Python script converts Omarchy's kitty.conf color definitions to Zellij's KDL format.

```mermaid
flowchart LR
    A[kitty.conf<br/>Hex Colors] -->|Parse & Extract| B[Python Script]
    B -->|Convert Hex to RGB| C[RGB Values]
    C -->|Map to UI Components| D[Zellij KDL Theme]
    
    style A fill:#E8F5E9
    style D fill:#E3F2FD
```

**Input (kitty.conf):**
```conf
foreground #D8DEE9
background #2E3440
color0  #3B4252  # black
color1  #BF616A  # red
```

**Output (Zellij KDL):**
```kdl
themes {
    nord {
        text_unselected {
            base 216 222 233
            background 46 52 64
            # ... more attributes
        }
    }
}
```

### 4. Zellij Auto-Reload

Zellij watches its config file for changes. When modified:

1. **Detects change:** inotify (Linux) or similar mechanism
2. **Validates config:** Ensures KDL syntax is correct
3. **Reloads theme:** Applies new colors to all panes
4. **Updates UI:** All visible elements update instantly

## Data Flow

### Initial Setup (Installation)

```mermaid
sequenceDiagram
    participant User
    participant Installer
    participant FileSystem
    participant Converter
    
    User->>Installer: Run install.sh
    Installer->>FileSystem: Copy hook to ~/.local/bin/
    Installer->>FileSystem: Register hook in Omarchy
    Installer->>Converter: Generate themes from kitty.conf
    Converter->>FileSystem: Create .kdl theme files
    Installer->>User: Installation complete!
```

### Runtime (Theme Change)

```mermaid
sequenceDiagram
    participant User
    participant Omarchy
    participant Hook
    participant Zellij
    
    User->>Omarchy: omarchy theme tokyo-night
    Omarchy->>Omarchy: Update internal theme state
    Omarchy->>Hook: Execute theme-set tokyo_night
    Hook->>Hook: Convert tokyo_night → tokyo-night
    Hook->>Hook: Validate theme directory exists
    Hook->>FileSystem: Update config.kdl
    FileSystem->>Zellij: Config file changed
    Zellij->>Zellij: Reload configuration
    Zellij->>User: Apply new theme ✨
```

## Theme Name Conventions

```mermaid
flowchart LR
    A[Omarchy Hook<br/>tokyo_night<br/>snake_case] -->|Bash conversion<br/>${THEME//_/-}| B[File System<br/>tokyo-night<br/>kebab-case]
    B -->|Load theme| C[Zellij Config<br/>theme tokyo-night]
    
    style A fill:#FFF3E0
    style B fill:#E8EAF6
    style C fill:#E0F2F1
```

**Conventions:**
- **Omarchy directories:** kebab-case (`tokyo-night`, `rose-pine`)
- **Hook arguments:** snake_case (`tokyo_night`, `rose_pine`)
- **Zellij themes:** kebab-case (`tokyo-night.kdl`)

## Performance

The theme switching is nearly instantaneous:

- **Hook execution:** ~5-10ms (bash script, sed operation)
- **Zellij reload:** ~50-100ms (config parse, UI update)
- **Total perceived delay:** < 200ms ⚡

## Error Handling

The hook script includes robust error handling:

```mermaid
flowchart TD
    A[Hook Called] --> B{Theme Directory<br/>Exists?}
    B -->|No| C[Error: Theme not found]
    B -->|Yes| D{Zellij Config<br/>Exists?}
    D -->|No| E[Error: Config not found]
    D -->|Yes| F[Update Config]
    F --> G[Success!]
    
    style C fill:#FFCDD2
    style E fill:#FFCDD2
    style G fill:#C8E6C9
```

**Safety features:**

1. **Strict mode:** `set -euo pipefail`
2. **Theme validation:** Checks if theme directory exists
3. **Config validation:** Checks if Zellij config exists
4. **Error messages:** Clear stderr output on failures

## Zellij UI Components

```mermaid
mindmap
  root((Zellij Theme))
    Text
      text_unselected
      text_selected
    Ribbon
      ribbon_unselected
      ribbon_selected
    Table
      table_title
      table_cell_unselected
      table_cell_selected
    List
      list_unselected
      list_selected
    Frame
      frame_unselected
      frame_selected
      frame_highlight
    Status
      exit_code_success
      exit_code_error
    Multiplayer
      multiplayer_user_colors
```

## Extensibility

The architecture is designed to be extensible:

### Adding New Themes

```mermaid
flowchart LR
    A[Add Theme<br/>to Omarchy] --> B[Ensure kitty.conf<br/>Exists]
    B --> C[Run converter]
    C --> D[Generate .kdl File]
    D --> E[Theme Available!]
```

### Supporting Other Tools

The same pattern can be used for other tools:

```mermaid
flowchart TD
    A[Omarchy Hook System] --> B[omarchy-zellij-hook]
    A --> C[omarchy-alacritty-hook]
    A --> D[omarchy-kitty-hook]
    A --> E[omarchy-neovim-hook]
    
    style A fill:#E1BEE7
    style B fill:#BBDEFB
    style C fill:#C5E1A5
    style D fill:#FFE082
    style E fill:#FFCCBC
```

## Comparison with Similar Tools

| Feature | omarchy-tmux | omarchy-zellij |
|---------|--------------|----------------|
| Integration method | TPM plugin + systemd | Hook script |
| Auto-reload | systemd service | Zellij native |
| Installation | curl \| bash + TPM | curl \| bash |
| Dependencies | tmux, TPM, systemd | zellij, python3 |
| Theme format | tmux.conf | KDL |

### Advantages

- ✅ **Simpler:** No systemd service required
- ✅ **Native:** Uses Zellij's built-in reload
- ✅ **Lightweight:** Just a bash script and Python converter
- ✅ **Fast:** Direct config file modification

## Technical References

- [Zellij Configuration](https://zellij.dev/documentation/configuration)
- [Zellij Themes](https://zellij.dev/documentation/themes)
- [KDL Language](https://kdl.dev/)
- [Omarchy](https://github.com/basecamp/omarchy)
- [Mermaid Diagrams](https://mermaid.js.org/)
