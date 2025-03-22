import os
import pickle
from typing import List, Optional
from person import Person  # Assuming Person class is defined in person.py

class Customer(Person):
    def __init__(self, Bill=0, ID=0, CNIC="", Name="", Contact_No=""):
        super().__init__(ID, CNIC, Name, Contact_No)
        self.Bill = Bill  # increases after every HOUR when a customers has Booked car(s)

    def get_Bill(self):
        return self.Bill

    def set_Bill(self, Bill):
        self.Bill = Bill

    def __str__(self):
        return super().__str__() + f"Customer{{Bill={self.Bill}}}" + "\n"

    def Add(self):
        customers = Customer.View()
        if not customers:
            self.ID = 1
        else:
            self.ID = customers[-1].ID + 1  # Auto ID...
        
        customers.append(self)
        
        try:
            with open("Customer.pkl", "wb") as file:
                for customer in customers:
                    pickle.dump(customer, file)
        except Exception as ex:
            print(ex)

    def Update(self):
        customers = Customer.View()

        # Replace customer with matching ID
        for i in range(len(customers)):
            if customers[i].ID == self.ID:
                customers[i] = self
                
        # Write updated customers back to file
        try:
            with open("Customer.pkl", "wb") as file:
                for customer in customers:
                    pickle.dump(customer, file)
        except Exception as ex:
            print(ex)

    def Remove(self):
        customers = Customer.View()
        
        # Remove customer with matching ID
        customers = [customer for customer in customers if customer.ID != self.ID]
        
        # Write updated customers back to file
        try:
            with open("Customer.pkl", "wb") as file:
                for customer in customers:
                    pickle.dump(customer, file)
        except Exception as ex:
            print(ex)

    @staticmethod
    def SearchByName(name: str) -> List['Customer']:
        customers = Customer.View()
        results = []
        
        for customer in customers:
            if customer.Name.lower() == name.lower():
                results.append(customer)
                
        return results

    @staticmethod
    def SearchByCNIC(CustomerCNIC: str) -> Optional['Customer']:
        customers = Customer.View()
        for customer in customers:
            if customer.CNIC.lower() == CustomerCNIC.lower():
                return customer
        return None

    @staticmethod
    def SearchByID(id: int) -> Optional['Customer']:
        customers = Customer.View()
        for customer in customers:
            if customer.ID == id:
                return customer
        return None

    @staticmethod
    def View() -> List['Customer']:
        customer_list = []
        
        if not os.path.exists("Customer.pkl"):
            return customer_list
            
        try:
            with open("Customer.pkl", "rb") as file:
                while True:
                    try:
                        my_obj = pickle.load(file)
                        customer_list.append(my_obj)
                    except EOFError:
                        break
                    except Exception as e:
                        print(e)
        except Exception as e:
            print(e)
            
        return customer_list