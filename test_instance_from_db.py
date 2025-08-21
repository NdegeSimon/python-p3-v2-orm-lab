#!/usr/bin/env python3

import sys
import os

# Add the lib directory to the path so we can import the modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))

from review import Review
from employee import Employee
from department import Department
from __init__ import CURSOR, CONN

def test_instance_from_db():
    # Clean up any existing tables
    Review.drop_table()
    Employee.drop_table()
    Department.drop_table()
    
    # Create tables
    Department.create_table()
    Employee.create_table()
    Review.create_table()
    
    # Create a department
    department = Department("Engineering", "Building A")
    department.save()
    
    # Create an employee
    employee = Employee("John Doe", "Software Engineer", department.id)
    employee.save()
    
    # Create a review directly in the database
    sql = """
        INSERT INTO reviews (year, summary, employee_id)
        VALUES (?, ?, ?)
    """
    CURSOR.execute(sql, (2023, "Excellent work!", employee.id))
    CONN.commit()
    
    # Get the row from the database
    sql = "SELECT * FROM reviews"
    row = CURSOR.execute(sql).fetchone()
    
    print(f"Row from database: {row}")
    
    # Test instance_from_db method
    review = Review.instance_from_db(row)
    
    print(f"Review instance: {review}")
    print(f"Review attributes - id: {review.id}, year: {review.year}, summary: {review.summary}, employee_id: {review.employee_id}")
    
    # Verify the attributes match
    assert review.id == row[0]
    assert review.year == row[1]
    assert review.summary == row[2]
    assert review.employee_id == row[3]
    
    # Verify the instance is cached
    assert Review.all.get(review.id) is review
    
    # Test that calling instance_from_db again with the same row returns the same instance
    review2 = Review.instance_from_db(row)
    assert review2 is review
    
    print("All tests passed!")

if __name__ == "__main__":
    test_instance_from_db()