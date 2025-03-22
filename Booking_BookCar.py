import tkinter as tk
from tkinter import messagebox, StringVar
import time
from datetime import datetime

# Backend classes to simulate the Java backend
class Car:
    all_cars = {}  # Class variable to store all cars
    
    def __init__(self, car_id, model, year, is_rented=False):
        self.car_id = car_id
        self.model = model
        self.year = year
        self.is_rented = is_rented
        Car.all_cars[car_id] = self
    
    @classmethod
    def search_by_id(cls, car_id):
        return cls.all_cars.get(car_id)
    
    def __str__(self):
        return f"Car ID: {self.car_id}, Model: {self.model}, Year: {self.year}, Rented: {'Yes' if self.is_rented else 'No'}"


class Customer:
    all_customers = {}  # Class variable to store all customers
    
    def __init__(self, customer_id, name, phone):
        self.customer_id = customer_id
        self.name = name
        self.phone = phone
        Customer.all_customers[customer_id] = self
    
    @classmethod
    def search_by_id(cls, customer_id):
        return cls.all_customers.get(customer_id)
    
    def __str__(self):
        return f"Customer ID: {self.customer_id}, Name: {self.name}, Phone: {self.phone}"


class Booking:
    all_bookings = []  # Class variable to store all bookings
    
    def __init__(self, booking_id, customer, car, booking_time, return_time=0):
        self.booking_id = booking_id if booking_id > 0 else len(Booking.all_bookings) + 1
        self.customer = customer
        self.car = car
        self.booking_time = booking_time
        self.return_time = return_time
    
    def add(self):
        self.car.is_rented = True
        Booking.all_bookings.append(self)
        return True
    
    def __str__(self):
        booking_date = datetime.fromtimestamp(self.booking_time / 1000).strftime('%Y-%m-%d %H:%M:%S')
        return_date = "Not returned yet" if self.return_time == 0 else datetime.fromtimestamp(self.return_time / 1000).strftime('%Y-%m-%d %H:%M:%S')
        return f"Booking ID: {self.booking_id}, Customer: {self.customer.name}, Car: {self.car.model}, Booked on: {booking_date}, Return: {return_date}"


# Main application classes
class ParentFrame:
    _main_frame = None
    
    @classmethod
    def get_main_frame(cls):
        if cls._main_frame is None:
            cls._main_frame = tk.Tk()
            cls._main_frame.title("Car Rental System")
            cls._main_frame.geometry("800x600")
        return cls._main_frame
    
    @classmethod
    def refresh_frame(cls, panel):
        for widget in cls.get_main_frame().winfo_children():
            widget.destroy()
        cls.get_main_frame().add(panel)


class BookingDetails:
    def __init__(self):
        self.main_panel = tk.Frame(ParentFrame.get_main_frame())
        # Here you would implement the booking details view
        # For brevity, this is just a placeholder
        label = tk.Label(self.main_panel, text="Booking Details")
        label.pack(pady=20)
        
        # Display all bookings
        for booking in Booking.all_bookings:
            booking_info = tk.Label(self.main_panel, text=str(booking))
            booking_info.pack(pady=5)
    
    def get_main_panel(self):
        return self.main_panel


class BookingBookCar(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Book Car")
        self.geometry("300x200")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Initialize member variables
        self.car = None
        self.customer = None
        
        # Create UI components
        self.create_widgets()
        
        # Center the window
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_widgets(self):
        # Car ID input section
        self.car_id_label = tk.Label(self, text="Enter Car ID to be Booked")
        self.car_id_label.pack(pady=(10, 0))
        
        self.car_id_var = StringVar()
        self.car_id_textfield = tk.Entry(self, textvariable=self.car_id_var, width=30)
        self.car_id_textfield.pack()
        
        self.car_id_validity_label = tk.Label(self, text="", fg="red")
        self.car_id_validity_label.pack()
        
        # Customer ID input section
        self.customer_id_label = tk.Label(self, text="Enter Customer ID")
        self.customer_id_label.pack()
        
        self.customer_id_var = StringVar()
        self.customer_id_textfield = tk.Entry(self, textvariable=self.customer_id_var, width=30)
        self.customer_id_textfield.pack()
        
        self.customer_id_validity_label = tk.Label(self, text="", fg="red")
        self.customer_id_validity_label.pack()
        
        # Buttons
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)
        
        self.book_button = tk.Button(button_frame, text="Book", width=10, command=self.on_book)
        self.book_button.pack(side=tk.LEFT, padx=5)
        
        self.cancel_button = tk.Button(button_frame, text="Cancel", width=10, command=self.on_closing)
        self.cancel_button.pack(side=tk.LEFT, padx=5)
    
    def on_book(self):
        # Validate Car ID
        car_id = self.car_id_var.get().strip()
        if car_id:
            try:
                car_id_int = int(car_id)
                if car_id_int > 0:
                    self.car_id_validity_label.config(text="")
                    self.car = Car.search_by_id(car_id_int)
                    if self.car:
                        if not self.car.is_rented:
                            self.car_id_validity_label.config(text="")
                        else:
                            self.car = None
                            messagebox.showinfo("Error", "This car is already booked!")
                            return
                    else:
                        car_id = None
                        self.car_id_validity_label.config(text="Car ID does not exist!")
                        return
                else:
                    car_id = None
                    self.car_id_validity_label.config(text="ID cannot be '0' or negative!")
                    return
            except ValueError:
                car_id = None
                self.car_id_validity_label.config(text="Invalid ID!")
                return
        else:
            car_id = None
            self.car_id_validity_label.config(text="Enter Car ID!")
            return
        
        # Validate Customer ID
        customer_id = self.customer_id_var.get().strip()
        if customer_id:
            try:
                customer_id_int = int(customer_id)
                if customer_id_int > 0:
                    self.customer_id_validity_label.config(text="")
                    self.customer = Customer.search_by_id(customer_id_int)
                    if self.customer:
                        self.customer_id_validity_label.config(text="")
                    else:
                        customer_id = None
                        messagebox.showinfo("Error", "Customer ID does not exist!")
                        return
                else:
                    customer_id = None
                    self.customer_id_validity_label.config(text="ID cannot be '0' or negative!")
                    return
            except ValueError:
                customer_id = None
                self.customer_id_validity_label.config(text="Invalid ID!")
                return
        else:
            customer_id = None
            self.customer_id_validity_label.config(text="Enter Customer ID!")
            return
        
        # If both car and customer are valid, proceed with booking
        if car_id and customer_id:
            self.state('normal')
            confirm = messagebox.askokcancel(
                "Book Confirmation",
                f"You are about to Book the Car: \n{self.car}\n against the Customer: \n{self.customer}\n Are you sure you want to continue?"
            )
            
            if confirm:
                # Create a new booking
                booking = Booking(0, self.customer, self.car, int(time.time() * 1000))
                booking.add()
                
                # Update the main frame
                main_frame = ParentFrame.get_main_frame()
                for widget in main_frame.winfo_children():
                    widget.destroy()
                
                booking_details = BookingDetails()
                booking_details.get_main_panel().pack(fill=tk.BOTH, expand=True)
                
                messagebox.showinfo("Success", "Car Successfully Booked!")
                main_frame.state('normal')
                self.destroy()
            else:
                self.state('normal')
    
    def on_closing(self):
        ParentFrame.get_main_frame().state('normal')
        self.destroy()


# Sample data initialization
def create_sample_data():
    # Create sample cars
    Car(1, "Toyota Camry", 2020)
    Car(2, "Honda Civic", 2021)
    Car(3, "Ford Mustang", 2022)
    
    # Create sample customers
    Customer(1, "John Doe", "555-1234")
    Customer(2, "Jane Smith", "555-5678")
    Customer(3, "Bob Johnson", "555-9012")


if __name__ == "__main__":
    # Initialize sample data
    create_sample_data()
    
    # Create the main application window
    root = ParentFrame.get_main_frame()
    
    # Open the booking window
    booking_window = BookingBookCar()
    root.state("normal")  # Disable the main window while booking
    
    # Start the application
    root.mainloop()