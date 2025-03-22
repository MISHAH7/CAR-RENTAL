import tkinter as tk
from tkinter import messagebox, simpledialog
import datetime
from backend_code.car import Car

class Car_Remove(tk.Toplevel):
    """
    A window for removing a car from the system
    """
    
    def __init__(self, parent):
        """Initialize the Car_Remove window"""
        super().__init__(parent)
        self.title("Remove Car")
        self.geometry("300x140")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.parent = parent
        
        # Center the window
        self.position_center()
        
        # Create GUI components
        self.car_id_label = tk.Label(self, text="Enter Car ID to be removed")
        self.car_id_textfield = tk.Entry(self, width=30)
        self.car_id_validity_label = tk.Label(self, text="", fg="red")
        
        self.remove_button = tk.Button(self, text="Remove", width=10, command=self.remove_car)
        self.cancel_button = tk.Button(self, text="Cancel", width=10, command=self.on_close)
        
        # Layout components
        self.car_id_label.pack(pady=(10, 0))
        self.car_id_textfield.pack(pady=(5, 0))
        self.car_id_validity_label.pack(pady=(2, 10), fill=tk.X)
        
        button_frame = tk.Frame(self)
        button_frame.pack(pady=(0, 10))
        self.remove_button.pack(side=tk.LEFT, padx=5, in_=button_frame)
        self.cancel_button.pack(side=tk.LEFT, padx=5, in_=button_frame)
        
        # Make this window modal
        self.transient(parent)
        self.grab_set()
        parent.wait_window(self)
    
    def position_center(self):
        """Center the window on the screen"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'+{x}+{y}')
    
    def remove_car(self):
        """Handle the remove car button action"""
        car_id = self.car_id_textfield.get().strip()
        
        if not car_id:
            self.car_id_validity_label.config(text="Enter Car ID!")
            return
            
        try:
            car_id_int = int(car_id)
            if car_id_int <= 0:
                self.car_id_validity_label.config(text="ID cannot be '0' or negative!")
                return
                
            # Clear any previous validation messages
            self.car_id_validity_label.config(text="")
            
            # Search for the car by ID
            car = Car.search_by_id(car_id_int)
            
            if car:
                # Confirm removal with the user
                confirm = messagebox.askokcancel(
                    "Confirmation",
                    f"You are about to remove this car\n{car}\nAre you sure you want to continue??"
                )
                
                if confirm:
                    # Remove the car
                    car.remove()
                    
                    # Update the main window's content
                    self.parent.content_pane.destroy()
                    from gui.car_details import Car_Details
                    car_details = Car_Details(self.parent)
                    self.parent.content_pane = car_details.get_main_panel()
                    self.parent.content_pane.pack(fill=tk.BOTH, expand=True)
                    
                    # Close this window
                    self.on_close()
            else:
                messagebox.showerror("Error", "Car ID not found!")
                
        except ValueError:
            self.car_id_validity_label.config(text="Invalid ID!")
    
    def on_close(self):
        """Handle window close event"""
        self.parent.deiconify()  # Re-enable the parent window
        self.parent.focus_set()  # Set focus back to the parent window
        self.destroy()  # Close this window


# Example usage:
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    app = Car_Remove(root)  # This will run the dialog
    root.mainloop()