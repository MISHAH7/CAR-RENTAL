import tkinter as tk
from tkinter import messagebox, Frame, Button, Label, Entry, StringVar, Toplevel
import sys
sys.path.append('..')  # Add parent directory to path
from backend_code.car_owner import CarOwner


class CarOwnerUpdate:
    car_owner = None  # Class variable to store the found car owner

    def __init__(self):
        self.frame = tk.Toplevel()
        self.frame.title("Update CarOwner")
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
        self.id_label = Label(self.frame, text="Enter ID to be Updated")
        self.id_label.place(x=10, y=5, width=175, height=22)
        
        self.id_text_field = Entry(self.frame)
        self.id_text_field.place(x=195, y=5, width=240, height=22)
        
        self.id_validity_label = Label(self.frame, fg="red")
        self.id_validity_label.place(x=195, y=30, width=240, height=9)
        
        self.ok_button = Button(self.frame, text="OK", command=self.find_car_owner)
        self.ok_button.place(x=100, y=225, width=100, height=22)
        
        self.cancel_button = Button(self.frame, text="Cancel", command=self.cancel)
        self.cancel_button.place(x=250, y=225, width=100, height=22)

    def find_car_owner(self):
        car_owner_id = self.id_text_field.get().strip()
        
        if not car_owner_id:
            self.id_validity_label.config(text="Enter ID!")
            return
            
        if CarOwner.is_id_valid(car_owner_id):
            # Save the class variable
            CarOwnerUpdate.car_owner = CarOwner.search_by_id(int(car_owner_id))
            if CarOwnerUpdate.car_owner is not None:
                self.get_parent_frame().setEnabled(False)
                self.frame.destroy()
                update_inner = UpdateCarOwnerInner()
                update_inner.set_visible(True)
            else:
                messagebox.showinfo("Not Found", "Required ID is not found!")
        else:
            self.id_validity_label.config(text="Invalid ID!")

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


class UpdateCarOwnerInner:
    def __init__(self):
        self.frame = tk.Toplevel()
        self.frame.title("Update CarOwner")
        self.frame.geometry("450x290")
        self.frame.resizable(False, False)
        self.frame.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Get the car owner data from the class variable
        self.car_owner = CarOwnerUpdate.car_owner
        
        # Create widgets
        self.cnic_label = Label(self.frame, text="Enter CNIC (without dashes)")
        self.cnic_label.place(x=10, y=5, width=175, height=22)
        
        self.cnic_text_field = Entry(self.frame)
        self.cnic_text_field.insert(0, self.car_owner.get_cnic())
        self.cnic_text_field.place(x=195, y=5, width=240, height=22)
        
        self.cnic_validity_label = Label(self.frame, fg="red")
        self.cnic_validity_label.place(x=195, y=30, width=240, height=9)
        
        self.name_label = Label(self.frame, text="Enter Name")
        self.name_label.place(x=10, y=42, width=175, height=22)
        
        self.name_text_field = Entry(self.frame)
        self.name_text_field.insert(0, self.car_owner.get_name())
        self.name_text_field.place(x=195, y=42, width=240, height=22)
        
        self.name_validity_label = Label(self.frame, fg="red")
        self.name_validity_label.place(x=195, y=66, width=240, height=9)
        
        self.contact_label = Label(self.frame, text="Enter Contact")
        self.contact_label.place(x=10, y=77, width=175, height=22)
        
        self.contact_text_field = Entry(self.frame)
        self.contact_text_field.insert(0, self.car_owner.get_contact_no())
        self.contact_text_field.place(x=195, y=77, width=240, height=22)
        
        self.contact_validity_label = Label(self.frame, fg="red")
        self.contact_validity_label.place(x=195, y=102, width=240, height=9)
        
        self.update_button = Button(self.frame, text="Update", command=self.update_car_owner)
        self.update_button.place(x=100, y=225, width=100, height=22)
        
        self.cancel_button = Button(self.frame, text="Cancel", command=self.cancel)
        self.cancel_button.place(x=250, y=225, width=100, height=22)
        
    def update_car_owner(self):
        cnic = self.cnic_text_field.get().strip()
        name = self.name_text_field.get().strip()
        contact = self.contact_text_field.get().strip()
        
        # Validate CNIC
        if not cnic:
            self.cnic_validity_label.config(text="Enter CNIC!")
            cnic = None
        elif not CarOwner.is_cnic_valid(cnic):
            self.cnic_validity_label.config(text="Invalid CNIC!")
            cnic = None
        else:
            print("CNIC is valid")
            co = CarOwner.search_by_cnic(cnic)
            if co is not None:
                if cnic == self.car_owner.get_cnic():
                    print("no change in cnic")
                else:
                    cnic = None
                    messagebox.showinfo("Error", "This CNIC is already registered!")
            else:
                print("new CNIC is entered")
        
        # Validate Name
        if not name:
            self.name_validity_label.config(text="Enter Name!")
            name = None
        elif not CarOwner.is_name_valid(name):
            self.name_validity_label.config(text="Invalid Name!")
            name = None
        else:
            print("valid car owner name!")
        
        # Validate Contact
        if not contact:
            self.contact_validity_label.config(text="Enter Contact Number!")
            contact = None
        elif not CarOwner.is_contact_no_valid(contact):
            self.contact_validity_label.config(text="Invalid Contact Number!")
            contact = None
        else:
            print("Valid car owner contact!")
        
        # If all fields are valid, update the car owner
        if cnic is not None and name is not None and contact is not None:
            # Create a new car owner object with updated values
            updated_car_owner = CarOwner(
                self.car_owner.get_balance(),
                self.car_owner.get_id(),
                cnic,
                name,
                contact
            )
            print(updated_car_owner)
            updated_car_owner.update()
            
            # Update the main frame
            parent_frame = self.get_parent_frame()
            if parent_frame:
                for widget in parent_frame.winfo_children():
                    widget.destroy()
                from gui.car_owner_details import CarOwnerDetails
                car_owner_details = CarOwnerDetails()
                parent_frame.add(car_owner_details.get_main_panel())
                parent_frame.update_idletasks()
            
            messagebox.showinfo("Success", "Record Successfully Updated!")
            self.enable_parent_frame()
            self.frame.destroy()
    
    def cancel(self):
        self.enable_parent_frame()
        self.frame.destroy()
    
    def on_closing(self):
        self.enable_parent_frame()
        self.frame.destroy()
    
    def set_visible(self, visible):
        if visible:
            self.frame.deiconify()
        else:
            self.frame.withdraw()
    
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
    app = CarOwnerUpdate()
    root.mainloop()