from student import Student

class TeachingModule:
    def __init__(self):
        self.teachers = []
        self.courses = []
        self.students = []

    def add_course(self, course):
        self.courses.append(course)

    def add_teacher(self, teacher):
        self.teachers.append(teacher)

    def add_student(self, first_name, last_name, email, campus):
        new_student = Student(first_name, last_name, email, campus)
        self.students.append(new_student)
    
    def delete_student(self, student_id):
        student_to_delete = next((s for s in self.students if s.student_id == student_id), None)
        if student_to_delete:
            self.students.remove(student_to_delete)
            print(f"Student with ID {student_id} has been deleted.")
        else:
            print(f"No student found with ID {student_id}.")
        
    def list_students(self, sort_by):
        if sort_by == 'id':
            sorted_students = sorted(self.students, key=lambda s: s.student_id)
        elif sort_by == 'first_name':
            sorted_students = sorted(self.students, key=lambda s: s.first_name)
        elif sort_by == 'last_name':
            sorted_students = sorted(self.students, key=lambda s: s.last_name)
        elif sort_by == 'campus':
            sorted_students = sorted(self.students, key=lambda s: s.campus)
        else:
            print("Invalid sorting key. Showing unsorted list.")
            sorted_students = self.students

        return sorted_students
    
    def search_student(self, key, value):
        if key == "id":
            return [student for student in self.students if student.student_id == value]
        elif key == "first_name":
            return [student for student in self.students if student.first_name == value]
        elif key == "last_name":
            return [student for student in self.students if student.last_name == value]
        else:
            return []

    def enroll_student_in_course(self, student, course):
        if course in self.courses and student in self.students:
            course.enroll_student(student)
            print(f"{student.first_name} {student.last_name} has been enrolled in {course.title}")

    def notify_teachers(self, message):
        for teacher in self.teachers:
            if teacher.course:
                teacher.make_announcement(message)

    def notify_students(self, course, message):
        for student in course.enrolled_students:
            student.receive_announcement(message)

    def view_courses(self):
        if not self.courses:
            print("No courses available.")
            return
        print("Available Courses:")
        for i, course in enumerate(self.courses, 1):
            print(f"{i}. {course}")

    def view_course_details(self, course_index):
        if course_index < 0 or course_index >= len(self.courses):
            print("Invalid course selection.")
            return
        course = self.courses[course_index]
        print(f"Course: {course.title}")
        teacher = course.get_teacher()
        if teacher:
            print(f"Teacher: {teacher.name}")
        else:
            print("No teacher assigned.")
        students = course.get_students()
        if students:
            print("Enrolled Students:")
            for student in students:
                print(f" - {student.first_name} {student.last_name}")
        else:
            print("No students enrolled.")

    def assign_courses_to_students(self):
        from random import choice
        for student in self.students:
            course = choice(self.courses)
            self.enroll_student_in_course(student, course)