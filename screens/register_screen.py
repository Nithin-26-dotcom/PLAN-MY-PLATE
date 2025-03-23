from kivy.uix.screenmanager import Screen
from kivy.app import App
import re

class RegisterScreen(Screen):
    def register_account(self):
        new_username = self.ids.new_username_input.text.strip()
        new_password = self.ids.new_password_input.text
        confirm_password = self.ids.confirm_password_input.text

        if not new_username or not new_password or not confirm_password:
            self.ids.register_error.text = "All fields are required."
            return

        if not self.is_valid_username(new_username):
            self.ids.register_error.text = "Invalid username. Only letters, numbers, '-' and '_' are allowed."
            return

        if new_password != confirm_password:
            self.ids.register_error.text = "Passwords do not match."
            return

        app = App.get_running_app()
        if app.db.add_user(new_username, new_password):
            self.manager.current = "login"
            self.ids.register_error.text = ""
        else:
            self.ids.register_error.text = "Username already exists. Please choose another."

    def go_to_login(self):
        self.manager.current = "login"

    def is_valid_username(self, username):
        return bool(re.match(r'^[\w-]+$', username))
