# Git Setup Guide for AI Agent Workshop

This guide will help you install and configure Git on Windows 11, macOS, and Linux systems.

## Table of Contents
- [Windows 11 Setup](#windows-11-setup)
- [macOS Setup](#macos-setup)
- [Linux Setup](#linux-setup)
- [Git Configuration](#git-configuration)
- [Cloning the Repository](#cloning-the-repository)
- [Troubleshooting](#troubleshooting)

---

## Windows 11 Setup

### Option 1: Git for Windows (Recommended)

1. **Download Git for Windows**
   - Visit: https://gitforwindows.org/
   - Click "Download" to get the latest version

2. **Run the Installer**
   - Run the downloaded `.exe` file
   - Click "Next" through the default options
   - Choose "Use Git from Git Bash only" when asked
   - Choose "Use Windows' default console window" for the terminal emulator
   - Click "Install"

3. **Verify Installation**
   ```bash
   git --version
   ```

### Option 2: Windows Terminal + Git

1. **Install Windows Terminal** (if not already installed)
   - Open Microsoft Store
   - Search for "Windows Terminal"
   - Click "Get" to install

2. **Install Git via Winget**
   ```powershell
   winget install --id Git.Git -e --source winget
   ```

3. **Verify Installation**
   ```bash
   git --version
   ```

---

## macOS Setup

### Option 1: Xcode Command Line Tools (Recommended)

1. **Install Xcode Command Line Tools**
   ```bash
   xcode-select --install
   ```
   - Click "Install" when prompted
   - Wait for installation to complete

2. **Verify Installation**
   ```bash
   git --version
   ```

### Option 2: Homebrew Installation

1. **Install Homebrew** (if not already installed)
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Install Git**
   ```bash
   brew install git
   ```

3. **Verify Installation**
   ```bash
   git --version
   ```

### Option 3: GitHub Desktop

1. **Download GitHub Desktop**
   - Visit: https://desktop.github.com/
   - Download and install the macOS version

2. **Git will be installed automatically with GitHub Desktop**

---

## Linux Setup

### Ubuntu/Debian

```bash
# Update package list
sudo apt update

# Install Git
sudo apt install git

# Verify installation
git --version
```

### CentOS/RHEL/Fedora

```bash
# For CentOS/RHEL
sudo yum install git

# For Fedora
sudo dnf install git

# Verify installation
git --version
```

### Arch Linux

```bash
# Install Git
sudo pacman -S git

# Verify installation
git --version
```

### Universal Linux Installation

If your distribution isn't listed above, you can compile Git from source:

```bash
# Install dependencies
sudo apt update && sudo apt install -y dh-autoreconf libcurl4-gnutls-dev libexpat1-dev gettext libz-dev libssl-dev

# Download and extract Git source
wget https://github.com/git/git/archive/refs/tags/v2.40.0.tar.gz
tar -xzf v2.40.0.tar.gz
cd git-2.40.0

# Compile and install
make configure
./configure --prefix=/usr
make all
sudo make install

# Verify installation
git --version
```

---

## Git Configuration

After installing Git, configure it with your information:

### Basic Configuration

```bash
# Set your name
git config --global user.name "Your Full Name"

# Set your email
git config --global user.email "your.email@example.com"

# Set default branch name to main
git config --global init.defaultBranch main

# Enable colored output
git config --global color.ui auto
```

### Verify Configuration

```bash
# Check your settings
git config --global --list

# Check Git version
git --version
```

### SSH Key Setup (Optional but Recommended)

For GitHub authentication without passwords:

1. **Generate SSH Key**
   ```bash
   ssh-keygen -t ed25519 -C "your.email@example.com"
   ```

2. **Add SSH Key to ssh-agent**
   ```bash
   # Start ssh-agent
   eval "$(ssh-agent -s)"

   # Add your key
   ssh-add ~/.ssh/id_ed25519
   ```

3. **Copy Public Key**
   ```bash
   # Display public key
   cat ~/.ssh/id_ed25519.pub
   ```

4. **Add to GitHub**
   - Go to GitHub.com → Settings → SSH and GPG keys
   - Click "New SSH key"
   - Paste your public key
   - Click "Add SSH key"

---

## Cloning the Repository

Once Git is installed and configured:

```bash
# Clone the AI Agent Workshop repository
git clone https://github.com/your-username/ai-agent-workshop.git

# Navigate to the project directory
cd ai-agent-workshop

# Verify the clone worked
ls -la
```

### If Using SSH (after SSH key setup)

```bash
# Clone using SSH (no password needed)
git clone git@github.com:your-username/ai-agent-workshop.git
cd ai-agent-workshop
```

---

## Troubleshooting

### "Command not found" Error

**Windows:**
- Make sure Git is in your PATH
- Try restarting your terminal/command prompt
- Check if you installed Git correctly

**macOS/Linux:**
- Check if Git is installed: `which git`
- If not found, reinstall following the steps above

### Permission Denied Errors

**When cloning:**
```bash
# Try using HTTPS instead of SSH
git clone https://github.com/username/repo.git

# Or check your SSH key setup
ssh -T git@github.com
```

### Git Version Too Old

**Update Git:**

**Windows:**
- Download latest Git for Windows installer
- Run installer (it will update existing installation)

**macOS:**
```bash
brew upgrade git
```

**Ubuntu/Debian:**
```bash
sudo apt update && sudo apt upgrade git
```

### Network Issues

If you're behind a corporate firewall:
```bash
# Configure proxy (replace with your proxy settings)
git config --global http.proxy http://proxy.company.com:8080
git config --global https.proxy http://proxy.company.com:8080
```

### Common Git Commands

```bash
# Check status
git status

# Add files
git add .

# Commit changes
git commit -m "Your message"

# Push changes
git push origin main

# Pull latest changes
git pull origin main
```

---

## Next Steps

Once Git is set up and you've cloned the repository:

1. **Follow the main README.md** for project setup
2. **Run the installation commands** as described
3. **Start with Session 1** to learn about AI agents

## Support

If you encounter issues:
1. Check this guide again
2. Search online for your specific error message
3. Ask for help in the project discussions

Happy coding! 🚀