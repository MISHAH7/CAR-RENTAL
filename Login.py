import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import sys

class Login:
    def __init__(self):
        # Create panels
        self.mini_panel = tk.Frame(bg="blue")
        self.main_panel = tk.Frame()
        
        # Create buttons
        self.close_button = tk.Button(self.mini_panel, text="Close", width=10, height=1, command=self.handle_close)
        self.login_button = tk.Button(self.mini_panel, text="Login", width=10, height=1, command=self.handle_login)
        
        # Create labels
        self.pw_label = tk.Label(self.mini_panel, text="Password", font=("Consolas", 18), fg="white", bg="blue", width=10)
        self.un_label = tk.Label(self.mini_panel, text="Username", font=("Consolas", 18), fg="white", bg="blue", width=10)
        self.info_label = tk.Label(self.mini_panel, text="Please Enter your Login Details", 
                                  font=("Consolas", 18, "bold"), fg="white", bg="blue")
        
        # Create text fields
        self.un_text_field = tk.Entry(self.mini_panel, width=20)
        self.password_field = tk.Entry(self.mini_panel, show="*", width=20)
        
        # Set up the main panel
        self.main_panel.configure(width=1366, height=730)
        
        # Try to load the background image
        try:
            self.bg_image = Image.open("c:\Users\User\Desktop\CAR RENTAL\LoginImage.JPG")
            self.bg_photo = ImageTk.PhotoImage(self.bg_image)
            self.image_label = tk.Label(self.main_panel, image=self.bg_photo)
            self.image_label.place(x=0, y=0)
        except Exception as e:
            print(f"Could not load background image: {e}")
            # Create a plain label as fallback
            self.image_label = tk.Label(self.main_panel, width=1366, height=730, bg="lightgray")
            self.image_label.place(x=0, y=0)
        
        # Add components to mini panel using grid
        self.info_label.grid(row=0, column=0, columnspan=2, pady=5)
        self.un_label.grid(row=1, column=0, sticky="w", padx=5)
        self.un_text_field.grid(row=1, column=1, padx=5, pady=2)
        self.pw_label.grid(row=2, column=0, sticky="w", padx=5)
        self.password_field.grid(row=2, column=1, padx=5, pady=2)
        
        # Create a frame for buttons to center them
        button_frame = tk.Frame(self.mini_panel, bg="blue")
        button_frame.grid(row=3, column=0, columnspan=2, pady=5)
        
        self.login_button.pack(side=tk.LEFT, padx=5)
        self.close_button.pack(side=tk.LEFT, padx=5)
        
        # Place mini panel on main panel
        self.mini_panel.place(x=50, y=150, width=350, height=125)
        
    def get_main_panel(self):
        return self.main_panel
    
    def handle_close(self):
        response = messagebox.askokcancel(
            "Close Confirmation",
            "You are about to terminate the program.\nAre you sure you want to continue?",
            icon=messagebox.WARNING
        )
        if response:
            sys.exit(0)
    
    def handle_login(self):
        username = self.un_text_field.get().strip().lower()
        password = self.password_field.get()
        
        if username == "admin" and password == "123":
            self.un_text_field.delete(0, tk.END)
            self.password_field.delete(0, tk.END)
            
            # Close current window and open main menu
            runner.get_frame().destroy()
            parent_frame = ParentJFrame()
            menu = MainMenu()
            main_frame = parent_frame.get_main_frame()
            main_frame.add(menu.get_main_panel())
            main_frame.set_visible(True)
        else:
            messagebox.showerror("Error", "Invalid UserName/Password")


# Mock classes to simulate the Java structure
class Runner:
    _frame = None
    
    @staticmethod
    def get_frame():
        if Runner._frame is None:
            Runner._frame = tk.Tk()
            Runner._frame.title("Car Rental System")
            Runner._frame.geometry("1366x730")
        return Runner._frame


class ParentJFrame:
    _main_frame = None
    
    def __init__(self):
        ParentJFrame._main_frame = tk.Tk()
        ParentJFrame._main_frame.title("Car Rental Management System")
        ParentJFrame._main_frame.geometry("1366x730")
        ParentJFrame._main_frame.withdraw()  # Hide initially
    
    @staticmethod
    def get_main_frame():
        return ParentJFrame._main_frame


class MainMenu:
    def __init__(self):
        self.main_panel = tk.Frame()
        # Add menu components here
    
    def get_main_panel(self):
        return self.main_panel


# Example usage
if __name__ == "__main__":
    runner = Runner()
    root = runner.get_frame()
    login = Login()
    root.add_widget = lambda widget: widget.pack(fill=tk.BOTH, expand=True)
    root.add_widget(login.get_main_panel())
    root.mainloop()