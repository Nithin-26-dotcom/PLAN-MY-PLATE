from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from screens import LoginScreen, RegisterScreen, AddRecipeScreen, MainInterfaceScreen, HomeScreen, AccountDetailsScreen, RecipeDetailsScreen, AIGenScreen, FavouritesScreen
from db import Database

class RecipeApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database()  
        self.current_username = None
        self.selected_title = None 

    def build(self):
        self.title = "PlanMyPlate"
        Builder.load_file("kv/recipe_app.kv")

        sm = ScreenManager()
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(RegisterScreen(name="register"))
        sm.add_widget(MainInterfaceScreen(name="main_interface"))
        sm.add_widget(AddRecipeScreen(name="add_recipe"))
        sm.add_widget(HomeScreen(name="home_screen"))
        sm.add_widget(FavouritesScreen(name="favourites_screen"))
        sm.add_widget(AccountDetailsScreen(name="account_details")) 
        sm.add_widget(RecipeDetailsScreen(name="recipe_details"))
        sm.add_widget(AIGenScreen(name="ai_gen"))
        return sm

    def logout(self):
        self.current_username = None
        self.root.current = 'login'

if __name__ == "__main__":
    RecipeApp().run()
