
import hid
import time
import serial

path = b'\\\\?\\HID#VID_16C0&PID_05DF#8&20d8742f&0&0000#{4d1e55b2-f16f-11cf-88cb-001111000030}'
device_path = b'\\\\?\\HID#VID_16C0&PID_05DF#8&e1ec38a&0&0000#{4d1e55b2-f16f-11cf-88cb-001111000030}'



def terminate():
    device = hid.device()
    device.open_path(device_path)


    for i in range(1, 9):
        cmd = [0x00, 0xFD, i]
        device.send_feature_report(cmd)
    '''
    device = hid.device()
    device.open_path(device_path)


    for i in range(1, 9):
        cmd = [0x00, 0xFD, i]
        device.send_feature_report(cmd)
    '''

if __name__ == '__main__':
    for device in hid.enumerate():
        print(f"Device Info:\n{'-'*40}")
        for key, value in device.items():
            print(f"{key}: {value}")
        print("\n")

    device = hid.device()
    device.open_path(device_path)
    cmd = [0x00, 0xFD, 3]
    device.send_feature_report(cmd)
    cmd = [0x00, 0xFD, 4]
    device.send_feature_report(cmd)


'''
if __name__ == '__main__':
    device = hid.device()
    device.open_path(path)
    cmd = [0x00, 0xFF, 1]
    device.send_feature_report(cmd)
    cmd = [0x00, 0xFF, 2]
    device.send_feature_report(cmd)
    '''