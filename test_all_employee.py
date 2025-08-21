#!/usr/bin/env python3

import sys
import os
import unittest

# Add the lib directory to the path so we can import the modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))

from review import Review
from employee import Employee
from department import Department
from __init__ import CURSOR, CONN

class TestEmployee(unittest.TestCase):
    
    def setUp(self):
        '''drop tables prior to each test.'''
        CURSOR.execute("DROP TABLE IF EXISTS reviews")
        CURSOR.execute("DROP TABLE IF EXISTS employees")
        CURSOR.execute("DROP TABLE IF EXISTS departments")
        
        Department.all = {}
        Employee.all = {}
        Review.all = {}
        
    def test_creates_table(self):
        '''contains method "create_table()" that creates table "employees" if it does not exist.'''
        Department.create_table()  # ensure Department table exists due to FK constraint
        Employee.create_table()
        self.assertTrue(CURSOR.execute("SELECT * FROM employees"))
        
    def test_drops_table(self):
        '''contains method "drop_table()" that drops table "employees" if it exists.'''
        sql = """
            CREATE TABLE IF NOT EXISTS departments
                (id INTEGER PRIMARY KEY,
                name TEXT,
                location TEXT)
        """
        CURSOR.execute(sql)
        
        sql = """  
            CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY,
            name TEXT,
            job_title TEXT,
            department_id INTEGER,
            FOREIGN KEY (department_id) REFERENCES departments(id))
        """
        CURSOR.execute(sql)
        
        Employee.drop_table()
        
        # Confirm departments table exists
        sql_table_names = """
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='departments'
            LIMIT 1
        """
        result = CURSOR.execute(sql_table_names).fetchone()
        self.assertTrue(result)
        
        # Confirm employees table does not exist
        sql_table_names = """
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='employees'
            LIMIT 1
        """
        result = CURSOR.execute(sql_table_names).fetchone()
        self.assertIsNone(result)
        
    def test_saves_employee(self):
        '''contains method "save()" that saves an Employee instance to the db and sets the instance id.'''
        Department.create_table()
        department = Department("Payroll", "Building A, 5th Floor")
        department.save()  # tested in department_test.py
        
        Employee.create_table()
        employee = Employee("Sasha", "Manager", department.id)
        employee.save()
        
        sql = """
            SELECT * FROM employees
        """
        
        row = CURSOR.execute(sql).fetchone()
        self.assertEqual((row[0], row[1], row[2], row[3]),
                        (employee.id, employee.name, employee.job_title, employee.department_id))
        self.assertEqual((employee.id, "Sasha", "Manager", department.id),
                        (employee.id, "Sasha", "Manager", department.id))
        
    def test_creates_employee(self):
        '''contains method "create()" that creates a new row in the db using the parameter data and returns an Employee instance.'''
        Department.create_table()
        department = Department("Payroll", "Building A, 5th Floor")
        department.save()  # tested in department_test.py
        
        Employee.create_table()
        employee = Employee.create("Kai", "Web Developer", department.id)
        
        sql = """
            SELECT * FROM employees
        """
        row = CURSOR.execute(sql).fetchone()
        self.assertEqual((row[0], row[1], row[2], row[3]),
                        (employee.id, employee.name, employee.job_title, employee.department_id))
        self.assertEqual((employee.id, "Kai", "Web Developer", department.id),
                        (employee.id, "Kai", "Web Developer", department.id))
        
    def test_instance_from_db(self):
        '''contains method "instance_from_db()" that takes a db row and creates an Employee instance.'''
        Department.create_table()
        department = Department("Payroll", "Building A, 5th Floor")
        department.save()  # tested in department_test.py
        
        Employee.create_table()
        sql = """
            INSERT INTO employees (name, job_title, department_id)
            VALUES ('Amir', 'Programmer', ?)
        """
        CURSOR.execute(sql, (department.id,))
        
        sql = """
            SELECT * FROM employees
        """
        row = CURSOR.execute(sql).fetchone()
        
        employee = Employee.instance_from_db(row)
        self.assertEqual((row[0], row[1], row[2], row[3]),
                        (employee.id, employee.name, employee.job_title, employee.department_id))
        self.assertEqual((employee.id, "Amir", "Programmer", department.id),
                        (employee.id, "Amir", "Programmer", department.id))
        
    def test_finds_by_id(self):
        '''contains method "find_by_id()" that returns a Employee instance corresponding to its db row retrieved by id.'''
        Department.create_table()
        department = Department("Payroll", "Building A, 5th Floor")
        department.save()
        Employee.create_table()
        
        employee1 = Employee.create("John", "Manager", department.id)
        employee2 = Employee.create("Jane", "Web Developer", department.id)
        
        employee = Employee.find_by_id(employee1.id)
        self.assertEqual(
            (employee.id, employee.name, employee.job_title, employee.department_id),
            (employee1.id, employee1.name, employee1.job_title, employee1.department_id)
        )
        
        employee = Employee.find_by_id(employee2.id)
        self.assertEqual(
            (employee.id, employee.name, employee.job_title, employee.department_id),
            (employee2.id, employee2.name, employee2.job_title, employee2.department_id)
        )
        
        employee = Employee.find_by_id(3)
        self.assertIsNone(employee)
        
    def test_finds_by_name(self):
        '''contains method "find_by_name()" that returns an Employee instance corresponding to the db row retrieved by name.'''
        Department.create_table()
        department = Department("Payroll", "Building A, 5th Floor")
        department.save()
        Employee.create_table()
        
        employee1 = Employee.create("John", "Manager", department.id)
        employee2 = Employee.create("Jane", "Web Developer", department.id)
        
        employee = Employee.find_by_name(employee1.name)
        self.assertEqual(
            (employee.id, employee.name, employee.job_title, employee.department_id),
            (employee1.id, employee1.name, employee1.job_title, employee1.department_id)
        )
        employee = Employee.find_by_name(employee2.name)
        self.assertEqual(
            (employee.id, employee.name, employee.job_title, employee.department_id),
            (employee2.id, employee2.name, employee2.job_title, employee2.department_id)
        )
        employee = Employee.find_by_name("Unknown")
        self.assertIsNone(employee)
        
    def test_updates_row(self):
        '''contains a method "update()" that updates an instance's corresponding database record to match its new attribute values.'''
        Department.create_table()
        department1 = Department("Payroll", "Building A, 5th Floor")
        department1.save()
        department2 = Department("Human Resources", "Building C, 2nd Floor")
        department2.save()
        
        Employee.create_table()
        
        employee1 = Employee.create("Raha", "Accountant", department1.id)
        employee2 = Employee.create("Tal", "Benefits Coordinator", department2.id)
        id1 = employee1.id
        id2 = employee2.id
        employee1.name = "Raha Lee"
        employee1.job_title = "Senior Accountant"
        employee1.department_id = department2.id
        employee1.update()
        
        # Confirm employee updated
        employee = Employee.find_by_id(id1)
        self.assertEqual((employee.id, employee.name, employee.job_title, employee.department_id),
                        (employee1.id, employee1.name, employee1.job_title, employee1.department_id))
        self.assertEqual((id1, "Raha Lee", "Senior Accountant", department2.id),
                        (id1, "Raha Lee", "Senior Accountant", department2.id))
        
        # Confirm employee not updated
        employee = Employee.find_by_id(id2)
        self.assertEqual((employee.id, employee.name, employee.job_title, employee.department_id),
                        (employee2.id, employee2.name, employee2.job_title, employee2.department_id))
        self.assertEqual((id2, "Tal", "Benefits Coordinator", department2.id),
                        (id2, "Tal", "Benefits Coordinator", department2.id))
        
    def test_deletes_row(self):
        '''contains a method "delete()" that deletes the instance's corresponding database record'''
        Department.create_table()
        department = Department("Payroll", "Building A, 5th Floor")
        department.save()
        
        Employee.create_table()
        
        employee1 = Employee.create("Raha", "Accountant", department.id)
        id1 = employee1.id
        employee2 = Employee.create("Tal", "Benefits Coordinator", department.id)
        id2 = employee2.id
        
        employee = Employee.find_by_id(id1)
        employee.delete()
        # assert row deleted
        self.assertIsNone(Employee.find_by_id(employee1.id))
        # assert Employee object state is correct, id should be None
        self.assertEqual((employee1.id, employee1.name, employee1.job_title, employee1.department_id),
                        (None, "Raha", "Accountant", department.id))
        # assert dictionary entry was deleted
        self.assertIsNone(Employee.all.get(id1))
        
        employee = Employee.find_by_id(id2)
        # assert employee2 row not modified, employee2 object not modified
        self.assertEqual((employee.id, employee.name, employee.job_title, employee.department_id),
                        (employee2.id, employee2.name, employee2.job_title, employee2.department_id))
        self.assertEqual((id2, "Tal", "Benefits Coordinator", department.id),
                        (id2, "Tal", "Benefits Coordinator", department.id))
        
    def test_gets_all(self):
        '''contains method "get_all()" that returns a list of Employee instances for every record in the db.'''
        Department.create_table()
        department = Department("Payroll", "Building A, 5th Floor")
        department.save()
        
        Employee.create_table()
        employee1 = Employee.create("Tristan", "Fullstack Developer", department.id)
        employee2 = Employee.create("Sasha", "Manager", department.id)
        
        employees = Employee.get_all()
        self.assertEqual(len(employees), 2)
        self.assertEqual((employees[0].id, employees[0].name, employees[0].job_title, employees[0].department_id),
                        (employee1.id, employee1.name, employee1.job_title, employee1.department_id))
        self.assertEqual((employees[1].id, employees[1].name, employees[1].job_title, employees[1].department_id),
                        (employee2.id, employee2.name, employee2.job_title, employee2.department_id))
        
    def test_get_reviews(self):
        '''contain a method "reviews" that gets the reviews for the current Employee instance '''
        Department.create_table()
        department1 = Department.create("Payroll", "Building A, 5th Floor")
        
        Employee.create_table()
        employee1 = Employee.create("Raha", "Accountant", department1.id)
        employee2 = Employee.create("Tal", "Senior Accountant", department1.id)
        
        Review.create_table()
        review1 = Review.create(2022, "Good Python coding skills", employee1.id)
        review2 = Review.create(2023, "Great Python coding skills", employee1.id)
        review3 = Review.create(2022, "Good SQL coding skills", employee2.id)
        
        reviews = employee1.reviews()
        self.assertEqual(len(reviews), 2)
        self.assertEqual((reviews[0].id, reviews[0].year, reviews[0].summary, reviews[0].employee_id),
                        (review1.id, review1.year, review1.summary, review1.employee_id))
        self.assertEqual((reviews[1].id, reviews[1].year, reviews[1].summary, reviews[1].employee_id),
                        (review2.id, review2.year, review2.summary, review2.employee_id))

if __name__ == "__main__":
    unittest.main()