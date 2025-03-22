from abc import ABC, abstractmethod

class Person(ABC):
    def __init__(self, ID=0, CNIC="", Name="", Contact_No=""):
        self.ID = ID
        self.CNIC = CNIC
        self.Name = Name
        self.Contact_No = Contact_No

    def get_ID(self):
        return self.ID

    def set_ID(self, ID):
        self.ID = ID

    def get_CNIC(self):
        return self.CNIC

    def set_CNIC(self, CNIC):
        self.CNIC = CNIC

    def get_Name(self):
        return self.Name

    def set_Name(self, Name):
        self.Name = Name

    def get_Contact_No(self):
        return self.Contact_No

    def set_Contact_No(self, Contact_No):
        self.Contact_No = Contact_No

    @abstractmethod
    def Add(self):
        pass

    @abstractmethod
    def Update(self):
        pass

    @abstractmethod
    def Remove(self):
        pass

    def __str__(self):
        return f"Person_new{{ID={self.ID}, CNIC={self.CNIC}, Name={self.Name}, Contact_No={self.Contact_No}}}"

    @staticmethod
    def isCNICValid(cnic):
        """
        A valid CNIC consists of 13 characters, only digits.
        
        Args:
            cnic: The CNIC whose validity is to be checked
            
        Returns:
            bool: True if the passed CNIC is valid
        """
        if len(cnic) != 13:
            return False
            
        return all(char.isdigit() for char in cnic)

    @staticmethod
    def isContactNoValid(contact):
        """
        A valid Contact No. has 11 digits and starts with "03"
        
        Args:
            contact: The contact number to check
            
        Returns:
            bool: True if the contact is valid
        """
        if len(contact) != 11:
            return False
            
        if not contact.startswith("03"):
            return False
            
        return all(char.isdigit() for char in contact)

    @staticmethod
    def isNameValid(Name):
        """
        A valid name can contain only letters and white spaces
        
        Args:
            Name: The name to check
            
        Returns:
            bool: True if the name is valid
        """
        if not Name:
            return False
            
        return all(char.isalpha() or char.isspace() for char in Name)

    @staticmethod
    def isIDvalid(ID):
        """
        A valid ID can only be digit greater than 0
        
        Args:
            ID: The ID to check
            
        Returns:
            bool: True if the ID is valid
        """
        if not ID:
            return False
            
        if not all(char.isdigit() for char in ID):
            return False
            
        return int(ID) > 0