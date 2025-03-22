import tkinter as tk
from tkinter import messagebox, font
import time
from backend.booking import Booking
from backend.car import Car
from backend.car_owner import CarOwner
from backend.customer import Customer

class BookingUnbookCar(tk.Toplevel):
    def __init__(self, parent_frame):
        super().__init__()
        self.title("UnBook Car")
        self.geometry("300x145")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.parent_frame = parent_frame
        self.car = None
        
        # Create UI elements
        self.car_id_label = tk.Label(self, text="Enter Car ID to be UnBooked")
        self.car_id_textfield = tk.Entry(self, width=30)
        self.car_id_validity_label = tk.Label(self, text="", fg="red")
        
        self.unbook_button = tk.Button(self, text="UnBook", width=12, command=self.unbook_action)
        self.cancel_button = tk.Button(self, text="Cancel", width=12, command=self.on_closing)
        
        # Place UI elements
        self.car_id_label.pack(pady=(10, 0))
        self.car_id_textfield.pack(pady=(5, 0))
        self.car_id_validity_label.pack(pady=(2, 0))
        
        button_frame = tk.Frame(self)
        button_frame.pack(pady=(10, 0))
        self.unbook_button.pack(side=tk.LEFT, padx=5, in_=button_frame)
        self.cancel_button.pack(side=tk.LEFT, padx=5, in_=button_frame)
        
        # Center the window
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        
    def unbook_action(self):
        car_id = self.car_id_textfield.get().strip()
        
        if car_id:
            try:
                car_id_int = int(car_id)
                if car_id_int > 0:
                    self.car_id_validity_label.config(text="")
                    self.car = Car.search_by_id(car_id_int)
                    
                    if self.car is not None:
                        if self.car.is_rented():
                            self.car_id_validity_label.config(text="")
                        else:
                            self.car = None
                            messagebox.showinfo("Information", "This car is not booked!")
                    else:
                        self.car = None
                        messagebox.showinfo("Information", "Car ID does not exist!")
                else:
                    car_id = None
                    self.car_id_validity_label.config(text="ID cannot be '0' or negative!")
            except ValueError:
                car_id = None
                self.car_id_validity_label.config(text="Invalid ID!")
        else:
            car_id = None
            self.car_id_validity_label.config(text="Enter Car ID!")
        
        if car_id is not None and self.car is not None:
            self.attributes('-disabled', True)
            confirm_message = f"You are about to UnBook this Car\n{self.car}\nAre you sure you want to continue??"
            confirm = messagebox.askokcancel("UnBook Confirmation", confirm_message)
            
            if confirm:
                # Get booking information
                booking_list = Booking.search_by_car_id(int(car_id))
                last_booking = booking_list[-1]  # Get the last booking
                
                # Update booking return time
                last_booking.set_return_time(int(time.time() * 1000))  # Current time in milliseconds
                last_booking.update()
                
                # Calculate bill
                bill = last_booking.calculate_bill()
                
                # Update car owner's balance
                car_owner = last_booking.get_car().get_car_owner()
                car_owner.set_balance(car_owner.get_balance() + bill)
                car_owner.update()
                
                # Update customer's bill
                customer = last_booking.get_customer()
                customer.set_bill(customer.get_bill() + bill)
                customer.update()
                
                # Update UI
                from gui.booking_details import BookingDetails
                self.parent_frame.content_pane.destroy()
                self.parent_frame.content_pane = BookingDetails(self.parent_frame).get_main_panel()
                self.parent_frame.content_pane.pack(fill=tk.BOTH, expand=True)
                
                messagebox.showinfo("Success", "Car Successfully UnBooked!")
                self.parent_frame.enable()
                self.destroy()
            else:
                self.attributes('-disabled', False)
    
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
        
    def show_booking_unbook_car(self):
        self.disable()
        BookingUnbookCar(self)
        
    def run(self):
        self.root.mainloop()


# Example usage (if this module is run directly)
if __name__ == "__main__":
    # This would typically be part of a larger application
    app = ParentFrame()
    app.show_booking_unbook_car()
    app.run()