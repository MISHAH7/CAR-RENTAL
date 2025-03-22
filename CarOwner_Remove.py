import tkinter as tk
from tkinter import messagebox, Frame, Button, Label, Entry, StringVar
import sys
sys.path.append('..')  # Add parent directory to path
from backend_code.car import Car
from backend_code.car_owner import CarOwner

class CarOwnerRemove:
    def __init__(self):
        self.frame = tk.Toplevel()
        self.frame.title("Remove CarOwner")
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
        self.id_label = Label(self.frame, text="Enter ID (without dashes)")
        self.id_label.place(x=10, y=5, width=175, height=22)
        
        self.id_text_field = Entry(self.frame)
        self.id_text_field.place(x=195, y=5, width=240, height=22)
        
        self.id_validity_label = Label(self.frame, fg="red")
        self.id_validity_label.place(x=195, y=30, width=240, height=9)
        
        self.remove_button = Button(self.frame, text="Remove", command=self.remove_car_owner)
        self.remove_button.place(x=100, y=225, width=100, height=22)
        
        self.cancel_button = Button(self.frame, text="Cancel", command=self.cancel)
        self.cancel_button.place(x=250, y=225, width=100, height=22)

    def remove_car_owner(self):
        car_id = self.id_text_field.get().strip()
        
        if CarOwner.is_id_valid(car_id):
            car_owner = CarOwner.search_by_id(int(car_id))
            if car_owner is not None:
                message = (f"You are about to remove the following Car Owner.\n{car_owner}\n"
                          f"All the data including Cars and Balance for this car owner will also be deleted!\n"
                          f"Are you sure you want to continue??")
                confirm = messagebox.askokcancel("Remove Car Owner", message)
                
                if confirm:
                    # Delete all cars for this car owner
                    cars = car_owner.get_all_cars()
                    print("Deleting all cars for this car owner!")
                    for car in cars:
                        car.remove()
                    print("All cars deleted!")
                    
                    car_owner.remove()
                    print("Car owner deleted!")
                    
                    parent_frame = self.get_parent_frame()
                    if parent_frame:
                        for widget in parent_frame.winfo_children():
                            widget.destroy()
                        from gui.car_owner_details import CarOwnerDetails
                        car_owner_details = CarOwnerDetails()
                        parent_frame.add_widget(car_owner_details.get_main_panel())
                        parent_frame.update_idletasks()
                    
                    messagebox.showinfo("Success", "Record successfully Removed!")
                    self.enable_parent_frame()
                    self.frame.destroy()
                else:
                    self.frame.lift()
            else:
                messagebox.showerror("Error", "This ID does not exist!")
        else:
            messagebox.showerror("Error", "Enter a valid ID!\n(A valid ID is an integer number greater than 0)")

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
    app = CarOwnerRemove()
    root.mainloop()