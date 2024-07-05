import json
from datetime import datetime

class Student:
    def __init__(self, first_name, last_name, email, campus, id=None, enrolled_courses=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.campus = campus
        self.id = id if id else self.generate_id()
        self.enrolled_courses = enrolled_courses if enrolled_courses else []

    def generate_id(self):
        year = datetime.now().year
        id = f"{self.first_name[:3]}{self.last_name[:3]}{year}"
        return id

# StudentDatabase class with different algorithms
class StudentDatabase:
    def __init__(self, filename):
        self.filename = filename
        self.students = self.load_students()

    def load_students(self):
        try:
            with open(self.filename, 'r') as file:
                students = json.load(file)
                return [Student(**s) for s in students]
        except FileNotFoundError:
            return []

    def save_students(self):
        with open(self.filename, 'w') as file:
            json.dump([s.__dict__ for s in self.students], file)

    def add_student(self, first_name, last_name, email, campus):
        student = Student(first_name, last_name, email, campus)
        self.students.append(student)
        self.save_students()

    def delete_student(self, student_id):
        self.students = [s for s in self.students if s.id != student_id]
        self.save_students()

    # Merge Sort implementation for sorting students
    def list_students(self, key=None):
        def merge_sort(lst, key):
            if len(lst) > 1:
                mid = len(lst) // 2
                L = lst[:mid]
                R = lst[mid:]

                merge_sort(L, key)
                merge_sort(R, key)

                i = j = k = 0

                while i < len(L) and j < len(R):
                    if getattr(L[i], key) < getattr(R[j], key):
                        lst[k] = L[i]
                        i += 1
                    else:
                        lst[k] = R[j]
                        j += 1
                    k += 1

                while i < len(L):
                    lst[k] = L[i]
                    i += 1
                    k += 1

                while j < len(R):
                    lst[k] = R[j]
                    j += 1
                    k += 1

        merge_sort(self.students, key)
        return self.students

    # Binary Search implementation for searching students
    def search_student(self, key, value):
        def binary_search(lst, key, value):
            low = 0
            high = len(lst) - 1
            while low <= high:
                mid = (low + high) // 2
                if getattr(lst[mid], key) == value:
                    return lst[mid]
                elif getattr(lst[mid], key) < value:
                    low = mid + 1
                else:
                    high = mid - 1
            return None

        # Ensure the list is sorted before searching
        self.list_students(key)
        return binary_search(self.students, key, value)

# Functions for Menu Operations (same as before)
def add_student_menu(db):
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

        db.add_student(first_name, last_name, email, campus)
        print("\n** Record Successfully Added. **\n")

        another = input("DO YOU WANT TO ADD ANOTHER RECORD (PRESS Y OR N): ")
        if another.lower() == 'n':
            break
        elif another.lower() != 'y':
            print("Invalid input. Returning to main menu.")
            break

def delete_student_menu(db):
    while True:
        print("\n************************")
        print("DELETE STUDENT MENU")
        print("************************")
        student_id = input("Enter student ID to delete the record: ")
        
        # Check if the student exists before attempting deletion
        student_exists = any(s.id == student_id for s in db.students)
        
        if not student_exists:
            print(f"*** No student found with ID {student_id}. ***")
            return
        else:
            db.delete_student(student_id)
            print(f"*** Student with ID {student_id} has been deleted from the system. ***\n")
        
        another = input("DO YOU WANT TO DELETE ANOTHER RECORD (PRESS Y OR N): ")
        if another.lower() == 'n':
            break
        elif another.lower() != 'y':
            print("Invalid input. Returning to main menu.")
            break

def list_students_menu(db):
    print("\n************************")
    print("STUDENTS SHOW MENU")
    print("************************")
    print("1. SHOW ALL STUDENTS BY ID (ASCENDING ORDER)")
    print("2. SHOW ALL STUDENTS BY FIRST NAME (ASCENDING ORDER)")
    print("3. SHOW ALL STUDENTS BY LAST NAME (ASCENDING ORDER)")
    print("4. SHOW ALL STUDENTS BY CAMPUS (ASCENDING ORDER)")
    choice = input("\nYour Choice: ")
    key = {'1': 'id', '2': 'first_name', '3': 'last_name', '4': 'campus'}.get(choice)

    if key:
        students = db.list_students(key)
        if students:
            print()
            for student in students:
                print(f"{student.id} - {student.first_name} {student.last_name} - {student.email} - {student.campus}")
        else:
            print("No students found.")
    else:
        print("Invalid choice. Returning to main menu.")
        return

def search_student_menu(db):
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
        student = db.search_student(key, value)
        if student:
            print(f"{student.id} - {student.first_name} {student.last_name} - {student.email} - {student.campus}")
        else:
            print("No student found.")
    else:
        print("Invalid choice. Returning to main menu.")
        return

# Main Program
def main():
    db = StudentDatabase("students.txt")
    while True:
        print("\n**** Welcome to WHITECLIFFE College of Information Technology ****")
        print("************************* STUDENT PORTAL *************************")
        print("\nMAIN MENU\n")
        print("1. ADD NEW STUDENT")
        print("2. DELETE STUDENT")
        print("3. SHOW STUDENTS")
        print("4. SEARCH STUDENT")
        print("\nType EXIT to quit the application..\n")
        choice = input("Your Choice: ")
        if choice == '1':
            add_student_menu(db)
        elif choice == '2':
            delete_student_menu(db)
        elif choice == '3':
            list_students_menu(db)
        elif choice == '4':
            search_student_menu(db)
        elif choice.lower() == 'exit':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
