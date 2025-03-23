from kivy.uix.screenmanager import Screen
import google.generativeai as genai
from db import Database
from kivy.app import App


class AIGenScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database()  
        self.api_key = "AIzaSyCOZh59AMq_WVWUD8swvAKs_KKoN9ruB9o"  
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def generate_recipe(self):
        ingredients = self.ids.ingredients_input.text
        prompt = (
            f"Create a recipe using the following ingredients: {ingredients}. "
            "Include a title(max limit of title is 25 characters), additional ingredients if necessary, and detailed steps. "
            "Instructions for how to prompt are: first line should have only title, "
            "second line should have only Ingredients: ingredients separated by comma, "
            "and third line should have Steps: paragraph of steps (that is no next line and steps are separated by period."
        )
        
        response = self.model.generate_content(prompt)
        r = response.text
        recipe_details = r.strip().splitlines()
        if len(recipe_details) >= 3:
            self.ids.output_label.text = recipe_details[0]  
            self.ids.steps_output.text = recipe_details[4].replace("Steps:", "").strip()  
            self.ingredients = recipe_details[2].replace("Ingredients:", "").strip() 

    def save_generated_recipe(self):
        title = self.ids.output_label.text
        ingredients = self.ingredients.split(', ')  
        steps = self.ids.steps_output.text.split('. ')  
        
        if title and ingredients and steps:
            app = App.get_running_app()
            username = app.current_username
            self.db.save_recipe(title, ingredients, steps, username)
            self.ids.output_label.text = "Recipe saved!"
            self.ids.ingredients_input.text = ""
            main_interface_screen = app.root.get_screen('main_interface')
            main_interface_screen.switch_content("home")

        else:
            self.ids.output_label.text = "Error: Fill in all fields before saving."

        
