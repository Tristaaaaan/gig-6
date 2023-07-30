from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivymd.uix.button import MDRaisedButton
from jnius import autoclass, PythonJavaClass, java_method

# Load KivyMD theme
Builder.load_string('''
BoxLayout:
    orientation: 'vertical'
    
    MDRaisedButton:
        text: "Check Bluetooth Status"
        on_release: app.check_bluetooth_status()

    MDLabel:
        id: status_label
        text: app.bluetooth_status_text
        halign: 'center'
        theme_text_color: 'Secondary'
''')

class BluetoothStatus(PythonJavaClass):
    __javainterfaces__ = ['android/content/Context']

    def __init__(self):
        super().__init__()

    @java_method('(Ljava/lang/String;)Z')
    def isBluetoothEnabled(self, service):
        BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
        adapter = BluetoothAdapter.getDefaultAdapter()
        if adapter:
            return adapter.isEnabled()
        return False
    
class MyApp(App):
    bluetooth_status_text = StringProperty("")

    def build(self):
        return Builder.load_string(kv)

    def check_bluetooth_status(self):
        try:
            context = autoclass('org.kivy.android.PythonActivity').mActivity
            bt_status = BluetoothStatus()
            is_enabled = bt_status.isBluetoothEnabled(context)
            if is_enabled:
                self.bluetooth_status_text = "Bluetooth is ON"
            else:
                self.bluetooth_status_text = "Bluetooth is OFF"
        except Exception as e:
            self.bluetooth_status_text = "Error: " + str(e)

if __name__ == '__main__':
    MyApp().run()