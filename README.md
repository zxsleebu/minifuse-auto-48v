# Arturia MiniFuse CLI Control

A Python script to programmatically toggle **+48V Phantom Power**, **Direct Mono** and **Instrument** toggle on **Arturia MiniFuse** audio interfaces.

This script is specifically designed for **Windows** and leverages the official Arturia driver API to control the hardware without interrupting audio streams.

## Prerequisites

1.  **Python 3.x** (64-bit required)
2.  **Arturia MiniFuse Drivers** (Must be installed)
3.  Arturia MiniFuse 1 or 2

## Configuration

The script relies on the official Arturia API DLL (`arturiaminifuseusbaudioapi_x64.dll`).

By default, the script looks in the standard driver installation directory:

`C:\Program Files\Arturia\MiniFuseAudioDriver\x64\arturiaminifuseusbaudioapi_x64.dll`

If you installed the Arturia software to a custom location, open the Python script and update the `DLL_PATH` variable to match your system.

## Usage

Open a terminal (Command Prompt/PowerShell) in the directory containing the script.

```bash
python main.py [power|mono|inst] [on/off] (optional: channel number for inst [1-2])
```

### Direct Mono

**Turn ON:**
```bash
python main.py mono on
```

**Turn OFF:**
```bash
python main.py mono off
```

## Technical Details

**The Problem:** On Windows, audio interface drivers (ASIO/WASAPI) take exclusive control of the USB device interface. Methods using `pyusb` or `libusb` fail with `Access Denied` because they cannot claim the interface while audio is active.

**The Solution:** Instead of attempting to inject raw USB packets via filter drivers, this script loads the official Thesycon/Arturia API DLL. It invokes the exported function `TUSBAUDIO_AudioControlRequestSet` to send specific Vendor Requests to the hardware using Control Selectors `0x04` (Phantom Power), `0x05` (Direct Mono) and `0x00` (Instrument).

## Troubleshooting

*   **`Error: DLL not found`**: Verify that Arturia MiniFuse drivers are installed. If installed to a non-default location, edit the `DLL_PATH` variable in the script.
*   **`Error loading DLL`**: Ensure you are using a 64-bit version of Python, as the target API is a 64-bit DLL.
*   **`No devices found`**: Ensure the MiniFuse is connected and recognized by Windows Device Manager.
