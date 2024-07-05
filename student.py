from datetime import datetime

class Student:
    def __init__(self, first_name, last_name, email, campus, student_id=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.campus = campus
        self.student_id = student_id if student_id else self.generate_id()
        self.enrolled_courses = [] 

    def __str__(self):
        return f"{self.student_id} - {self.first_name} {self.last_name} - {self.email} - {self.campus}"

    def generate_id(self):
        year = datetime.now().year
        id = f"{self.first_name[:3]}{self.last_name[:3]}{year}"
        return id

    def add_course(self, course):
        if course not in self.enrolled_courses:
            self.enrolled_courses.append(course)

    def receive_announcement(self, announcement):
        print(f"Notification for {self.first_name} {self.last_name}: {announcement}")

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email} - {self.campus}"