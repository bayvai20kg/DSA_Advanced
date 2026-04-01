import tkinter as tk
from tkinter import ttk, messagebox
from student import Student
from manager import StudentManager

class PlaceholderEntry(tk.Entry):
    def __init__(self, master=None, placeholder="", color='grey', *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']

        self.bind("<FocusIn>", self._focus_in)
        self.bind("<FocusOut>", self._focus_out)

        self._put_placeholder()

    def _put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color

    def _focus_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color

    def _focus_out(self, *args):
        if not self.get():
            self._put_placeholder()

    def get_value(self):
        val = self.get()
        if val == self.placeholder and self['fg'] == self.placeholder_color:
            return ""
        return val

    def clear_text(self):
        self.delete(0, tk.END)
        self._put_placeholder()

class StudentAppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Hệ Thống Quản Lý Sinh Viên - B-Tree")
        self.root.geometry("1100x750") # Tăng chiều rộng để đủ chỗ cho 2 bảng
        self.root.configure(bg="#E0F7FA") 
        
        # Đã thay đổi thành cây Bậc 3 theo yêu cầu
        self.manager = StudentManager(order=3)
        
        style = ttk.Style()
        style.theme_use("clam")
        
        style.configure("TNotebook", background="#E0F7FA")
        style.configure("TNotebook.Tab", font=("Arial", 11, "bold"), padding=[20, 8], background="#B2EBF2", foreground="#006064")
        style.map("TNotebook.Tab", background=[("selected", "#00BCD4")], foreground=[("selected", "#FFFFFF")])
        
        style.configure("TFrame", background="#FFFFFF")
        style.configure("TLabel", background="#FFFFFF", font=("Arial", 10), foreground="#004D40")
        
        self.setup_ui()
        self.refresh_table()

    def setup_ui(self):
        lbl_title = tk.Label(self.root, text="QUẢN LÝ SINH VIÊN BẰNG B-TREE", font=("Arial", 18, "bold"), bg="#E0F7FA", fg="#00695C")
        lbl_title.pack(pady=10)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="x", padx=20, pady=5)

        self.tab_add = ttk.Frame(self.notebook, padding=20)
        self.tab_search = ttk.Frame(self.notebook, padding=20)
        self.tab_delete = ttk.Frame(self.notebook, padding=20)

        self.notebook.add(self.tab_add, text="📝 Thêm Sinh Viên")
        self.notebook.add(self.tab_search, text="🔍 Tìm Kiếm")
        self.notebook.add(self.tab_delete, text="🗑️ Xóa Sinh Viên")

        self._build_add_tab()
        self._build_search_tab()
        self._build_delete_tab()

        # --- KHU VỰC HIỂN THỊ CHIA ĐÔI ---
        bottom_frame = tk.Frame(self.root, bg="#E0F7FA")
        bottom_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Trái: Bảng dữ liệu gốc
        table_container = tk.LabelFrame(bottom_frame, text="Bảng Dữ Liệu Gốc", bg="#E0F7FA", font=("Arial", 11, "bold"), fg="#004D40")
        table_container.pack(side="left", fill="both", expand=True, padx=(0, 10))

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"), background="#80DEEA", foreground="#004D40")
        style.configure("Treeview", font=("Arial", 10), rowheight=25)
        
        columns = ("id", "name", "gender")
        self.tree = ttk.Treeview(table_container, columns=columns, show="headings")
        self.tree.heading("id", text="Mã SV")
        self.tree.heading("name", text="Họ và Tên")
        self.tree.heading("gender", text="Giới tính")
        self.tree.column("id", width=100, anchor="center")
        self.tree.column("name", width=180)
        self.tree.column("gender", width=80, anchor="center")

        scrollbar = ttk.Scrollbar(table_container, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Phải: Cấu trúc Index B-Tree
        index_container = tk.LabelFrame(bottom_frame, text="Cây Chỉ Mục (B-Tree Bậc 3 - Mã SV)", bg="#E0F7FA", font=("Arial", 11, "bold"), fg="#D32F2F")
        index_container.pack(side="right", fill="both", expand=True)

        self.text_index = tk.Text(index_container, font=("Consolas", 12, "bold"), bg="#1E1E1E", fg="#4CAF50", state="disabled", wrap="none")
        self.text_index.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        index_scroll = ttk.Scrollbar(index_container, orient=tk.VERTICAL, command=self.text_index.yview)
        self.text_index.configure(yscrollcommand=index_scroll.set)
        index_scroll.pack(side="right", fill="y")

    # ================= CÁC TAB CHỨC NĂNG =================

    def _build_add_tab(self):
        container = tk.Frame(self.tab_add, bg="#FFFFFF")
        container.pack(pady=10, anchor="center")

        ttk.Label(container, text="Mã SV:").grid(row=0, column=0, sticky="w", pady=10)
        self.add_id = PlaceholderEntry(container, placeholder="VD: 23520713", width=25, font=("Arial", 11))
        self.add_id.grid(row=0, column=1, padx=15, pady=10)

        ttk.Label(container, text="Họ và Tên:").grid(row=0, column=2, sticky="w", pady=10, padx=(30, 0))
        self.add_name = PlaceholderEntry(container, placeholder="VD: Nguyễn Thị B", width=35, font=("Arial", 11))
        self.add_name.grid(row=0, column=3, padx=15, pady=10)

        ttk.Label(container, text="Giới tính:").grid(row=1, column=0, sticky="w", pady=10)
        self.add_gender = ttk.Combobox(container, values=["Nam", "Nữ", "Khác"], width=23, font=("Arial", 11), state="readonly")
        self.add_gender.grid(row=1, column=1, padx=15, pady=10)
        self.add_gender.current(0)

        ttk.Label(container, text="Năm sinh:").grid(row=1, column=2, sticky="w", pady=10, padx=(30, 0))
        self.add_dob = PlaceholderEntry(container, placeholder="VD: 2005", width=35, font=("Arial", 11))
        self.add_dob.grid(row=1, column=3, padx=15, pady=10)

        ttk.Label(container, text="Quê quán:").grid(row=2, column=0, sticky="w", pady=10)
        self.add_hometown = PlaceholderEntry(container, placeholder="VD: Bình Dương", width=78, font=("Arial", 11))
        self.add_hometown.grid(row=2, column=1, columnspan=3, sticky="w", padx=15, pady=10)

        btn_frame = tk.Frame(container, bg="#FFFFFF")
        btn_frame.grid(row=3, column=0, columnspan=4, pady=25)
        
        tk.Button(btn_frame, text="✅ Xác nhận Thêm", bg="#43A047", fg="white", font=("Arial", 11, "bold"), width=18, pady=5, command=self.handle_add).pack(side="left", padx=10)
        tk.Button(btn_frame, text="🔄 Làm mới form", bg="#FB8C00", fg="white", font=("Arial", 11, "bold"), width=15, pady=5, command=self.clear_add_form).pack(side="left", padx=10)

    def _build_search_tab(self):
        container = tk.Frame(self.tab_search, bg="#FFFFFF")
        container.pack(pady=20, anchor="center")

        ttk.Label(container, text="Nhập Mã SV hoặc Họ Tên để tìm kiếm nhanh:", font=("Arial", 10, "italic"), foreground="#E53935").grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 15))

        ttk.Label(container, text="Mã SV:").grid(row=1, column=0, sticky="w", pady=10)
        self.search_id = PlaceholderEntry(container, placeholder="VD: 23520713", width=30, font=("Arial", 11))
        self.search_id.grid(row=1, column=1, padx=15, pady=10)

        ttk.Label(container, text="Họ và Tên:").grid(row=1, column=2, sticky="w", pady=10, padx=(40, 0))
        self.search_name = PlaceholderEntry(container, placeholder="VD: Nguyễn Thị B", width=35, font=("Arial", 11))
        self.search_name.grid(row=1, column=3, padx=15, pady=10)

        btn_frame = tk.Frame(container, bg="#FFFFFF")
        btn_frame.grid(row=2, column=0, columnspan=4, pady=25)

        tk.Button(btn_frame, text="🔍 Tìm Kiếm", bg="#1E88E5", fg="white", font=("Arial", 11, "bold"), width=18, pady=5, command=self.handle_search).pack(side="left", padx=10)
        tk.Button(btn_frame, text="📋 Xem tất cả", bg="#8E24AA", fg="white", font=("Arial", 11, "bold"), width=15, pady=5, command=self.refresh_table).pack(side="left", padx=10)

    def _build_delete_tab(self):
        container = tk.Frame(self.tab_delete, bg="#FFFFFF")
        container.pack(pady=30, anchor="center")

        ttk.Label(container, text="Nhập Mã SV của sinh viên cần xóa khỏi hệ thống:").grid(row=0, column=0, sticky="w", pady=20)
        self.del_id = PlaceholderEntry(container, placeholder="VD: 23520713", width=30, font=("Arial", 11))
        self.del_id.grid(row=0, column=1, padx=15, pady=20)

        tk.Button(container, text="🗑️ Xóa Sinh Viên", bg="#E53935", fg="white", font=("Arial", 11, "bold"), width=18, pady=5, command=self.handle_delete).grid(row=0, column=2, padx=15, pady=20)

    # ================= CÁC HÀM XỬ LÝ SỰ KIỆN =================

    def handle_add(self):
        sv_id = self.add_id.get_value().strip()
        name = self.add_name.get_value().strip()
        gender = self.add_gender.get().strip()
        dob = self.add_dob.get_value().strip()
        hometown = self.add_hometown.get_value().strip()

        if not sv_id or not name:
            messagebox.showerror("Thêm thất bại", "Vui lòng nhập bắt buộc: Mã SV và Họ Tên!")
            return

        if self.manager.search_by_id(sv_id) is not None:
            messagebox.showerror("Thêm thất bại", f"Mã Sinh Viên '{sv_id}' đã tồn tại trong hệ thống!")
            return

        try:
            new_student = Student(sv_id, name, gender, dob, hometown)
            self.manager.add_student(new_student)
            
            self.refresh_table()
            messagebox.showinfo("Thêm thành công", f"Đã thêm vào hệ thống:\n\n🎓 Họ Tên: {name}\n🆔 Mã SV: {sv_id}")
            self.clear_add_form()
        except Exception as e:
            messagebox.showerror("Thêm thất bại", f"Có lỗi xảy ra: {str(e)}")

    def handle_search(self):
        sv_id = self.search_id.get_value().strip()
        name = self.search_name.get_value().strip()

        if not sv_id and not name:
            messagebox.showwarning("Nhắc nhở", "Vui lòng nhập Mã SV hoặc Họ Tên để tìm kiếm.")
            return

        self.clear_tree()
        results_to_display = []

        if sv_id:
            sv = self.manager.search_by_id(sv_id)
            if sv:
                if name and name.lower() not in sv.full_name.lower():
                    pass 
                else:
                    results_to_display.append(sv)
        else:
            res = self.manager.search_by_name(name)
            if res:
                results_to_display.extend(res)

        if results_to_display:
            for r in results_to_display:
                self.insert_to_tree(r)
        else:
            messagebox.showinfo("Kết quả tìm kiếm", "Không tìm thấy sinh viên nào khớp với thông tin bạn nhập.")

    def handle_delete(self):
        sv_id = self.del_id.get_value().strip()
        if not sv_id:
            messagebox.showwarning("Nhắc nhở", "Vui lòng nhập Mã SV cần xóa.")
            return

        confirm = messagebox.askyesno("Xác nhận xóa", f"Hành động này không thể hoàn tác.\nBạn có chắc chắn muốn xóa sinh viên mã '{sv_id}'?")
        if confirm:
            success = self.manager.delete_by_id(sv_id)
            if success:
                messagebox.showinfo("Xóa thành công", f"Đã xóa thành công sinh viên có mã '{sv_id}'.")
                self.del_id.clear_text()
                self.refresh_table()
            else:
                messagebox.showerror("Xóa thất bại", "Không tìm thấy Mã SV này trong hệ thống!")

    def clear_add_form(self):
        self.add_id.clear_text()
        self.add_name.clear_text()
        self.add_gender.current(0)
        self.add_dob.clear_text()
        self.add_hometown.clear_text()

    def clear_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def insert_to_tree(self, student):
        self.tree.insert("", tk.END, values=(
            student.student_id, 
            student.full_name, 
            student.gender
        ))

    def refresh_table(self):
        self.clear_tree()
        
        # Cập nhật Bảng gốc
        if hasattr(self.manager.id_index, 'get_all_values'):
            all_students = [sv for sv in self.manager.id_index.get_all_values() if sv is not None]
            for sv in all_students:
                self.insert_to_tree(sv)
                
        # Cập nhật Box trạng thái Index B-Tree
        self.text_index.config(state="normal")
        self.text_index.delete("1.0", tk.END)
        
        tree_text = self.manager.id_index.get_tree_text()
        if not tree_text.strip() or tree_text.strip() == "➔ Gốc: []":
            tree_text = "Cây chỉ mục đang rỗng."
            
        self.text_index.insert(tk.END, tree_text)
        self.text_index.config(state="disabled")