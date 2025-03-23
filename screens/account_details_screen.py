from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.app import App

class AccountDetailsScreen(Screen):
    def on_kv_post(self, base_widget):
        self.display_user_details()

    def display_user_details(self):
        app = App.get_running_app()
        current_user = app.current_username
        self.ids.username_label.text = f"User: {current_user}"

        try:
            recipes = app.db.get_user_recipes(current_user)
            recipes_display_text = "\n".join(recipes) if recipes else "No recipes found."
            self.ids.recipes_display.text = recipes_display_text
            self.ids.error_label.text = ""  
        except Exception as e:
            self.ids.error_label.text = f"Error fetching recipes: {str(e)}"
            self.ids.recipes_display.text = "" 
    def logout(self, *args):
        app = App.get_running_app()
        app.current_username = None
        app.root.current = 'login'
