import unittest
import deepseekLibrary as mod


class TestBasic (unittest.TestCase):
    def setUp (self):
        self.library = mod.Library ()
        self.customer = mod.Customer (123456789, "Israel Israeli", 547000000)
        self.book = mod.Book (3, "Harry Potter and the Philosopher Stone", "J.K. Rowling", 1997, "fiction")
        self.disk = mod.Disk (1, "Shetah Afor", "Ishay Ribo", 2018)
        self.magazine = mod.Magazine (452, "Maariv Lanoar", "Maariv", 32)

    def testCustomer (self):
        self.assertEqual (self.customer.id, 123456789)
        self.assertEqual (self.customer.name, "Israel Israeli")
        self.assertEqual (self.customer.telephone, 547000000)
        self.assertEqual (str (self.customer), "Customer 123456789: Israel Israeli - 547000000")

    def testBook (self):
        self.assertEqual (self.book.id, "B3")
        self.assertEqual (self.book.name, "Harry Potter and the Philosopher Stone")
        self.assertEqual (self.book.author, "J.K. Rowling")
        self.assertEqual (self.book.year, 1997)
        self.assertEqual (self.book.department, "fiction")
        self.assertEqual (self.book.type, "Book")
        self.assertEqual (self.book.status, "available")
        self.book.borrow ()
        self.assertEqual (self.book.status, "borrowed")
        self.book.returning ()
        self.assertEqual (self.book.status, "available")
        self.book.repair ()
        self.assertEqual (self.book.status, "under repair")
        self.book.returning ()
        self.assertEqual (self.book.status, "available")
        self.assertEqual (str (self.book), "B3: 'Harry Potter and the Philosopher Stone' by J.K. Rowling (1997)")

    def testDisk (self):
        self.assertEqual (self.disk.id, "D1")
        self.assertEqual (self.disk.name, "Shetah Afor")
        self.assertEqual (self.disk.singer, "Ishay Ribo")
        self.assertEqual (self.disk.year, 2018)
        self.assertEqual (self.disk.type, "Disk")
        self.assertEqual (self.disk.status, "available")
        self.disk.borrow ()
        self.assertEqual (self.disk.status, "borrowed")
        self.disk.returning ()
        self.assertEqual (self.disk.status, "available")
        self.disk.repair ()
        self.assertEqual (self.disk.status, "under repair")
        self.disk.returning ()
        self.assertEqual (self.disk.status, "available")
        self.assertEqual (str (self.disk), "D1: 'Shetah Afor' by Ishay Ribo (2018)")
        
    def testMagazine (self):
        self.assertEqual (self.magazine.id, "M452")
        self.assertEqual (self.magazine.name, "Maariv Lanoar")
        self.assertEqual (self.magazine.publisher, "Maariv")
        self.assertEqual (self.magazine.serialNumber, 32)
        self.assertEqual (self.magazine.type, "Magazine")
        self.assertEqual (self.magazine.status, "available")
        self.magazine.borrow ()
        self.assertEqual (self.magazine.status, "borrowed")
        self.magazine.returning ()
        self.assertEqual (self.magazine.status, "available")
        self.magazine.repair ()
        self.assertEqual (self.magazine.status, "under repair")
        self.magazine.returning ()
        self.assertEqual (self.magazine.status, "available")
        self.assertEqual (str (self.magazine), "M452: 'Maariv Lanoar' by Maariv - number 32")

    def testAddRemoveResource (self):
        self.assertEqual (len (self.library.resources), 0)
        self.library.add (self.book)
        self.assertEqual (len (self.library.resources), 1)
        self.library.add (self.disk)
        self.assertEqual (len (self.library.resources), 2)
        self.library.add (self.magazine)
        self.assertEqual (len (self.library.resources), 3)
        self.assertIn (self.book, self.library.resources)
        self.assertIn (self.disk, self.library.resources)
        self.assertIn (self.magazine, self.library.resources)
        self.assertTrue (self.library.removeResource (self.book.id))
        self.assertEqual (len (self.library.resources), 2)
        self.assertTrue (self.library.removeResource (self.disk.id))
        self.assertEqual (len (self.library.resources), 1)
        self.assertTrue (self.library.removeResource (self.magazine.id))
        self.assertEqual (len (self.library.resources), 0)
        
    def testAddRemoveCustomer (self):
        self.assertEqual (len (self.library.customers), 0)
        self.library.add (self.customer)
        self.assertEqual (len (self.library.customers), 1)
        self.assertEqual (self.library.customers[0].id, self.customer.id)
        self.assertTrue (self.library.removeCustomer (self.customer.id))
        self.assertEqual (len (self.library.customers), 0)

    def testBorrowReturning (self):
        self.library.add (self.customer)
        self.library.add (self.book)
        self.library.add (self.disk)
        self.library.add (self.magazine)
        self.assertTrue (self.library.borrowResource (self.customer, self.book))
        self.assertTrue (self.library.borrowResource (self.customer, self.disk))
        self.assertTrue (self.library.borrowResource (self.customer, self.magazine))
        self.assertTrue (type (self.library.borrowing) == dict)
        self.assertTrue (type (self.library.borrowing[self.customer.id]) == list)
        self.assertEqual (len (self.library.borrowing[self.customer.id]), 3)
        self.assertIn (self.book, self.library.borrowing[self.customer.id])
        self.assertIn (self.disk, self.library.borrowing[self.customer.id])
        self.assertIn (self.magazine, self.library.borrowing[self.customer.id])
        self.assertEqual (self.book.status, "borrowed")
        self.assertEqual (self.disk.status, "borrowed")
        self.assertEqual (self.magazine.status, "borrowed")

        #test availables method
        books = self.library.availables ("Book")
        self.assertTrue (type (self.library.availables ()) == dict)
        self.assertTrue (type (books) == list)
        self.assertEqual (len (books), 0)

        self.assertTrue (self.library.returnResource (self.customer, self.book))
        self.assertTrue (self.library.returnResource (self.customer, self.disk))
        self.assertTrue (self.library.returnResource (self.customer, self.magazine))
        self.assertEqual (len (self.library.borrowing[self.customer.id]), 0)
        self.assertEqual (self.book.status, "available")
        self.assertEqual (self.disk.status, "available")
        self.assertEqual (self.magazine.status, "available")

        books = self.library.availables ("Book")
        self.assertEqual (len (books), 1)
        self.assertEqual (books[0].id, self.book.id)
        self.assertEqual (self.library.availables ()["Disk"][0].id, self.disk.id)
        self.assertEqual (self.library.availables ()["Magazine"][0].id, self.magazine.id)

class TestAbstraction (unittest.TestCase):
    """
    In this test we check if the abstraction of the library is correct.
    Checks if errors are generated in some methods
    """
    def setUp (self):
        self.library = mod.Library ()
        self.customer = mod.Customer (123456789, "Israel Israeli", 547000000)
        self.book = mod.Book (3, "Harry Potter and the Philosopher Stone", "J.K. Rowling", 1997, "fiction")
        self.disk = mod.Disk (1, "Shetah Afor", "Ishay Ribo", 2018)
        self.library.add (self.customer)
        self.library.add (self.book)

    def testCustomer (self):
        """
        Check if errors are raised when creating customer with wrong parameters
        """
        with self.assertRaises (Exception):
            newCustomer = mod.Customer ("Arieh", "Ankri", 547878747) #id is a string
        with self.assertRaises (Exception):
            newCustomer = mod.Customer (123456789, 45, 547878747) #name is a number
        with self.assertRaises (Exception):
            newCustomer = mod.Customer (123456789, "Ankri", "aaa@gmail.com") #phone is a string

    def testBook (self):
        """
        Check if errors are raised when creating book with wrong parameters
        """
        with self.assertRaises (Exception):
            newBook = mod.Book ("Harry Potter", "And the chamber of secrets", "J.K. Rowling", 1997, "fiction") #id is a string
        with self.assertRaises (Exception):
            newBook = mod.Book (2, 2, "J.K. Rowling", 1997, "fiction") #name is a number
        with self.assertRaises (Exception):
            newBook = mod.Book (2, "Harry Potter And the chamber of secrets", 45, 1997, "fiction") #author is a number
        with self.assertRaises (Exception):
            newBook = mod.Book (2, "Harry Potter And the chamber of secrets", "J.K. Rowling", "13PM", "fiction") #year is a string
        with self.assertRaises (Exception):
            newBook = mod.Book (2, "Harry Potter And the chamber of secrets", "J.K. Rowling", 1997, 35) #department is a number

    def testDisk (self):
        """
        Check if errors are raised when creating disk with wrong parameters
        """
        with self.assertRaises (Exception):
            newDisk = mod.Disk ("D32", "Shetah Afor", "Ishay Ribo", 2018) #id is a string
        with self.assertRaises (Exception):
            newDisk = mod.Disk (32, 456, "Ishay Ribo", 2018) #name is a number
        with self.assertRaises (Exception):
            newDisk = mod.Disk (32, "Shetah Afor", 1990, 2018) #author is a number
        with self.assertRaises (Exception):
            newDisk = mod.Disk (32, "Shetah Afor", "Ishay Ribo", "last year") #year is a string

    def testMagazine (self):
        """
        Check if errors are raised when creating magazine with wrong parameters
        """
        with self.assertRaises (Exception):
            newMagazine = mod.Magazine ("M72", "Maariv Lanoar", "Maariv", 52) #id is a string
        with self.assertRaises (Exception):
            newMagazine = mod.Magazine (72, 48, "Maariv", 52) #name is a number
        with self.assertRaises (Exception):
            newMagazine = mod.Magazine (72, "Maariv Lanoar", 1, 52) #publisher is a number
        with self.assertRaises (Exception):
            newMagazine = mod.Magazine (72, "Maariv Lanoar", "Maariv", "The best") #serialNumber is a string

    def testAddRemoveCustomer (self):
        """
        Check if raise error when added a customer that already exists
        Check correct data type
        Check unable to remove no registered customer
        """
        self.assertRaises (Exception, self.library.add, self.customer)
        newCustomer = mod.Customer (self.customer.id, "Arieh Ankri", 545474877)
         #should raise an error because the id is the same
        self.assertRaises (Exception, self.library.add, newCustomer)
         #should raise an error because need to be Customer or Resource object
        self.assertRaises (Exception, self.library.add, "Arieh Ankri")
         #should return False because customer not in the library
        self.assertFalse (self.library.removeCustomer (1))
        self.assertIn (self.customer, self.library.customers) #the previous customer should not be removed

    def testAddRemoveResource (self):
        """
        Check if raise error when added a resource that already exists
        Check correct data type
        Check unable to remove no registered resource
        """
        self.assertRaises (Exception, self.library.add, self.book)
        newBook = mod.Book (3, "The Lion King", "Walt Disney", 1994, "children")
         #should raise an error because the id is the same
        self.assertRaises (Exception, self.library.add, newBook)
         #should return False because customer not in the library
        self.assertFalse (self.library.removeResource (1))
        self.assertIn (self.book, self.library.resources) #the previous resource should not be removed
    
    def testBorrowAndReturn (self):
        """
        Check if the customer can borrow and the resource can be borrowed and returned
        Check unable to remove customer with borrow or borrowed resource
        """
        self.book.repair ()
        self.assertRaises (Exception, self.library.borrowResource, self.customer, self.book) #book under repair
        self.book.returning ()
        newCustomer = mod.Customer (456, "Arieh Ankri", 545474877)
        self.assertRaises (Exception, self.library.borrowResource, newCustomer, self.book) #newCustomer unregistered
        self.library.borrowResource (self.customer, self.book)
        self.library.add (newCustomer)
        self.assertRaises (Exception, self.library.borrowResource, newCustomer, self.book) #book borrowed
        #test types
        self.assertRaises (Exception, self.library.borrowResource, newCustomer, 123)
        self.library.add (self.disk)
        self.assertRaises (Exception, self.library.borrowResource, "Arieh Ankri", self.disk)

        #test returning
        self.assertRaises (Exception, self.library.returnResource, newCustomer, self.book) #newCustomer did not borrowed book
        self.assertRaises (Exception, self.library.removeCustomer, self.customer.id) #cannot remove customer with resources
        self.assertRaises (Exception, self.library.removeResource, self.book.id) #cannot remove borrowed resource
        self.disk.repair ()
        self.assertRaises (Exception, self.library.removeResource, self.disk.id) #cannot remove unavailable resource
        self.disk.returning ()
        self.assertRaises (Exception, self.library.returnResource, newCustomer, self.disk) #disk is available
        #test types
        self.assertRaises (Exception, self.library.returnResource, self.customer, 123)
        self.assertRaises (Exception, self.library.returnResource, "Arieh Ankri", self.book)
        
class testEncapsulation (unittest.TestCase):
    """
    Check if the encapsulation is correctly implemented
    Need to be unable to modify attributes without some control
    """
    def testLibrary (self):
        library = mod.Library ()
        with self.assertRaises (Exception):
            library.customers = []
        with self.assertRaises (Exception):
            library.resources = []
        with self.assertRaises (Exception):
            library.borrowing = dict ()

    def testCustomer (self):
        customer = mod.Customer (123456789, "Israel Israeli", 547000000)
        with self.assertRaises (Exception):
            customer.id = "hello"
        with self.assertRaises (Exception):
            customer.name = [1]
        with self.assertRaises (Exception):
            customer.telephone = "hello"
            
    def testBook (self):
        book = mod.Book (3, "Harry Potter and the Philosopher Stone", "J.K. Rowling", 1997, "fiction")
        with self.assertRaises (Exception):
            book.id = 123.4
        with self.assertRaises (Exception):
            book.name = [1]
        with self.assertRaises (Exception):
            book.type = "Disk"
        with self.assertRaises (Exception):
            book.status = "hello"
        with self.assertRaises (Exception):
            book.author = [1]
        with self.assertRaises (Exception):
            book.year = "hello"
        with self.assertRaises (Exception):
            book.department = [1]
            
    def testDisk (self):
        disk = mod.Disk (1, "Shetah Afor", "Ishay Ribo", 2018)
        with self.assertRaises (Exception):
            disk.id = 123
        with self.assertRaises (Exception):
            disk.name = [1]
        with self.assertRaises (Exception):
            disk.type = "Book"
        with self.assertRaises (Exception):
            disk.status = "hello"
        with self.assertRaises (Exception):
            disk.singer = [1]
        with self.assertRaises (Exception):
            disk.year = "hello"
            
    def testMagazine (self):
        magazine = mod.Magazine (452, "Maariv Lanoar", "Maariv", 32)
        with self.assertRaises (Exception):
            magazine.id = 123
        with self.assertRaises (Exception):
            magazine.name = [1]
        with self.assertRaises (Exception):
            magazine.type = "Book"
        with self.assertRaises (Exception):
            magazine.status = "hello"
        with self.assertRaises (Exception):
            magazine.publisher = [1]
        with self.assertRaises (Exception):
            magazine.serialNumber = "hello"

class testInheritance (unittest.TestCase):
    """
    Test if Resource class has been implemented correctly
    This section is almost entirely copied from the paper
    """
    def testInheritance (self):
        superBook = mod.Book.__bases__
        superDisk = mod.Disk.__bases__
        superMagazine = mod.Magazine.__bases__
        superLibrary = mod.Library.__bases__
        self.assertEqual (superBook, superDisk)
        self.assertEqual (superBook, superMagazine)
        self.assertNotEqual (superBook, superLibrary)
        
    def testSuperClass (self):
        """
        Test if super class has been implemented as abstract class
        """
        superBook = mod.Book.__bases__[0]
        self.assertRaises (TypeError, superBook)
        self.assertRaises (TypeError, superBook, 3, "Harry Potter and the Philosopher Stone")
    
    def testInheritMethodsProperties (self):
        """
        Check that methods and properties that should be inherited are, in fact, inherited
        """
        #methods
        self.assertNotEqual (mod.Book.borrow.__qualname__, "Book.borrow")
        self.assertNotEqual (mod.Book.returning.__qualname__, "Book.returning")
        self.assertNotEqual (mod.Book.repair.__qualname__, "Book.repair")
        self.assertNotEqual (mod.Disk.borrow.__qualname__, "Disk.borrow")
        self.assertNotEqual (mod.Disk.returning.__qualname__, "Disk.returning")
        self.assertNotEqual (mod.Disk.repair.__qualname__, "Disk.repair")
        self.assertNotEqual (mod.Magazine.borrow.__qualname__, "Magazine.borrow")
        self.assertNotEqual (mod.Magazine.returning.__qualname__, "Magazine.returning")
        self.assertNotEqual (mod.Magazine.repair.__qualname__, "Magazine.repair")
        #properties
        self.assertNotIn ("name", mod.Book.__dict__)
        self.assertNotIn ("status", mod.Book.__dict__)
        self.assertNotIn ("name", mod.Disk.__dict__)
        self.assertNotIn ("status", mod.Disk.__dict__)
        self.assertNotIn ("name", mod.Magazine.__dict__)
        self.assertNotIn ("status", mod.Magazine.__dict__)

    def testNotNeededAttibutes (self):
        book = mod.Book (3, "Harry Potter and the Philosopher Stone", "J.K. Rowling", 1997, "fiction")
        disk = mod.Disk (1, "Shetah Afor", "Ishay Ribo", 2018)
        magazine = mod.Magazine (452, "Maariv Lanoar", "Maariv", 32)
        with self.assertRaises (AttributeError):
            a = book.singer
        with self.assertRaises (AttributeError):
            a = book.serialNumber
        with self.assertRaises (AttributeError):
            a = book.publisher
        with self.assertRaises (AttributeError):
            a = disk.author
        with self.assertRaises (AttributeError):
            a = disk.department
        with self.assertRaises (AttributeError):
            a = disk.serialNumber
        with self.assertRaises (AttributeError):
            a = disk.publisher
        with self.assertRaises (AttributeError):
            a = magazine.singer
        with self.assertRaises (AttributeError):
            a = magazine.author
        with self.assertRaises (AttributeError):
            a = magazine.year
        with self.assertRaises (AttributeError):
            a = magazine.department

class testPolimorphism (unittest.TestCase):
    """
    Test overriding
    Overloading is in methods Library.add and Library.availables and already tested
    """
    def testOverriding (self):
        """
        Check if id and type properties were in the base class
        """
        superClass = mod.Book.__bases__[0]
        self.assertIn ("id", dir (superClass))
        self.assertIn ("type", dir (superClass))

if __name__ == "__main__":
    unittest.main (verbosity=2)
