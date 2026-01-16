import json
import os
from tkinter import messagebox
from config import DATA_FILE

class DataManager:
    def load_data(self) -> dict:
        if not os.path.exists(DATA_FILE):
            return {}
        
        try:
            with open(DATA_FILE, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return {}

    def save_entry(self, website, email, password):
        new_data = {
            website: {
                "email": email,
                "password": password
            }
        }

        data = self.load_data()
        data.update(new_data)

        try:
            with open(DATA_FILE, "w") as file:
                json.dump(data, file, indent=4)
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Could not save data: {e}")
            return False

    def search_entry(self, website_query):
        data = self.load_data()
        
        key_map = {k.lower(): k for k in data.keys()}
        
        query_lower = website_query.lower()
        
        if query_lower in key_map:
            real_key = key_map[query_lower]
            return real_key, data[real_key]
        else:
            return None, None