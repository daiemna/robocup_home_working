from evdev import InputDevice, categorize, ecodes

key_map = {
    115: "FRWD",
    114: "BKWD",
    165: "LEFT",
    163: "RIGHT",
    164: "BTN_A",
    304: "SUPER_UP",
    305: "SUPER_DOWN",
}

remote = InputDevice("/dev/input/event2")
print("Device : {}".format(remote))

for event in remote.read_loop():
    c_event = categorize(event)
    # print("categorized event : {}".format())
    if event.type == ecodes.EV_KEY:
        print("key: {}".format(remote.active_keys(verbose=False)))