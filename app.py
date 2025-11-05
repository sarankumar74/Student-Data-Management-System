
import mysql
import streamlit as st
import pandas as pd
import mysql.connector.connection

def create_connection():
    return mysql.connector.connect(
        host="localhost",  
        user="root",       
        password="password", 
        database="student_management" 
    )

# --- Department dictionary ---
departments = {
    "Finance": ["B.COM", "B.COM CA", "B.COM PA", "BBA"],
    "Computer Student": ["CS", "BCA", "IT", "AIML", "DS", "AIDS"],
    "Physical Science": ["EC", "Physics", "Chemistry", "Maths"],
    "Literacy Student": ["HMCS", "English", "TFT", "BioChemistry"]
}

# --- Functions ---
def filter_by_department(dept):
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT Name, Gender, Department, `Year`, District, Type, Address  
        FROM student_table
        WHERE Department = %s
    """
    cursor.execute(query, (dept,))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def filter_by_year(year):
    conn = create_connection()
    query = "SELECT Name, Department, Age, Type, `Year` FROM student_table WHERE `Year` = %s"
    df = pd.read_sql(query, conn, params=(year,))
    conn.close()
    return df

def department(year):
    conn = create_connection()
    query = "SELECT Name, Department, Age, Type, `Year` FROM student_table WHERE Department = %s"
    df = pd.read_sql(query, conn, params=(year,))
    conn.close()
    return df

def get_students_by_type(student_type):
    conn = create_connection()
    query = """
        SELECT Name, Gender, Department, `Year`, District, Type, Address, `Phone Number`
        FROM student_table
        WHERE Type = %s
    """
    df = pd.read_sql(query, conn, params=(student_type,))
    conn.close()
    return df


# --- Streamlit App ---
st.title("🎓 Student Management System")

menus = ["View All Students", "Department", "Filter Students"]
choices = st.sidebar.selectbox("Menu", menus)

if choices == "View All Students":
    st.subheader("📋 All Student Records")
    conn = create_connection()
    df = pd.read_sql("SELECT * FROM student_table", conn)
    conn.close()
    st.dataframe(df)
elif choices == "Department":
    category = st.selectbox("Choose Student Category:", list(departments.keys()))
    selected_department = st.selectbox("Choose Department:", departments[category])
    data = filter_by_department(selected_department)
    st.subheader(f"📋 Students in {selected_department}")
    if data:
        st.dataframe(pd.DataFrame(data))
    else:
       st.info("No students found for this department.")

elif choices == "Filter Students":
    year_options = {
            "First Year": 1,
            "Second Year": 2,
            "Third Year": 3
        }
    selected_year = st.selectbox("Select Year:", list(year_options.keys()))
    year_num = year_options[selected_year]
    df_year = filter_by_year(year_num)
    st.subheader(f"📋 {selected_year} Students")
    if not df_year.empty:
        st.dataframe(df_year)
    else:
       st.info("No students found for this year.")
   


menu = ["Student Type", "College Bus", "DayScholar", "Hostel", "OutBus"]
menu_choice = st.sidebar.selectbox("Menu", menu)

if menu_choice == "Student Type":
    st.subheader("📋 Select a Student Type from Sidebar")

elif menu_choice in ["College Bus", "DayScholar", "Hostel", "OutBus"]:
    st.subheader(f"📋 All Students: {menu_choice}")
    df = get_students_by_type(menu_choice)
    if not df.empty:
        st.dataframe(df)
    else:
        st.info(f"No students found for {menu_choice}.")

# crud operations
def add_student(name, age, email, gender, department, year, district, stype, dateofbirth, address):
    conn = create_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO student_table 
        (Name, Age, Email, Gender, Department, Year, District, Type, DateOfBirth, Address)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """
    cursor.execute(query, (name, age, email, gender, department, year, district, stype, dateofbirth, address))
    conn.commit()
    cursor.close()
    conn.close()

def view_students():
    conn = create_connection()
    df = pd.read_sql("SELECT * FROM student_table", conn)
    conn.close()
    return df

def update_student(student_id, name, age, email, gender, department, year, district, stype, dateofbirth, address):
    conn = create_connection()
    cursor = conn.cursor()
    query = """
        UPDATE student_table SET 
        Name=%s, Age=%s, Email=%s, Gender=%s, Department=%s, Year=%s, District=%s, Type=%s, DateOfBirth=%s, Address=%s
        WHERE ID=%s
    """
    cursor.execute(query, (name, age, email, gender, department, year, district, stype, dateofbirth, address, student_id))
    conn.commit()
    cursor.close()
    conn.close()

def delete_student(student_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM student_table WHERE ID=%s", (student_id,))
    conn.commit()
    cursor.close()
    conn.close()

# --- Streamlit App ---
menu = ["Add Student", "View Students", "Update Student", "Delete Student"]
choice = st.sidebar.selectbox("Menu", menu)

# --- If-Else Structure for CRUD ---
if choice == "Add Student":
    st.subheader("➕ Add New Student")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=18, max_value=30)
    email = st.text_input("Email")
    gender = st.selectbox("Gender", ["Male", "Female"])
    department = st.text_input("Department")
    year = st.number_input("Year", min_value=1, max_value=5)
    district = st.text_input("District")
    stype = st.selectbox("Type", ["College Bus", "DayScholar", "Hostel", "OutBus"])
    dateofbirth = st.date_input("Date of Birth")
    address = st.text_input("Address")

    if st.button("Add Student"):
        add_student(name, age, email, gender, department, year, district, stype, dateofbirth, address)
        st.success(f"Student {name} added successfully!")

elif choice == "View Students":
    st.subheader("📋 All Students")
    df = view_students()
    st.dataframe(df)

elif choice == "Update Student":
    st.subheader("✏️ Update Student")
    student_id = st.number_input("Enter Student ID to Update", min_value=1)
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=18, max_value=30)
    email = st.text_input("Email")
    gender = st.selectbox("Gender", ["Male", "Female"])
    department = st.text_input("Department")
    year = st.number_input("Year", min_value=1, max_value=5)
    district = st.text_input("District")
    stype = st.selectbox("Type", ["College Bus", "DayScholar", "Hostel", "OutBus"])
    dateofbirth = st.date_input("Date of Birth")
    address = st.text_input("Address")

    if st.button("Update Student"):
        update_student(student_id, name, age, email, gender, department, year, district, stype, dateofbirth, address)
        st.success(f"Student ID {student_id} updated successfully!")

elif choice == "Delete Student":
    st.subheader("🗑️ Delete Student")
    student_id = st.number_input("Enter Student ID to Delete", min_value=1)
    if st.button("Delete Student"):
        delete_student(student_id)
        st.success(f"Student ID {student_id} deleted successfully!")

else:
    st.info("Select a menu option to proceed.")
