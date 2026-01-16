from tkinter import *
from tkinter import messagebox
from config import *
from utils import generate_strong_password, copy_to_clipboard
from data_manager import DataManager

class PasswordManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("KeeP - Secure Manager")
        self.root.config(padx=50, pady=50, bg=THEME_COLOR)
        
        self.data_manager = DataManager()
        
        self._setup_ui()

    def _setup_ui(self):
        # logo
        self.canvas = Canvas(height=200, width=200, bg=THEME_COLOR, highlightthickness=0)
        self._draw_lock_icon() # cool feature
        self.canvas.grid(row=0, column=1)

        # labels
        Label(text="Website:", bg=THEME_COLOR, font=FONT_MAIN).grid(row=1, column=0)
        Label(text="Email/Username:", bg=THEME_COLOR, font=FONT_MAIN).grid(row=2, column=0)
        Label(text="Password:", bg=THEME_COLOR, font=FONT_MAIN).grid(row=3, column=0)

        # entries
        self.website_entry = Entry(width=30)
        self.website_entry.grid(row=1, column=1, sticky="W")
        self.website_entry.focus()

        self.email_entry = Entry(width=52)
        self.email_entry.grid(row=2, column=1, columnspan=2, sticky="W")
        self.email_entry.insert(0, "user@example.com") 

        self.password_entry = Entry(width=30)
        self.password_entry.grid(row=3, column=1, sticky="W")

        # buttons
        self.btn_search = Button(text="Search", width=14, command=self.search_password)
        self.btn_search.grid(row=1, column=2)

        self.btn_generate = Button(text="Generate Password", command=self.generate_password)
        self.btn_generate.grid(row=3, column=2)

        self.btn_add = Button(text="Add to Vault", width=44, command=self.save_password)
        self.btn_add.grid(row=4, column=1, columnspan=2, pady=10)

    def _draw_lock_icon(self):
        self.canvas.create_arc(70, 20, 130, 120, start=0, extent=180, 
                               style=ARC, outline="#E7305B", width=15)
        self.canvas.create_rectangle(50, 70, 150, 170, fill="#E7305B", outline="")
        self.canvas.create_oval(90, 105, 110, 125, fill="white")
        self.canvas.create_line(100, 125, 100, 145, fill="white", width=4)

    def generate_password(self):
        password = generate_strong_password()
        self.password_entry.delete(0, END)
        self.password_entry.insert(0, password)
        
        # copy to clipboard and notify
        copy_to_clipboard(password, self.root)
        messagebox.showinfo(title="Success", message="Password copied to clipboard!\n(Will clear in 60s)")

    def save_password(self):
        website = self.website_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        if not website or not password or not email:
            messagebox.showwarning(title="Oops", message="Please don't leave any fields empty!")
            return

        is_ok = messagebox.askokcancel(title=website, 
                                       message=f"Save details?\nEmail: {email}\nPassword: {password}")
        if is_ok:
            success = self.data_manager.save_entry(website, email, password)
            if success:
                self.website_entry.delete(0, END)
                self.password_entry.delete(0, END)
                messagebox.showinfo("Saved", "Entry added to vault.")

    def search_password(self):
        website = self.website_entry.get().strip()
        if not website:
            return

        key, result = self.data_manager.search_entry(website)
        
        if result:
            email = result.get("email")
            password = result.get("password")
            messagebox.showinfo(title=key, message=f"Email: {email}\nPassword: {password}")
            
            copy_to_clipboard(password, self.root)
        else:
            messagebox.showerror(title="Not Found", message=f"No details for {website} exists.")

if __name__ == "__main__":
    window = Tk()
    app = PasswordManagerApp(window)
    window.mainloop()