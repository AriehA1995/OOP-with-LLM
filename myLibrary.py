from abc import ABC, abstractmethod
"""
This is my solution for the assessment
Note: abstract methods are used with the abc library
"""
class Library:
    def __init__(self):
        self.__customers = []
        self.__resources = []
        self.__borrowing = dict ()

    #all these properties return the copy of the list and not the list itself - encapsulation
    @property
    def customers (self):
        return list (self.__customers)

    @property
    def resources (self):
        return list (self.__resources)

    @property
    def borrowing (self):
        return dict (self.__borrowing)

    #overloading
    def __contains__ (self, item):
        """
        This method checks if a customer or a resource is in the library
        """
        if isinstance (item, Customer):
            for customer in self.customers:
                if customer.id == item.id:
                    return True
            return False
        elif isinstance (item, Resource):
            for resource in self.resources:
                if resource.id == item.id:
                    return True
            return False
        else:
            return False

    #overloading
    def add (self, item):
        """
        This method adds a customer or a resource to the library
        """
        if isinstance (item, Customer):
            if item in self:
                raise ValueError (f"customer {item.id} already exists")
            else:
                self.__customers.append (item)
                self.__borrowing [item.id] = [] #add an empty list to manage to resources this customer borrows
        elif isinstance (item, Resource):
            if item in self:
                raise ValueError (f"resource {item.id} already exists")
            else:
                self.__resources.append (item)
        else:
            raise TypeError ("the object should be a customer or a resource")

    def removeCustomer (self, id):
        """
        This method remove a customer from the library
        return True if exists, False if not
        raise an error if the customer borrowed some resource
        """
        for customer in self.customers:
            if customer.id == id:
                if len (self.borrowing [id]) == 0:
                    self.__customers.remove (customer)
                    self.__borrowing.pop (customer.id)
                    return True
                else:
                    raise Exception ("cannot remove customer with borrowed resources")
        return False
    
    def removeResource (self, id):
        """
        This method remove a resource from the library
        return True if exists, False if not
        raise an error if the resource is not available
        """
        for resource in self.resources:
            if resource.id == id:
                if resource.status == "available":
                    self.__resources.remove (resource)
                    return True
                else:
                    raise Exception ("cannot remove unavailable resources")
        return False

    def borrowResource (self, customer, resource):
        """
        This method take a customer and a resource and borrow the resource to the customer if available
        """
        if isinstance (customer, Customer) and isinstance (resource, Resource):
            if customer not in self.customers:
                raise ValueError (f"{customer.name} is not a registered to this library!")
            elif resource not in self.resources:
                raise ValueError (f"{resource.name} is not a resource in this library!")
            elif resource.borrow ():
                self.__borrowing [customer.id].append (resource)
                return True
            else:
                raise ValueError (f"cannot borrow this {resource.type}")
        else:
            raise TypeError ("customer or resource incorrect")
            
    def returnResource (self, customer, resource):
        """
        This method take a customer and a resource and return the resource to the library if borrowed to that customer
        """
        if isinstance (customer, Customer) and isinstance (resource, Resource):
            if resource in self.__borrowing [customer.id]:
                resource.returning ()
                self.__borrowing [customer.id].remove (resource)
                return True
            else:
                raise ValueError (f"customer {customer.id} did not borrowed {resource}")
        else:
            raise TypeError ("customer or resource incorrect")

    #overloading
    def availables (self, resourceType = None):
        """
        This method returns a dict if no attributes and a list if attributes
        return a dict of all the resources type with a list of available resources from that type
        if a type is specified, returns a list of available resources from that type
        """
        if resourceType:
            return list (filter (lambda resource: resource.type == resourceType and resource.status == "available", self.resources))
        else:
            availables = dict ()
            for resource in self.resources:
                if resource.status == "available":
                    if resource.type in availables:
                        availables[resource.type].append (resource)
                    else:
                        availables[resource.type] = [resource]
            return availables

    def search (self, id):
        for resource in self.resources:
            if resource.id == id:
                return resource
        return None


class Resource (ABC):
    """
    This is the abstract class for the resource
    resource must have an id, a name, a type and a string representation
    the property status and all the methods connected are already implented
    """
    @abstractmethod
    def __init__ (self, id, name):
        self.__status = "available" #default status is available
        if type (id) == int:
            self.__id = id
        else:
            raise TypeError ("id must be an integer")
        self.name = name

    @property
    def id (self):
        return self.__id

    @property
    def name (self):
        return self.__name
        
    @name.setter
    def name (self, value):
        if type (value) == str:
            self.__name = value
        else:
            raise TypeError ("name must be a string")
        
    @property
    @abstractmethod
    def type (self):
        pass

    @abstractmethod
    def __str__ (self):
        pass

    @property
    def status (self):
        return self.__status

    def borrow (self):
        """
        This method change the status to borrowed if available
        return True if success, else False
        """
        if self.status == "available":
            self.__status = "borrowed"
            return True
        else:
            return False
        
    def returning (self):
        """
        This method change the status to available if borrowed or under repair
        return True if success, else False
        """
        if self.status in ("borrowed", "under repair"):
            self.__status = "available"
            return True
        else:
            return False
        
    def repair (self):
        """
        This method change the status to under repair if available
        return True if success, else False
        """
        if self.status == "available":
            self.__status = "under repair"
            return True
        else:
            return False
        

class Book (Resource):
    """
    Implementation of book class
    """
    def __init__(self, id, name, author, year, department):
        super ().__init__(id, name)
        self.author = author
        self.year = year
        self.department = department

    @property
    def id (self):
        """
        The id is the integer provided with prefix B
        """
        return f"B{super().id}"
        
    @property
    def type (self):
        return "Book"

    def __str__ (self):
        return f"{self.id}: '{self.name}' by {self.author} ({self.year})"
            
    @property
    def author (self):
        return self.__author
        
    @author.setter
    def author (self, value):
        if type (value) == str:
            self.__author = value
        else:
            raise TypeError ("author must be a string")
            
    @property
    def year (self):
        return self.__year
        
    @year.setter
    def year (self, value):
        if type (value) == int:
            self.__year = value
        else:
            raise TypeError ("year must be an integer")
            
    @property
    def department (self):
        return self.__department
        
    @department.setter
    def department (self, value):
        if type (value) == str:
            self.__department = value
        else:
            raise TypeError ("department must be a string")


class Magazine (Resource):
    """
    Implementation of magazine class
    """
    def __init__(self, id, name, publisher, serialNumber):
        super ().__init__(id, name)
        self.publisher = publisher
        self.serialNumber = serialNumber

    @property
    def id (self):
        """
        The id is the integer provided with prefix M
        """
        return f"M{super().id}"
        
    @property
    def type (self):
        return "Magazine"

    def __str__ (self):
        return f"{self.id}: '{self.name}' by {self.publisher} - number {self.serialNumber}"
        
    @property
    def publisher (self):
        return self.__publisher
        
    @publisher.setter
    def publisher (self, value):
        if type (value) == str:
            self.__publisher = value
        else:
            raise TypeError ("publisher must be a string")
            
    @property
    def serialNumber (self):
        return self.__serialNumber
        
    @serialNumber.setter
    def serialNumber (self, value):
        if type (value) == int:
            self.__serialNumber = value
        else:
            raise TypeError ("serialNumber must be an integer")


class Disk (Resource):
    """
    Implementation of disk class
    """
    def __init__(self, id, name, singer, year):
        super ().__init__(id, name)
        self.singer = singer
        self.year = year

    @property
    def id (self):
        """
        The id is the integer provided with prefix D
        """
        return f"D{super().id}"
        
    @property
    def type (self):
        return "Disk"

    def __str__ (self):
        return f"{self.id}: '{self.name}' by {self.singer} ({self.year})"
        
    @property
    def singer (self):
        return self.__singer
        
    @singer.setter
    def singer (self, value):
        if type (value) == str:
            self.__singer = value
        else:
            raise TypeError ("singer must be a string")
            
    @property
    def year (self):
        return self.__year
        
    @year.setter
    def year (self, value):
        if type (value) == int:
            self.__year = value
        else:
            raise TypeError ("year must be an integer")


class Customer ():
    """
    This class define a customer
    """
    def __init__(self, id, name, telephone):
        #setters are handled separately
        self.id = id
        self.name = name
        self.telephone = telephone

    @property
    def id (self):
        return self.__id
    
    @id.setter
    def id (self, value):
        if type (value) == int:
            self.__id = value
        else:
            raise TypeError ("id should be an integer")
    
    @property
    def name (self):
        return self.__name
    
    @name.setter
    def name (self, value):
        if type (value) == str:
            self.__name = value
        else:
            raise TypeError ("name should be a string")
    
    @property
    def telephone (self):
        return self.__telephone
    
    @telephone.setter
    def telephone (self, value):
        if type (value) == int:
            self.__telephone = value
        else:
            raise TypeError ("telephone should be an integer")
    
    def __str__ (self):
        return f"Customer {self.id}: {self.name} - {self.telephone}"
    
if __name__ == "__main__":
    library = Library ()
    
    library.add (Book (1, "Harry Potter and the Philosopher Stone", "J.K. Rowling", 1997, "fiction"))
    library.add (Book (2, "The Origin of Species", "Charles Darwin", 1859, "science"))
    library.add (Disk (1, "Shetah Afor", "Ishay Ribo", 2018))
    library.add (Disk (2, "Izun", "Hanan Ben Ari", 2016))
    library.add (Magazine (1, "Maariv Lanoar", "Maariv", 32))
    library.add (Magazine (2, "Israel Finances", "A.B.C Finances", 770))

    customer = Customer (123456789, "Israel Israeli", 547000000)
    library.add (customer)
    library.borrowResource (customer, library.resources [5])

    print ("Welcome to my library!")
    id = input ("What is your id number? ")
    name = input ("What is your name? ")
    phone = input ("What is your phone number? ")

    try:
        user = Customer (int (id), name, int (phone))
    except ValueError:
        print ("Invalid input")
        exit ()
    
    library.add (user)
    print ()
    print ("Here is the list of available resources: ")
    for category, result in library.availables ().items ():
        print (category + "s:")
        for item in result:
            print ("\t", item)

    print ()
    resourceId = input ("What resource id do you want to borrow? ")
    resource = library.search (resourceId)
    if resource:
        library.borrowResource (user, resource)
        print (f"Successfully borrowed {resource}!")
    else:
        print ("There is no resource with that id")