import tkinter as tk
from tkinter import messagebox
from backend_code.customer import Customer

class CustomerUpdate:
    # Class variable to store customer for use in inner class
    customer = None  
    
    def __init__(self):
        self.frame = tk.Toplevel()
        self.frame.title("Update Customer")
        self.frame.geometry("450x290")
        self.frame.resizable(False, False)
        self.frame.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Center window relative to main frame
        self.frame.transient(parent_frame.get_main_frame())
        self.frame.geometry(f"+{parent_frame.get_main_frame().winfo_x() + 50}+{parent_frame.get_main_frame().winfo_y() + 50}")
        
        # Create widgets
        self.id_label = tk.Label(self.frame, text="Enter ID to be Updated")
        self.id_label.place(x=10, y=5, width=175, height=22)
        
        self.id_text_field = tk.Entry(self.frame)
        self.id_text_field.place(x=195, y=5, width=240, height=22)
        
        self.id_validity_label = tk.Label(self.frame, fg="red")
        self.id_validity_label.place(x=195, y=30, width=240, height=9)
        
        self.ok_button = tk.Button(self.frame, text="OK", command=self.handle_ok)
        self.ok_button.place(x=100, y=225, width=100, height=22)
        
        self.cancel_button = tk.Button(self.frame, text="Cancel", command=self.handle_cancel)
        self.cancel_button.place(x=250, y=225, width=100, height=22)
        
        # Disable main frame
        parent_frame.get_main_frame().attributes('-disabled', True)
    
    def on_closing(self):
        parent_frame.get_main_frame().attributes('-disabled', False)
        self.frame.destroy()
    
    def handle_ok(self):
        co = Customer()
        customer_id = self.id_text_field.get().strip()
        
        if customer_id:
            if Customer.is_id_valid(customer_id):
                co.set_id(int(customer_id))
                CustomerUpdate.customer = Customer.search_by_id(int(customer_id))
                
                if CustomerUpdate.customer is not None:
                    parent_frame.get_main_frame().attributes('-disabled', False)
                    self.frame.destroy()
                    update_inner = UpdateCustomerInner()
                    update_inner.set_visible(True)
                else:
                    messagebox.showinfo("Error", "Required ID is not found!")
            else:
                self.id_validity_label.config(text="Invalid ID!")
        else:
            self.id_validity_label.config(text="Enter ID!")
    
    def handle_cancel(self):
        parent_frame.get_main_frame().attributes('-disabled', False)
        self.frame.destroy()


class UpdateCustomerInner:
    def __init__(self):
        self.window = tk.Toplevel()
        self.window.title("Update Customer")
        self.window.geometry("450x290")
        self.window.resizable(False, False)
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Center window
        self.window.geometry(f"+{parent_frame.get_main_frame().winfo_x() + 50}+{parent_frame.get_main_frame().winfo_y() + 50}")
        
        # Create widgets
        self.cnic_label = tk.Label(self.window, text="Enter CNIC (without dashes)")
        self.cnic_label.place(x=10, y=5, width=175, height=22)
        
        self.cnic_text_field = tk.Entry(self.window)
        self.cnic_text_field.insert(0, CustomerUpdate.customer.get_cnic())
        self.cnic_text_field.place(x=195, y=5, width=240, height=22)
        
        self.cnic_validity_label = tk.Label(self.window, fg="red")
        self.cnic_validity_label.place(x=195, y=30, width=240, height=9)
        
        self.name_label = tk.Label(self.window, text="Enter Name")
        self.name_label.place(x=10, y=42, width=175, height=22)
        
        self.name_text_field = tk.Entry(self.window)
        self.name_text_field.insert(0, CustomerUpdate.customer.get_name())
        self.name_text_field.place(x=195, y=42, width=240, height=22)
        
        self.name_validity_label = tk.Label(self.window, fg="red")
        self.name_validity_label.place(x=195, y=66, width=240, height=9)
        
        self.contact_label = tk.Label(self.window, text="Enter Contact")
        self.contact_label.place(x=10, y=77, width=175, height=22)
        
        self.contact_text_field = tk.Entry(self.window)
        self.contact_text_field.insert(0, CustomerUpdate.customer.get_contact_no())
        self.contact_text_field.place(x=195, y=77, width=240, height=22)
        
        self.contact_validity_label = tk.Label(self.window, fg="red")
        self.contact_validity_label.place(x=195, y=102, width=240, height=9)
        
        self.update_button = tk.Button(self.window, text="Update", command=self.handle_update)
        self.update_button.place(x=100, y=225, width=100, height=22)
        
        self.cancel_button = tk.Button(self.window, text="Cancel", command=self.handle_cancel)
        self.cancel_button.place(x=250, y=225, width=100, height=22)
    
    def set_visible(self, visible):
        if visible:
            self.window.deiconify()
        else:
            self.window.withdraw()
    
    def on_closing(self):
        parent_frame.get_main_frame().attributes('-disabled', False)
        self.window.destroy()
    
    def handle_update(self):
        cnic = self.cnic_text_field.get().strip()
        name = self.name_text_field.get().strip()
        contact = self.contact_text_field.get().strip()
        
        # Validate CNIC
        if cnic:
            print("cnic is not empty")
            if Customer.is_cnic_valid(cnic):
                print("CNIC is valid")
                co = Customer.search_by_cnic(cnic)
                if co is not None:
                    if cnic == CustomerUpdate.customer.get_cnic():
                        print("no change in cnic")
                    else:
                        cnic = None
                        messagebox.showinfo("Error", "This CNIC is already registered!")
                else:
                    print("new CNIC is entered")
            else:
                cnic = None
                self.cnic_validity_label.config(text="Invalid CNIC!")
        else:
            cnic = None
            self.cnic_validity_label.config(text="Enter CNIC!")
        
        # Validate Name
        if name:
            if Customer.is_name_valid(name):
                print("valid Customer name!")
            else:
                name = None
                self.name_validity_label.config(text="Invalid Name!")
        else:
            name = None
            self.name_validity_label.config(text="Enter Name!")
        
        # Validate Contact
        if contact:
            if Customer.is_contact_no_valid(contact):
                print("Valid Customer contact!")
            else:
                contact = None
                self.contact_validity_label.config(text="Invalid Contact Number!")
        else:
            contact = None
            self.contact_validity_label.config(text="Enter Contact Number!")
        
        print(f"the value of cnic before null condition is {cnic}")
        
        # If all validations pass, update the customer
        if cnic is not None and name is not None and contact is not None:
            customer = Customer(
                CustomerUpdate.customer.get_bill(),
                CustomerUpdate.customer.get_id(),
                cnic,
                name,
                contact
            )
            print(customer)
            customer.update()
            
            # Update main frame
            parent_frame.get_main_frame().clear_all()
            customer_details = CustomerDetails()
            parent_frame.get_main_frame().add(customer_details.get_main_panel())
            parent_frame.get_main_frame().revalidate()
            
            messagebox.showinfo("Success", "Record Successfully Updated!")
            parent_frame.get_main_frame().attributes('-disabled', False)
            self.window.destroy()
    
    def handle_cancel(self):
        parent_frame.get_main_frame().attributes('-disabled', False)
        self.window.destroy()


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
        self.main_panel = tk.Frame()
        # Add customer details components here
    
    def get_main_panel(self):
        return self.main_panel


# Create global parent_frame instance
parent_frame = ParentFrame()

# Usage example
if __name__ == "__main__":
    customer_update = CustomerUpdate()
    parent_frame.get_main_frame().mainloop()