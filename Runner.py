import tkinter as tk
from PIL import Image, ImageTk
import time

# This would be your converted Login module
# from login import Login

class Runner:
    # Class variable for the frame
    _frame = None
    
    @staticmethod
    def get_frame():
        return Runner._frame
    
    def __init__(self):
        # Initialize the frame if it doesn't exist
        if Runner._frame is None:
            Runner._frame = tk.Tk()
            
        # Configure the frame properties
        Runner._frame.overrideredirect(True)  # Equivalent to setUndecorated(true)
        Runner._frame.geometry("1000x534")
        Runner._frame.eval('tk::PlaceWindow . center')  # Center the window
        
        # Load the welcome image
        try:
            image = Image.open("WelcomeImage.jpg")
            self.icon = ImageTk.PhotoImage(image)
            self.label = tk.Label(Runner._frame, image=self.icon)
            self.label.pack(fill=tk.BOTH, expand=True)
        except Exception as e:
            # Fallback if image isn't available
            print(f"Error loading image: {e}")
            self.label = tk.Label(Runner._frame, text="Welcome", font=("Arial", 24))
            self.label.pack(fill=tk.BOTH, expand=True)


def main():
    # Create the runner instance
    runner = Runner()
    Runner.get_frame().update()  # Force update to show the frame
    
    # Show the frame
    Runner.get_frame().deiconify()
    
    try:
        # Sleep for 1 second (splash screen)
        time.sleep(1)
        
        # Clear the frame and add login panel
        for widget in Runner.get_frame().winfo_children():
            widget.destroy()
        
        # Add login panel
        # login_object = Login()
        # Runner.get_frame().add(login_object.get_main_panel())
        # For now, just add a placeholder label
        placeholder = tk.Label(Runner.get_frame(), text="Login Screen", font=("Arial", 24))
        placeholder.pack(fill=tk.BOTH, expand=True)
        
        # Update the frame
        Runner.get_frame().update()
        
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
    # Start the Tkinter main loop
    Runner.get_frame().mainloop()