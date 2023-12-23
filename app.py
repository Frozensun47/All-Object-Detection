import streamlit as st
import pandas as pd
from flask import Flask, jsonify
from streamlit.components.v1 import html

# Sample data
employees_data = [
    {
        "EmployeeID": 1,
        "FirstName": "John",
        "LastName": "Doe",
        "BirthDate": "1980-05-15",
        "Department": "IT",
        "Position": "Software Engineer",
        "Salary": 75000
    },
    {
        "EmployeeID": 2,
        "FirstName": "Jane",
        "LastName": "Smith",
        "BirthDate": "1985-10-22",
        "Department": "HR",
        "Position": "HR Manager",
        "Salary": 90000
    },
    {
        "EmployeeID": 3,
        "FirstName": "Bob",
        "LastName": "Johnson",
        "BirthDate": "1992-03-08",
        "Department": "Marketing",
        "Position": "Marketing Analyst",
        "Salary": 60000
    },
    {
        "EmployeeID": 4,
        "FirstName": "Alice",
        "LastName": "Williams",
        "BirthDate": "1988-12-17",
        "Department": "Finance",
        "Position": "Financial Analyst",
        "Salary": 80000
    }
]

# Convert data to DataFrame
df = pd.DataFrame(employees_data)

# Flask API
app = Flask(__name__)

@app.route('/api/employees', methods=['GET'])
def get_employees():
    return jsonify(df.to_dict(orient='records'))

# Streamlit app
def main():
    st.title("Employee Data CRUD App")

    # Display the current dataset
    st.subheader("Current Employee Dataset")
    st.table(df)

    # CRUD operations
    operation = st.sidebar.selectbox("Select Operation", ["View", "Add", "Update", "Delete"])

    if operation == "View":
        st.subheader("View Employee Data")
        employee_id = st.number_input("Enter Employee ID:", min_value=1, max_value=df["EmployeeID"].max())
        view_employee_data(employee_id)
    elif operation == "Add":
        st.subheader("Add Employee Data")
        add_employee_data()
    elif operation == "Update":
        st.subheader("Update Employee Data")
        update_employee_data()
    elif operation == "Delete":
        st.subheader("Delete Employee Data")
        delete_employee_data()

# Helper functions for CRUD operations
def view_employee_data(employee_id):
    employee = df[df["EmployeeID"] == employee_id]
    if not employee.empty:
        st.write("Employee Data:")
        st.write(employee)
    else:
        st.warning("Employee not found.")

def add_employee_data():
    employee_id = st.number_input("Employee ID", min_value=1, step=1)
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    birth_date = st.date_input("Birth Date")
    department = st.text_input("Department")
    position = st.text_input("Position")
    salary = st.number_input("Salary", min_value=0, step=1000)

    if st.button("Add Employee"):
        new_employee = {
            "EmployeeID": employee_id,
            "FirstName": first_name,
            "LastName": last_name,
            "BirthDate": str(birth_date),
            "Department": department,
            "Position": position,
            "Salary": salary
        }
        df.loc[employee_id] = new_employee
        st.success("Employee added successfully.")

def update_employee_data():
    employee_id = st.number_input("Enter Employee ID to update", min_value=1, max_value=df["EmployeeID"].max())
    employee = df[df["EmployeeID"] == employee_id]

    if not employee.empty:
        st.write("Current Employee Data:")
        st.write(employee)

        # Get updated information
        first_name = st.text_input("Update First Name", value=employee["FirstName"].iloc[0])
        last_name = st.text_input("Update Last Name", value=employee["LastName"].iloc[0])
        birth_date = st.date_input("Update Birth Date", pd.to_datetime(employee["BirthDate"].iloc[0]))
        department = st.text_input("Update Department", value=employee["Department"].iloc[0])
        position = st.text_input("Update Position", value=employee["Position"].iloc[0])
        salary = st.number_input("Update Salary", value=employee["Salary"].iloc[0], min_value=0, step=1000)

        if st.button("Update Employee"):
            df.loc[df["EmployeeID"] == employee_id, "FirstName"] = first_name
            df.loc[df["EmployeeID"] == employee_id, "LastName"] = last_name
            df.loc[df["EmployeeID"] == employee_id, "BirthDate"] = str(birth_date)
            df.loc[df["EmployeeID"] == employee_id, "Department"] = department
            df.loc[df["EmployeeID"] == employee_id, "Position"] = position
            df.loc[df["EmployeeID"] == employee_id, "Salary"] = salary

            st.success("Employee updated successfully.")
    else:
        st.warning("Employee not found.")

def delete_employee_data():
    employee_id = st.number_input("Enter Employee ID to delete", min_value=1, max_value=df["EmployeeID"].max())

    if st.button("Delete Employee"):
        df.drop(df[df["EmployeeID"] == employee_id].index, inplace=True)
        st.success("Employee deleted successfully.")

# Embed the Flask API in the Streamlit app
if __name__ == "__main__":
    with st.spinner("Waiting for Flask app to start..."):
        html_code = f"""
            <iframe 
                src="http://localhost:5000/api/employees" 
                width="1" 
                height="1" 
                style="display:none;"
            ></iframe>
        """
        st.components.v1.html(html_code, height=0)
        main()
