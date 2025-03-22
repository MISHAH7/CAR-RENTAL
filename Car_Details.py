import tkinter as tk
from tkinter import ttk, messagebox
from functools import partial
import sys

# Import equivalent backend modules (assuming they exist in Python)
from backend_code.booking import Booking
from backend_code.car import Car
from backend_code.car_owner import CarOwner

class CarDetails:
    # Class variable for table model (will be accessible from other classes)
    tablemodel = None
    
    def __init__(self):
        self.main_panel = tk.Frame()
        # Set the title in the parent frame/window
        # Assuming Parent_JFrame is implemented elsewhere
        
        # Create buttons
        self.search_reg_no_button = tk.Button(self.main_panel, text="Search Reg_No", command=partial(self.action_performed, "Search Reg_No"))
        self.search_reg_no_textfield = tk.Entry(self.main_panel)
        
        self.search_name_button = tk.Button(self.main_panel, text="Search Name", command=partial(self.action_performed, "Search Name"))
        self.search_name_textfield = tk.Entry(self.main_panel)
        
        self.add_button = tk.Button(self.main_panel, text="Add", command=partial(self.action_performed, "Add"))
        self.update_button = tk.Button(self.main_panel, text="Update", command=partial(self.action_performed, "Update"))
        self.remove_button = tk.Button(self.main_panel, text="Remove", command=partial(self.action_performed, "Remove"))
        self.back_button = tk.Button(self.main_panel, text="Back", command=partial(self.action_performed, "Back"))
        self.logout_button = tk.Button(self.main_panel, text="Logout", command=partial(self.action_performed, "Logout"))
        
        # Create table with scrollbar
        self.create_table()
        
        # Layout using place (equivalent to AbsoluteLayout)
        self.search_reg_no_button.place(x=10, y=15, width=130, height=22)
        self.search_reg_no_textfield.place(x=145, y=15, width=240, height=22)
        self.search_name_button.place(x=390, y=15, width=130, height=22)
        self.search_name_textfield.place(x=525, y=15, width=240, height=22)
        self.table_scroll.place(x=10, y=60, width=1330, height=550)
        self.remove_button.place(x=785, y=625, width=130, height=22)
        self.add_button.place(x=450, y=625, width=130, height=22)
        self.update_button.place(x=620, y=625, width=130, height=22)
        self.back_button.place(x=1106, y=625, width=100, height=22)
        self.logout_button.place(x=1236, y=625, width=100, height=22)
        
    def create_table(self):
        # Create scrollable table
        self.table_scroll = tk.Frame(self.main_panel)
        
        # Define column names
        columns = ["Sr#", "ID", "Maker", "Name", "Colour", "Type", "Seats", "Model", 
                   "Condition", "Reg No.", "Rent/hour", "Car Owner"]
        
        # Create Treeview (equivalent to JTable)
        self.table = ttk.Treeview(self.table_scroll, columns=columns, show='headings')
        
        # Configure each column
        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, anchor='center')
        
        # Set column widths
        self.table.column("Sr#", width=20)
        self.table.column("ID", width=20)
        self.table.column("Maker", width=170)
        self.table.column("Name", width=170)
        self.table.column("Colour", width=140)
        self.table.column("Type", width=150)
        self.table.column("Seats", width=90)
        self.table.column("Model", width=90)
        self.table.column("Condition", width=160)
        self.table.column("Reg No.", width=170)
        self.table.column("Rent/hour", width=150)
        self.table.column("Car Owner", width=150)
        
        # Add scrollbars
        vsb = ttk.Scrollbar(self.table_scroll, orient="vertical", command=self.table.yview)
        hsb = ttk.Scrollbar(self.table_scroll, orient="horizontal", command=self.table.xview)
        self.table.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Place scrollbars
        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")
        self.table.pack(expand=True, fill="both")
        
        # Populate table with car data
        self.populate_table()
        
        # Set the class variable tablemodel to be accessible from other classes
        CarDetails.tablemodel = self.table
        
    def populate_table(self):
        # Clear existing table data
        for i in self.table.get_children():
            self.table.delete(i)
        
        # Get car objects from backend
        car_objects = Car.view()
        
        # Populate table with car data
        for i, car in enumerate(car_objects):
            car_id = car.get_id()
            maker = car.get_maker()
            name = car.get_name()
            color = car.get_colour()
            car_type = car.get_type()
            seating_capacity = car.get_seating_capacity()
            model = car.get_model()
            condition = car.get_condition()
            reg_no = car.get_reg_no()
            rent_per_hour = car.get_rent_per_hour()
            car_owner = car.get_car_owner()
            
            # Insert data into table
            self.table.insert("", "end", values=(
                i+1, car_id, maker, name, color, car_type, seating_capacity,
                model, condition, reg_no, rent_per_hour, 
                f"{car_owner.get_id()}: {car_owner.get_name()}"
            ))
    
    def get_main_panel(self):
        return self.main_panel
    
    @staticmethod
    def get_tablemodel():
        return CarDetails.tablemodel
    
    def action_performed(self, command):
        if command == "Search Reg_No":
            reg_no = self.search_reg_no_textfield.get().strip()
            if reg_no:
                if Car.is_reg_no_valid(reg_no):
                    car = Car.search_by_reg_no(reg_no)
                    if car:
                        messagebox.showinfo("Car Information", str(car))
                        self.search_reg_no_textfield.delete(0, tk.END)
                    else:
                        messagebox.showinfo("Not Found", "Required Car not found")
                        self.search_reg_no_textfield.delete(0, tk.END)
                else:
                    messagebox.showwarning("Invalid Input", "Invalid Reg No.")
            else:
                messagebox.showwarning("Missing Input", "Please Enter Car Reg no first!")
                
        elif command == "Search Name":
            name = self.search_name_textfield.get().strip()
            if name:
                if Car.is_name_valid(name):
                    cars = Car.search_by_name(name)
                    if cars:
                        messagebox.showinfo("Car Information", str(cars))
                        self.search_name_textfield.delete(0, tk.END)
                    else:
                        messagebox.showinfo("Not Found", "Required Car not found")
                        self.search_name_textfield.delete(0, tk.END)
                else:
                    messagebox.showwarning("Invalid Input", "Invalid Name!")
                    self.search_name_textfield.delete(0, tk.END)
            else:
                messagebox.showwarning("Missing Input", "Please Enter Car Name first!")
                
        elif command == "Add":
            # Disable the main frame
            # parent_frame.set_enabled(False)
            # Show Car_Add window
            car_add = CarAdd()
            car_add.show()
            
        elif command == "Update":
            # Disable the main frame
            # parent_frame.set_enabled(False)
            # Show Car_Update window
            car_update = CarUpdate()
            car_update.show()
            
        elif command == "Remove":
            # Disable the main frame
            # parent_frame.set_enabled(False)
            # Show Car_Remove window
            car_remove = CarRemove()
            car_remove.show()
            
        elif command == "Back":
            # Change to main menu
            # parent_frame.set_title("Rent-A-Car Management System [REBORN]")
            main_menu = MainMenu()
            # parent_frame.get_content_pane().remove_all()
            # parent_frame.add(main_menu.get_main_panel())
            # parent_frame.get_content_pane().revalidate()
            
        elif command == "Logout":
            # Dispose main frame and show login
            # parent_frame.dispose()
            runner = Runner()
            frame = runner.get_frame()
            login = Login()
            panel = login.get_main_panel()
            # frame.add(panel)
            # frame.set_visible(True)
            
        elif command == "Book":
            if Booking.get_unbooked_cars():
                # Disable main frame
                # parent_frame.set_enabled(False)
                booking = BookingBookCar()
                booking.show()
            else:
                messagebox.showinfo("No Cars", "No UnBooked Cars are available!")
                
        elif command == "Unbook":
            if Booking.get_booked_cars():
                # Disable main frame
                # parent_frame.set_enabled(False)
                unbooking = BookingUnBookCar()
                unbooking.show()
            else:
                messagebox.showinfo("No Cars", "No Booked Cars found!")


# Placeholder for other required classes
class CarAdd:
    def __init__(self):
        # Implementation details
        pass
    
    def show(self):
        # Implementation details
        pass

class CarUpdate:
    def __init__(self):
        # Implementation details
        pass
    
    def show(self):
        # Implementation details
        pass

class CarRemove:
    def __init__(self):
        # Implementation details
        pass
    
    def show(self):
        # Implementation details
        pass

class MainMenu:
    def __init__(self):
        # Implementation details
        pass
    
    def get_main_panel(self):
        # Implementation details
        pass

class Runner:
    def __init__(self):
        # Implementation details
        pass
    
    def get_frame(self):
        # Implementation details
        pass

class Login:
    def __init__(self):
        # Implementation details
        pass
    
    def get_main_panel(self):
        # Implementation details
        pass

class BookingBookCar:
    def __init__(self):
        # Implementation details
        pass
    
    def show(self):
        # Implementation details
        pass

class BookingUnBookCar:
    def __init__(self):
        # Implementation details
        pass
    
    def show(self):
        # Implementation details
        pass


# Main application entry point
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Car Details - Rent-A-Car Management System")
    root.geometry("1366x730")
    
    app = CarDetails()
    app.get_main_panel().pack(fill="both", expand=True)
    
    root.mainloop()