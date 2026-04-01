class Student:
    def __init__(self, student_id, full_name, gender, date_of_birth, hometown):
        self.student_id = student_id
        self.full_name = full_name
        self.gender = gender
        self.date_of_birth = date_of_birth
        self.hometown = hometown

    def __str__(self):
        return f"[{self.student_id}] {self.full_name} | Giới tính: {self.gender} | Quê quán: {self.hometown}"
