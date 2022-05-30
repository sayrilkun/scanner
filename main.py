from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivymd.app import MDApp
from kivy_garden.zbarcam import ZBarCam
import pyrebase

from android.storage import app_storage_path, primary_external_storage_path, secondary_external_storage_path
from android.permissions import request_permissions, Permission

request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE, Permission.CAMERA])
primary_ext_storage = primary_external_storage_path()

config = {
    "apiKey": "AIzaSyBH3WOpmUdPj0vGIpneswkW2CS8fFidlXw",
    "authDomain": "pnri-demeter.firebaseapp.com",
    "databaseURL": "https://pnri-demeter-default-rtdb.firebaseio.com",
    "projectId": "pnri-demeter",
    "storageBucket": "pnri-demeter.appspot.com",
    "messagingSenderId": "456214792415",
    "appId": "1:456214792415:web:773d7ea18f8ba214df816a",
    "measurementId": "G-00QH790MRG",
}


firebase = pyrebase.initialize_app(config)
db= firebase.database()
class LoginScreen(Screen):
    pass

class QRScreen(Screen):
    pass

class ScannerScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self._after_init)
        # self.ids.zbarcam_id.ids.xcamera.play=True

    def _after_init(self, dt):
        """
        Binds `ZBarCam.on_symbols()` event.
        """
        zbarcam = self.ids.zbarcam_id
        zbarcam.bind(symbols=self.on_symbols)

    def on_symbols(self, zbarcam, symbols):
        self.ids.data.clear_widgets()

        """
        Loads the first symbol data to the `QRFoundScreen.data_property`.
        """
        # going from symbols found to no symbols found state would also
        # trigger `on_symbols`
        if not symbols:
            return

        # qrfound_screen = self.manager.current_screen
        symbol = symbols[0]
        data = symbol.data.decode('utf8')
        sub = 'ac&@%!'
        if sub in data:
            hey = db.child("Hoya").order_by_child("scan_id").equal_to(data).get()
            for user in hey.each():
                self.ids.data.text = user.key()  
        else:
            self.ids.data.text = "NO DOCUMENT AVAILABLE"

        print(data)
        # self.ids.data.text= data

        # self.manager.get_screen('qr').ids.data.text= data
        # self.manager.transition.direction = 'left'
        # self.manager.current = 'qr'
        # qrfound_screen.data_property = data



class DemoApp(MDApp):
    def sign_in(self):
        username = self.help.get_screen('login').ids.username.text
        password = self.help.get_screen('login').ids.password.text

        if username == 'admin' and password == '12345':
            self.help.current = 'menu'
            self.help.transition.direction = 'right'
        
        else:
            self.help.get_screen('login').ids.status.text = 'Invalid credentials. Please try again.'
    def build(self):
    # screen =Screen()
    
        self.title='Demeter'
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "LightGreen"   

        self.help = Builder.load_file('main.kv')
        # screen.add_widget(self.help)
        return self.help

DemoApp().run()