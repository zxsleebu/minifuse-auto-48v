import ctypes
import sys
import struct
import os

DLL_PATH = r"C:\Program Files\Arturia\MiniFuseAudioDriver\x64\arturiaminifuseusbaudioapi_x64.dll"

# Control Selectors
SELECTOR_PHANTOM_POWER = 4
SELECTOR_DIRECT_MONO   = 5

def set_minifuse_param(target_selector, turn_on):
    if not os.path.exists(DLL_PATH):
        print(f"[-] Error: DLL not found at {DLL_PATH}")
        return

    try:
        lib = ctypes.CDLL(DLL_PATH)
    except OSError as e:
        print(f"[-] Error loading DLL: {e}")
        return

    print("[+] Arturia API Loaded.")

    if hasattr(lib, 'TUSBAUDIO_EnumerateDevices'):
        lib.TUSBAUDIO_EnumerateDevices()

    lib.TUSBAUDIO_OpenDeviceByIndex.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_void_p)]
    lib.TUSBAUDIO_OpenDeviceByIndex.restype = ctypes.c_int
    
    handle = ctypes.c_void_p()
    res = lib.TUSBAUDIO_OpenDeviceByIndex(0, ctypes.byref(handle))
    
    if res != 0 or not handle:
        print(f"[-] Failed to open device. Error Code: {res}")
        return

    # print(f"[*] Device opened. Handle: {handle.value}")

    # TUsbAudioStatus TUSBAUDIO_AudioControlRequestSet(...)
    send_req = lib.TUSBAUDIO_AudioControlRequestSet
    send_req.argtypes = [
        ctypes.c_void_p,        # Handle
        ctypes.c_ubyte,         # EntityID
        ctypes.c_ubyte,         # Request
        ctypes.c_ubyte,         # ControlSelector
        ctypes.c_ubyte,         # Channel
        ctypes.c_void_p,        # Buffer Pointer
        ctypes.c_uint,          # Buffer Length
        ctypes.c_void_p,        # Bytes Transferred
        ctypes.c_uint           # Timeout
    ]
    send_req.restype = ctypes.c_int

    val = 1 if turn_on else 0
    data = struct.pack('<H', val) # 2 Bytes
    buf = ctypes.create_string_buffer(data)

    target_name = "Phantom Power" if target_selector == SELECTOR_PHANTOM_POWER else "Direct Mono"
    print(f"[*] Setting {target_name} to {'ON' if turn_on else 'OFF'}...")
    
    # Execute
    # EntityID = 0
    # Request = 34 (SET_CUR)
    # Selector = Passed Argument (4 or 5)
    # Channel = 0
    res = send_req(handle, 0, 34, target_selector, 0, buf, 2, None, 1000)

    if res == 0:
        print(f"[+] SUCCESS! {target_name} toggled.")
    else:
        print(f"[-] Command failed with Error Code: {res}")

    if hasattr(lib, 'TUSBAUDIO_CloseDevice'):
        lib.TUSBAUDIO_CloseDevice(handle)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python script.py power [on/off]")
        print("  python script.py mono [on/off]")
        sys.exit(1)

    target_cmd = sys.argv[1].lower()
    selector = None

    if target_cmd == "power":
        selector = SELECTOR_PHANTOM_POWER
    elif target_cmd == "mono":
        selector = SELECTOR_DIRECT_MONO
    else:
        print(f"[-] Unknown command: '{target_cmd}'. Use 'power' or 'mono'.")
        sys.exit(1)

    state = True # Default to ON
    if len(sys.argv) > 2:
        state_cmd = sys.argv[2].lower()
        if state_cmd == "off":
            state = False
        elif state_cmd == "on":
            state = True
        else:
            print(f"[-] Unknown state: '{state_cmd}'. Use 'on' or 'off'.")
            sys.exit(1)

    set_minifuse_param(selector, state)
