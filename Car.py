import os
import pickle
from typing import List, Optional

class CarOwner:
    # This is a placeholder class as it's referenced but not defined in the original code
    def __init__(self):
        pass
        
    def __str__(self):
        return "CarOwner Details"  # Placeholder for toString() method

class Car:
    def __init__(self, ID=0, Maker="", Name="", Colour="", Type="", 
                 SeatingCapacity=0, Model="", Condition="", RegNo="", 
                 RentPerHour=0, carOwner=None):
        self.ID = ID
        self.Maker = Maker
        self.Name = Name
        self.Colour = Colour
        self.Type = Type
        self.SeatingCapacity = SeatingCapacity
        self.Model = Model
        self.Condition = Condition
        self.RegNo = RegNo
        self.RentPerHour = RentPerHour
        self.carOwner = carOwner if carOwner else CarOwner()

    # Getters and setters
    def get_ID(self):
        return self.ID

    def set_ID(self, ID):
        self.ID = ID

    def get_Maker(self):
        return self.Maker

    def set_Maker(self, Maker):
        self.Maker = Maker

    def get_Name(self):
        return self.Name

    def set_Name(self, Name):
        self.Name = Name

    def get_Colour(self):
        return self.Colour

    def set_Colour(self, Colour):
        self.Colour = Colour

    def get_Type(self):
        return self.Type

    def set_Type(self, Type):
        self.Type = Type

    def get_SeatingCapacity(self):
        return self.SeatingCapacity

    def set_SeatingCapacity(self, SeatingCapacity):
        self.SeatingCapacity = SeatingCapacity

    def get_Model(self):
        return self.Model

    def set_Model(self, Model):
        self.Model = Model

    def get_Condition(self):
        return self.Condition

    def set_Condition(self, Condition):
        self.Condition = Condition

    def get_RegNo(self):
        return self.RegNo

    def set_RegNo(self, RegNo):
        self.RegNo = RegNo

    def get_RentPerHour(self):
        return self.RentPerHour

    def set_RentPerHour(self, RentPerHour):
        self.RentPerHour = RentPerHour

    def get_CarOwner(self):
        return self.carOwner

    def set_CarOwner(self, carOwner):
        self.carOwner = carOwner

    def __str__(self):
        return (f"Car_new{{ID={self.ID}, Maker={self.Maker}, Name={self.Name}, "
                f"Colour={self.Colour}, \nType={self.Type}, SeatingCapacity={self.SeatingCapacity}, "
                f"Model={self.Model}, Condition={self.Condition}, RegNo={self.RegNo}, "
                f"RentPerHour={self.RentPerHour}, \ncarOwner={self.carOwner}}}") + "\n"

    def Add(self):
        cars = Car.View()
        if not cars:
            self.ID = 1
        else:
            self.ID = cars[-1].ID + 1  # Auto ID...
        
        cars.append(self)
        
        try:
            with open("Car.pkl", "wb") as file:
                for car in cars:
                    pickle.dump(car, file)
        except Exception as ex:
            print(ex)

    def Update(self):
        cars = Car.View()

        # Replace car with matching ID
        for i in range(len(cars)):
            if cars[i].ID == self.ID:
                cars[i] = self
                
        # Write updated cars back to file
        try:
            with open("Car.pkl", "wb") as file:
                for car in cars:
                    pickle.dump(car, file)
        except Exception as ex:
            print(ex)

    def Remove(self):
        cars = Car.View()
        
        # Remove car with matching ID
        cars = [car for car in cars if car.ID != self.ID]
        
        # Write updated cars back to file
        try:
            with open("Car.pkl", "wb") as file:
                for car in cars:
                    pickle.dump(car, file)
        except Exception as ex:
            print(ex)

    @staticmethod
    def SearchByName(name: str) -> List['Car']:
        cars = Car.View()
        return [car for car in cars if car.Name.lower() == name.lower()]

    @staticmethod
    def SearchByID(id: int) -> Optional['Car']:
        cars = Car.View()
        for car in cars:
            if car.ID == id:
                return car
        return None

    @staticmethod
    def SearchByRegNo(regNo: str) -> Optional['Car']:
        cars = Car.View()
        for car in cars:
            if car.RegNo.lower() == regNo.lower():
                return car
        return None

    @staticmethod
    def View() -> List['Car']:
        car_list = []
        
        if not os.path.exists("Car.pkl"):
            return car_list
            
        try:
            with open("Car.pkl", "rb") as file:
                while True:
                    try:
                        my_obj = pickle.load(file)
                        car_list.append(my_obj)
                    except EOFError:
                        break
                    except Exception as e:
                        print(e)
        except Exception as e:
            print(e)
            
        return car_list

    @staticmethod
    def isNameValid(Name: str) -> bool:
        if not Name:
            return False
            
        for char in Name:
            if not (char.isalpha() or char.isdigit() or char == ' '):
                return False
        return True

    @staticmethod
    def isRegNoValid(RegNo: str) -> bool:
        # reg no must contain letters followed by digits, both separated by '-' dash
        # EXAMPLE: ASD-2343
        tokens = RegNo.split("-")
        if len(tokens) == 2:
            if not tokens[0].isalpha():
                return False
            if not tokens[1].isdigit():
                return False
            return True
        return False

    def isRented(self) -> bool:
        from booking import Booking  # Assuming Booking class is defined elsewhere
        booked_cars = Booking.getBookedCars()
        return any(car.ID == self.ID for car in booked_cars)