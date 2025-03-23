import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name="planmyplate.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_users_table()
        self.create_recipes_table()
        self.create_favourites_table()
        self.cursor.execute("SELECT COUNT(*) FROM recipes")
        recipe_count = int(self.cursor.fetchone()[0])

        if recipe_count == 0:
            sample_username = "sample"
            self.add_user(sample_username, "123")
            self.add_sample_recipes(sample_username)

    def create_users_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        self.connection.commit()

    def create_recipes_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS recipes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                ingredients TEXT NOT NULL,
                steps TEXT NOT NULL,
                username TEXT NOT NULL,
                date TEXT NOT NULL
            )
        ''')
        self.connection.commit()

    def create_favourites_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS favourites (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                ingredients TEXT NOT NULL,
                user TEXT NOT NULL
            )
        ''')
        self.connection.commit()


    def add_user(self, username, password):
        try:
            self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def validate_login(self, username, password):
        self.cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        return self.cursor.fetchone() is not None

    def save_recipe(self, title, ingredients, steps, username):
        ingredients_str = ', '.join(ingredients)
        steps_str = '\n'.join(steps)
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute("INSERT INTO recipes (title, ingredients, steps, username, date) VALUES (?, ?, ?, ?, ?)",
                            (title, ingredients_str, steps_str, username, date))
        self.connection.commit()

    def get_user_recipes(self, username):
        self.cursor.execute("SELECT title FROM recipes WHERE username = ?", (username,))
        return [row[0] for row in self.cursor.fetchall()]

    def get_all_users(self):
        self.cursor.execute("SELECT * FROM users")
        return self.cursor.fetchall()

    def get_all_recipes(self):
        self.cursor.execute("SELECT * FROM recipes")
        return self.cursor.fetchall()

    def close(self):
        self.connection.close()

    def add_sample_recipes(self, username):
        
        sample_recipes = [
            {
                "title": "Spaghetti Aglio e Olio",
                "ingredients": [
                    "200g spaghetti", 
                    "4 cloves garlic, sliced", 
                    "60ml olive oil", 
                    "1 tsp red pepper flakes", 
                    "Salt to taste", 
                    "Fresh parsley, chopped"
                ],
                "steps": [
                    "Cook spaghetti according to package instructions until al dente. Drain and set aside.", 
                    "In a large skillet, heat olive oil over medium heat.", 
                    "Add sliced garlic and red pepper flakes, cooking until the garlic is golden.", 
                    "Toss in the cooked spaghetti and season with salt.", 
                    "Garnish with chopped parsley before serving."
                ]
            },
            {
                "title": "Vegetable Stir-Fry",
                "ingredients": [
                    "1 cup broccoli florets", 
                    "1 cup bell peppers, sliced", 
                    "1 cup carrots, sliced", 
                    "2 tbsp soy sauce", 
                    "1 tbsp sesame oil", 
                    "1 clove garlic, minced"
                ],
                "steps": [
                    "Heat sesame oil in a wok over high heat.", 
                    "Add garlic and sauté for 30 seconds.", 
                    "Add broccoli, bell peppers, and carrots; stir-fry for 5-7 minutes.", 
                    "Pour in soy sauce and stir until vegetables are tender-crisp.", 
                    "Serve hot over rice or noodles."
                ]
            },
            {
                "title": "Chicken Tacos",
                "ingredients": [
                    "500g chicken breast, cooked and shredded", 
                    "8 small tortillas", 
                    "1 cup lettuce, shredded", 
                    "1 cup tomatoes, diced", 
                    "1 cup cheese, shredded", 
                    "Salsa and sour cream (for serving)"
                ],
                "steps": [
                    "Warm the tortillas in a skillet or microwave.", 
                    "Fill each tortilla with shredded chicken, lettuce, tomatoes, and cheese.", 
                    "Top with salsa and sour cream before serving."
                ]
            },
            {
                "title": "Banana Pancakes",
                "ingredients": [
                    "1 cup flour", 
                    "2 ripe bananas, mashed", 
                    "1 cup milk", 
                    "1 egg", 
                    "2 tbsp sugar", 
                    "1 tsp baking powder", 
                    "Butter (for cooking)"
                ],
                "steps": [
                    "In a bowl, mix flour, sugar, and baking powder.", 
                    "In another bowl, combine mashed bananas, milk, and egg.", 
                    "Pour the wet ingredients into the dry ingredients and mix until just combined.", 
                    "Heat a skillet over medium heat and add butter.", 
                    "Pour batter onto the skillet to form pancakes, cooking until bubbles form on the surface. Flip and cook until golden brown."
                ]
            },
            {
                "title": "Caprese Salad",
                "ingredients": [
                    "2 large tomatoes, sliced", 
                    "1 ball of fresh mozzarella cheese, sliced", 
                    "Fresh basil leaves", 
                    "2 tbsp olive oil", 
                    "Salt and pepper to taste"
                ],
                "steps": [
                    "Layer tomato slices and mozzarella slices on a plate.", 
                    "Tuck fresh basil leaves between layers.", 
                    "Drizzle with olive oil and season with salt and pepper before serving."
                ]
            }
        ]

        for recipe in sample_recipes:
            self.save_recipe(recipe["title"], recipe["ingredients"], recipe["steps"], username)
