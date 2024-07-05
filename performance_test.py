import json
from datetime import datetime
import timeit
import matplotlib.pyplot as plt

# Student class
class Student:
    def __init__(self, first_name, last_name, email, campus, id=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.campus = campus
        self.id = id if id else self.generate_id()

    def generate_id(self):
        year = datetime.now().year
        id = f"{self.first_name[:3]}{self.last_name[:3]}{year}"
        return id

# StudentDatabase class for Solution 1
class StudentDatabase1:
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

    def list_students(self, key=None):
        return sorted(self.students, key=lambda s: getattr(s, key))

    def search_student(self, key, value):
        return [s for s in self.students if getattr(s, key) == value]

# StudentDatabase class for Solution 2 with different algorithms
class StudentDatabase2:
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

# Timing function
def time_operation(db, operation, *args, iterations=10):
    timer = timeit.Timer(lambda: getattr(db, operation)(*args))
    time_taken = timer.timeit(number=iterations) / iterations
    return time_taken

# Sample performance test
if __name__ == "__main__":
    db1 = StudentDatabase1("students1.txt")
    db2 = StudentDatabase2("students2.txt")

    # Sample student data
    names = [
        ("Ayhan", "Habib", "ayhan.habib@gmail.com", "Auckland"),
        ("Roshni", "Khan", "roshni.khan@hotmail.com", "Christchurch"),
        ("Ahmed", "Gala", "ahmed.gala@yahoo.com", "Wellington"),
        ("Ayesha", "Aslam", "ayesha.aslam@gmail.com", "Auckland"),
        ("Maryam", "Saeed", "maryam.saeed@yahoo.com", "Christchurch")
    ]

    # Add times
    add_times1 = []
    add_times2 = []
    for first_name, last_name, email, campus in names:
        add_times1.append(time_operation(db1, 'add_student', first_name, last_name, email, campus))
        add_times2.append(time_operation(db2, 'add_student', first_name, last_name, email, campus))

    # Generate IDs for delete and search operations
    ids = [Student(first_name, last_name, email, campus).generate_id() for first_name, last_name, email, campus in names]

    # Delete times
    delete_times1 = []
    delete_times2 = []
    for student_id in ids:
        delete_times1.append(time_operation(db1, 'delete_student', student_id))
        delete_times2.append(time_operation(db2, 'delete_student', student_id))

    # Search times
    search_times1 = []
    search_times2 = []
    for first_name, last_name, email, _ in names:
        search_times1.append(time_operation(db1, 'search_student', 'first_name', first_name))
        search_times2.append(time_operation(db2, 'search_student', 'first_name', first_name))

    print(f"Solution 1 Add Times: {add_times1}")
    print(f"Solution 2 Add Times: {add_times2}")
    print(f"Solution 1 Delete Times: {delete_times1}")
    print(f"Solution 2 Delete Times: {delete_times2}")
    print(f"Solution 1 Search Times: {search_times1}")
    print(f"Solution 2 Search Times: {search_times2}")

    # Compute average times
    avg_add_time1 = sum(add_times1) / len(add_times1)
    avg_add_time2 = sum(add_times2) / len(add_times2)
    avg_delete_time1 = sum(delete_times1) / len(delete_times1)
    avg_delete_time2 = sum(delete_times2) / len(delete_times2)
    avg_search_time1 = sum(search_times1) / len(search_times1)
    avg_search_time2 = sum(search_times2) / len(search_times2)

    avg_times1 = [avg_add_time1, avg_delete_time1, avg_search_time1]
    avg_times2 = [avg_add_time2, avg_delete_time2, avg_search_time2]

    operations = ['Add', 'Delete', 'Search']
    
    # Line Plot
    plt.figure(1)
    plt.plot(operations, avg_times1, label='Solution 1', marker='o')
    plt.plot(operations, avg_times2, label='Solution 2', marker='o')
    plt.xlabel('Operation')
    plt.ylabel('Time (seconds)')
    plt.title('Performance Comparison - Line Graph')
    plt.legend()
    plt.grid(True)
    plt.show(block=False)  # Use block=False to prevent blocking and allow for multiple windows

    # Bar Plot
    plt.figure(2)
    width = 0.35
    x = range(len(operations))
    plt.bar(x, avg_times1, width, label='Solution 1')
    plt.bar([p + width for p in x], avg_times2, width, label='Solution 2')
    plt.xlabel('Operation')
    plt.ylabel('Time (seconds)')
    plt.title('Performance Comparison - Bar Graph')
    plt.xticks([p + width / 2 for p in x], operations)
    plt.legend()
    plt.grid(True)
    plt.show(block=False)  # Use block=False to prevent blocking and allow for multiple windows

    # Pie Chart for Solution 1
    plt.figure(3)
    pie_data = [avg_add_time1, avg_delete_time1, avg_search_time1]
    pie_labels = ['Add', 'Delete', 'Search']
    plt.pie(pie_data, labels=pie_labels, autopct='%1.1f%%', startangle=140)
    plt.title('Solution 1 - Time Distribution')
    plt.show(block=False)  # Use block=False to prevent blocking and allow for multiple windows

    # Pie Chart for Solution 2
    plt.figure(4)
    pie_data = [avg_add_time2, avg_delete_time2, avg_search_time2]
    pie_labels = ['Add', 'Delete', 'Search']
    plt.pie(pie_data, labels=pie_labels, autopct='%1.1f%%', startangle=140)
    plt.title('Solution 2 - Time Distribution')
    plt.show()