import tkinter as tk
from tkinter import ttk, messagebox
import datetime
from backend.car import Car
from backend.car_owner import CarOwner

class CarAdd(tk.Toplevel):
    def __init__(self, parent_frame):
        super().__init__()
        self.title("Add Car")
        self.geometry("450x475")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.parent_frame = parent_frame
        
        # Create all labels
        self.maker_label = tk.Label(self, text="Maker")
        self.name_label = tk.Label(self, text="Name")
        self.color_label = tk.Label(self, text="Color")
        self.model_label = tk.Label(self, text="Model")
        self.type_label = tk.Label(self, text="Car type")
        self.seating_capacity_label = tk.Label(self, text="Seating capacity")
        self.reg_no_label = tk.Label(self, text="Reg no (ABC-0123)")
        self.owner_id_label = tk.Label(self, text="Owner ID")
        self.rent_per_hour_label = tk.Label(self, text="Rent Per Hour (in PKR)")
        self.condition_label = tk.Label(self, text="Condition")
        
        # Create validation labels
        self.maker_validity_label = tk.Label(self, text="", fg="red")
        self.name_validity_label = tk.Label(self, text="", fg="red")
        self.reg_no_validity_label = tk.Label(self, text="", fg="red")
        self.owner_id_validity_label = tk.Label(self, text="", fg="red")
        self.rent_per_hour_validity_label = tk.Label(self, text="", fg="red")
        
        # Create text fields
        self.maker_textfield = tk.Entry(self, width=30)
        self.name_textfield = tk.Entry(self, width=30)
        self.reg_no_textfield = tk.Entry(self, width=30)
        self.owner_id_textfield = tk.Entry(self, width=30)
        self.rent_per_hour_textfield = tk.Entry(self, width=30)
        
        # Create dropdown menus
        colours = ["White", "Red", "Silver", "Blue", "Black"]
        self.colour_combobox = ttk.Combobox(self, values=colours, width=27)
        self.colour_combobox.current(0)  # Set default selection
        
        car_types = ["Familycar", "Comercial", "Microcar", "Compact car", 
                    "Mid-size car", "Supercar", "Convertible", "Sports cars"]
        self.type_combobox = ttk.Combobox(self, values=car_types, width=27)
        self.type_combobox.current(0)  # Set default selection
        
        # Creating model years dropdown (current year to 1950)
        current_year = datetime.datetime.now().year
        years = [str(year) for year in range(current_year, 1949, -1)]
        self.model_combobox = ttk.Combobox(self, values=years, width=27)
        self.model_combobox.current(0)  # Set default selection
        
        conditions = ["Excellent", "Good", "Average", "Bad"]
        self.condition_combobox = ttk.Combobox(self, values=conditions, width=27)
        self.condition_combobox.current(0)  # Set default selection
        
        # Create spinner for seating capacity
        self.seating_var = tk.IntVar(value=4)
        self.seating_capacity_spinner = ttk.Spinbox(
            self, from_=1, to=20, textvariable=self.seating_var, width=5)
        
        # Create buttons
        self.add_button = tk.Button(self, text="Add", width=12, command=self.add_action)
        self.cancel_button = tk.Button(self, text="Cancel", width=12, command=self.on_closing)
        
        # Layout all components using grid for better control
        self.maker_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.maker_textfield.grid(row=0, column=1, sticky="w", padx=10, pady=5)
        self.maker_validity_label.grid(row=1, column=0, columnspan=2, sticky="w", padx=10)
        
        self.name_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.name_textfield.grid(row=2, column=1, sticky="w", padx=10, pady=5)
        self.name_validity_label.grid(row=3, column=0, columnspan=2, sticky="w", padx=10)
        
        self.reg_no_label.grid(row=4, column=0, sticky="w", padx=10, pady=5)
        self.reg_no_textfield.grid(row=4, column=1, sticky="w", padx=10, pady=5)
        self.reg_no_validity_label.grid(row=5, column=0, columnspan=2, sticky="w", padx=10)
        
        self.owner_id_label.grid(row=6, column=0, sticky="w", padx=10, pady=5)
        self.owner_id_textfield.grid(row=6, column=1, sticky="w", padx=10, pady=5)
        self.owner_id_validity_label.grid(row=7, column=0, columnspan=2, sticky="w", padx=10)
        
        self.rent_per_hour_label.grid(row=8, column=0, sticky="w", padx=10, pady=5)
        self.rent_per_hour_textfield.grid(row=8, column=1, sticky="w", padx=10, pady=5)
        self.rent_per_hour_validity_label.grid(row=9, column=0, columnspan=2, sticky="w", padx=10)
        
        self.model_label.grid(row=10, column=0, sticky="w", padx=10, pady=5)
        self.model_combobox.grid(row=10, column=1, sticky="w", padx=10, pady=5)
        
        self.type_label.grid(row=11, column=0, sticky="w", padx=10, pady=5)
        self.type_combobox.grid(row=11, column=1, sticky="w", padx=10, pady=5)
        
        self.seating_capacity_label.grid(row=12, column=0, sticky="w", padx=10, pady=5)
        self.seating_capacity_spinner.grid(row=12, column=1, sticky="w", padx=10, pady=5)
        
        self.color_label.grid(row=13, column=0, sticky="w", padx=10, pady=5)
        self.colour_combobox.grid(row=13, column=1, sticky="w", padx=10, pady=5)
        
        self.condition_label.grid(row=14, column=0, sticky="w", padx=10, pady=5)
        self.condition_combobox.grid(row=14, column=1, sticky="w", padx=10, pady=5)
        
        button_frame = tk.Frame(self)
        button_frame.grid(row=15, column=0, columnspan=2, pady=10)
        self.add_button.pack(side=tk.LEFT, padx=10)
        self.cancel_button.pack(side=tk.LEFT, padx=10)
        
        # Center the window
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    
    def add_action(self):
        # Get all input values
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
            else:
                reg_no = None
                self.reg_no_validity_label.config(text="Invalid Reg no!")
        else:
            reg_no = None
            self.reg_no_validity_label.config(text="Enter Reg No!")
        
        # Validate owner ID
        if owner_id:
            try:
                if int(owner_id) > 0:
                    self.owner_id_validity_label.config(text="")
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
                if int(rent_per_hour) > 0:
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
        
        # If all validations pass, create and add car
        try:
            if maker and name and reg_no and owner_id and rent_per_hour:
                car_owner = CarOwner.search_by_id(int(owner_id))
                existing_car = Car.search_by_reg_no(reg_no)
                
                if car_owner:
                    if not existing_car:
                        # Create new car object
                        # (0 for ID as it's auto-generated in the backend)
                        car = Car(
                            id=0,
                            maker=maker,
                            name=name,
                            color=self.colour_combobox.get(),
                            car_type=self.type_combobox.get(),
                            seating_capacity=self.seating_var.get(),
                            model=self.model_combobox.get(),
                            condition=self.condition_combobox.get(),
                            reg_no=reg_no,
                            rent_per_hour=int(rent_per_hour),
                            car_owner=car_owner
                        )
                        car.add()
                        
                        # Update parent frame
                        from gui.car_details import CarDetails
                        self.parent_frame.content_pane.destroy()
                        self.parent_frame.content_pane = CarDetails(self.parent_frame).get_main_panel()
                        self.parent_frame.content_pane.pack(fill=tk.BOTH, expand=True)
                        
                        messagebox.showinfo("Success", "Record Successfully Added!")
                        self.parent_frame.enable()
                        self.destroy()
                    else:
                        messagebox.showinfo("Error", "This Car Registration no is already registered!")
                else:
                    messagebox.showinfo("Error", "Owner ID does not exist!")
        except Exception as ex:
            print(f"Error in car_add.py: {ex}")
    
    def on_closing(self):
        self.parent_frame.enable()
        self.destroy()


class ParentFrame:
    """Placeholder for the parent frame functionality that would be implemented in the main application"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Car Rental System")
        self.root.geometry("800x600")
        self.content_pane = tk.Frame(self.root)
        self.content_pane.pack(fill=tk.BOTH, expand=True)
        
    def get_main_frame(self):
        return self
        
    def enable(self):
        self.root.attributes('-disabled', False)
        
    def disable(self):
        self.root.attributes('-disabled', True)
        
    def show_car_add(self):
        self.disable()
        CarAdd(self)
        
    def run(self):
        self.root.mainloop()


# Example usage (if this module is run directly)
if __name__ == "__main__":
    # This would typically be part of a larger application
    app = ParentFrame()
    app.show_car_add()
    app.run()