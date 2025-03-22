import tkinter as tk
from tkinter import ttk, messagebox
import sys
sys.path.append('../')  # Assuming BackendCode is in parent directory
from BackendCode.CarOwner import CarOwner
from BackendCode.Car import Car

class CarOwner_Details:
    def __init__(self):
        self.MainPanel = tk.Frame()
        self.parent_frame = self.get_parent_frame()
        self.parent_frame.title("Car Owner Details - Rent-A-Car Management System")
        self.MainPanel.pack(fill=tk.BOTH, expand=True)
        
        # Create UI components
        self.create_widgets()
        self.populate_table()
        
    def create_widgets(self):
        # Search controls
        search_frame = tk.Frame(self.MainPanel)
        search_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.SearchName_Button = tk.Button(search_frame, text="Search Name", width=15, command=lambda: self.action_performed("Search Name"))
        self.SearchName_TextField = tk.Entry(search_frame, width=30)
        self.SearchID_Button = tk.Button(search_frame, text="Search ID", width=15, command=lambda: self.action_performed("Search ID"))
        self.SearchID_TextField = tk.Entry(search_frame, width=30)
        
        self.SearchName_Button.grid(row=0, column=0, padx=5)
        self.SearchName_TextField.grid(row=0, column=1, padx=5)
        self.SearchID_Button.grid(row=0, column=2, padx=5)
        self.SearchID_TextField.grid(row=0, column=3, padx=5)
        
        # Table
        table_frame = tk.Frame(self.MainPanel)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        columns = ("Sr#", "ID", "CNIC", "Name", "Contact Number", "Car Given for rent", "Balance")
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings')
        
        # Set column headings and widths
        self.tree.heading("Sr#", text="Sr#")
        self.tree.heading("ID", text="ID")
        self.tree.heading("CNIC", text="CNIC")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Contact Number", text="Contact Number")
        self.tree.heading("Car Given for rent", text="Car Given for rent")
        self.tree.heading("Balance", text="Balance")
        
        self.tree.column("Sr#", width=70, anchor=tk.CENTER)
        self.tree.column("ID", width=150, anchor=tk.CENTER)
        self.tree.column("CNIC", width=170, anchor=tk.CENTER)
        self.tree.column("Name", width=110, anchor=tk.CENTER)
        self.tree.column("Contact Number", width=180, anchor=tk.CENTER)
        self.tree.column("Car Given for rent", width=140, anchor=tk.CENTER)
        self.tree.column("Balance", width=100, anchor=tk.CENTER)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        # Pack table and scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Buttons
        button_frame = tk.Frame(self.MainPanel)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.ClearBalance_Button = tk.Button(button_frame, text="Clear Balance", width=20, command=lambda: self.action_performed("Clear Balance"))
        self.Add_Button = tk.Button(button_frame, text="Add", width=15, command=lambda: self.action_performed("Add"))
        self.Update_Button = tk.Button(button_frame, text="Update", width=15, command=lambda: self.action_performed("Update"))
        self.Remove_Button = tk.Button(button_frame, text="Remove", width=15, command=lambda: self.action_performed("Remove"))
        self.Back_Button = tk.Button(button_frame, text="Back", width=12, command=lambda: self.action_performed("Back"))
        self.Logout_Button = tk.Button(button_frame, text="Logout", width=12, command=lambda: self.action_performed("Logout"))
        
        self.ClearBalance_Button.pack(side=tk.LEFT, padx=5)
        self.Add_Button.pack(side=tk.LEFT, padx=5)
        self.Update_Button.pack(side=tk.LEFT, padx=5)
        self.Remove_Button.pack(side=tk.LEFT, padx=5)
        self.Back_Button.pack(side=tk.RIGHT, padx=5)
        self.Logout_Button.pack(side=tk.RIGHT, padx=5)
    
    def populate_table(self):
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get car owners and populate table
        car_owners = CarOwner.View()
        for i, owner in enumerate(car_owners):
            ID = owner.getID()
            CNIC = owner.getCNIC()
            Name = owner.getName()
            ContactNo = owner.getContact_No()
            Balance = owner.getBalance()
            
            # Getting all cars for this Owner
            cars_on_rent = ""
            cars = Car.View()
            
            for car in cars:
                if car.getCarOwner().getID() == ID:
                    cars_on_rent += f"{car.getID()}: {car.getName()}  "
            
            if not cars_on_rent:
                cars_on_rent = "No Cars given for Rent !"
            
            # Add to table
            values = (i+1, ID, CNIC, Name, ContactNo, cars_on_rent, Balance)
            self.tree.insert('', tk.END, values=values)
    
    def get_parent_frame(self):
        # This is equivalent to Parent_JFrame.getMainFrame() in Java
        # In a real application, you would have a reference to the main frame
        # For this conversion, we'll assume we're creating a new parent frame
        try:
            return tk._default_root
        except:
            return tk.Tk()
    
    def get_main_panel(self):
        return self.MainPanel
    
    def action_performed(self, command):
        if command == "Search ID":
            id_text = self.SearchID_TextField.get().strip()
            if id_text:
                if CarOwner.isIDvalid(id_text):
                    co = CarOwner.SearchByID(int(id_text))
                    if co:
                        messagebox.showinfo("Car Owner Details", co.__str__())
                        self.SearchID_TextField.delete(0, tk.END)
                    else:
                        messagebox.showinfo("Not Found", "Required person not found")
                        self.SearchID_TextField.delete(0, tk.END)
                else:
                    messagebox.showwarning("Invalid Input", "Invalid ID !")
            else:
                messagebox.showwarning("Empty Field", "Please Enter ID first !")
        
        elif command == "Search Name":
            name = self.SearchName_TextField.get().strip()
            if name:
                if CarOwner.isNameValid(name):
                    car_owner_list = CarOwner.SearchByName(name)
                    record = ""
                    
                    if car_owner_list:
                        for owner in car_owner_list:
                            record += f"{owner.__str__()}\n"
                        messagebox.showinfo("Car Owner Details", record)
                        self.SearchName_TextField.delete(0, tk.END)
                    else:
                        messagebox.showinfo("Not Found", "Required person not found")
                        self.SearchName_TextField.delete(0, tk.END)
                else:
                    messagebox.showwarning("Invalid Input", "Invalid Name !")
            else:
                messagebox.showwarning("Empty Field", "Please Enter Name first !")
        
        elif command == "Add":
            self.parent_frame.attributes('-disabled', True)
            # Import here to avoid circular imports
            from GUI.CarOwner_Add import CarOwner_Add
            add_window = CarOwner_Add(self.parent_frame)
            add_window.show()
            # After window is closed, refresh the table
            self.populate_table()
        
        elif command == "Remove":
            self.parent_frame.attributes('-disabled', True)
            # Import here to avoid circular imports
            from GUI.CarOwner_Remove import CarOwner_Remove
            remove_window = CarOwner_Remove(self.parent_frame)
            remove_window.show()
            # After window is closed, refresh the table
            self.populate_table()
        
        elif command == "Update":
            self.parent_frame.attributes('-disabled', True)
            # Import here to avoid circular imports
            from GUI.CarOwner_Update import CarOwner_Update
            update_window = CarOwner_Update(self.parent_frame)
            update_window.show()
            # After window is closed, refresh the table
            self.populate_table()
        
        elif command == "Clear Balance":
            # Get all car owners
            view = CarOwner.View()
            if view:
                # Create a list of IDs for owners with balance > 0
                ids_array = []
                for owner in view:
                    if owner.getBalance() != 0:
                        ids_array.append(str(owner.getID()))
                
                if not ids_array:
                    messagebox.showinfo("No Balance", "No car owner has a balance to clear!")
                    return
                
                # Show input dialog for selecting an ID
                selected_id = tk.StringVar()
                dialog = tk.Toplevel(self.parent_frame)
                dialog.title("Clear Balance")
                dialog.transient(self.parent_frame)
                dialog.grab_set()
                
                tk.Label(dialog, text="Select ID for Car Owner whose balance you want to clear:").pack(pady=10)
                id_menu = ttk.Combobox(dialog, textvariable=selected_id, values=ids_array)
                id_menu.pack(pady=5)
                
                def on_ok():
                    if selected_id.get():
                        dialog.destroy()
                        self.process_clear_balance(int(selected_id.get()))
                
                def on_cancel():
                    dialog.destroy()
                
                button_frame = tk.Frame(dialog)
                button_frame.pack(pady=10)
                tk.Button(button_frame, text="OK", command=on_ok).pack(side=tk.LEFT, padx=5)
                tk.Button(button_frame, text="Cancel", command=on_cancel).pack(side=tk.LEFT, padx=5)
                
                # Center the dialog relative to parent
                dialog.update_idletasks()
                x = self.parent_frame.winfo_x() + (self.parent_frame.winfo_width() - dialog.winfo_width()) // 2
                y = self.parent_frame.winfo_y() + (self.parent_frame.winfo_height() - dialog.winfo_height()) // 2
                dialog.geometry(f"+{x}+{y}")
                
                dialog.wait_window()
            else:
                messagebox.showinfo("No Car Owners", "No Car Owner is registered !")
        
        elif command == "Back":
            # Import here to avoid circular imports
            from GUI.MainMenu import MainMenu
            self.parent_frame.title("Rent-A-Car Management System [REBORN]")
            main_menu = MainMenu()
            
            # Clear current content
            for widget in self.parent_frame.winfo_children():
                widget.destroy()
            
            # Add main menu
            main_panel = main_menu.get_main_panel()
            main_panel.pack(fill=tk.BOTH, expand=True)
        
        elif command == "Logout":
            self.parent_frame.destroy()
            # Import here to avoid circular imports
            from GUI.Runner import Runner
            from GUI.Login import Login
            
            runner = Runner()
            frame = Runner.get_frame()
            login = Login()
            panel = login.get_main_panel()
            panel.pack(fill=tk.BOTH, expand=True)
            frame.deiconify()
    
    def process_clear_balance(self, owner_id):
        car_owner = CarOwner.SearchByID(owner_id)
        
        # Show confirmation dialog
        message = f"You are about to clear the balance for the following Car Owner\n{car_owner}\nAre you sure you want to continue?"
        confirm = messagebox.askyesno("Clear Balance Confirmation", message)
        
        if confirm:
            car_owner.setBalance(0)
            car_owner.Update()
            
            # Refresh table
            self.populate_table()
            messagebox.showinfo("Success", "Balance Successfully Cleared!")

# For testing purposes
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1366x730")
    app = CarOwner_Details()
    root.mainloop()