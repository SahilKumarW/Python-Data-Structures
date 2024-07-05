import json
from student import Student
from course import Course
from teacher import Teacher
from teaching_module import TeachingModule

def load_students_from_file(filename):
    students = []
    with open(filename, 'r') as file:
        data = json.load(file)
        for student_data in data:
            student = Student(
                first_name=student_data["first_name"],
                last_name=student_data["last_name"],
                email=student_data["email"],
                campus=student_data["campus"],
                student_id=student_data["id"]
            )
            students.append(student)
    return students

def add_student_menu(teaching_module):
    valid_campuses = ["Christchurch", "Auckland", "Wellington"]

    while True:
        print("\n************************")
        print("STUDENT ADD MENU")
        print("************************")
        print("Enter the student details")
        first_name = input("First name: ")
        last_name = input("Last name: ")
        email = input("Email Address: ")
        
        # Validate campus input
        while True:
            campus = input("Campus (Christchurch/Auckland/Wellington): ").title()
            if campus in valid_campuses:
                break
            else:
                print("Invalid campus. Please enter one of the following: Christchurch, Auckland, Wellington.")

        teaching_module.add_student(first_name, last_name, email, campus)
        print("\n** Record Successfully Added. **\n")

        another = input("DO YOU WANT TO ADD ANOTHER RECORD (PRESS Y OR N): ")
        if another.lower() == 'n':
            break
        elif another.lower() != 'y':
            print("Invalid input. Returning to main menu.")
            break

def delete_student_menu(teaching_module):
    while True:
        print("\n************************")
        print("DELETE STUDENT MENU")
        print("************************")
        student_id = input("Enter student ID to delete the record: ")

        # Check if the student exists before attempting deletion
        student = teaching_module.search_student("id", student_id)
        
        if not student:
            print(f"*** No student found with ID {student_id}. ***")
            return
        else:
            teaching_module.delete_student(student_id)
            print(f"*** Student with ID {student_id} has been deleted from the system. ***\n")

        another = input("DO YOU WANT TO DELETE ANOTHER RECORD (PRESS Y OR N): ")
        if another.lower() == 'n':
            break
        elif another.lower() != 'y':
            print("Invalid input. Returning to main menu.")
            break

def list_students_menu(teaching_module):
    print("\n************************")
    print("STUDENTS SHOW MENU")
    print("************************")
    print("1. SHOW ALL STUDENTS BY ID (ASCENDING ORDER)")
    print("2. SHOW ALL STUDENTS BY FIRST NAME (ASCENDING ORDER)")
    print("3. SHOW ALL STUDENTS BY LAST NAME (ASCENDING ORDER)")
    print("4. SHOW ALL STUDENTS BY CAMPUS (ASCENDING ORDER)")
    
    choice = input("Your Choice: ").strip()
    
    sort_by = None
    if choice == "1":
        sort_by = 'id'
    elif choice == "2":
        sort_by = 'first_name'
    elif choice == "3":
        sort_by = 'last_name'
    elif choice == "4":
        sort_by = 'campus'
    else:
        print("Invalid choice. Showing unsorted list.")
        return

    students = teaching_module.list_students(sort_by)
    
    for student in students:
        print(f"{student.student_id} - {student.first_name} {student.last_name} - {student.email} - {student.campus}")

def search_student_menu(teaching_module):
    print("\n************************")
    print("STUDENT SEARCH MENU")
    print("************************")
    print("1. SEARCH STUDENT BY ID")
    print("2. SEARCH STUDENT BY FIRST NAME")
    print("3. SEARCH STUDENT BY LAST NAME")
    choice = input("\nYour Choice: ")
    key = {'1': 'id', '2': 'first_name', '3': 'last_name'}.get(choice)

    if key:
        value = input(f"Enter {key.replace('_', ' ')}: ")
        students = teaching_module.search_student(key, value)
        if students:
            for student in students:
                print(f"{student.student_id} - {student.first_name} {student.last_name} - {student.email} - {student.campus}")
        else:
            print("No students found.")
    else:
        print("Invalid choice. Returning to main menu.")
        return

def add_teachers(teaching_module):
    teachers = [
        Teacher("Talha Abid"),
        Teacher("Faizan Ahmed Faiz"),
        Teacher("Hassan Raza Butt"),
        Teacher("Zeeshan Ahmed"),
        Teacher("Zehra Shah")
    ]
    for teacher in teachers:
        teaching_module.add_teacher(teacher)

def main():
    teaching_module = TeachingModule()

    # Create Courses
    course1 = Course("Mathematics", "MTH101")
    course2 = Course("Computer Science", "CS102")
    course3 = Course("Physics", "PHY103")
    course4 = Course("Chemistry", "CHE104")

    # Add Courses to Teaching Module
    teaching_module.add_course(course1)
    teaching_module.add_course(course2)
    teaching_module.add_course(course3)
    teaching_module.add_course(course4)

    # Create Teachers
    teacher1 = Teacher("Dr. Wahabuddin", course1)
    teacher2 = Teacher("Ms. Sheerina", course2)

    # Add Teachers
    add_teachers(teaching_module)

# Assign random teachers to courses
    from random import choice
    for course in teaching_module.courses:
        teacher = choice(teaching_module.teachers)
        course.assign_teacher(teacher)

    # Load Students from File
    students = load_students_from_file('students.txt')
    for student in students:
        teaching_module.students.append(student)

    # Enroll Students in Random Courses
    teaching_module.assign_courses_to_students()

    while True:
        print("\n**** Welcome to WHITECLIFFE College of Information Technology ****")
        print("************************* STUDENT PORTAL *************************")
        print("\nMAIN MENU\n")
        print("1. ADD NEW STUDENT")
        print("2. DELETE STUDENT")
        print("3. SHOW STUDENTS")
        print("4. SEARCH STUDENT")
        print("5. VIEW COURSES")
        print("6. VIEW COURSE DETAILS")
        print("\nType EXIT to quit the application..\n")
        choice = input("Your Choice: ")
        if choice == '1':
            add_student_menu(teaching_module)
        elif choice == '2':
            delete_student_menu(teaching_module)
        elif choice == '3':
            list_students_menu(teaching_module)
        elif choice == '4':
            search_student_menu(teaching_module)
        elif choice == '5':
            teaching_module.view_courses()
        elif choice == '6':
            teaching_module.view_courses()
            course_index = int(input("Select a course by number: ")) - 1
            teaching_module.view_course_details(course_index)
        elif choice.lower() == 'exit':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
