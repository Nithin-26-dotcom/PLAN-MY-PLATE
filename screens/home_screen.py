from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.clock import Clock
from kivy.metrics import dp


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        self.recipes = []  
        Clock.schedule_once(self.update_columns)

    def on_kv_post(self, base_widget):
        self.load_recipes()
        self.bind(size=self.update_columns)  
    
    def update_columns(self, *args):
        grid_layout = self.ids.recipes_container
        grid_layout.cols = self.calculate_columns()  

    def calculate_columns(self):
        screen_width = self.width
        button_width = dp(230)  
        return max(1, int(screen_width / button_width))

    def load_recipes(self):
        self.ids.recipes_container.clear_widgets()
        
        app = App.get_running_app()
        app.db.cursor.execute("SELECT title,ingredients FROM recipes ORDER BY date DESC")        
        self.recipes = app.db.cursor.fetchall() 

        for (title,ingredients) in self.recipes:
            self.add_recipe_button(title,ingredients)

    def add_recipe_button(self, title, ingredients):
        ingredients_list = ingredients.split(',')[:3]
        formatted_ingredients = '\n'.join(f"• {ingredient.strip()}" for ingredient in ingredients_list)
        button_text = f"{title}\n{formatted_ingredients}"

        btn = Button(
            text=button_text,
            size_hint_y=None,
            height=dp(100),  
            background_color=(0.82, 0.52, 0.25, 0.5),  
            color=(0.1, 0.1, 0.1, 1),
            halign='left',
            valign='middle',
            padding=(10, 10)  
        )
       
        btn.bind(on_release=lambda instance, t=title: self.open_recipe_detail(t))
        self.ids.recipes_container.add_widget(btn)

    def update_recipes(self, search_text):
        self.ids.recipes_container.clear_widgets()
        app = App.get_running_app()
        app.db.cursor.execute("SELECT title,ingredients FROM recipes ORDER BY date DESC")        
        self.recipes = app.db.cursor.fetchall()

        filtered_recipes = [
            (title, ingredients) for (title,ingredients) in self.recipes
            if search_text.lower() in title.lower() or search_text.lower() in ingredients.lower()
        ]

        for title, ingredients in filtered_recipes:
            self.add_recipe_button(title, ingredients)


    def open_recipe_detail(self, title):
        app = App.get_running_app()
        app.selected_title = title
        app.root.current = 'recipe_details'
