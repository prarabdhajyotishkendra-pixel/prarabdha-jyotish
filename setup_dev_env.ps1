<#
.SYNOPSIS
    Automated Development Environment Setup Script for Windows using Chocolatey.
.DESCRIPTION
    This script installs Chocolatey, reloads the environment, and installs primary developer
    tools such as Python, Git, NodeJS, and Visual Studio Build Tools.
    
    Please run this script as an ADMINISTRATOR.
#>

$ErrorActionPreference = "Stop"

function Write-Step ($message) {
    Write-Host ">>> $message" -ForegroundColor Cyan
}

function Write-Success ($message) {
    Write-Host "[SUCCESS] $message" -ForegroundColor Green
}

function Write-ErrorMsg ($message) {
    Write-Host "[ERROR] $message" -ForegroundColor Red
}

function Reload-Path {
    Write-Step "Reloading environment variables..."
    if (Get-Command refreshenv -ErrorAction SilentlyContinue) {
        refreshenv
    } else {
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
    }
}

# Ensure running as Admin
$IsAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $IsAdmin) {
    Write-ErrorMsg "This script must be run as Administrator! Please open PowerShell as Administrator and run again."
    Write-Host "Fallback Instruction: Right click the Start Button -> Windows PowerShell (Admin)." -ForegroundColor Yellow
    exit 1
}

# 1. Install Chocolatey
Write-Step "Checking for Chocolatey..."
if (-not (Get-Command choco -ErrorAction SilentlyContinue)) {
    try {
        Write-Step "Installing Chocolatey..."
        Set-ExecutionPolicy Bypass -Scope Process -Force
        [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
        iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
        Write-Success "Chocolatey installed successfully."
    } catch {
        Write-ErrorMsg "Failed to install Chocolatey. Error: $_"
        Write-Host "Fallback Instruction: Navigate to https://chocolatey.org/install for manual installation instructions." -ForegroundColor Yellow
        exit 1
    }
} else {
    Write-Success "Chocolatey is already installed."
}

# 2. Restart/Reload Environment
Reload-Path

# Validate Choco
if (-not (Get-Command choco -ErrorAction SilentlyContinue)) {
    Write-ErrorMsg "Chocolatey command 'choco' is not recognized even after reloading PATH."
    Write-Host "Fallback Instruction: You may need to completely restart your PowerShell window or your PC, then run this script again." -ForegroundColor Yellow
    exit 1
}

# 3 & 6. Install Tools
$packages = @("python", "git", "nodejs", "visualstudio2022buildtools")

foreach ($pkg in $packages) {
    Write-Step "Installing $pkg..."
    try {
        choco install $pkg -y
        Write-Success "$pkg installed successfully."
    } catch {
        Write-ErrorMsg "Failed to install $pkg. Error: $_"
        if ($pkg -eq "python") {
            Write-Step "Retrying Python installation..."
            try {
                choco install python -y --force
                Write-Success "Python installed successfully on retry."
            } catch {
                Write-ErrorMsg "Python retry failed. Fallback: Download manually from https://www.python.org/downloads/"
            }
        }
    }
}

# Reload Environment after installations
Reload-Path

# 4. Verify Python Installation
Write-Step "Verifying Python Installation..."
try {
    $pyVer = python --version 2>&1
    Write-Success "Python is accessible globally: $pyVer"
    
    $pipVer = pip --version 2>&1
    Write-Success "Pip is accessible globally: $pipVer"
} catch {
    Write-ErrorMsg "Could not verify Python or Pip globally. They might have been installed but the PATH hasn't updated in this session."
    Write-Host "Fallback Verification: Please close this PowerShell window, open a new one, and type 'python --version'." -ForegroundColor Yellow
}

Write-Step "Verifying Node.js Installation..."
try {
    $nodeVer = node --version 2>&1
    Write-Success "Node.js is accessible globally: $nodeVer"
} catch {
    Write-Host "Node verification failed. You may need to restart your terminal." -ForegroundColor Yellow
}

Write-Success "Environment Setup Complete! You are ready to deploy your project."
