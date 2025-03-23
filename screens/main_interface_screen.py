from kivy.uix.screenmanager import Screen
from .add_recipe_screen import AddRecipeScreen
from .home_screen import HomeScreen
from .favourites_screen import FavouritesScreen
from .ai_gen_screen import AIGenScreen
from .account_details_screen import AccountDetailsScreen

class MainInterfaceScreen(Screen):
    def on_kv_post(self, base_widget):
        self.ids.content_area.add_widget(HomeScreen())

    def switch_content(self, screen_name):
        self.ids.content_area.clear_widgets()  
        if screen_name == "add_recipe":
            self.ids.content_area.add_widget(AddRecipeScreen())
        elif screen_name == "home":
            self.ids.content_area.add_widget(HomeScreen())
        elif screen_name == "favourites":
            self.ids.content_area.add_widget(FavouritesScreen())
        elif screen_name == "ai_gen":
            self.ids.content_area.add_widget(AIGenScreen())
        elif screen_name == "account_details":
            self.ids.content_area.add_widget(AccountDetailsScreen())

           
