import pickle
import os
from datetime import datetime
import sys
import traceback

class Booking:
    def __init__(self, ID=None, customer=None, car=None, rent_time=None, return_time=None):
        self.ID = ID
        self.customer = customer
        self.car = car
        self.rent_time = rent_time
        self.return_time = return_time if return_time is not None else 0

    def get_ID(self):
        return self.ID

    def set_ID(self, ID):
        self.ID = ID

    def get_customer(self):
        return self.customer

    def set_customer(self, customer):
        self.customer = customer

    def get_car(self):
        return self.car

    def set_car(self, car):
        self.car = car

    def get_rent_time(self):
        return self.rent_time

    def set_rent_time(self, rent_time):
        self.rent_time = rent_time

    def get_return_time(self):
        return self.return_time

    def set_return_time(self, return_time):
        self.return_time = return_time

    def __str__(self):
        return f"Booking{{ID={self.ID}, \ncustomer={self.customer}, \ncar={self.car}, \nRentTime={self.rent_time}, ReturnTime={self.return_time}}}\n"

    def add(self):
        booking = Booking.view()
        if not booking:
            self.ID = 1
        else:
            self.ID = booking[-1].ID + 1  # Auto ID
        
        self.return_time = 0
        booking.append(self)
        
        try:
            with open("Booking.pkl", "wb") as file:
                for b in booking:
                    pickle.dump(b, file)
        except Exception as ex:
            print(ex)
            traceback.print_exc()

    def update(self):
        booking = Booking.view()
        
        # Replace old booking with same ID
        for i in range(len(booking)):
            if booking[i].ID == self.ID:
                booking[i] = self
        
        try:
            with open("Booking.pkl", "wb") as file:
                for b in booking:
                    pickle.dump(b, file)
        except Exception as ex:
            print(ex)
            traceback.print_exc()

    def remove(self):
        booking = Booking.view()
        
        # Filter out the booking with matching ID
        new_bookings = [b for b in booking if b.ID != self.ID]
        
        try:
            with open("Booking.pkl", "wb") as file:
                for b in new_bookings:
                    pickle.dump(b, file)
        except Exception as ex:
            print(ex)
            traceback.print_exc()

    def calculate_bill(self):
        # Rent calculation
        rent_time = self.get_rent_time()
        return_time = self.get_return_time()
        total_time = return_time - rent_time
        total_time_hours = total_time / (1000 * 60 * 60)  # Convert milliseconds to hours
        
        rent_per_hour = self.get_car().get_rent_per_hour()
        if total_time_hours != 0:
            return int(rent_per_hour * total_time_hours)
        else:
            return rent_per_hour

    @staticmethod
    def search_by_customer_ID(customer_ID):
        booking_list = []
        try:
            if not os.path.exists("Booking.pkl"):
                return booking_list
                
            with open("Booking.pkl", "rb") as file:
                while True:
                    try:
                        my_obj = pickle.load(file)
                        if my_obj.customer.get_ID() == customer_ID:
                            booking_list.append(my_obj)
                    except EOFError:
                        break
                    except Exception as e:
                        print(e)
                        traceback.print_exc()
        except Exception as e:
            print(e)
            traceback.print_exc()
        
        return booking_list

    @staticmethod
    def search_by_car_reg_no(car_reg_no):
        booking_list = []
        try:
            if not os.path.exists("Booking.pkl"):
                return booking_list
                
            with open("Booking.pkl", "rb") as file:
                while True:
                    try:
                        my_obj = pickle.load(file)
                        if my_obj.car.get_reg_no().lower() == car_reg_no.lower():
                            booking_list.append(my_obj)
                    except EOFError:
                        break
                    except Exception as e:
                        print(e)
                        traceback.print_exc()
        except Exception as e:
            print(e)
            traceback.print_exc()
        
        return booking_list

    @staticmethod
    def search_by_car_ID(car_ID):
        booking_list = []
        try:
            if not os.path.exists("Booking.pkl"):
                return booking_list
                
            with open("Booking.pkl", "rb") as file:
                while True:
                    try:
                        my_obj = pickle.load(file)
                        if my_obj.car.get_ID() == car_ID:
                            booking_list.append(my_obj)
                    except EOFError:
                        break
                    except Exception as e:
                        print(e)
                        traceback.print_exc()
        except Exception as e:
            print(e)
            traceback.print_exc()
        
        return booking_list

    @staticmethod
    def view():
        booking_list = []
        try:
            if not os.path.exists("Booking.pkl"):
                return booking_list
                
            with open("Booking.pkl", "rb") as file:
                while True:
                    try:
                        my_obj = pickle.load(file)
                        booking_list.append(my_obj)
                    except EOFError:
                        break
                    except Exception as e:
                        print(e)
                        traceback.print_exc()
        except Exception as e:
            print(e)
            traceback.print_exc()
        
        return booking_list

    @staticmethod
    def get_booked_cars():
        booked_cars = []
        bookings = Booking.view()
        for booking in bookings:
            if booking.return_time == 0:
                booked_cars.append(booking.car)
        return booked_cars

    @staticmethod
    def get_unbooked_cars():
        from Car import Car  # Import here to avoid circular imports
        all_cars = Car.view()
        booked_cars = Booking.get_booked_cars()
        
        # Return cars that are not in booked_cars
        return [car for car in all_cars if car not in booked_cars]