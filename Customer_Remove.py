import tkinter as tk
from tkinter import messagebox, Frame
import sys
from backend_code.booking import Booking
from backend_code.customer import Customer

class CustomerRemove:
    def __init__(self):
        self.frame = tk.Toplevel()
        self.frame.title("Remove Customer")
        self.frame.geometry("450x290")
        self.frame.resizable(False, False)
        self.frame.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Center the window relative to main frame
        self.frame.transient(parent_frame.get_main_frame())
        self.frame.geometry(f"+{parent_frame.get_main_frame().winfo_x() + 50}+{parent_frame.get_main_frame().winfo_y() + 50}")
        
        # Create widgets
        self.id_label = tk.Label(self.frame, text="Enter ID (without dashes)")
        self.id_label.place(x=10, y=5, width=175, height=22)
        
        self.id_text_field = tk.Entry(self.frame)
        self.id_text_field.place(x=195, y=5, width=240, height=22)
        
        self.id_validity_label = tk.Label(self.frame, fg="red")
        self.id_validity_label.place(x=195, y=30, width=240, height=9)
        
        self.remove_button = tk.Button(self.frame, text="Remove", command=self.handle_remove)
        self.remove_button.place(x=100, y=225, width=100, height=22)
        
        self.cancel_button = tk.Button(self.frame, text="Cancel", command=self.handle_cancel)
        self.cancel_button.place(x=250, y=225, width=100, height=22)
        
        # Disable main frame
        parent_frame.get_main_frame().attributes('-disabled', True)
    
    def on_closing(self):
        parent_frame.get_main_frame().attributes('-disabled', False)
        self.frame.destroy()
    
    def handle_remove(self):
        customer_id = self.id_text_field.get().strip()
        if Customer.is_id_valid(customer_id):
            try:
                customer = Customer.search_by_id(int(customer_id))
                if customer is not None:
                    message = (f"You are about to remove the following Customer.\n{customer}\n"
                              f"All the data including Booked Cars and Balance for this Customer will also be deleted!\n"
                              "Are you sure you want to continue??")
                    confirm = messagebox.askokcancel("Remove Customer", message)
                    
                    if confirm:
                        # Deleting all the booking records of customer
                        bookings = Booking.view()
                        for booking in bookings:
                            if customer.get_id() == booking.get_customer().get_id():
                                booking.remove()
                        
                        # Delete the customer
                        customer.remove()
                        
                        print("Customer deleted!")
                        
                        # Update the main frame
                        parent_frame.get_main_frame().clear_all()
                        customer_details = CustomerDetails()
                        parent_frame.get_main_frame().add(customer_details.get_main_panel())
                        parent_frame.get_main_frame().revalidate()
                        
                        messagebox.showinfo("Success", "Record successfully Removed!")
                        parent_frame.get_main_frame().attributes('-disabled', False)
                        self.frame.destroy()
                    else:
                        self.frame.attributes('-disabled', False)
                else:
                    messagebox.showinfo("Error", "This ID does not exist!")
            except ValueError:
                messagebox.showinfo("Error", "Enter a valid ID!\n(A valid ID is an integer number greater than 0)")
        else:
            messagebox.showinfo("Error", "Enter a valid ID!\n(A valid ID is an integer number greater than 0)")
    
    def handle_cancel(self):
        parent_frame.get_main_frame().attributes('-disabled', False)
        self.frame.destroy()


# Mock parent_frame class to replace the Java Parent_JFrame
class ParentFrame:
    def __init__(self):
        self.main_frame = tk.Tk()
        self.main_frame.title("Customer Management System")
        self.main_frame.geometry("800x600")
    
    def get_main_frame(self):
        return self.main_frame
    
    def clear_all(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
    def add(self, panel):
        panel.pack(fill=tk.BOTH, expand=True)
    
    def revalidate(self):
        self.main_frame.update()


# Mock CustomerDetails class
class CustomerDetails:
    def __init__(self):
        self.main_panel = Frame()
        # Add customer details components here
    
    def get_main_panel(self):
        return self.main_panel


# Create global parent_frame instance
parent_frame = ParentFrame()

# Usage example
if __name__ == "__main__":
    customer_remove = CustomerRemove()
    parent_frame.get_main_frame().mainloop()