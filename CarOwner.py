import os
import pickle
from typing import List, Optional
from person import Person  # Assuming Person class is defined in person.py
from car import Car  # Importing Car class from car.py

class CarOwner(Person):
    def __init__(self, Balance=0, ID=0, CNIC="", Name="", Contact_No=""):
        super().__init__(ID, CNIC, Name, Contact_No)
        self.Balance = Balance  # increases after every HOUR when Owner's car(s) is booked

    def get_Balance(self):
        return self.Balance

    def set_Balance(self, Balance):
        self.Balance = Balance

    def __str__(self):
        return super().__str__() + f" CarOwner{{Balance={self.Balance}}}" + "\n"

    def Add(self):
        car_owners = CarOwner.View()
        if not car_owners:
            self.ID = 1
        else:
            self.ID = car_owners[-1].ID + 1  # Auto ID ...
        
        car_owners.append(self)
        
        try:
            with open("CarOwner.pkl", "wb") as file:
                for owner in car_owners:
                    pickle.dump(owner, file)
        except Exception as ex:
            print(ex)

    def Update(self):
        car_owners = CarOwner.View()

        # Replace car owner with matching ID
        for i in range(len(car_owners)):
            if car_owners[i].ID == self.ID:
                car_owners[i] = self
                
        # Write updated car owners back to file
        try:
            with open("CarOwner.pkl", "wb") as file:
                for owner in car_owners:
                    pickle.dump(owner, file)
        except Exception as ex:
            print(ex)

    def Remove(self):
        car_owners = CarOwner.View()
        
        # Remove car owner with matching ID
        car_owners = [owner for owner in car_owners if owner.ID != self.ID]
        
        # Write updated car owners back to file
        try:
            with open("CarOwner.pkl", "wb") as file:
                for owner in car_owners:
                    pickle.dump(owner, file)
        except Exception as ex:
            print(ex)

    @staticmethod
    def SearchByName(name: str) -> List['CarOwner']:
        car_owners = CarOwner.View()
        results = []
        
        for owner in car_owners:
            if owner.Name.lower() == name.lower():
                results.append(owner)
                
        return results

    @staticmethod
    def SearchByCNIC(carOwnerCNIC: str) -> Optional['CarOwner']:
        car_owners = CarOwner.View()
        for owner in car_owners:
            if owner.CNIC.lower() == carOwnerCNIC.lower():
                return owner
        return None

    @staticmethod
    def SearchByID(id: int) -> Optional['CarOwner']:
        car_owners = CarOwner.View()
        for owner in car_owners:
            if owner.ID == id:
                return owner
        return None

    def getAllCars(self) -> List[Car]:
        cars = Car.View()
        owner_cars = []
        for car in cars:
            if car.get_CarOwner().ID == self.ID:
                owner_cars.append(car)
        return owner_cars

    @staticmethod
    def View() -> List['CarOwner']:
        car_owner_list = []
        
        if not os.path.exists("CarOwner.pkl"):
            return car_owner_list
            
        try:
            with open("CarOwner.pkl", "rb") as file:
                while True:
                    try:
                        my_obj = pickle.load(file)
                        car_owner_list.append(my_obj)
                    except EOFError:
                        break
                    except Exception as e:
                        print(e)
        except Exception as e:
            print(e)
            
        return car_owner_list