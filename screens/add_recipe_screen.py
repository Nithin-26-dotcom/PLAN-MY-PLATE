from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.app import App

class AddRecipeScreen(Screen):
    def add_ingredient(self):
        ingredient_num = len(self.ids.ingredients_container.children) + 1
        new_ingredient = TextInput(
            hint_text=f"Ingredient {ingredient_num}",
            size_hint_x=None,
            width=100,
            height=40,
            background_color=(0.98, 0.96, 0.91, 1),
            foreground_color=(0.2, 0.2, 0.1, 1),  
            hint_text_color=(0.5, 0.4, 0.3, 1)
        )
        self.ids.ingredients_container.add_widget(new_ingredient)

    def add_step(self):
        step_num = len(self.ids.steps_container.children) + 1
        new_step = TextInput(
            hint_text=f"Step {step_num}",
            multiline=True,
            size_hint_y=None,
            height=80,
            background_color=(0.98, 0.96, 0.91, 1),
            foreground_color=(0.2, 0.2, 0.1, 1),  
            hint_text_color=(0.5, 0.4, 0.3, 1),
        )
        self.ids.steps_container.add_widget(new_step)

    def finish_recipe(self):
        title = self.ids.title_input.text
        ingredients = [child.text for child in reversed(self.ids.ingredients_container.children) if isinstance(child, TextInput)]
        steps = [child.text for child in reversed(self.ids.steps_container.children) if isinstance(child, TextInput)]
        
        app = App.get_running_app()
        username = app.current_username
        app.db.save_recipe(title, ingredients, steps, username)
        main_interface_screen = app.root.get_screen('main_interface')
        main_interface_screen.switch_content("home")