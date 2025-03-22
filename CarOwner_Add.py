import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sys
sys.path.append('./');  # Assuming BackendCode is in parent directory
  # You'll need to implement this class separately

class CarOwner_Add:
    def __init__(self, parent_frame=None):
        self.frame = tk.Toplevel()
        self.frame.title("Add CarOwner")
        self.frame.geometry("450x290")
        self.frame.resizable(False, False)
        self.frame.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.frame.transient(parent_frame)  # Set parent relationship
        self.parent_frame = parent_frame
        
        if parent_frame:
            parent_frame.attributes('-disabled', True)  # Disable parent frame
            # Center the window relative to parent
            x = parent_frame.winfo_x() + (parent_frame.winfo_width() - 450) // 2
            y = parent_frame.winfo_y() + (parent_frame.winfo_height() - 290) // 2
            self.frame.geometry(f"+{x}+{y}")
        
        # Create widgets
        self.create_widgets()
        
    def create_widgets(self):
        # Labels
        self.CNIC_Label = tk.Label(self.frame, text="Enter CNIC (without dashes)", width=25, anchor="w")
        self.Name_Label = tk.Label(self.frame, text="Enter Name", width=25, anchor="w")
        self.Contact_Label = tk.Label(self.frame, text="Enter Contact", width=25, anchor="w")
        
        # Text Fields
        self.CNIC_TextField = tk.Entry(self.frame, width=30)
        self.Name_TextField = tk.Entry(self.frame, width=30)
        self.Contact_TextField = tk.Entry(self.frame, width=30)
        
        # Validation Labels
        self.CNICValidity_Label = tk.Label(self.frame, text="", fg="red", width=30)
        self.NameValidity_Label = tk.Label(self.frame, text="", fg="red", width=30)
        self.contactValidity_Label = tk.Label(self.frame, text="", fg="red", width=30)
        
        # Buttons
        self.Add_Button = tk.Button(self.frame, text="Add", width=10, command=self.add_car_owner)
        self.Cancel_Button = tk.Button(self.frame, text="Cancel", width=10, command=self.cancel)
        
        # Place widgets using place manager (equivalent to AbsoluteLayout)
        self.CNIC_Label.place(x=10, y=5)
        self.CNIC_TextField.place(x=195, y=5)
        self.CNICValidity_Label.place(x=195, y=30)
        
        self.Name_Label.place(x=10, y=42)
        self.Name_TextField.place(x=195, y=42)
        self.NameValidity_Label.place(x=195, y=66)
        
        self.Contact_Label.place(x=10, y=77)
        self.Contact_TextField.place(x=195, y=77)
        self.contactValidity_Label.place(x=195, y=102)
        
        self.Add_Button.place(x=100, y=225)
        self.Cancel_Button.place(x=250, y=225)
    
    def add_car_owner(self):
        cnic = self.CNIC_TextField.get().strip()
        name = self.Name_TextField.get().strip()
        contact = self.Contact_TextField.get().strip()
        
        if CarOwner.isCNICValid(cnic):
            car_owner = CarOwner.SearchByCNIC(cnic)
            if car_owner is None:
                if CarOwner.isNameValid(name):
                    if CarOwner.isContactNoValid(contact):
                        # Create and add new car owner (ID is Auto)
                        new_owner = CarOwner(0, 0, cnic, name, contact)
                        new_owner.Add()
                        
                        # Update parent frame
                        if self.parent_frame:
                            self.parent_frame.attributes('-disabled', False)
                            # You'll need to implement this part according to your application structure
                            # This is equivalent to:
                            # Parent_JFrame.getMainFrame().getContentPane().removeAll();
                            # CarOwner_Details cd = new CarOwner_Details();
                            # Parent_JFrame.getMainFrame().add(cd.getMainPanel());
                            # Parent_JFrame.getMainFrame().getContentPane().revalidate();
                            
                        messagebox.showinfo("Success", "Car Owner added successfully!")
                        self.frame.destroy()
                    else:
                        messagebox.showwarning("Invalid Input", "Invalid contact no.!")
                else:
                    messagebox.showwarning("Invalid Input", "Invalid Name!")
            else:
                messagebox.showwarning("Duplicate", "This CNIC is already registered!")
        else:
            messagebox.showwarning("Invalid Input", "Invalid CNIC")
    
    def cancel(self):
        if self.parent_frame:
            self.parent_frame.attributes('-disabled', False)
        self.frame.destroy()
    
    def on_closing(self):
        if self.parent_frame:
            self.parent_frame.attributes('-disabled', False)
        self.frame.destroy()
    
    def show(self):
        self.frame.grab_set()  # Make window modal
        self.frame.focus_set()  # Take over input focus
        self.frame.wait_window()  # Wait for window to be destroyed

# Usage example
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    root.title("Parent Frame")
    
    def open_car_owner_add():
        app = CarOwner_Add(root)
        app.show()
    
    open_button = tk.Button(root, text="Open Car Owner Add", command=open_car_owner_add)
    open_button.pack(pady=20)
    
    root.mainloop()