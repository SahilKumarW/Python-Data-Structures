class Teacher:
    def __init__(self, name, course=None):
        self.name = name
        self.course = course

    def assign_course(self, course):
        self.course = course

    def make_announcement(self, announcement):
        if self.course:
            print(f"Announcement from {self.name}: {announcement}")
            for student in self.course.enrolled_students:
                student.receive_announcement(announcement)