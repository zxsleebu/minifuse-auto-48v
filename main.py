import usb.core
import usb.util
import usb.backend.libusb1
import ctypes
import sys
import os

# --- CONFIGURATION ---
VENDOR_ID = 0x1c75

# Map Product IDs to Device Names
SUPPORTED_PIDS = {
    0xaf90: "Arturia MiniFuse 2",
    0xaf80: "Arturia MiniFuse 1"
}

lib_file = "./libusb-1.0.dll"

if not os.path.exists(lib_file):
    print("[-] Error: libusb-1.0.dll not found in this folder.")
    print("    Please download the 'VS2019/MS64' (if 64-bit) version of libusb-1.0.dll")
    print("    and put it next to this script.")
    sys.exit(1)

def set_phantom_power(turn_on=True):
    print(f"Looking for Arturia MiniFuse devices (VID: {hex(VENDOR_ID)})...")

    backend = usb.backend.libusb1.get_backend(find_library=lambda x: lib_file)
    
    if backend is None:
        print("[-] Error: Could not load the backend.")
        print("    Ensure your Python is 64-bit and you are using the 64-bit DLL (MS64).")
        sys.exit(1)

    try:
        # void libusb_set_option(ctx, option);
        backend.lib.libusb_set_option.argtypes = [ctypes.c_void_p, ctypes.c_int]
        
        res = backend.lib.libusb_set_option(backend.ctx, 1)
        
        if res == 0:
            print("[+] UsbDk mode enabled.")
        else:
            print(f"[-] Warning: Failed to enable UsbDk (Error Code: {res})")
            
    except Exception as e:
        print(f"[-] Could not set UsbDk option: {e}")
        print("    (Proceeding anyway, but it might fail...)")

    dev = None
    device_name = "Unknown"

    # Search for both MiniFuse 1 and 2
    for pid, name in SUPPORTED_PIDS.items():
        found = usb.core.find(idVendor=VENDOR_ID, idProduct=pid, backend=backend)
        if found:
            dev = found
            device_name = name
            print(f"[+] Found {device_name} (PID: {hex(pid)}) via UsbDk backend!")
            break

    if dev is None:
        print("[-] Device not found.")
        print("    1. Is the device plugged in?")
        print("    2. Is 'UsbDk Runtime Library' installed in Windows Settings?")
        print("    3. Did you reboot after installing UsbDk?")
        return

    bmRequestType = 0x21
    bRequest = 0x22
    wValue = 0x0400
    wIndex = 0x0000
    data = b'\x01\x00' if turn_on else b'\x00\x00'

    try:
        print(f"Sending +48V {'ON' if turn_on else 'OFF'} command to {device_name}...")
        dev.ctrl_transfer(bmRequestType, bRequest, wValue, wIndex, data)
        print("[+] SUCCESS! Phantom power switched.")
        
    except usb.core.USBError as e:
        print(f"[-] Command failed: {e}")
        if "NotImplemented" in str(e):
             print("    Error: The library is not using UsbDk. Try reinstalling UsbDk.")

if __name__ == "__main__":
    state = True
    if len(sys.argv) > 1 and sys.argv[1].lower() == "off":
        state = False
        
    set_phantom_power(state)
