# Omarchy Zellij

<div align="center">

**Zellij themes that automatically sync with Omarchy theme changes**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[Features](#features) • [Quick Start](#quick-start) • [Documentation](#documentation) • [Themes](#supported-themes)

</div>

---

## Features

✨ **All 13 Omarchy themes supported**  
🔄 **Automatic theme synchronization**  
🚀 **Zero-configuration after installation**  
🎨 **Seamless integration** with Omarchy's theme system  
📦 **Easy one-line installation**

## Quick Start

```bash
curl -fsSL https://raw.githubusercontent.com/cedricwider/omarchy-zellij/main/scripts/install.sh | bash
```

> **Security Tip**: Always review scripts before running. See [docs/installation.md](docs/installation.md) for manual installation.

## How It Works

When you change themes in Omarchy, this integration:

1. **Captures the event** via Omarchy's hook system
2. **Converts the theme name** from snake_case to kebab-case
3. **Updates Zellij's config** automatically
4. **Zellij reloads** and applies the new theme instantly ✨

No manual intervention required!

## Requirements

- [Omarchy](https://github.com/basecamp/omarchy)
- [Zellij](https://zellij.dev/)
- Python 3.x
- Bash shell

## Supported Themes

All official Omarchy themes are supported:

<table>
<tr>
<td>

- Catppuccin (Mocha)
- Catppuccin Latte
- Everforest
- Flexoki Light
- Gruvbox

</td>
<td>

- Kanagawa
- Matte Black
- Nord
- Osaka Jade

</td>
<td>

- Ristretto
- Rose Pine
- Roseofdune
- Tokyo Night

</td>
</tr>
</table>

## Documentation

- 📖 [Installation Guide](docs/installation.md) - Detailed installation instructions
- 🔧 [How It Works](docs/how-it-works.md) - Technical architecture and details
- 🐛 [Troubleshooting](docs/troubleshooting.md) - Common issues and solutions

## Usage

Once installed, simply change your Omarchy theme:

```bash
omarchy theme tokyo-night
```

Zellij will automatically update to match! 🎨

## Project Structure

```
omarchy-zellij/
├── scripts/
│   ├── install.sh              # Installation script
│   ├── omarchy-zellij-hook     # Hook script that updates Zellij
│   └── convert_theme.py        # Theme converter (kitty.conf → KDL)
├── docs/
│   ├── installation.md         # Installation guide
│   ├── how-it-works.md        # Technical documentation
│   └── troubleshooting.md     # Troubleshooting guide
├── assets/                     # Screenshots and assets
├── LICENSE                     # MIT License
└── README.md                   # This file
```

## Inspiration

This project was inspired by [omarchy-tmux](https://github.com/joaofelipegalvao/omarchy-tmux) by João Felipe Galvão.

## Contributing

Contributions are welcome! Feel free to:

- 🐛 Report bugs
- 💡 Suggest new features
- 🔧 Submit pull requests
- 📖 Improve documentation

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Credits

- [Omarchy](https://github.com/basecamp/omarchy) by Basecamp
- [Zellij](https://zellij.dev/) - A terminal workspace
- Theme definitions based on Omarchy's official theme collection

---

<div align="center">

Made with ❤️ for the terminal

</div>
