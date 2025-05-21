# Password Clarity

<img src="https://raw.githubusercontent.com/bkearan/PasswordClarity/main/icon/password-clarity-icon.png" alt="Password Clarity Icon" width="150">

## About

Password Clarity is a specialized visualization tool that solves the common problem of distinguishing between similar-looking characters in passwords and security codes. Ever struggled with telling apart a capital "I" from a lowercase "l" or the number "0" from the letter "O"? Password Clarity makes this distinction crystal clear through intuitive color-coding.

The tool provides real-time visual feedback as you type, transforming plain text into a color-coded format where each character type (uppercase, lowercase, numbers, and symbols) is instantly recognizable.

## Features

- **Character Type Distinction**: Instantly distinguishes between:
  - **Capital letters**: Displayed in green
  - **Lowercase letters**: Displayed in blue
  - **Numbers**: Displayed in red
  - **Symbols**: Displayed in black

- **Real-time Statistics**:
  - Live character counts for each type
  - Password strength score (0-100)
  - Strength rating indicator (Weak/Moderate/Strong)

- **Cross-Platform Support**:
  - Windows version (PowerShell/WPF)
  - Linux/macOS version (Python/Tkinter)

- **Privacy-Focused**: All processing happens locally - no data is sent over the network

## Implementations

### PowerShell Version (Windows)

The Windows implementation leverages Windows Presentation Foundation (WPF) to provide a native experience with minimal dependencies.

```powershell
# To run directly from PowerShell:
.\PasswordClarity.ps1
```

**Screenshots:**
(Coming soon)

### Python Version (Cross-Platform)

The Python implementation uses Tkinter for a consistent experience across Linux, macOS, and Windows.

```bash
# To run:
python PasswordClarity.py
```

**Screenshots:**
(Coming soon)

## Why Password Clarity?

Password Clarity was born from the frustration of dealing with ambiguous characters in passwords, security codes, and API keys. It's particularly useful for:

- IT professionals who regularly work with system passwords
- Developers copying API keys and tokens
- Anyone who needs to accurately communicate passwords verbally
- Users who want to ensure their passwords contain a good mix of character types

## How It Works

When you type or paste text into Password Clarity:

1. Each character is analyzed and categorized in real-time
2. Characters are displayed with color-coding based on their type
3. Character type counts are updated instantly
4. The password strength algorithm evaluates the security of your input
5. The password strength rating is updated with appropriate color coding

No data is stored or transmitted - everything happens locally on your device.

## Installation

### Windows
```powershell
# Clone the repository
git clone https://github.com/bkearan/PasswordClarity.git

# Navigate to the PowerShell directory
cd PasswordClarity/powershell

# Run the script (must be run from PowerShell)
.\PasswordClarity.ps1
```

### Linux/macOS
```bash
# Clone the repository
git clone https://github.com/bkearan/PasswordClarity.git

# Navigate to the Python directory
cd PasswordClarity/python

# Run the script
python PasswordClarity.py
```

### Building Standalone Executables

#### For Windows
```powershell
# Create an executable from the PowerShell script
# Requires PS2EXE module
Install-Module -Name PS2EXE
Invoke-ps2exe -InputFile .\PasswordClarity.ps1 -OutputFile .\PasswordClarity.exe -NoConsole
```

#### For Linux
```bash
# Create a standalone executable from the Python script
# Requires PyInstaller
pip install pyinstaller
pyinstaller --onefile --windowed --hidden-import tkinter --hidden-import tkinter.font --name "Password Clarity" PasswordClarity.py
```

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Feel free to:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Acknowledgments

- Inspired by the common frustration of ambiguous characters in passwords
- Thanks to the open-source community for tools and libraries that made this project possible
