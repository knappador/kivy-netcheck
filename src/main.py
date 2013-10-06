from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.properties import StringProperty
from kivy.clock import Clock
from kivy.logger import Logger
from kivy import platform

import netcheck

import sys
import time
if sys.hexversion > 0x30000f0:
    # py3k hack
    import http.client as httplib
else:
    import httplib


class AskUser(RelativeLayout):
    ''' Callback(bool) if user wants to do something'''
    action_name = StringProperty()
    cancel_name = StringProperty()
    text = StringProperty()
    
    def __init__(self, 
                 action_name='Okay', 
                 cancel_name='Cancel', 
                 text='Are you Sure?',
                 callback=None, # Why would you do this?
                 *args, **kwargs):
        self.action_name = action_name
        self.cancel_name = cancel_name
        self._callback = callback
        self.text = text
        super(AskUser, self).__init__(*args, **kwargs)

    def answer(self, yesno):
        ''' Callbacks in prompts that open prompts lead to errant clicks'''
        app.modal.dismiss()
        if self._callback:
            def delay_me(*args):
                self._callback(yesno)
            Clock.schedule_once(delay_me, 0.1)


class DebugPanel(BoxLayout):
    def __init__(self, ncui, *args, **kwargs):
        super(DebugPanel, self).__init__(*args, **kwargs)
        self.mock_result.bind(active=ncui.set_mock_result)
        self.mock_settings_result.bind(active=ncui.set_mock_settings_result)
        self.mock_result.active = netcheck._get_ref().MOCK_RESULT
        self.mock_settings_result.active = \
        netcheck._get_ref().MOCK_SETTINGS_RESULT
        


class NetCheckUI(RelativeLayout):
    available=StringProperty('-')
    network_result=StringProperty('-')

    def __init__(self, **kwargs):
        super(NetCheckUI, self).__init__(**kwargs)
        if platform() != 'android':
            self.output.add_widget(DebugPanel(self))
        netcheck.set_prompt(self.ask_connect)

    def ask_connect(self, tried_connect_callback):
        Logger.info('Opening net connect prompt')
        text = ('You need internet access to do that.  Do you '
                'want to go to settings to try connecting?')
        content = AskUser(text=text,
                          action_name='Settings',
                          callback=tried_connect_callback,
                          auto_dismiss=False)
        p = Popup(title = 'Network Unavailable',
                  content = content,
                  size_hint=(0.8, 0.4),
                  pos_hint={'x':0.1, 'y': 0.35})
        app.modal = p
        p.open()

    def network_activity(self, available):
        self.display_network_available(available)
        if available:
            conn = httplib.HTTPConnection('www.google.com')
            conn.request("GET", "/index.html")
            r = conn.getresponse()
            self.network_result = '{} {} at {}'.format(r.status, 
                                                       r.reason,
                                                       time.strftime('%X'))
        else:
            self.network_result = 'No network available'

    def display_network_available(self, available):
        self.available = str(available) + ' at: ' + str(time.strftime('%X'))
        
    def set_mock_result(self, instance, available):
        Logger.info(str(available))
        netcheck._get_ref()._set_debug(MOCK_RESULT=available)

    def set_mock_settings_result(self, instance, available):
        netcheck._get_ref()._set_debug(MOCK_SETTINGS_RESULT=available)

            

class NetCheckApp(App):
    def __init__(self, *args, **kwargs):
        super(NetCheckApp, self).__init__(*args, **kwargs)
        global app
        app = self

    def build(self):
        return NetCheckUI()

    def on_pause(self):
        return True

    def on_resume(self):
        pass


if __name__ == '__main__':
    NetCheckApp().run()
