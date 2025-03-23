from kivy.uix.screenmanager import Screen
from kivy.app import App

class LoginScreen(Screen):
    def validate_login(self):
        username = self.ids.username_input.text
        password = self.ids.password_input.text

        app = App.get_running_app()
        if app.db.validate_login(username, password):
            self.manager.current = "main_interface"
            app.current_username = username  

            self.ids.login_error.text = ""
        else:
            self.ids.login_error.text = "Invalid username or password. Please try again."

    def go_to_register(self):
        self.manager.current = "register"