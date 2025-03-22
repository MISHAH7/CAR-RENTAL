import tkinter as tk
from tkinter import messagebox, ttk
import datetime
import re
from backend_code.car import Car
from backend_code.car_owner import CarOwner

class Car_Update(tk.Toplevel):
    """
    A window for updating car information
    """
    
    def __init__(self, parent):
        """Initialize the Car_Update window"""
        super().__init__(parent)
        self.title("Update Car")
        self.geometry("300x140")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.parent = parent
        
        # Center the window
        self.position_center()
        
        # Create GUI components
        self.car_id_label = tk.Label(self, text="Enter Car ID to be updated")
        self.car_id_textfield = tk.Entry(self, width=30)
        self.car_id_validity_label = tk.Label(self, text="", fg="red")
        
        self.update_button = tk.Button(self, text="Update", width=10, command=self.update_car)
        self.cancel_button = tk.Button(self, text="Cancel", width=10, command=self.on_close)
        
        # Layout components
        self.car_id_label.pack(pady=(10, 0))
        self.car_id_textfield.pack(pady=(5, 0))
        self.car_id_validity_label.pack(pady=(2, 10), fill=tk.X)
        
        button_frame = tk.Frame(self)
        button_frame.pack(pady=(0, 10))
        self.update_button.pack(side=tk.LEFT, padx=5, in_=button_frame)
        self.cancel_button.pack(side=tk.LEFT, padx=5, in_=button_frame)
        
        # Initialize car attribute
        self.car = None
        
        # Make this window modal
        self.transient(parent)
        self.grab_set()
    
    def position_center(self):
        """Center the window on the screen"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'+{x}+{y}')
    
    def update_car(self):
        """Handle the update car button action"""
        car_id = self.car_id_textfield.get().strip()
        
        if not car_id:
            self.car_id_validity_label.config(text="Enter Car ID!")
            return
            
        try:
            car_id_int = int(car_id)
            if car_id_int <= 0:
                self.car_id_validity_label.config(text="ID cannot be '0' or negative!")
                return
                
            # Clear any previous validation messages
            self.car_id_validity_label.config(text="")
            
            # Search for the car by ID
            self.car = Car.search_by_id(car_id_int)
            
            if self.car:
                # Show the inner update window
                Car_UpdateInner(self, self.car)
                self.withdraw()  # Hide this window
            else:
                messagebox.showerror("Error", "Car ID not found!")
                
        except ValueError:
            self.car_id_validity_label.config(text="Invalid ID!")
    
    def on_close(self):
        """Handle window close event"""
        self.parent.deiconify()  # Re-enable the parent window
        self.parent.focus_set()  # Set focus back to the parent window
        self.destroy()  # Close this window


class Car_UpdateInner(tk.Toplevel):
    """
    Inner window for updating car details
    """
    
    def __init__(self, parent, car):
        """Initialize the Car_UpdateInner window"""
        super().__init__(parent)
        self.title("Update Car")
        self.geometry("450x475")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        
        self.parent = parent
        self.car = car
        self.car_owner = None
        
        # Center the window
        self.position_center()
        
        # Create GUI components
        self.maker_label = tk.Label(self, text="Enter Maker", width=20, anchor="w")
        self.name_label = tk.Label(self, text="Enter Name", width=20, anchor="w")
        self.color_label = tk.Label(self, text="Enter Color", width=20, anchor="w")
        self.type_label = tk.Label(self, text="Enter Car type", width=20, anchor="w")
        self.seating_capacity_label = tk.Label(self, text="Enter Seating capacity", width=20, anchor="w")
        self.model_label = tk.Label(self, text="Enter Model", width=20, anchor="w")
        self.condition_label = tk.Label(self, text="Condition", width=20, anchor="w")
        self.reg_no_label = tk.Label(self, text="Enter Reg no (ABC-0123)", width=20, anchor="w")
        self.owner_id_label = tk.Label(self, text="Enter Owner ID", width=20, anchor="w")
        self.rent_per_hour_label = tk.Label(self, text="Enter Rent Per Hour (in PKR)", width=20, anchor="w")
        
        self.maker_validity_label = tk.Label(self, text="", fg="red")
        self.name_validity_label = tk.Label(self, text="", fg="red")
        self.reg_no_validity_label = tk.Label(self, text="", fg="red")
        self.owner_id_validity_label = tk.Label(self, text="", fg="red")
        self.rent_per_hour_validity_label = tk.Label(self, text="", fg="red")
        
        self.maker_textfield = tk.Entry(self, width=30)
        self.name_textfield = tk.Entry(self, width=30)
        self.reg_no_textfield = tk.Entry(self, width=30)
        self.owner_id_textfield = tk.Entry(self, width=30)
        self.rent_per_hour_textfield = tk.Entry(self, width=30)
        
        # ComboBoxes
        colors = ["White", "Red", "Silver", "Blue", "Black"]
        self.color_combobox = ttk.Combobox(self, values=colors, width=29)
        
        types = ["Familycar", "Comercial", "Microcar", "Compact car", "Mid-size car", "Supercar", "Convertible", "Sports cars"]
        self.type_combobox = ttk.Combobox(self, values=types, width=29)
        
        # Create years for model dropdown
        current_year = datetime.datetime.now().year
        years = [str(year) for year in range(current_year, 1949, -1)]
        self.model_combobox = ttk.Combobox(self, values=years, width=29)
        
        conditions = ["Excellent", "Good", "Average", "Bad"]
        self.condition_combobox = ttk.Combobox(self, values=conditions, width=29)
        
        # Spinner for seating capacity
        self.seating_capacity_var = tk.IntVar(value=4)
        self.seating_capacity_spinner = tk.Spinbox(self, from_=1, to=20, width=5, textvariable=self.seating_capacity_var)
        
        # Buttons
        self.update_button = tk.Button(self, text="Update", width=10, command=self.update_car)
        self.cancel_button = tk.Button(self, text="Cancel", width=10, command=self.on_close)
        
        # Fill in fields with car data
        self.maker_textfield.insert(0, self.car.get_maker())
        self.name_textfield.insert(0, self.car.get_name())
        self.reg_no_textfield.insert(0, self.car.get_reg_no())
        self.owner_id_textfield.insert(0, str(self.car.get_car_owner().get_id()))
        self.rent_per_hour_textfield.insert(0, str(self.car.get_rent_per_hour()))
        
        self.model_combobox.set(self.car.get_model())
        self.type_combobox.set(self.car.get_type())
        self.seating_capacity_var.set(self.car.get_seating_capacity())
        self.color_combobox.set(self.car.get_colour())
        self.condition_combobox.set(self.car.get_condition())
        
        # Layout components
        self.maker_label.pack(anchor="w", padx=10, pady=(10, 0))
        self.maker_textfield.pack(padx=10, pady=(0, 0))
        self.maker_validity_label.pack(padx=10, fill=tk.X)
        
        self.name_label.pack(anchor="w", padx=10)
        self.name_textfield.pack(padx=10)
        self.name_validity_label.pack(padx=10, fill=tk.X)
        
        self.reg_no_label.pack(anchor="w", padx=10)
        self.reg_no_textfield.pack(padx=10)
        self.reg_no_validity_label.pack(padx=10, fill=tk.X)
        
        self.owner_id_label.pack(anchor="w", padx=10)
        self.owner_id_textfield.pack(padx=10)
        self.owner_id_validity_label.pack(padx=10, fill=tk.X)
        
        self.rent_per_hour_label.pack(anchor="w", padx=10)
        self.rent_per_hour_textfield.pack(padx=10)
        self.rent_per_hour_validity_label.pack(padx=10, fill=tk.X)
        
        # Create frames for comboboxes and spinner to organize layout
        model_frame = tk.Frame(self)
        model_frame.pack(fill=tk.X, padx=10, pady=5)
        self.model_label.pack(in_=model_frame, side=tk.LEFT)
        self.model_combobox.pack(in_=model_frame, side=tk.LEFT, padx=(0, 10))
        
        type_frame = tk.Frame(self)
        type_frame.pack(fill=tk.X, padx=10, pady=5)
        self.type_label.pack(in_=type_frame, side=tk.LEFT)
        self.type_combobox.pack(in_=type_frame, side=tk.LEFT, padx=(0, 10))
        
        seat_frame = tk.Frame(self)
        seat_frame.pack(fill=tk.X, padx=10, pady=5)
        self.seating_capacity_label.pack(in_=seat_frame, side=tk.LEFT)
        self.seating_capacity_spinner.pack(in_=seat_frame, side=tk.LEFT, padx=(0, 10))
        
        color_frame = tk.Frame(self)
        color_frame.pack(fill=tk.X, padx=10, pady=5)
        self.color_label.pack(in_=color_frame, side=tk.LEFT)
        self.color_combobox.pack(in_=color_frame, side=tk.LEFT, padx=(0, 10))
        
        condition_frame = tk.Frame(self)
        condition_frame.pack(fill=tk.X, padx=10, pady=5)
        self.condition_label.pack(in_=condition_frame, side=tk.LEFT)
        self.condition_combobox.pack(in_=condition_frame, side=tk.LEFT, padx=(0, 10))
        
        # Button frame
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)
        self.update_button.pack(side=tk.LEFT, padx=5, in_=button_frame)
        self.cancel_button.pack(side=tk.LEFT, padx=5, in_=button_frame)
        
        # Make this window modal
        self.transient(parent)
        self.grab_set()
    
    def position_center(self):
        """Center the window on the screen"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'+{x}+{y}')
    
    def update_car(self):
        """Handle the update car button action"""
        maker = self.maker_textfield.get().strip()
        name = self.name_textfield.get().strip()
        reg_no = self.reg_no_textfield.get().strip()
        owner_id = self.owner_id_textfield.get().strip()
        rent_per_hour = self.rent_per_hour_textfield.get().strip()
        
        # Validate name
        if name:
            if Car.is_name_valid(name):
                self.name_validity_label.config(text="")
            else:
                name = None
                self.name_validity_label.config(text="Invalid Car Name!")
        else:
            name = None
            self.name_validity_label.config(text="Enter Car Name!")
        
        # Validate maker
        if maker:
            if Car.is_name_valid(maker):
                self.maker_validity_label.config(text="")
            else:
                maker = None
                self.maker_validity_label.config(text="Invalid Maker's Name!")
        else:
            maker = None
            self.maker_validity_label.config(text="Enter Maker's Name!")
        
        # Validate registration number
        if reg_no:
            if Car.is_reg_no_valid(reg_no):
                self.reg_no_validity_label.config(text="")
                car2 = Car.search_by_reg_no(reg_no)
                # Check if reg_no is already registered to a different car
                if car2 is not None and reg_no.lower() != self.car.get_reg_no().lower():
                    reg_no = None
                    messagebox.showerror("Error", "This Car Registration no is already registered!")
            else:
                reg_no = None
                self.reg_no_validity_label.config(text="Invalid Reg no!")
        else:
            reg_no = None
            self.reg_no_validity_label.config(text="Enter Reg No!")
        
        # Validate owner ID
        if owner_id:
            try:
                owner_id_int = int(owner_id)
                if owner_id_int > 0:
                    self.owner_id_validity_label.config(text="")
                    self.car_owner = CarOwner.search_by_id(owner_id_int)
                    if self.car_owner is None:
                        owner_id = None
                        messagebox.showerror("Error", "Owner ID does not exist!")
                else:
                    owner_id = None
                    self.owner_id_validity_label.config(text="ID cannot be '0' or negative!")
            except ValueError:
                owner_id = None
                self.owner_id_validity_label.config(text="Invalid ID!")
        else:
            owner_id = None
            self.owner_id_validity_label.config(text="Enter Owner ID!")
        
        # Validate rent per hour
        if rent_per_hour:
            try:
                rent_per_hour_int = int(rent_per_hour)
                if rent_per_hour_int > 0:
                    self.rent_per_hour_validity_label.config(text="")
                else:
                    rent_per_hour = None
                    self.rent_per_hour_validity_label.config(text="Rent cannot be '0' or negative!")
            except ValueError:
                rent_per_hour = None
                self.rent_per_hour_validity_label.config(text="Invalid Rent!")
        else:
            rent_per_hour = None
            self.rent_per_hour_validity_label.config(text="Enter Rent!")
        
        # If all inputs are valid, update the car
        if all([maker, name, reg_no, owner_id, rent_per_hour]):
            try:
                # Create updated car object
                updated_car = Car(
                    self.car.get_id(),
                    maker,
                    name,
                    self.color_combobox.get(),
                    self.type_combobox.get(),
                    int(self.seating_capacity_var.get()),
                    self.model_combobox.get(),
                    self.condition_combobox.get(),
                    reg_no,
                    int(rent_per_hour),
                    self.car_owner
                )
                
                # Update the car in the database
                updated_car.update()
                
                # Update the main window's content
                self.parent.parent.content_pane.destroy()
                from gui.car_details import Car_Details
                car_details = Car_Details(self.parent.parent)
                self.parent.parent.content_pane = car_details.get_main_panel()
                self.parent.parent.content_pane.pack(fill=tk.BOTH, expand=True)
                
                # Show success message
                messagebox.showinfo("Success", "Record Successfully Updated!")
                
                # Close windows
                self.on_close()
                
            except Exception as ex:
                messagebox.showerror("Error", f"Error updating car: {str(ex)}")
                print(ex)
    
    def on_close(self):
        """Handle window close event"""
        self.parent.parent.deiconify()  # Re-enable the main window
        self.parent.parent.focus_set()  # Set focus back to the main window
        self.parent.destroy()  # Close parent window
        self.destroy()  # Close this window


# Example usage:
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    app = Car_Update(root)  # This will run the dialog
    root.mainloop()