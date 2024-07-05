class Course:
    def __init__(self, title, name):
        self.title = title
        self.name = name
        self.enrolled_students = []
        self.teacher = None

    def enroll_student(self, student):
        if student not in self.enrolled_students:
            self.enrolled_students.append(student)
            student.add_course(self)

    def assign_teacher(self, teacher):
        self.teacher = teacher

    def get_teacher(self):
        return self.teacher

    def get_students(self):
        return self.enrolled_students

    def __str__(self):
        return f"{self.title} - {self.name}"