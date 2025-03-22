import tkinter as tk
from tkinter import messagebox, Frame, Button, Label, Entry, StringVar, Toplevel
import sys
sys.path.append('..')  # Add parent directory to path
from backend_code.customer import Customer

class CustomerAdd:
    def __init__(self):
        self.frame = tk.Toplevel()
        self.frame.title("Add Customer")
        self.frame.geometry("450x290")
        self.frame.resizable(False, False)
        self.frame.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Center the window relative to the main frame
        parent_frame = self.get_parent_frame()
        if parent_frame:
            x = parent_frame.winfo_x() + (parent_frame.winfo_width() - 450) // 2
            y = parent_frame.winfo_y() + (parent_frame.winfo_height() - 290) // 2
            self.frame.geometry(f"+{x}+{y}")
        
        # Create widgets
        # CNIC field
        self.cnic_label = Label(self.frame, text="Enter CNIC (without dashes)")
        self.cnic_label.place(x=10, y=5, width=175, height=22)
        
        self.cnic_text_field = Entry(self.frame)
        self.cnic_text_field.place(x=195, y=5, width=240, height=22)
        
        self.cnic_validity_label = Label(self.frame, fg="red")
        self.cnic_validity_label.place(x=195, y=30, width=240, height=9)
        
        # Name field
        self.name_label = Label(self.frame, text="Enter Name")
        self.name_label.place(x=10, y=42, width=175, height=22)
        
        self.name_text_field = Entry(self.frame)
        self.name_text_field.place(x=195, y=42, width=240, height=22)
        
        self.name_validity_label = Label(self.frame, fg="red")
        self.name_validity_label.place(x=195, y=66, width=240, height=9)
        
        # Contact field
        self.contact_label = Label(self.frame, text="Enter Contact")
        self.contact_label.place(x=10, y=77, width=175, height=22)
        
        self.contact_text_field = Entry(self.frame)
        self.contact_text_field.place(x=195, y=77, width=240, height=22)
        
        self.contact_validity_label = Label(self.frame, fg="red")
        self.contact_validity_label.place(x=195, y=102, width=240, height=9)
        
        # Email field (commented out as it's not used in original code)
        # self.email_label = Label(self.frame, text="Enter Email")
        # self.email_label.place(x=10, y=112, width=175, height=22)
        # 
        # self.email_text_field = Entry(self.frame)
        # self.email_text_field.place(x=195, y=112, width=240, height=22)
        # 
        # self.email_validity_label = Label(self.frame, fg="red")
        # self.email_validity_label.place(x=195, y=137, width=240, height=9)
        
        # Username field (commented out as it's not used in original code)
        # self.username_label = Label(self.frame, text="Enter Username")
        # self.username_label.place(x=10, y=147, width=175, height=22)
        # 
        # self.username_text_field = Entry(self.frame)
        # self.username_text_field.place(x=195, y=147, width=240, height=22)
        # 
        # self.username_validity_label = Label(self.frame, fg="red")
        # self.username_validity_label.place(x=195, y=172, width=240, height=9)
        
        # Password field (commented out as it's not used in original code)
        # self.password_label = Label(self.frame, text="Enter Password")
        # self.password_label.place(x=10, y=182, width=175, height=22)
        # 
        # self.password_text_field = Entry(self.frame)
        # self.password_text_field.place(x=195, y=182, width=240, height=22)
        # 
        # self.password_validity_label = Label(self.frame, fg="red")
        # self.password_validity_label.place(x=195, y=207, width=240, height=9)
        
        # Buttons
        self.add_button = Button(self.frame, text="Add", command=self.add_customer)
        self.add_button.place(x=100, y=225, width=100, height=22)
        
        self.cancel_button = Button(self.frame, text="Cancel", command=self.cancel)
        self.cancel_button.place(x=250, y=225, width=100, height=22)

    def add_customer(self):
        cnic = self.cnic_text_field.get().strip()
        name = self.name_text_field.get().strip()
        contact = self.contact_text_field.get().strip()
        
        if Customer.is_cnic_valid(cnic):
            customer = Customer.search_by_cnic(cnic)
            if customer is None:
                if Customer.is_name_valid(name):
                    if Customer.is_contact_no_valid(contact):
                        # Create and add new customer (ID is auto-generated)
                        new_customer = Customer(0, 0, cnic, name, contact)
                        new_customer.add()
                        
                        # Update the main frame
                        parent_frame = self.get_parent_frame()
                        if parent_frame:
                            for widget in parent_frame.winfo_children():
                                widget.destroy()
                            from gui.customer_details import CustomerDetails
                            customer_details = CustomerDetails()
                            parent_frame.add(customer_details.get_main_panel())
                            parent_frame.update_idletasks()
                        
                        self.enable_parent_frame()
                        messagebox.showinfo("Success", "Customer added successfully!")
                        self.frame.destroy()
                    else:
                        messagebox.showerror("Error", "Invalid contact no.!")
                else:
                    messagebox.showerror("Error", "Invalid Name!")
            else:
                messagebox.showerror("Error", "This CNIC is already registered!")
        else:
            messagebox.showerror("Error", "Invalid CNIC")

    def cancel(self):
        self.enable_parent_frame()
        self.frame.destroy()
    
    def on_closing(self):
        self.enable_parent_frame()
        self.frame.destroy()
    
    def get_parent_frame(self):
        from gui.parent_frame import ParentFrame
        return ParentFrame.get_main_frame()
    
    def enable_parent_frame(self):
        parent_frame = self.get_parent_frame()
        if parent_frame:
            parent_frame.setEnabled(True)


# For testing purposes
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    app = CustomerAdd()
    root.mainloop()