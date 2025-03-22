import tkinter as tk
from tkinter import ttk, messagebox
import time
from datetime import datetime
from functools import partial

# Importing the backend modules we created earlier
# For this example, I'll create stub classes to represent the backend
class Car:
    all_cars = {}
    
    def __init__(self, car_id, name, reg_no, is_rented=False):
        self.id = car_id
        self.name = name
        self.reg_no = reg_no
        self.is_rented = is_rented
        Car.all_cars[reg_no] = self
    
    @classmethod
    def search_by_reg_no(cls, reg_no):
        return cls.all_cars.get(reg_no)
    
    @classmethod
    def is_reg_no_valid(cls, reg_no):
        # Simple validation - in a real app would check format
        return len(reg_no) > 3
    
    @classmethod
    def get_unbooked_cars(cls):
        return [car for car in cls.all_cars.values() if not car.is_rented]
    
    @classmethod
    def get_booked_cars(cls):
        return [car for car in cls.all_cars.values() if car.is_rented]
    
    def __str__(self):
        return f"Car ID: {self.id}, Name: {self.name}, Reg No: {self.reg_no}, Rented: {'Yes' if self.is_rented else 'No'}"


class Customer:
    all_customers = {}
    
    def __init__(self, customer_id, name, phone):
        self.id = customer_id
        self.name = name
        self.phone = phone
        Customer.all_customers[customer_id] = self
    
    @classmethod
    def search_by_id(cls, customer_id):
        return cls.all_customers.get(customer_id)
    
    @classmethod
    def is_id_valid(cls, customer_id):
        try:
            id_int = int(customer_id)
            return id_int > 0
        except ValueError:
            return False
    
    def __str__(self):
        return f"Customer ID: {self.id}, Name: {self.name}, Phone: {self.phone}"


class Booking:
    all_bookings = []
    
    def __init__(self, booking_id, customer, car, rent_time, return_time=0):
        self.id = booking_id if booking_id > 0 else len(Booking.all_bookings) + 1
        self.customer = customer
        self.car = car
        self.rent_time = rent_time
        self.return_time = return_time
        
    def add(self):
        self.car.is_rented = True
        Booking.all_bookings.append(self)
        return True
    
    def unbook(self):
        self.car.is_rented = False
        self.return_time = int(time.time() * 1000)
        return True
    
    @classmethod
    def view(cls):
        return cls.all_bookings
    
    @classmethod
    def search_by_customer_id(cls, customer_id):
        return [booking for booking in cls.all_bookings if booking.customer.id == customer_id]
    
    @classmethod
    def search_by_car_reg_no(cls, reg_no):
        return [booking for booking in cls.all_bookings if booking.car.reg_no == reg_no]
    
    @classmethod
    def get_booked_cars(cls):
        return [booking.car for booking in cls.all_bookings if booking.return_time == 0]
    
    @classmethod
    def get_unbooked_cars(cls):
        rented_car_ids = [booking.car.id for booking in cls.all_bookings if booking.return_time == 0]
        return [car for car in Car.all_cars.values() if car.id not in rented_car_ids]
    
    def __str__(self):
        rent_time_str = datetime.fromtimestamp(self.rent_time / 1000).strftime('%H:%M %p %d-%m-%Y')
        if self.return_time != 0:
            return_time_str = datetime.fromtimestamp(self.return_time / 1000).strftime('%H:%M %p %d-%m-%Y')
        else:
            return_time_str = "Not returned yet!"
            
        return (f"Booking ID: {self.id}, Customer: {self.customer.id}: {self.customer.name}, "
                f"Car: {self.car.id}: {self.car.name}, Rent Time: {rent_time_str}, Return Time: {return_time_str}")


# Main application classes
class ParentFrame:
    _main_frame = None
    
    @classmethod
    def get_main_frame(cls):
        if cls._main_frame is None:
            cls._main_frame = tk.Tk()
            cls._main_frame.title("Rent-A-Car Management System")
            cls._main_frame.geometry("1366x730")
        return cls._main_frame


class BookingBookCar(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Book Car")
        self.geometry("300x200")
        # Implementation would be similar to the previous file


class BookingUnBookCar(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Unbook Car")
        self.geometry("300x200")
        # Implementation would follow a similar pattern to BookingBookCar


class MainMenu:
    def __init__(self):
        self.main_panel = tk.Frame(ParentFrame.get_main_frame())
        # Simple main menu implementation
        label = tk.Label(self.main_panel, text="Main Menu - Rent-A-Car Management System", font=("Arial", 18))
        label.pack(pady=20)
        
        booking_button = tk.Button(self.main_panel, text="Booking Details", 
                                  command=self.open_booking_details)
        booking_button.pack(pady=10)
        
        # Add other menu options here
    
    def open_booking_details(self):
        parent_frame = ParentFrame.get_main_frame()
        parent_frame.title("Booking Details - Rent-A-Car Management System")
        for widget in parent_frame.winfo_children():
            widget.destroy()
        
        booking_details = BookingDetails()
        booking_details.get_main_panel().pack(fill=tk.BOTH, expand=True)
    
    def get_main_panel(self):
        return self.main_panel


class Runner:
    def __init__(self):
        self.frame = tk.Tk()
        self.frame.title("Rent-A-Car Management System")
        self.frame.geometry("1366x730")
    
    def get_frame(self):
        return self.frame


class Login:
    def __init__(self):
        self.main_panel = tk.Frame()
        # Simple login implementation
        label = tk.Label(self.main_panel, text="Login - Rent-A-Car Management System", font=("Arial", 18))
        label.pack(pady=20)
        
        # Add login fields here
    
    def get_main_panel(self):
        return self.main_panel


class BookingDetails:
    def __init__(self):
        self.main_panel = tk.Frame(ParentFrame.get_main_frame())
        self.main_panel.pack(fill=tk.BOTH, expand=True)
        
        # Create the UI elements for BookingDetails
        self.create_widgets()
        
        # Populate the table with data
        self.populate_table()
    
    def create_widgets(self):
        # Top frame for search controls
        top_frame = tk.Frame(self.main_panel)
        top_frame.pack(fill=tk.X, pady=10)
        
        # Search by Car RegNo
        self.search_car_reg_button = tk.Button(top_frame, text="Search by Car RegNo", 
                                              command=lambda: self.button_handler("Search by Car RegNo"))
        self.search_car_reg_button.grid(row=0, column=0, padx=10)
        
        self.car_reg_textfield = tk.Entry(top_frame, width=30)
        self.car_reg_textfield.grid(row=0, column=1, padx=10)
        
        # Search by Customer ID
        self.search_customer_id_button = tk.Button(top_frame, text="Search by Customer ID", 
                                                  command=lambda: self.button_handler("Search by Customer ID"))
        self.search_customer_id_button.grid(row=0, column=2, padx=10)
        
        self.customer_id_textfield = tk.Entry(top_frame, width=30)
        self.customer_id_textfield.grid(row=0, column=3, padx=10)
        
        # Create table for data display
        table_frame = tk.Frame(self.main_panel)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Treeview for table display
        self.table = ttk.Treeview(table_frame, columns=("sr", "id", "customer", "car", "rent_time", "return_time"),
                                 show="headings", height=20)
        
        # Define column headings
        self.table.heading("sr", text="Sr#")
        self.table.heading("id", text="ID")
        self.table.heading("customer", text="Customer ID+Name")
        self.table.heading("car", text="Car Name")
        self.table.heading("rent_time", text="Rent Time")
        self.table.heading("return_time", text="Return Time")
        
        # Set column widths
        self.table.column("sr", width=80, anchor=tk.CENTER)
        self.table.column("id", width=80, anchor=tk.CENTER)
        self.table.column("customer", width=400, anchor=tk.CENTER)
        self.table.column("car", width=300, anchor=tk.CENTER)
        self.table.column("rent_time", width=230, anchor=tk.CENTER)
        self.table.column("return_time", width=235, anchor=tk.CENTER)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.table.yview)
        self.table.configure(yscroll=scrollbar.set)
        
        # Pack table and scrollbar
        self.table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bottom frame for action buttons
        bottom_frame = tk.Frame(self.main_panel)
        bottom_frame.pack(fill=tk.X, pady=10)
        
        # Action buttons
        self.book_car_button = tk.Button(bottom_frame, text="Book", width=15, 
                                        command=lambda: self.button_handler("Book"))
        self.book_car_button.grid(row=0, column=0, padx=10)
        
        self.unbook_car_button = tk.Button(bottom_frame, text="Unbook", width=15, 
                                          command=lambda: self.button_handler("Unbook"))
        self.unbook_car_button.grid(row=0, column=1, padx=10)
        
        # Spacer to push Back and Logout buttons to the right
        spacer = tk.Label(bottom_frame, text="")
        spacer.grid(row=0, column=2, padx=10, sticky=tk.W+tk.E)
        bottom_frame.grid_columnconfigure(2, weight=1)
        
        self.back_button = tk.Button(bottom_frame, text="Back", width=10, 
                                    command=lambda: self.button_handler("Back"))
        self.back_button.grid(row=0, column=3, padx=10)
        
        self.logout_button = tk.Button(bottom_frame, text="Logout", width=10, 
                                      command=lambda: self.button_handler("Logout"))
        self.logout_button.grid(row=0, column=4, padx=10)
    
    def populate_table(self):
        # Clear existing data
        for item in self.table.get_children():
            self.table.delete(item)
        
        # Get all bookings
        bookings = Booking.view()
        
        # Add each booking to the table
        for i, booking in enumerate(bookings):
            customer_info = f"{booking.customer.id}: {booking.customer.name}"
            car_info = f"{booking.car.id}: {booking.car.name}"
            
            # Format rent time
            rent_time_date = datetime.fromtimestamp(booking.rent_time / 1000)
            rent_time_str = rent_time_date.strftime('%H:%M %p %d-%m-%Y')
            
            # Format return time
            if booking.return_time != 0:
                return_time_date = datetime.fromtimestamp(booking.return_time / 1000)
                return_time_str = return_time_date.strftime('%H:%M %p %d-%m-%Y')
            else:
                return_time_str = "Not returned yet!"
            
            # Insert into table
            self.table.insert("", tk.END, values=(i+1, booking.id, customer_info, car_info, rent_time_str, return_time_str))
    
    def button_handler(self, command):
        if command == "Back":
            parent_frame = ParentFrame.get_main_frame()
            parent_frame.title("Rent-A-Car Management System [REBORN]")
            for widget in parent_frame.winfo_children():
                widget.destroy()
            
            main_menu = MainMenu()
            main_menu.get_main_panel().pack(fill=tk.BOTH, expand=True)
        
        elif command == "Logout":
            parent_frame = ParentFrame.get_main_frame()
            parent_frame.destroy()
            
            runner = Runner()
            frame = runner.get_frame()
            login = Login()
            login.get_main_panel().pack(fill=tk.BOTH, expand=True)
            frame.mainloop()
        
        elif command == "Book":
            if Booking.get_unbooked_cars():
                parent_frame = ParentFrame.get_main_frame()
                parent_frame.state('disabled')
                book_car = BookingBookCar()
                book_car.grab_set()  # Make the dialog modal
                book_car.focus_set()
            else:
                messagebox.showinfo("Information", "No UnBooked Cars are available!")
        
        elif command == "Unbook":
            if Booking.get_booked_cars():
                parent_frame = ParentFrame.get_main_frame()
                parent_frame.state('disabled')
                unbook_car = BookingUnBookCar()
                unbook_car.grab_set()  # Make the dialog modal
                unbook_car.focus_set()
            else:
                messagebox.showinfo("Information", "No Booked Cars found!")
        
        elif command == "Search by Customer ID":
            customer_id = self.customer_id_textfield.get().strip()
            if customer_id:
                if Customer.is_id_valid(customer_id):
                    customer = Customer.search_by_id(int(customer_id))
                    if customer:
                        bookings = Booking.search_by_customer_id(int(customer_id))
                        if bookings:
                            booking_info = "\n".join([str(booking) for booking in bookings])
                            messagebox.showinfo("Booking Information", booking_info)
                        else:
                            messagebox.showinfo("Information", "This Customer has not booked any cars yet!")
                    else:
                        messagebox.showinfo("Information", "Customer ID not found!")
                else:
                    messagebox.showinfo("Information", "Invalid Customer ID!")
            else:
                messagebox.showinfo("Information", "Enter Customer ID first!")
            
            self.customer_id_textfield.delete(0, tk.END)
        
        elif command == "Search by Car RegNo":
            car_reg_no = self.car_reg_textfield.get().strip()
            if car_reg_no:
                if Car.is_reg_no_valid(car_reg_no):
                    car = Car.search_by_reg_no(car_reg_no)
                    if car:
                        bookings = Booking.search_by_car_reg_no(car_reg_no)
                        if bookings:
                            booking_info = "\n".join([str(booking) for booking in bookings])
                            messagebox.showinfo("Booking Information", booking_info)
                        else:
                            messagebox.showinfo("Information", "This Car is not booked yet!")
                    else:
                        messagebox.showinfo("Information", "Registration No. not found!")
                else:
                    messagebox.showinfo("Information", "Invalid Registration No!")
            else:
                messagebox.showinfo("Information", "Enter Car Registration No. first!")
            
            self.car_reg_textfield.delete(0, tk.END)
    
    def get_main_panel(self):
        return self.main_panel


# Sample data initialization
def create_sample_data():
    # Create sample cars
    car1 = Car(1, "Toyota Camry", "ABC123")
    car2 = Car(2, "Honda Civic", "XYZ789")
    car3 = Car(3, "Ford Mustang", "PQR456")
    
    # Create sample customers
    customer1 = Customer(1, "John Doe", "555-1234")
    customer2 = Customer(2, "Jane Smith", "555-5678")
    
    # Create sample bookings
    current_time = int(time.time() * 1000)
    day_in_ms = 24 * 60 * 60 * 1000
    
    booking1 = Booking(1, customer1, car1, current_time - (3 * day_in_ms))
    booking1.add()
    
    booking2 = Booking(2, customer2, car2, current_time - (7 * day_in_ms), current_time - (2 * day_in_ms))
    booking2.add()


if __name__ == "__main__":
    # Initialize sample data
    create_sample_data()
    
    # Create the main application window
    root = ParentFrame.get_main_frame()
    
    # Display booking details
    booking_details = BookingDetails()
    
    # Start the application
    root.mainloop()