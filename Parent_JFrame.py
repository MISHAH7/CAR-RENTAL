import tkinter as tk
from tkinter import messagebox
import os
import subprocess
import sys

# These would be your other Python modules (converted from Java)
# from backend_code.booking import Booking
# from backend_code.car import Car
# from car_add import CarAdd
# from car_update import CarUpdate
# from car_remove import CarRemove
# from customer_add import CustomerAdd
# from customer_update import CustomerUpdate
# from customer_remove import CustomerRemove
# from car_owner_add import CarOwnerAdd
# from car_owner_update import CarOwnerUpdate
# from car_owner_remove import CarOwnerRemove

class ParentFrame:
    _main_frame = None
    
    def __init__(self):
        # Create the main frame
        ParentFrame._main_frame = tk.Tk()
        ParentFrame._main_frame.title("Rent-A-Car Management System")
        ParentFrame._main_frame.geometry("1366x730")
        
        # Set up window close handling
        ParentFrame._main_frame.protocol("WM_DELETE_WINDOW", self.on_window_close)
        
        # Create menu bar
        self.menu_bar = tk.Menu(ParentFrame._main_frame)
        
        # Create menu items
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.car_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.customer_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.car_owner_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        
        # Add commands to File menu
        self.file_menu.add_command(label="Exit", command=self.exit_app)
        
        # Add commands to Car menu
        self.car_menu.add_command(label="Add Car", command=self.add_car)
        self.car_menu.add_command(label="Update Car", command=self.update_car)
        self.car_menu.add_command(label="Remove Car", command=self.remove_car)
        self.car_menu.add_command(label="View booked Cars", command=self.view_booked_cars)
        self.car_menu.add_command(label="View Unbooked Cars", command=self.view_unbooked_cars)
        
        # Add commands to Customer menu
        self.customer_menu.add_command(label="Add Customer", command=self.add_customer)
        self.customer_menu.add_command(label="Update Customer", command=self.update_customer)
        self.customer_menu.add_command(label="Remove Customer", command=self.remove_customer)
        
        # Add commands to Car Owner menu
        self.car_owner_menu.add_command(label="Add Car Owner", command=self.add_car_owner)
        self.car_owner_menu.add_command(label="Update Car Owner", command=self.update_car_owner)
        self.car_owner_menu.add_command(label="Remove Car Owner", command=self.remove_car_owner)
        
        # Add commands to Help menu
        self.help_menu.add_command(label="View JavaDoc", command=self.view_javadoc)
        self.help_menu.add_command(label="View Documentation", command=self.view_documentation)
        self.help_menu.add_command(label="About", command=self.show_about)
        
        # Add menus to menu bar
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.menu_bar.add_cascade(label="Cars", menu=self.car_menu)
        self.menu_bar.add_cascade(label="Customer", menu=self.customer_menu)
        self.menu_bar.add_cascade(label="Car Owner", menu=self.car_owner_menu)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)
        
        # Set the menu bar
        ParentFrame._main_frame.config(menu=self.menu_bar)
    
    @staticmethod
    def get_main_frame():
        return ParentFrame._main_frame
    
    def on_window_close(self):
        confirm = messagebox.askokcancel(
            "Close Confirmation", 
            "You are about to terminate the program.\nAre you sure you want to continue?",
            icon="warning"
        )
        if confirm:
            sys.exit(0)
    
    def exit_app(self):
        self.on_window_close()
    
    def add_car(self):
        ParentFrame._main_frame.attributes("-disabled", True)
        # car_add = CarAdd()
        # car_add.setVisible(True)
        print("Add Car window opened")
    
    def update_car(self):
        ParentFrame._main_frame.attributes("-disabled", True)
        # car_update = CarUpdate()
        # car_update.setVisible(True)
        print("Update Car window opened")
    
    def remove_car(self):
        ParentFrame._main_frame.attributes("-disabled", True)
        # car_remove = CarRemove()
        # car_remove.setVisible(True)
        print("Remove Car window opened")
    
    def view_booked_cars(self):
        # In a real implementation, you would get the actual data
        # booked_cars = Booking.get_booked_cars()
        
        # For demonstration purposes
        booked_cars = []  # This would be populated with car objects
        
        if booked_cars:
            result = ""
            for i, car in enumerate(booked_cars):
                result += f"{i+1}: {car}\n"
        else:
            result = "No Cars are Booked!"
        
        messagebox.showinfo("Booked Cars", result)
    
    def view_unbooked_cars(self):
        # In a real implementation, you would get the actual data
        # unbooked_cars = Booking.get_unbooked_cars()
        
        # For demonstration purposes
        unbooked_cars = []  # This would be populated with car objects
        
        if unbooked_cars:
            result = ""
            for i, car in enumerate(unbooked_cars):
                result += f"{i+1}: {car}\n"
        else:
            result = "No UnBooked Cars are available!"
        
        messagebox.showinfo("Unbooked Cars", result)
    
    def add_customer(self):
        ParentFrame._main_frame.attributes("-disabled", True)
        # customer_add = CustomerAdd()
        # customer_add.frame.setVisible(True)
        print("Add Customer window opened")
    
    def update_customer(self):
        ParentFrame._main_frame.attributes("-disabled", True)
        # CustomerUpdate().frame.setVisible(True)
        print("Update Customer window opened")
    
    def remove_customer(self):
        ParentFrame._main_frame.attributes("-disabled", True)
        # CustomerRemove().frame.setVisible(True)
        print("Remove Customer window opened")
    
    def add_car_owner(self):
        ParentFrame._main_frame.attributes("-disabled", True)
        # car_owner_add = CarOwnerAdd()
        # car_owner_add.frame.setVisible(True)
        print("Add Car Owner window opened")
    
    def update_car_owner(self):
        ParentFrame._main_frame.attributes("-disabled", True)
        # CarOwnerUpdate().frame.setVisible(True)
        print("Update Car Owner window opened")
    
    def remove_car_owner(self):
        ParentFrame._main_frame.attributes("-disabled", True)
        # CarOwnerRemove().frame.setVisible(True)
        print("Remove Car Owner window opened")
    
    def view_javadoc(self):
        self._open_file("JavaDoc_Documentation_About.pdf")
    
    def view_documentation(self):
        self._open_file("JavaDoc_Documentation_About.pdf")
    
    def _open_file(self, filename):
        # Check if file exists and open it using the default application
        if os.path.exists(filename):
            try:
                if sys.platform == 'win32':
                    os.startfile(filename)
                elif sys.platform == 'darwin':  # macOS
                    subprocess.call(['open', filename])
                else:  # Linux
                    subprocess.call(['xdg-open', filename])
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open file: {e}")
        else:
            messagebox.showerror("Error", "Documentation not found!")
    
    def show_about(self):
        messagebox.showinfo("About", "THIS PROGRAM IS WRITTEN AS A SEMESTER PROJECT OF OBJECT ORIENTED PROGRAMMING BY EMMANUEL MAROA!")


# Example usage
if __name__ == "__main__":
    app = ParentFrame()
    ParentFrame.get_main_frame().mainloop()