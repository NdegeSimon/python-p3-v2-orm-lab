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

class TestEmployeeReviews(unittest.TestCase):
    
    def setUp(self):
        '''drop tables prior to each test.'''
        CURSOR.execute("DROP TABLE IF EXISTS reviews")
        CURSOR.execute("DROP TABLE IF EXISTS employees")
        CURSOR.execute("DROP TABLE IF EXISTS departments")
        
        Department.all = {}
        Employee.all = {}
        Review.all = {}
        
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
        self.assertEqual(reviews[0].id, review1.id)
        self.assertEqual(reviews[0].year, review1.year)
        self.assertEqual(reviews[0].summary, review1.summary)
        self.assertEqual(reviews[0].employee_id, review1.employee_id)
        self.assertEqual(reviews[1].id, review2.id)
        self.assertEqual(reviews[1].year, review2.year)
        self.assertEqual(reviews[1].summary, review2.summary)
        self.assertEqual(reviews[1].employee_id, review2.employee_id)

if __name__ == "__main__":
    unittest.main()