from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.button import MDFlatButton
from kivymd.app import MDApp
from kivymd.toast import toast
from kivy import platform

from jnius import autoclass, cast

# Load the Java class
BluetoothScanner = autoclass("org.test.app.BluetoothScanner")


if platform == "android":
    from android.permissions import request_permissions, Permission
    request_permissions(
        [Permission.BLUETOOTH_SCAN, Permission.BLUETOOTH_ADMIN, Permission.BLUETOOTH])


class FirstWindow(Screen):

    Builder.load_file('firstwindow.kv')

    def start_bluetooth_scan(self):
        # Check if Bluetooth is supported and enabled
        if BluetoothScanner(context=None).bluetoothAdapter is None:
            toast("Bluetooth is not supported on this device.")
            return

        # Call the Java method to scan for devices
        bluetooth_scanner = BluetoothScanner(
            context=cast('android.content.Context', self))
        devices_list = bluetooth_scanner.scanDevices()

        # Display the list of detected devices
        if devices_list:
            toast("Available Bluetooth devices:\n" + "\n".join(devices_list))
        else:
            toast("No Bluetooth devices found.")


class WindowManager(ScreenManager):
    pass


class rawApp(MDApp):

    def build(self):

        return WindowManager()


if __name__ == '__main__':
    rawApp().run()
