from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.clock import Clock
from kivy.core.clipboard import Clipboard
import pyttsx3
import google.generativeai as genai
import threading

class RecipeDetailsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        genai.configure(api_key="AIzaSyCOZh59AMq_WVWUD8swvAKs_KKoN9ruB9o")
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        self.original_ingredients = ""
        self.updated_ingredients = ""
        self.engine = pyttsx3.init()  
        self.is_reading = False
        self.reading_thread = None
        
    def on_enter(self):
        self.ids.message_label.text = ""
        self.ids.people_input.text = ""
        app = App.get_running_app()
        title = app.selected_title
        app.db.cursor.execute("SELECT title, ingredients, steps FROM recipes WHERE title=?", (title,))
        recipe = app.db.cursor.fetchone()

        if recipe:
            title, ingredients, steps = recipe
            self.original_ingredients = ingredients  
            formatted_ingredients = "\n".join(f"• {ingredient.strip()}" for ingredient in ingredients.split(','))
            formatted_steps = "\n".join(f"• {step.strip()}" for step in steps.split('\n') if step)

            self.ids.title_label.text = f"Title: {title}"
            self.ids.ingredients_label.text = f"Ingredients:\n{formatted_ingredients}"
            self.ids.steps_label.text = f"Steps:\n{formatted_steps}"


    def update_ingredients_for_n_people(self):
        try:
            num_people = int(self.ids.people_input.text)
            title = self.ids.title_label.text.replace("Title: ", "")
            prompt = (
                f"Given the recipe titled '{title}' with the following ingredients: {self.original_ingredients}. "
                f"Update the ingredients' quantities to serve {num_people} people and return them in the format: "
                "Ingredients: ingredient1, ingredient2, ..."
            )

            response = self.model.generate_content(prompt)
            self.updated_ingredients = response.text.strip().replace("Ingredients:", "").strip()
            formatted_updated_ingredients = "\n".join(f"• {ingredient.strip()}" for ingredient in self.updated_ingredients.split(','))

            self.ids.ingredients_label.text = f"Ingredients (for {num_people} people):\n {formatted_updated_ingredients}"
        except ValueError:
            self.ids.ingredients_label.text = "Invalid number of people. Please enter a valid number."

    def add_to_favourites(self):
            app = App.get_running_app()
            user = app.current_username
            title = self.ids.title_label.text.replace("Title: ", "")
            app.db.cursor.execute("SELECT * FROM favourites WHERE user=? AND title=?", (user, title))
            existing_recipe = app.db.cursor.fetchone()
            if existing_recipe:
                self.ids.message_label.text = "Already added to your favourites"
            else:
                ingredients = self.original_ingredients  
                app.db.cursor.execute(
                "INSERT INTO favourites (title, ingredients, user) VALUES (?, ?, ?)",
                (title, ingredients, user)
            )
                app.db.connection.commit()
                self.ids.message_label.text = "Recipe added to your favourites"

            Clock.schedule_once(self.reset_message_label, 1.5)

    def reset_message_label(self, dt):
        self.ids.message_label.text = ""

    def calculate_calories(self):
        try:
            if self.updated_ingredients == "":
                self.ids.calories_label.text = "Update Ingredients first!"
            else:
                title = self.ids.title_label.text.replace("Title: ", "")
                prompt = (
                    f"Given the following ingredients for the recipe titled '{title}': {self.updated_ingredients}. "
                    "Calculate the approximate total calories for these ingredients and return the result in given format.(do not change calories value for same set of ingredients i.e. prompt same value for every same set of ingredients.No other format or extra prompt is allowed).format:"
                    "Calories: XXXX kcal."
                )

                response = self.model.generate_content(prompt)
                total_calories = response.text.strip().replace("Calories:", "").strip()

                self.ids.calories_label.text = f"Total Calories: {total_calories}"
        except Exception as e:
            self.ids.calories_label.text = f"Error calculating calories: {str(e)}"
    def copy_to_clipboard(self):
        content = (
            f"{self.ids.title_label.text}\n\n"
            f"{self.ids.ingredients_label.text}\n\n"
            f"{self.ids.steps_label.text}"
        )
        Clipboard.copy(content)
        self.ids.copy_button.text = "Copied"
        self.ids.copy_button.background_color=(0.5, 0.8, 0.2, 1)
        self.ids.message_label.text = "Recipe copied to clipboard!"
        Clock.schedule_once(self.set_copy_button, 2)
        Clock.schedule_once(self.reset_message_label, 1.5)
        
        

    def set_copy_button(self, dt):
        self.ids.copy_button.text = "Copy"
        self.ids.copy_button.background_color=(0.82, 0.52, 0.25, 0.8)

    def read_aloud(self):
        if not self.is_reading:
            title = self.ids.title_label.text
            ingredients = self.ids.ingredients_label.text
            steps = self.ids.steps_label.text

            full_text = f"{title}\n{ingredients}\n{steps}"

            self.reading_thread = threading.Thread(target=self._read_aloud, args=(full_text,))
            self.reading_thread.start()

            self.is_reading = True  
            self.ids.message_label.text = "Reading aloud started." 
        else:
            self.ids.message_label.text = "Already reading aloud."

    def _read_aloud(self, text):
        self.engine.say(text)
        self.engine.runAndWait()
        Clock.schedule_once(self.on_reading_finished)  

    def on_reading_finished(self, dt):
        self.is_reading = False 
        
    def stop_reading(self):
        if self.is_reading:
            self.engine.stop() 
            self.is_reading = False  
            self.ids.message_label.text = "Reading stopped." 
            Clock.schedule_once(self.reset_message_label, 1.5)  
