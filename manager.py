from btree import BTree
from student import Student

class StudentManager:
    def __init__(self, order=4):
        self.id_index = BTree(order)
        self.name_index = BTree(order)

    def add_student(self, student):
        self.id_index.insert(student.student_id, student)
        
        existing_list = self.name_index.search(student.full_name)
        if existing_list is not None:
            existing_list.append(student)
        else:
            self.name_index.insert(student.full_name, [student])
            
    def search_by_id(self, student_id):
        return self.id_index.search(student_id)

    def search_by_name(self, name):
        results = self.name_index.search(name)
        return results if results else []

    def advanced_search(self, student_id, name, gender, dob, hometown):
        # Ưu tiên lấy dữ liệu từ B-Tree index nếu có Mã SV hoặc Tên
        candidates = []
        if student_id:
            sv = self.search_by_id(student_id)
            if sv:
                candidates = [sv]
        elif name:
            res = self.search_by_name(name)
            if res:
                candidates = res
        else:
            candidates = self.id_index.get_all_values()
            
        final_result = []
        for sv in candidates:
            if not sv: continue
            if student_id and sv.student_id != student_id: continue
            if name and name.lower() not in sv.full_name.lower(): continue
            if gender and gender != "Tất cả" and sv.gender != gender: continue
            if dob and sv.date_of_birth != dob: continue
            if hometown and hometown.lower() not in sv.hometown.lower(): continue
            final_result.append(sv)
            
        return final_result

    def delete_by_id(self, student_id):
        student = self.search_by_id(student_id)
        if student:
            self.id_index.delete(student_id)
            name_list = self.name_index.search(student.full_name)
            if name_list:
                for s in name_list:
                    if s.student_id == student_id:
                        name_list.remove(s)
                        break
            return True
        return False
        
    def get_all_students(self):
        return [sv for sv in self.id_index.get_all_values() if sv is not None]