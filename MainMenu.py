import tkinter as tk
from tkinter import font as tkfont
from PIL import Image, ImageTk
import os

# These would be your other Python modules (converted from Java)
# from car_details import CarDetails
# from customer_details import CustomerDetails
# from car_owner_details import CarOwnerDetails
# from booking_details import BookingDetails
# from login import Login
# from runner import Runner

class MainMenu:
    def __init__(self, parent_frame=None):
        self.parent_frame = parent_frame
        
        # Create main panel
        self.main_panel = tk.Frame(width=1366, height=730)
        self.main_panel.pack_propagate(False)  # Don't shrink
        
        # Create buttons with specified font and color
        button_font = tkfont.Font(family="Tahoma", size=14, weight="bold")
        button_bg_color = "#F0F0F0"  # equivalent to new Color(240,240,240)
        
        self.booking_button = tk.Button(
            self.main_panel, 
            text="Booking Details", 
            font=button_font, 
            bg=button_bg_color,
            command=lambda: self.action_performed("Booking Details")
        )
        
        self.customer_button = tk.Button(
            self.main_panel, 
            text="Customer", 
            font=button_font, 
            bg=button_bg_color,
            command=lambda: self.action_performed("Customer")
        )
        
        self.cars_button = tk.Button(
            self.main_panel, 
            text="Cars", 
            font=button_font, 
            bg=button_bg_color,
            command=lambda: self.action_performed("Cars")
        )
        
        self.owner_button = tk.Button(
            self.main_panel, 
            text="Owner", 
            font=button_font, 
            bg=button_bg_color,
            command=lambda: self.action_performed("Owner")
        )
        
        self.logout_button = tk.Button(
            self.main_panel, 
            text="Logout", 
            font=button_font, 
            bg=button_bg_color,
            command=lambda: self.action_performed("Logout")
        )
        
        # Create image label
        # Note: In a real application, you'd need to ensure the image file exists
        try:
            image = Image.open("LoginImage.JPG")
            self.image_tk = ImageTk.PhotoImage(image)
            self.image_label = tk.Label(self.main_panel, image=self.image_tk)
        except:
            # Fallback if image isn't available
            self.image_label = tk.Label(self.main_panel, bg="lightgray", width=1370, height=710)
        
        # Place widgets on the panel (similar to AbsoluteLayout)
        self.booking_button.place(x=70, y=80, width=200, height=99)
        self.customer_button.place(x=70, y=220, width=200, height=99) 
        self.owner_button.place(x=70, y=360, width=200, height=99)
        self.cars_button.place(x=70, y=500, width=200, height=99)
        self.logout_button.place(x=1166, y=80, width=100, height=25)
        self.image_label.place(x=0, y=0, width=1370, height=710)
        
    def get_main_panel(self):
        return self.main_panel
    
    def action_performed(self, action):
        if action == "Cars":
            if self.parent_frame:
                for widget in self.parent_frame.winfo_children():
                    widget.destroy()
                # car_details = CarDetails()
                # self.parent_frame.add(car_details.get_main_panel())
                print("Navigating to Car Details")
                
        elif action == "Customer":
            if self.parent_frame:
                for widget in self.parent_frame.winfo_children():
                    widget.destroy()
                # customer_details = CustomerDetails()
                # self.parent_frame.add(customer_details.get_main_panel())
                print("Navigating to Customer Details")
                
        elif action == "Owner":
            if self.parent_frame:
                for widget in self.parent_frame.winfo_children():
                    widget.destroy()
                # car_owner_details = CarOwnerDetails()
                # self.parent_frame.add(car_owner_details.get_main_panel())
                print("Navigating to Car Owner Details")
                
        elif action == "Booking Details":
            if self.parent_frame:
                for widget in self.parent_frame.winfo_children():
                    widget.destroy()
                # booking_details = BookingDetails()
                # self.parent_frame.add(booking_details.get_main_panel())
                print("Navigating to Booking Details")
                
        elif action == "Logout":
            if self.parent_frame:
                self.parent_frame.destroy()
                # Create a new window for login
                # runner = Runner()
                # frame = runner.get_frame()
                # login = Login()
                # panel = login.get_main_panel()
                # frame.add(panel)
                # frame.set_visible(True)
                print("Logging out")


# Example usage 
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Car Rental System")
    root.geometry("1366x730")
    
    main_menu = MainMenu(root)
    main_menu.get_main_panel().pack(fill=tk.BOTH, expand=True)
    
    root.mainloop()