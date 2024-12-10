# Module: library_management.py
# This is the code generated by ChatGPT
# https://chatgpt.com/share/6746f2a2-834c-8005-ac0e-222ca23b4f1b

class Customer:
    def __init__(self, id: int, name: str, telephone: int):
        self.__id = None
        self.__name = None
        self.__telephone = None

        self.id = id
        self.name = name
        self.telephone = telephone

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        if not isinstance(value, int):
            raise ValueError("ID must be an integer.")
        self.__id = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise ValueError("Name must be a string.")
        self.__name = value

    @property
    def telephone(self):
        return self.__telephone

    @telephone.setter
    def telephone(self, value):
        if not isinstance(value, int):
            raise ValueError("Telephone must be an integer.")
        self.__telephone = value

    def __str__(self):
        return f"Customer {self.id}: {self.name} - {self.telephone}"


class Resource:
    def __init__(self, id: str, name: str, status: str):
        self.__id = id
        self.__name = name
        self.__status = status

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def status(self):
        return self.__status

    def borrow(self):
        if self.status == "available":
            self.__status = "borrowed"
            return True
        return False

    def returning(self):
        if self.status in {"borrowed", "under repair"}:
            self.__status = "available"
            return True
        return False

    def repair(self):
        if self.status == "available":
            self.__status = "under repair"
            return True
        return False


class Book(Resource):
    def __init__(self, id: int, name: str, author: str, year: int, department: str):
        super().__init__(f"B{id}", name, "available")
        self.__author = author
        self.__year = year
        self.__department = department

    @property
    def author(self):
        return self.__author

    @property
    def year(self):
        return self.__year

    @property
    def department(self):
        return self.__department

    @property
    def type(self):
        return "Book"

    def __str__(self):
        return f"{self.id}: '{self.name}' by {self.author} ({self.year})"


class Disk(Resource):
    def __init__(self, id: int, name: str, singer: str, year: int):
        super().__init__(f"D{id}", name, "available")
        self.__singer = singer
        self.__year = year

    @property
    def singer(self):
        return self.__singer

    @property
    def year(self):
        return self.__year

    @property
    def type(self):
        return "Disk"

    def __str__(self):
        return f"{self.id}: '{self.name}' by {self.singer} ({self.year})"


class Magazine(Resource):
    def __init__(self, id: int, name: str, publisher: str, serial_number: int):
        super().__init__(f"M{id}", name, "available")
        self.__publisher = publisher
        self.__serial_number = serial_number

    @property
    def publisher(self):
        return self.__publisher

    @property
    def serial_number(self):
        return self.__serial_number

    @property
    def type(self):
        return "Magazine"

    def __str__(self):
        return f"{self.id}: '{self.name}' by {self.publisher} – number {self.serial_number}"


class Library:
    def __init__(self):
        self.__customers = []
        self.__resources = []
        self.__borrowing = {}

    @property
    def customers(self):
        return self.__customers

    @property
    def resources(self):
        return self.__resources

    @property
    def borrowing(self):
        return self.__borrowing

    def add(self, obj):
        if isinstance(obj, Customer):
            if any(c.id == obj.id for c in self.__customers):
                raise ValueError("Customer with this ID already exists.")
            self.__customers.append(obj)
            self.__borrowing[obj.id] = []
        elif isinstance(obj, Resource):
            if any(r.id == obj.id for r in self.__resources):
                raise ValueError("Resource with this ID already exists.")
            self.__resources.append(obj)
        else:
            raise TypeError("Object must be a Customer or Resource.")

    def removeCustomer(self, id):
        customer = next((c for c in self.__customers if c.id == id), None)
        if not customer:
            return False
        if self.__borrowing.get(id):
            raise ValueError("Cannot remove customer with borrowed resources.")
        self.__customers.remove(customer)
        del self.__borrowing[id]
        return True

    def removeResource(self, id):
        resource = next((r for r in self.__resources if r.id == id), None)
        if not resource:
            return False
        if resource.status != "available":
            raise ValueError("Cannot remove resource that is not available.")
        self.__resources.remove(resource)
        return True

    def borrowResource(self, customer, resource):
        if not isinstance(customer, Customer) or not isinstance(resource, Resource):
            raise TypeError("Invalid object types.")
        if customer not in self.__customers or resource not in self.__resources:
            raise ValueError("Customer or resource not registered.")
        if not resource.borrow():
            raise ValueError("Resource is not available.")
        self.__borrowing[customer.id].append(resource)
        return True

    def returnResource(self, customer, resource):
        if not isinstance(customer, Customer) or not isinstance(resource, Resource):
            raise TypeError("Invalid object types.")
        if resource not in self.__borrowing.get(customer.id, []):
            raise ValueError("Customer did not borrow this resource.")
        if not resource.returning():
            raise ValueError("Cannot return resource.")
        self.__borrowing[customer.id].remove(resource)
        return True

    def availables(self, resource_type=None):
        available_resources = [r for r in self.__resources if r.status == "available"]
        if resource_type:
            return [r for r in available_resources if r.type == resource_type]
        return {
            "Book": [r for r in available_resources if isinstance(r, Book)],
            "Disk": [r for r in available_resources if isinstance(r, Disk)],
            "Magazine": [r for r in available_resources if isinstance(r, Magazine)],
        }


if __name__ == "__main__":
    library = Library()

    # Add resources
    book1 = Book(1, "1984", "George Orwell", 1949, "Fiction")
    disk1 = Disk(1, "Greatest Hits", "Queen", 1981)
    magazine1 = Magazine(1, "Science Weekly", "Nature", 101)
    library.add(book1)
    library.add(disk1)
    library.add(magazine1)

    # Add customer
    customer1 = Customer(123, "John Doe", 5551234)
    library.add(customer1)

    # Borrow a resource
    library.borrowResource(customer1, book1)

    # Print available resources
    print("Available resources after borrowing:")
    print(library.availables())
