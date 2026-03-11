import tkinter as tk
from tkinter import messagebox, simpledialog

class RabinKarpDetailedVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Trình Mô Phỏng Chi Tiết Thuật Toán Rabin-Karp")
        self.root.geometry("1200x850")
        self.root.configure(bg="#f3f4f6")
        
        self.text_data = ""
        self.pattern_data = ""
        self.sort_generator = None
        
        self.is_playing = False
        self.animations_running = 0  
        self.speed_ms = 800  
        
        self.ui_status = "Đang chờ nhập văn bản và mẫu tìm kiếm"
        
        self.text_blocks = []
        self.pattern_blocks = []
        self.window_rect = None
        
        # Mảng lưu trữ kết quả tìm kiếm
        self.found_indices = []
        
        # Tham số băm
        self.R = 311
        self.Q = 997
        
        self.setup_ui()
        self.draw_static_background()

    def setup_ui(self):
        frame_controls = tk.Frame(self.root, pady=10, bg="#ffffff", relief="ridge", bd=2)
        frame_controls.pack(fill=tk.X, padx=10, pady=10)

        btn_manual = tk.Button(frame_controls, text="1. Nhập Dữ Liệu", bg="#0ea5e9", fg="white", font=("Arial", 10, "bold"), command=self.input_manual_data)
        btn_manual.pack(side=tk.LEFT, padx=15)

        self.btn_start = tk.Button(frame_controls, text="2. Bắt Đầu Cài Đặt", bg="#10b981", fg="white", font=("Arial", 10, "bold"), command=self.start_simulation, state=tk.DISABLED)
        self.btn_start.pack(side=tk.LEFT, padx=5)

        frame_player = tk.Frame(frame_controls, bg="#ffffff")
        frame_player.pack(side=tk.RIGHT, padx=10)

        self.btn_auto = tk.Button(frame_player, text="▶ Tự Động Chạy", bg="#f59e0b", fg="white", font=("Arial", 10, "bold"), command=self.toggle_autoplay, state=tk.DISABLED)
        self.btn_auto.pack(side=tk.LEFT, padx=5)

        self.btn_next = tk.Button(frame_player, text="Bước Tiếp Theo ⏭", bg="#6366f1", fg="white", font=("Arial", 10, "bold"), command=self.next_step, state=tk.DISABLED)
        self.btn_next.pack(side=tk.LEFT, padx=5)

        self.lbl_status = tk.Label(self.root, text=self.ui_status, font=("Arial", 14, "bold"), fg="#1f2937", bg="#f3f4f6", pady=10)
        self.lbl_status.pack(fill=tk.X)

        self.canvas = tk.Canvas(self.root, bg="#f3f4f6", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    def draw_static_background(self):
        self.canvas.delete("all")
        self.text_blocks.clear()
        self.pattern_blocks.clear()
        self.window_rect = None
        
        self.canvas.create_rectangle(20, 20, 1150, 150, fill="#e0f2fe", outline="#bae6fd", width=2)
        self.canvas.create_text(30, 30, text="Văn Bản (Text - T)", anchor="nw", font=("Arial", 12, "bold"), fill="#0284c7")
        self.hash_window_text = self.canvas.create_text(30, 120, text="Hash(Window) = ?", anchor="nw", font=("Courier", 14, "bold"), fill="#b45309")

        self.canvas.create_rectangle(20, 170, 1150, 300, fill="#fef3c7", outline="#fde68a", width=2)
        self.canvas.create_text(30, 180, text="Mẫu Tìm Kiếm (Pattern - P)", anchor="nw", font=("Arial", 12, "bold"), fill="#b45309")
        self.hash_pattern_text = self.canvas.create_text(30, 270, text="Hash(Pattern) = ?", anchor="nw", font=("Courier", 14, "bold"), fill="#0284c7")

        self.canvas.create_rectangle(20, 320, 1150, 480, fill="#f5f3ff", outline="#c4b5fd", width=2)
        self.canvas.create_text(30, 330, text="Bảng Tính Toán Trực Tiếp", anchor="nw", font=("Arial", 12, "bold"), fill="#6d28d9")
        self.calc_formula_text = self.canvas.create_text(50, 370, text="Chưa có phép tính nào", anchor="nw", font=("Courier", 14, "bold"), fill="#4c1d95", width=1050)

        self.canvas.create_rectangle(20, 500, 1150, 700, fill="#dcfce7", outline="#86efac", width=2)
        self.canvas.create_text(30, 510, text="Kết Quả & Logs", anchor="nw", font=("Arial", 12, "bold"), fill="#166534")
        
        if not hasattr(self, 'log_frame'):
            self.log_frame = tk.Frame(self.canvas, bg="#dcfce7")
            self.log_text_widget = tk.Text(self.log_frame, font=("Courier", 12), bg="#dcfce7", fg="#0f172a", wrap=tk.WORD, bd=0, state=tk.DISABLED)
            self.log_scrollbar = tk.Scrollbar(self.log_frame, command=self.log_text_widget.yview)
            self.log_text_widget.config(yscrollcommand=self.log_scrollbar.set)
            
            self.log_text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            self.log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        else:
            self.log_text_widget.config(state=tk.NORMAL)
            self.log_text_widget.delete(1.0, tk.END)
            self.log_text_widget.config(state=tk.DISABLED)

        self.canvas.create_window(585, 615, window=self.log_frame, width=1090, height=150)

    def add_log(self, message):
        self.log_text_widget.config(state=tk.NORMAL)
        self.log_text_widget.insert(tk.END, message + "\n")
        self.log_text_widget.see(tk.END)
        self.log_text_widget.config(state=tk.DISABLED)

    def update_formula(self, text):
        self.canvas.itemconfig(self.calc_formula_text, text=text)

    def create_block(self, x, y, char, index=None, color="#bae6fd", text_color="#0f172a"):
        rect = self.canvas.create_rectangle(x, y, x+40, y+40, fill=color, outline="#38bdf8", width=2)
        text = self.canvas.create_text(x+20, y+20, text=char, font=("Courier", 14, "bold"), fill=text_color)
        
        if index is not None:
            self.canvas.create_text(x+20, y-12, text=str(index), font=("Arial", 10, "bold"), fill="#6b7280")
            
        return {"rect": rect, "text": text, "char": char, "x": x, "y": y, "index": index}

    def input_manual_data(self):
        text_input = simpledialog.askstring("Nhập Dữ Liệu", "Nhập chuỗi văn bản (Text):", initialvalue="RABINKARPTEST")
        if not text_input: return
        
        pattern_input = simpledialog.askstring("Nhập Dữ Liệu", "Nhập mẫu tìm kiếm (Pattern):", initialvalue="KARP")
        if not pattern_input: return

        if len(pattern_input) > len(text_input):
            messagebox.showerror("Lỗi", "Pattern không được dài hơn Text!")
            return

        self.text_data = text_input.upper()
        self.pattern_data = pattern_input.upper()
        
        self.draw_static_background()
        
        start_x, start_y = 50, 60
        for i, char in enumerate(self.text_data):
            self.text_blocks.append(self.create_block(start_x + i * 45, start_y, char, index=i))
            
        start_x, start_y = 50, 210
        for i, char in enumerate(self.pattern_data):
            self.pattern_blocks.append(self.create_block(start_x + i * 45, start_y, char, index=i, color="#fde68a"))

        self.btn_start.config(state=tk.NORMAL)
        self.ui_status = f"Đã nạp Text ({len(self.text_data)} ký tự) và Pattern ({len(self.pattern_data)} ký tự)."
        self.lbl_status.config(text=self.ui_status)

    def start_simulation(self):
        self.btn_start.config(state=tk.DISABLED)
        self.btn_next.config(state=tk.NORMAL)
        self.btn_auto.config(state=tk.NORMAL)
        
        self.found_indices = []
        
        self.sort_generator = self.run_rabin_karp_algo()
        self.ui_status = "Đã sẵn sàng. Bấm Bước Tiếp Theo hoặc Tự Động Chạy"
        self.lbl_status.config(text=self.ui_status)

    def toggle_autoplay(self):
        self.is_playing = not self.is_playing
        if self.is_playing:
            self.btn_auto.config(text="⏸ Dừng Chạy", bg="#ef4444")
            self.btn_next.config(state=tk.DISABLED)
            self.play_next()
        else:
            self.btn_auto.config(text="▶ Tự Động Chạy", bg="#f59e0b")
            self.btn_next.config(state=tk.NORMAL)

    def play_next(self):
        if not self.is_playing: return
        try:
            next(self.sort_generator)
            self.root.after(self.speed_ms, self.play_next)
        except StopIteration:
            self.finish_simulation()

    def next_step(self):
        try:
            next(self.sort_generator)
        except StopIteration:
            self.finish_simulation()

    def finish_simulation(self):
        self.is_playing = False
        self.btn_auto.config(state=tk.DISABLED, text="▶ Tự Động Chạy", bg="#f59e0b")
        self.btn_next.config(state=tk.DISABLED)
        self.lbl_status.config(text="HOÀN TẤT THUẬT TOÁN RABIN-KARP")
        self.update_formula("Thuật toán đã duyệt xong toàn bộ văn bản.")
        
        if len(self.found_indices) > 0:
            indices_str = ", ".join(map(str, self.found_indices))
            msg = f"Đã quét xong toàn bộ chuỗi văn bản.\nTìm thấy mẫu tại các vị trí (index): {indices_str}"
        else:
            msg = "Đã quét xong toàn bộ chuỗi văn bản.\nKhông tìm thấy mẫu trong văn bản."
            
        messagebox.showinfo("Kết quả tìm kiếm", msg)

    def run_rabin_karp_algo(self):
        M = len(self.pattern_data)
        N = len(self.text_data)
        
        self.lbl_status.config(text="BƯỚC 1: Tính giá trị RM và Hash ban đầu")
        self.add_log("Khởi tạo thuật toán. Đang tính mã băm")
        
        RM = 1
        for _ in range(M - 1):
            RM = (RM * self.R) % self.Q
            
        self.update_formula(f"Tính RM = (R^(M-1)) % Q \nRM = ({self.R}^({M}-1)) % {self.Q} = {RM}")
        yield

        p_hash = 0
        t_hash = 0

        self.update_formula("Tính Hash(Pattern) và Hash(Window 0) bằng phương pháp Horner")
        yield

        for i in range(M):
            p_hash = (self.R * p_hash + ord(self.pattern_data[i])) % self.Q
            t_hash = (self.R * t_hash + ord(self.text_data[i])) % self.Q
            
        self.canvas.itemconfig(self.hash_pattern_text, text=f"Hash(Pattern) = {p_hash}")
        self.canvas.itemconfig(self.hash_window_text, text=f"Hash(Window) = {t_hash}")
        
        win_x1 = 45
        win_y1 = 55
        win_x2 = 50 + M * 45
        win_y2 = 105
        self.window_rect = self.canvas.create_rectangle(win_x1, win_y1, win_x2, win_y2, outline="#ef4444", width=4)
        
        self.add_log(f"-> Hash Pattern: {p_hash}")
        self.add_log(f"-> Hash Window[0:{M-1}]: {t_hash}")
        yield

        for i in range(N - M + 1):
            self.lbl_status.config(text=f"BƯỚC 2: Kiểm tra cửa sổ trượt tại index {i}")
            self.canvas.itemconfig(self.window_rect, outline="#f59e0b")
            self.update_formula(f"So sánh băm:\nHash(Window) == Hash(Pattern)\n{t_hash} == {p_hash} ?")
            yield
            
            if p_hash == t_hash:
                self.lbl_status.config(text="Hash KHỚP! Bắt đầu kiểm tra từng ký tự để chống đụng độ (Spurious Hit)")
                self.add_log(f"Index {i}: Hash KHỚP ({p_hash} == {t_hash}). Bắt đầu kiểm tra ký tự")
                self.update_formula("Mã băm bằng nhau. Tiến hành đối sánh từng ký tự Text[i+j] == Pattern[j]")
                yield
                
                match = True
                for j in range(M):
                    tb = self.text_blocks[i + j]
                    pb = self.pattern_blocks[j]
                    
                    self.canvas.itemconfig(tb["rect"], fill="#fca5a5")
                    self.canvas.itemconfig(pb["rect"], fill="#fca5a5")
                    
                    self.update_formula(f"So sánh ký tự thứ {j}:\nText: '{self.text_data[i+j]}' (Mã ASCII: {ord(self.text_data[i+j])})\nPattern: '{self.pattern_data[j]}' (Mã ASCII: {ord(self.pattern_data[j])})")
                    yield
                    
                    if self.text_data[i + j] != self.pattern_data[j]:
                        match = False
                        self.add_log(f" -> Mismatch tại '{self.text_data[i+j]}' và '{self.pattern_data[j]}'")
                        self.update_formula(f"Ký tự khác nhau ('{self.text_data[i+j]}' != '{self.pattern_data[j]}'). Ngừng kiểm tra.")
                        self.canvas.itemconfig(tb["rect"], fill="#bae6fd")
                        self.canvas.itemconfig(pb["rect"], fill="#fde68a")
                        yield
                        break
                        
                    self.canvas.itemconfig(tb["rect"], fill="#86efac")
                    self.canvas.itemconfig(pb["rect"], fill="#86efac")
                    yield
                    
                if match:
                    self.lbl_status.config(text="TÌM THẤY! Chuỗi khớp hoàn toàn.")
                    self.add_log(f"*** TÌM THẤY PATTERN TẠI INDEX {i} ***")
                    self.update_formula(f"Tất cả {M} ký tự đều khớp. Lưu lại vị trí chỉ số {i}.")
                    self.canvas.itemconfig(self.window_rect, outline="#22c55e")
                    
                    self.found_indices.append(i)
                    
                    yield
                else:
                    self.lbl_status.config(text="Đụng độ băm (Spurious Hit)! Các ký tự không khớp.")
                    self.canvas.itemconfig(self.window_rect, outline="#ef4444")
                    yield
                    
                for pb in self.pattern_blocks:
                    self.canvas.itemconfig(pb["rect"], fill="#fde68a")
                if not match:
                    for j in range(M):
                        self.canvas.itemconfig(self.text_blocks[i+j]["rect"], fill="#bae6fd")
            else:
                self.lbl_status.config(text="Hash KHÔNG KHỚP. Bỏ qua so sánh chuỗi.")
                self.update_formula(f"Mã băm khác biệt ({t_hash} != {p_hash}).\nKết luận: Chuỗi con hiện tại chắc chắn không khớp với Pattern.")
                self.add_log(f"Index {i}: Bỏ qua (Hash {t_hash} != {p_hash})")
                self.canvas.itemconfig(self.window_rect, outline="#9ca3af")
                yield

            if i < N - M:
                self.lbl_status.config(text="BƯỚC 3: Cập nhật Hash cho cửa sổ tiếp theo (Rolling Hash)")
                
                old_char = self.text_data[i]
                new_char = self.text_data[i + M]
                old_val = ord(old_char)
                new_val = ord(new_char)
                
                math_str = f"H_new = ((H_old - ASCII(Ký_tự_cũ) * RM) * R + ASCII(Ký_tự_mới)) % Q\n"
                math_str += f"H_new = (({t_hash} - {old_val} * {RM}) * {self.R} + {new_val}) % {self.Q}"
                self.update_formula(math_str)
                yield
                
                t_hash = (t_hash - RM * old_val) % self.Q
                t_hash = (t_hash * self.R + new_val) % self.Q
                t_hash = (t_hash + self.Q) % self.Q 
                
                self.canvas.move(self.window_rect, 45, 0)
                self.canvas.itemconfig(self.hash_window_text, text=f"Hash(Window) = {t_hash}")
                
                math_str += f"\nKết quả Hash mới: {t_hash}"
                self.update_formula(math_str)
                self.add_log(f"Trượt: -'{old_char}', +'{new_char}' => Hash mới: {t_hash}")
                yield

if __name__ == "__main__":
    root = tk.Tk()
    app = RabinKarpDetailedVisualizer(root)
    root.mainloop()