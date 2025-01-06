import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import requests
from io import BytesIO

class MealApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Meal Finder App")
        self.root.geometry("1000x800")
        self.root.minsize(900, 600)  # Minimum size to make it responsive
        self.root.configure(bg="#fff8e1") 

        # Header frame
        self.header_frame = tk.Frame(self.root, bg="#ff5722", height=100)  
        self.header_frame.pack(fill=tk.X)

        # Header label
        self.header_label = tk.Label(self.header_frame, text="Meal Finder", font=("Arial", 30, "bold"), fg="white", bg="#ff5722")
        self.header_label.pack(pady=20)

        # Search
        self.search_frame = tk.Frame(self.root, bg="#fff8e1")
        self.search_frame.pack(pady=10)

        self.search_label = tk.Label(self.search_frame, text="Search Meal:", font=("Arial", 14), fg="#333", bg="#fff8e1")
        self.search_label.grid(row=0, column=0, padx=10)

        self.search_entry = tk.Entry(self.search_frame, font=("Arial", 14), width=30, relief="flat", bg="#ffffff")
        self.search_entry.grid(row=0, column=1, padx=10)

        self.search_button = tk.Button(self.search_frame, text="Search", font=("Arial", 12), bg="#ffc107", fg="white", command=self.search_meal, relief="flat", cursor="hand2")
        self.search_button.grid(row=0, column=2, padx=10)

        self.random_button = tk.Button(self.search_frame, text="Random Meal", font=("Arial", 12), bg="#4caf50", fg="white", command=self.get_random_meal, relief="flat", cursor="hand2")
        self.random_button.grid(row=0, column=3, padx=10)

        self.first_letter_button = tk.Button(self.search_frame, text="Search by First Letter", font=("Arial", 12), bg="#2196f3", fg="white", command=self.search_by_first_letter, relief="flat", cursor="hand2")
        self.first_letter_button.grid(row=0, column=4, padx=10)

        # Guide label for lists
        self.guide_label = tk.Label(self.root, text="Use the buttons below to explore meal categories, areas, or ingredients.", font=("Arial", 12), fg="#333", bg="#fff8e1")
        self.guide_label.pack(pady=5)

        # Filter frame
        self.filters_frame = tk.Frame(self.root, bg="#fff8e1")
        self.filters_frame.pack(pady=10)

        self.filter_label = tk.Label(self.filters_frame, text="Filter by:", font=("Arial", 14), fg="#333", bg="#fff8e1")
        self.filter_label.grid(row=0, column=0, padx=10)

        self.filter_type = tk.StringVar(value="Category")
        self.filter_dropdown = ttk.Combobox(self.filters_frame, textvariable=self.filter_type, values=["Category", "Area", "Ingredient"], state="readonly")
        self.filter_dropdown.grid(row=0, column=1, padx=10)
        self.filter_dropdown.configure(foreground="black")

        self.filter_entry = tk.Entry(self.filters_frame, font=("Arial", 14), width=20, relief="flat", bg="#ffffff")
        self.filter_entry.grid(row=0, column=2, padx=10)

        self.filter_button = tk.Button(self.filters_frame, text="Apply Filter", font=("Arial", 12), bg="#ff9800", fg="white", command=self.filter_meals, relief="flat", cursor="hand2")
        self.filter_button.grid(row=0, column=3, padx=10)

        # Result frame
        self.results_frame = tk.Frame(self.root, bg="#fff8e1")
        self.results_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.results_tree = ttk.Treeview(self.results_frame, columns=("Meal", "Category", "Area"), show="headings")
        self.results_tree.heading("Meal", text="Meal")
        self.results_tree.heading("Category", text="Category")
        self.results_tree.heading("Area", text="Area")
        self.results_tree.column("Meal", width=300)
        self.results_tree.column("Category", width=200)
        self.results_tree.column("Area", width=200)
        self.results_tree.pack(fill=tk.BOTH, expand=True, pady=10, padx=10)

        # Style treeview
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 12), rowheight=25, background="#fff3e0")
        style.configure("Treeview.Heading", font=("Arial", 14, "bold"), background="#ff5722", foreground="black")

        # Single-click to treeview
        self.results_tree.bind("<ButtonRelease-1>", self.show_meal_details)

        # Image of the food
        self.image_label = tk.Label(self.root, bg="#fff8e1")
        self.image_label.pack(pady=20)

        # Extra buttons for new features
        self.extra_features_frame = tk.Frame(self.root, bg="#fff8e1")
        self.extra_features_frame.pack(pady=10)

        self.list_categories_button = tk.Button(self.extra_features_frame, text="List Categories", font=("Arial", 12), bg="#3f51b5", fg="white", command=self.list_categories, relief="flat", cursor="hand2")
        self.list_categories_button.grid(row=0, column=0, padx=10)

        self.list_areas_button = tk.Button(self.extra_features_frame, text="List Areas", font=("Arial", 12), bg="#673ab7", fg="white", command=self.list_areas, relief="flat", cursor="hand2")
        self.list_areas_button.grid(row=0, column=1, padx=10)

        self.list_ingredients_button = tk.Button(self.extra_features_frame, text="List Ingredients", font=("Arial", 12), bg="#009688", fg="white", command=self.list_ingredients, relief="flat", cursor="hand2")
        self.list_ingredients_button.grid(row=0, column=2, padx=10)

    def search_meal(self):
        query = self.search_entry.get()
        if not query:
            messagebox.showwarning("Input Error", "Please enter a meal name to search.")
            return
        self.fetch_meals(f"https://www.themealdb.com/api/json/v1/1/search.php?s={query}")

    def search_by_first_letter(self):
        query = self.search_entry.get()
        if not query or len(query) != 1:
            messagebox.showwarning("Input Error", "Please enter a single letter to search by first letter.")
            return
        self.fetch_meals(f"https://www.themealdb.com/api/json/v1/1/search.php?f={query}")

    def get_random_meal(self):
        self.fetch_meals("https://www.themealdb.com/api/json/v1/1/random.php")

    def filter_meals(self):
        filter_type = self.filter_type.get().lower()
        query = self.filter_entry.get()
        if not query:
            messagebox.showwarning("Input Error", f"Please enter a {filter_type} to filter by.")
            return
        self.fetch_meals(f"https://www.themealdb.com/api/json/v1/1/filter.php?{filter_type[0]}={query}")

    def fetch_meals(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            meals = data.get("meals")
            if not meals:
                messagebox.showinfo("No Results", "No meals found.")
                return

            self.results_tree.delete(*self.results_tree.get_children())
            for meal in meals:
                self.results_tree.insert("", tk.END, values=(meal.get("strMeal"), meal.get("strCategory", "N/A"), meal.get("strArea", "N/A")))

            self.adjust_treeview_columns()

        except requests.RequestException as e:
            messagebox.showerror("Error", f"Failed to retrieve data: {e}")

    def show_meal_details(self, event):
        selected_item = self.results_tree.selection()
        if not selected_item:
            return

        meal_name = self.results_tree.item(selected_item, "values")[0]

        try:
            url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={meal_name}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            meal = data.get("meals")[0]
            details = (
                f"Meal: {meal['strMeal']}\n"
                f"Category: {meal['strCategory']}\n"
                f"Area: {meal['strArea']}\n"
                f"\nIngredients:\n"
            )

            ingredients = "\n".join(
                f"{meal[f'strIngredient{i}']} - {meal[f'strMeasure{i}']}"
                for i in range(1, 21)
                if meal[f'strIngredient{i}']
            )

            details += f"{ingredients}\n\n--------------------\n\nInstructions:\n"

            instructions = meal['strInstructions'].split(". ")
            for idx, instruction in enumerate(instructions, 1):
                if instruction.strip():
                    details += f"{idx}. {instruction.strip()}\n"

            if meal['strMealThumb']:
                img_url = meal['strMealThumb']
                img_response = requests.get(img_url)
                img_data = BytesIO(img_response.content)
                img = Image.open(img_data)
                img = img.resize((250, 250))
                self.img_tk = ImageTk.PhotoImage(img)
                self.image_label.config(image=self.img_tk)

            messagebox.showinfo("Meal Details", details)

        except requests.RequestException as e:
            messagebox.showerror("Error", f"Failed to retrieve details: {e}")

    def list_categories(self):
        try:
            url = "https://www.themealdb.com/api/json/v1/1/categories.php"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            categories = data.get("categories", [])

            self.results_tree.delete(*self.results_tree.get_children())
            for category in categories:
                self.results_tree.insert("", tk.END, values=(category["strCategory"], category["strCategoryDescription"][:50], ""))

            self.adjust_treeview_columns()

        except requests.RequestException as e:
            messagebox.showerror("Error", f"Failed to retrieve categories: {e}")

    def list_areas(self):
        try:
            url = "https://www.themealdb.com/api/json/v1/1/list.php?a=list"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            areas = data.get("meals", [])

            self.results_tree.delete(*self.results_tree.get_children())
            for area in areas:
                self.results_tree.insert("", tk.END, values=(area["strArea"], "", ""))

            self.adjust_treeview_columns()

        except requests.RequestException as e:
            messagebox.showerror("Error", f"Failed to retrieve areas: {e}")

    def list_ingredients(self):
        try:
            url = "https://www.themealdb.com/api/json/v1/1/list.php?i=list"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            ingredients = data.get("meals", [])

            self.results_tree.delete(*self.results_tree.get_children())
            for ingredient in ingredients:
                self.results_tree.insert("", tk.END, values=(ingredient["strIngredient"], ingredient.get("strDescription", "")[:50], ""))

            self.adjust_treeview_columns()

        except requests.RequestException as e:
            messagebox.showerror("Error", f"Failed to retrieve ingredients: {e}")

    def adjust_treeview_columns(self):
        for col in self.results_tree["columns"]:
            self.results_tree.column(col, width=tk.font.Font().measure(col) + 50)

if __name__ == "__main__":
    root = tk.Tk()
    app = MealApp(root)
    root.mainloop()
