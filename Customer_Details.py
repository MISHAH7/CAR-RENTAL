import tkinter as tk
from tkinter import ttk, messagebox
import sys
from typing import List, Optional

# Assuming these backend classes are defined elsewhere
# We'll include stub classes for demonstration purposes
class Customer:
    @staticmethod
    def View() -> List['Customer']:
        # This would normally fetch data from a database
        return []

    @staticmethod
    def isIDvalid(id_str: str) -> bool:
        try:
            int(id_str)
            return True
        except ValueError:
            return False

    @staticmethod
    def isNameValid(name: str) -> bool:
        return bool(name and name.strip())

    @staticmethod
    def SearchByID(id_num: int) -> Optional['Customer']:
        # This would normally search in a database
        return None

    @staticmethod
    def SearchByName(name: str) -> List['Customer']:
        # This would normally search in a database
        return []

    def __init__(self, id_num=0, cnic="", name="", contact_no="", bill=0):
        self._id = id_num
        self._cnic = cnic
        self._name = name
        self._contact_no = contact_no
        self._bill = bill

    def getID(self) -> int:
        return self._id

    def getCNIC(self) -> str:
        return self._cnic

    def getName(self) -> str:
        return self._name

    def getContact_No(self) -> str:
        return self._contact_no

    def getBill(self) -> int:
        return self._bill

    def setBill(self, bill: int) -> None:
        self._bill = bill

    def Update(self) -> None:
        # This would normally update the database
        pass

    def __str__(self) -> str:
        return f"ID: {self._id}, Name: {self._name}, CNIC: {self._cnic}, Contact: {self._contact_no}, Bill: {self._bill}"


class Booking:
    @staticmethod
    def SearchByCustomerID(customer_id: int) -> List['Booking']:
        # This would normally search in a database
        return []

    def __init__(self):
        self._car = None
        self._return_time = 0

    def getCar(self):
        return self._car

    def getReturnTime(self) -> int:
        return self._return_time


class Car:
    def __init__(self, id_num=0, name=""):
        self._id = id_num
        self._name = name

    def getID(self) -> int:
        return self._id

    def getName(self) -> str:
        return self._name


class CustomerDetails:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.parent_frame.title("Customer Details - Rent-A-Car Management System")
        
        # Create main frame
        self.main_frame = ttk.Frame(parent_frame, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create search frame
        search_frame = ttk.Frame(self.main_frame)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Search by name components
        ttk.Label(search_frame, text="Search by Name:").grid(row=0, column=0, padx=5, pady=5)
        self.search_name_entry = ttk.Entry(search_frame, width=30)
        self.search_name_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(search_frame, text="Search Name", command=self.search_by_name).grid(row=0, column=2, padx=5, pady=5)
        
        # Search by ID components
        ttk.Label(search_frame, text="Search by ID:").grid(row=0, column=3, padx=5, pady=5)
        self.search_id_entry = ttk.Entry(search_frame, width=30)
        self.search_id_entry.grid(row=0, column=4, padx=5, pady=5)
        ttk.Button(search_frame, text="Search ID", command=self.search_by_id).grid(row=0, column=5, padx=5, pady=5)
        
        # Create table frame
        table_frame = ttk.Frame(self.main_frame)
        table_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Create table
        columns = ("Sr#", "ID", "CNIC", "Name", "Contact Number", "Car Rented", "Bill")
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings')
        
        # Set column headings
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=tk.CENTER)
        
        # Set column widths
        self.tree.column("Sr#", width=70)
        self.tree.column("ID", width=150)
        self.tree.column("CNIC", width=170)
        self.tree.column("Name", width=110)
        self.tree.column("Contact Number", width=180)
        self.tree.column("Car Rented", width=140)
        self.tree.column("Bill", width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Create buttons frame
        buttons_frame = ttk.Frame(self.main_frame)
        buttons_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Add buttons
        ttk.Button(buttons_frame, text="Clear Bill", command=self.clear_bill).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(buttons_frame, text="Add", command=self.add_customer).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(buttons_frame, text="Update", command=self.update_customer).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(buttons_frame, text="Remove", command=self.remove_customer).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(buttons_frame, text="Back", command=self.go_back).pack(side=tk.RIGHT, padx=5, pady=5)
        ttk.Button(buttons_frame, text="Logout", command=self.logout).pack(side=tk.RIGHT, padx=5, pady=5)
        
        # Populate table
        self.populate_table()

    def populate_table(self):
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get customer data
        customer_objects = Customer.View()
        
        for i, customer in enumerate(customer_objects):
            customer_id = customer.getID()
            cnic = customer.getCNIC()
            name = customer.getName()
            contact_no = customer.getContact_No()
            bill = customer.getBill()
            
            # Get booked cars for customer
            bookings = Booking.SearchByCustomerID(customer_id)
            booked_cars = ""
            
            if bookings:
                for booking in bookings:
                    if booking.getReturnTime() == 0:
                        booked_cars += f"{booking.getCar().getID()}: {booking.getCar().getID()}\n"
                    else:
                        booked_cars = "No Cars Booked !"
            else:
                booked_cars = "No Cars Booked !"
            
            # Add data to table
            self.tree.insert("", "end", values=(i+1, customer_id, cnic, name, contact_no, booked_cars, bill))

    def search_by_id(self):
        id_str = self.search_id_entry.get().strip()
        
        if not id_str:
            messagebox.showinfo("Error", "Please Enter ID first !")
            return
        
        if not Customer.isIDvalid(id_str):
            messagebox.showinfo("Error", "Invalid ID !")
            return
        
        customer = Customer.SearchByID(int(id_str))
        
        if customer:
            messagebox.showinfo("Customer Details", str(customer))
            self.search_id_entry.delete(0, tk.END)
        else:
            messagebox.showinfo("Error", "Required person not found")
            self.search_id_entry.delete(0, tk.END)

    def search_by_name(self):
        name = self.search_name_entry.get().strip()
        
        if not name:
            messagebox.showinfo("Error", "Please Enter Name first !")
            return
        
        if not Customer.isNameValid(name):
            messagebox.showinfo("Error", "Invalid Name !")
            return
        
        customers = Customer.SearchByName(name)
        
        if customers:
            record = "\n".join(str(customer) for customer in customers)
            messagebox.showinfo("Customer Details", record)
            self.search_name_entry.delete(0, tk.END)
        else:
            messagebox.showinfo("Error", "Required person not found")
            self.search_name_entry.delete(0, tk.END)

    def add_customer(self):
        # This would normally open a new window to add a customer
        # For demonstration, we'll just show a message
        messagebox.showinfo("Add Customer", "This would open a window to add a new customer")

    def update_customer(self):
        # This would normally open a new window to update a customer
        # For demonstration, we'll just show a message
        messagebox.showinfo("Update Customer", "This would open a window to update a customer")

    def remove_customer(self):
        # This would normally open a new window to remove a customer
        # For demonstration, we'll just show a message
        messagebox.showinfo("Remove Customer", "This would open a window to remove a customer")

    def clear_bill(self):
        customers = Customer.View()
        
        if not customers:
            messagebox.showinfo("Error", "No Customer Currently Registered !")
            return
        
        ids_array = []
        for customer in customers:
            if customer.getBill() != 0:
                ids_array.append(str(customer.getID()))
        
        if not ids_array:
            messagebox.showinfo("Error", "No customers with outstanding bills")
            return
        
        selected_id = tk.simpledialog.askstring(
            "Clear Bill",
            "Select ID for Customer whose bill you want to clear.",
            initialvalue=ids_array[0] if ids_array else ""
        )
        
        if not selected_id:
            return
        
        customer = Customer.SearchByID(int(selected_id))
        
        if not customer:
            messagebox.showinfo("Error", "Customer not found")
            return
        
        confirm = messagebox.askyesno(
            "Clear Bill Confirmation",
            f"You are about to clear the balance for the following Customer\n{customer}\nAre you sure you want to continue ?"
        )
        
        if confirm:
            customer.setBill(0)
            customer.Update()
            self.populate_table()
            messagebox.showinfo("Success", "Bill Successfully Cleared !")

    def go_back(self):
        # This would normally go back to the main menu
        # For demonstration, we'll just show a message
        messagebox.showinfo("Back", "This would return to the main menu")

    def logout(self):
        # This would normally logout and return to the login screen
        # For demonstration, we'll just show a message
        messagebox.showinfo("Logout", "This would logout and return to the login screen")
        self.parent_frame.destroy()
        sys.exit()


class MainMenu:
    def __init__(self):
        pass


class CustomerAdd:
    def __init__(self):
        self.window = tk.Toplevel()
        self.window.title("Add Customer")
        self.window.geometry("400x300")
        self.window.transient()
        self.window.grab_set()


class CustomerRemove:
    def __init__(self):
        self.window = tk.Toplevel()
        self.window.title("Remove Customer")
        self.window.geometry("400x300")
        self.window.transient()
        self.window.grab_set()


class CustomerUpdate:
    def __init__(self):
        self.window = tk.Toplevel()
        self.window.title("Update Customer")
        self.window.geometry("400x300")
        self.window.transient()
        self.window.grab_set()


class Login:
    def __init__(self):
        pass


# Main application
class RentACarApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Rent-A-Car Management System [REBORN]")
        self.root.geometry("1366x730")
        
        # Create the customer details screen
        self.customer_details = CustomerDetails(self.root)
        
    def run(self):
        self.root.mainloop()


# Run the application
if __name__ == "__main__":
    app = RentACarApp()
    app.run()