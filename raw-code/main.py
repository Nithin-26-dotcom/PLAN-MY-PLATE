from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

# Store accounts as a dictionary for simplicity
USER_ACCOUNTS = {}

class LoginScreen(Screen):
    def validate_login(self):
        username = self.ids.username_input.text
        password = self.ids.password_input.text

        # Check if the credentials match any account
        if username in USER_ACCOUNTS and USER_ACCOUNTS[username] == password:
            self.manager.current = "main_interface"
        else:
            self.ids.login_error.text = "Invalid username or password. Try again."
  
    def go_to_register(self):
        self.manager.current = "register"

class RegisterScreen(Screen):
    def register_account(self):
        username = self.ids.new_username_input.text
        password = self.ids.new_password_input.text
        confirm_password = self.ids.confirm_password_input.text

        # Simple validation for empty fields
        if not username or not password:
            self.ids.register_error.text = "Fields cannot be empty."
            return
        
        if password != confirm_password:
            self.ids.register_error.text = "Passwords do not match."
            return

        if username in USER_ACCOUNTS:
            self.ids.register_error.text = "Username already exists."
            return
        
        # Save new account
        USER_ACCOUNTS[username] = password
        self.ids.register_error.text = "Account created! You can now log in."

        # Optionally, navigate back to login after registration
        self.manager.current = "login"

class MainInterfaceScreen(Screen):
    pass

class RecipeApp(App):
    def build(self):
        return Builder.load_file("recipe_app.kv")

if __name__ == '__main__':
    RecipeApp().run()
