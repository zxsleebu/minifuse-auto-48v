# Arturia MiniFuse Auto +48v

A Python script to programmatically toggle **+48V Phantom Power** on the **Arturia MiniFuse** audio interface. 

This script is specifically designed for **Windows**.

## Prerequisites

1.  **Python 3.x** (64-bit recommended)
2.  **UsbDk** (USB Development Kit)
3.  **libusb-1.0.dll**
4.  **pyusb** library
5.  Arturia Minifuse 1 or 2

## Installation Guide

### Step 1: Install Python Dependencies
Open your terminal (Command Prompt/PowerShell) and install `pyusb`:
```bash
pip install pyusb
```

### Step 2: Install UsbDk
The standard Windows driver locks the USB interface during audio playback. **UsbDk** allows us to bypass this lock.

1.  Download the latest **UsbDk_x.x.x_x64.msi** installer:  
    **[UsbDk Latest Release](https://github.com/daynix/UsbDk/releases/latest)**
2.  Run the installer.
3.  **Restart your computer.**.

### Step 3: Download the Library DLL
Python needs the low-level binary to talk to UsbDk.

1.  Download the latest **libusb** release (7z or zip):  
    **[libusb Latest Release](https://github.com/libusb/libusb/releases/latest)**
2.  Extract the archive.
3.  Navigate to `VS2019` -> `MS64`.
4.  Copy the file **`libusb-1.0.dll`** and paste it into the **same folder** as this script.

## Technical Details

**The Problem:** On Windows, audio interface drivers (ASIO/WASAPI) take exclusive control of the USB device interface.
Standard `pyusb` or `libusb` scripts fail with `Access Denied` or `Entity not found` because they cannot claim the interface.

**The Solution:** This script uses **UsbDk**, a filter driver framework. By setting the `LIBUSB_OPTION_USE_USBDK` flag via `ctypes`, we force `libusb` to route traffic through the UsbDk filter.
This allows us to inject the Control Transfer packet (Setup: `21 22 00 04`, Data: `01` or `00`) without detaching the kernel driver or interrupting audio streams.
These packets were dumped using Wireshark and USBPcap.

## Troubleshooting

*   **`Error: libusb-1.0.dll not found`**: Ensure the DLL is in the exact same folder as the script.
*   **`Device not found`**: 
    *  Ensure **UsbDk** is installed.
    *  Ensure you have **rebooted** after installing UsbDk.
    *  Check if the device is plugged in.
*   **`NotImplementedError` or `Access Denied`**: This means the script failed to activate UsbDk mode. Ensure you are using the latest `libusb-1.0.dll` (v1.0.22 or newer).
