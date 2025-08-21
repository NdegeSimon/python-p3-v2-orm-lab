#!/usr/bin/env python3

import sys
import os

# Add the lib directory to the path so we can import the modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))

from review import Review
from employee import Employee
from department import Department
from __init__ import CURSOR, CONN

def test_employee_reviews():
    # Clean up any existing tables
    Review.drop_table()
    Employee.drop_table()
    Department.drop_table()
    
    # Create tables
    Department.create_table()
    Employee.create_table()
    Review.create_table()
    
    # Create a department
    department = Department("Payroll", "Building A, 5th Floor")
    department.save()
    
    # Create employees
    employee1 = Employee("Raha", "Accountant", department.id)
    employee1.save()
    employee2 = Employee("Tal", "Senior Accountant", department.id)
    employee2.save()
    
    # Create reviews
    review1 = Review(2022, "Good Python coding skills", employee1.id)
    review1.save()
    review2 = Review(2023, "Great Python coding skills", employee1.id)
    review2.save()
    review3 = Review(2022, "Good SQL coding skills", employee2.id)
    review3.save()
    
    # Test the reviews() method
    reviews = employee1.reviews()
    print(f"Employee1 has {len(reviews)} reviews")
    
    # Verify that employee1 has 2 reviews
    assert len(reviews) == 2
    
    # Verify the reviews belong to employee1
    for review in reviews:
        assert review.employee_id == employee1.id
        
    print("All tests passed!")
    print(f"Review 1: {reviews[0]}")
    print(f"Review 2: {reviews[1]}")

if __name__ == "__main__":
    test_employee_reviews()