import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import struct
import os
import tempfile

FLOAT_FORMAT = 'd'
FLOAT_SIZE = struct.calcsize(FLOAT_FORMAT)
NUMS_PER_PAGE = 2  
BUFFER_PAGES = 3   
BUFFER_CAPACITY = NUMS_PER_PAGE * BUFFER_PAGES 

class ExternalSortSmoothVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Lab 1: Trình Mô Phỏng External Merge Sort Animation")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f3f4f6")
        
        self.input_file = ""
        self.output_file = ""
        self.runs_files = []
        self.sort_generator = None
        
        self.is_playing = False
        self.animations_running = 0  
        self.speed_ms = 15  
        
        self.ui_status = "Đang chờ dữ liệu đầu vào"
        self.blocks = [] 
        
        self.setup_ui()
        self.draw_static_background()

    def setup_ui(self):
        frame_controls = tk.Frame(self.root, pady=10, bg="#ffffff", relief="ridge", bd=2)
        frame_controls.pack(fill=tk.X, padx=10, pady=10)

        btn_gen = tk.Button(frame_controls, text="1a. Random", bg="#3b82f6", fg="white", font=("Arial", 10, "bold"), command=self.generate_data)
        btn_gen.pack(side=tk.LEFT, padx=5)

        btn_manual = tk.Button(frame_controls, text="1b. Nhập Tay", bg="#0ea5e9", fg="white", font=("Arial", 10, "bold"), command=self.input_manual_data)
        btn_manual.pack(side=tk.LEFT, padx=5)

        btn_select = tk.Button(frame_controls, text="1c. Chọn File", bg="#0284c7", fg="white", font=("Arial", 10, "bold"), command=self.select_file)
        btn_select.pack(side=tk.LEFT, padx=5)

        self.btn_out = tk.Button(frame_controls, text="2. Chọn Nơi Lưu", bg="#8b5cf6", fg="white", font=("Arial", 10, "bold"), command=self.select_output, state=tk.DISABLED)
        self.btn_out.pack(side=tk.LEFT, padx=15)

        self.btn_start = tk.Button(frame_controls, text="3. Bắt Đầu", bg="#10b981", fg="white", font=("Arial", 10, "bold"), command=self.start_simulation, state=tk.DISABLED)
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
        self.blocks.clear()
        
        self.canvas.create_rectangle(20, 20, 500, 200, fill="#e0f2fe", outline="#bae6fd", width=2)
        self.canvas.create_text(30, 30, text="Ổ Đĩa (Input)", anchor="nw", font=("Arial", 12, "bold"), fill="#0284c7")

        self.canvas.create_rectangle(600, 20, 1150, 410, fill="#fef3c7", outline="#fde68a", width=2)
        self.canvas.create_text(610, 30, text="Bộ Nhớ RAM (3 Buffers)", anchor="nw", font=("Arial", 12, "bold"), fill="#b45309")
        
        self.canvas.create_text(620, 55, text="Buffer 1", anchor="nw", font=("Arial", 10, "bold"), fill="#6b7280")
        self.canvas.create_rectangle(620, 75, 1130, 155, fill="#ffffff", outline="#d1d5db", dash=(4, 4))
        
        self.canvas.create_text(620, 175, text="Buffer 2", anchor="nw", font=("Arial", 10, "bold"), fill="#6b7280")
        self.canvas.create_rectangle(620, 195, 1130, 275, fill="#ffffff", outline="#d1d5db", dash=(4, 4))
        
        self.canvas.create_text(620, 295, text="Buffer 3 (Output)", anchor="nw", font=("Arial", 10, "bold"), fill="#ef4444")
        self.canvas.create_rectangle(620, 315, 1130, 395, fill="#ffffff", outline="#fca5a5", dash=(4, 4))

        self.canvas.create_rectangle(20, 230, 500, 500, fill="#f3f4f6", outline="#d1d5db", width=2)
        self.canvas.create_text(30, 240, text="Ổ Đĩa (Các Tệp Runs Tạm Thời)", anchor="nw", font=("Arial", 12, "bold"), fill="#4b5563")

        # Nới rộng chiều cao khung kết quả để chứa được nhiều dòng hơn
        self.canvas.create_rectangle(20, 520, 1150, 760, fill="#dcfce7", outline="#86efac", width=2)
        self.canvas.create_text(30, 530, text="Ổ Đĩa (Tệp Kết Quả Cuối Cùng)", anchor="nw", font=("Arial", 12, "bold"), fill="#166534")

    def create_block(self, x, y, value, color="#bae6fd"):
        rect = self.canvas.create_rectangle(x, y, x+50, y+50, fill=color, outline="#38bdf8", width=2)
        text = self.canvas.create_text(x+25, y+25, text=f"{value:.1f}", font=("Courier", 10, "bold"), fill="#0f172a")
        block = {"rect": rect, "text": text, "val": value, "x": x, "y": y}
        self.blocks.append(block)
        return block

    def animate_move(self, block, target_x, target_y, steps=30, callback=None):
        self.animations_running += 1 
        dx = (target_x - block["x"]) / steps
        dy = (target_y - block["y"]) / steps

        def step(current_step):
            if current_step < steps:
                self.canvas.move(block["rect"], dx, dy)
                self.canvas.move(block["text"], dx, dy)
                block["x"] += dx
                block["y"] += dy
                self.root.after(self.speed_ms, step, current_step + 1)
            else:
                exact_dx = target_x - block["x"]
                exact_dy = target_y - block["y"]
                self.canvas.move(block["rect"], exact_dx, exact_dy)
                self.canvas.move(block["text"], exact_dx, exact_dy)
                block["x"] = target_x
                block["y"] = target_y

                self.animations_running -= 1 
                if callback:
                    callback()
        step(0)

    def generate_data(self):
        filename = filedialog.asksaveasfilename(defaultextension=".bin", title="Lưu tệp mẫu")
        if filename:
            import random
            numbers = [round(random.uniform(1.0, 99.0), 1) for _ in range(12)]
            self.load_input_data(filename, numbers)

    def select_file(self):
        filename = filedialog.askopenfilename(filetypes=[("Binary files", "*.bin")])
        if filename:
            with open(filename, 'rb') as f:
                data = f.read()
                count = len(data) // FLOAT_SIZE
                numbers = list(struct.unpack(f"{count}{FLOAT_FORMAT}", data))
            self.load_input_data(filename, numbers)

    def input_manual_data(self):
        user_input = simpledialog.askstring("Nhập Dữ Liệu Thủ Công", 
            "Nhập các số thực cách nhau bởi dấu phẩy\nVD: 12.5, 3.1, 8.0, 44.2")
        if user_input:
            try:
                numbers = [float(x.strip()) for x in user_input.split(',')]
                if not numbers:
                    return
                filename = filedialog.asksaveasfilename(defaultextension=".bin", title="Lưu tệp dữ liệu vừa nhập")
                if filename:
                    self.load_input_data(filename, numbers)
            except ValueError:
                messagebox.showerror("Lỗi dữ liệu", "Vui lòng chỉ nhập các số thực hợp lệ, cách nhau bởi dấu phẩy")

    def load_input_data(self, filename, numbers):
        with open(filename, 'wb') as f:
            f.write(struct.pack(f"{len(numbers)}{FLOAT_FORMAT}", *numbers))
            
        self.input_file = filename
        self.draw_static_background()
        start_x = 40
        start_y = 60
        for i, val in enumerate(numbers):
            self.create_block(start_x + (i % 7)*60, start_y + (i // 7)*60, val)

        self.btn_out.config(state=tk.NORMAL)
        self.ui_status = f"Đã nạp {len(numbers)} phần tử. Vui lòng Chọn Nơi Lưu (Nút 2)"
        self.lbl_status.config(text=self.ui_status)

    def select_output(self):
        self.output_file = filedialog.asksaveasfilename(defaultextension=".bin", title="Lưu tệp kết quả")
        if self.output_file:
            self.btn_start.config(state=tk.NORMAL)
            self.ui_status = "Đã thiết lập đường dẫn lưu. Hãy nhấn Bắt Đầu (Nút 3)"
            self.lbl_status.config(text=self.ui_status)

    def start_simulation(self):
        self.btn_start.config(state=tk.DISABLED)
        self.btn_out.config(state=tk.DISABLED)
        self.btn_next.config(state=tk.NORMAL)
        self.btn_auto.config(state=tk.NORMAL)
        
        self.sort_generator = self.run_external_sort_algo()
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
        if not self.is_playing:
            return
        if self.animations_running > 0:
            self.root.after(50, self.play_next)
            return
        
        try:
            next(self.sort_generator)
            self.root.after(300, self.play_next)
        except StopIteration:
            self.finish_simulation()

    def next_step(self):
        if self.animations_running > 0:
            return
        try:
            next(self.sort_generator)
        except StopIteration:
            self.finish_simulation()

    def finish_simulation(self):
        self.is_playing = False
        self.btn_auto.config(state=tk.DISABLED, text="▶ Tự Động Chạy", bg="#f59e0b")
        self.btn_next.config(state=tk.DISABLED)
        self.ui_status = "HOÀN TẤT THUẬT TOÁN EXTERNAL MERGE SORT"
        self.lbl_status.config(text=self.ui_status)
        messagebox.showinfo("Thành công", f"File đã sắp xếp được lưu tại:\n{self.output_file}")

    def run_external_sort_algo(self):
        ram_slots_y = [90, 210, 330] 
        ram_start_x = 640
        
        disk_input_blocks = self.blocks.copy()
        run_blocks = []

        chunk_idx = 0
        while len(disk_input_blocks) > 0:
            current_chunk = []
            
            # CẬP NHẬT TRẠNG THÁI CHÍNH XÁC KHI BẮT ĐẦU ĐỌC
            self.lbl_status.config(text=f"BƯỚC 1: Đang nạp dữ liệu vào RAM để tạo Run {chunk_idx + 1}")
            
            for buffer_idx in range(3):
                for item_idx in range(2):
                    if len(disk_input_blocks) > 0:
                        blk = disk_input_blocks.pop(0)
                        current_chunk.append(blk)
                        target_x = ram_start_x + item_idx * 60
                        target_y = ram_slots_y[buffer_idx]
                        self.animate_move(blk, target_x, target_y)
                        yield 
            
            self.lbl_status.config(text=f"Đang sắp xếp các khối trong RAM (Run {chunk_idx + 1})")
            yield
            
            current_chunk.sort(key=lambda b: b["val"])
            
            for i, blk in enumerate(current_chunk):
                b_idx = i // 2
                i_idx = i % 2
                target_x = ram_start_x + i_idx * 60
                target_y = ram_slots_y[b_idx]
                self.animate_move(blk, target_x, target_y)
            yield

            self.lbl_status.config(text=f"Ghi Run {chunk_idx + 1} đã sắp xếp xuống Ổ Đĩa Tạm")
            yield
            
            for i, blk in enumerate(current_chunk):
                self.canvas.itemconfig(blk["rect"], fill="#d1d5db", outline="#9ca3af")
                target_x = 40 + (i % 7) * 60
                target_y = 270 + (chunk_idx * 60)
                self.animate_move(blk, target_x, target_y)
            yield
            
            run_blocks.append(current_chunk)
            chunk_idx += 1

        self.lbl_status.config(text="BƯỚC 2: Bắt đầu quá trình External Merge")
        yield

        f_out = open(self.output_file, 'wb')
        pass_number = 1

        while len(run_blocks) > 1:
            run1 = run_blocks.pop(0)
            run2 = run_blocks.pop(0)
            
            is_final_merge = (len(run_blocks) == 0) 
            
            out_buffer = []
            final_output = []
            buf1 = []
            buf2 = []

            def load_to_buffer(run_src, buf_dst, buffer_index):
                for _ in range(2):
                    if run_src:
                        blk = run_src.pop(0)
                        buf_dst.append(blk)
                        idx = len(buf_dst) - 1
                        self.animate_move(blk, ram_start_x + idx * 60, ram_slots_y[buffer_index])
            
            self.lbl_status.config(text=f"Nạp dữ liệu từ các Runs vào RAM (Pass {pass_number})")
            load_to_buffer(run1, buf1, 0)
            yield
            load_to_buffer(run2, buf2, 1)
            yield

            while buf1 or buf2:
                self.lbl_status.config(text=f"Đang so sánh hai khối nhỏ nhất (Pass {pass_number})")
                
                if not buf1:
                    chosen = buf2.pop(0)
                elif not buf2:
                    chosen = buf1.pop(0)
                elif buf1[0]["val"] < buf2[0]["val"]:
                    chosen = buf1.pop(0)
                else:
                    chosen = buf2.pop(0)

                out_buffer.append(chosen)
                idx = len(out_buffer) - 1
                self.canvas.itemconfig(chosen["rect"], fill="#fca5a5", outline="#ef4444")
                self.animate_move(chosen, ram_start_x + idx * 60, ram_slots_y[2])
                yield

                if len(out_buffer) == 2:
                    if is_final_merge:
                        self.lbl_status.config(text="Buffer 3 đầy, ghi kết quả xuống Tệp Kết Quả Cuối Cùng")
                        out_vals = [b["val"] for b in out_buffer]
                        f_out.write(struct.pack(f"{len(out_vals)}{FLOAT_FORMAT}", *out_vals))
                    else:
                        self.lbl_status.config(text="Buffer 3 đầy, xả dữ liệu xuống Ổ Đĩa Tạm")

                    for blk in out_buffer:
                        if is_final_merge:
                            self.canvas.itemconfig(blk["rect"], fill="#86efac", outline="#22c55e")
                            final_idx = len(final_output)
                            target_x = 40 + (final_idx % 18) * 60
                            target_y = 560 + (final_idx // 18) * 60
                        else:
                            self.canvas.itemconfig(blk["rect"], fill="#d1d5db", outline="#9ca3af")
                            final_idx = len(final_output)
                            target_x = 40 + (final_idx % 7) * 60
                            target_y = 270 + ((chunk_idx + pass_number) * 60)
                            
                        final_output.append(blk)
                        self.animate_move(blk, target_x, target_y)
                    out_buffer.clear()
                    yield

                if not buf1 and run1:
                    self.lbl_status.config(text="Buffer 1 trống, nạp thêm dữ liệu từ Run 1")
                    load_to_buffer(run1, buf1, 0)
                    yield

                if not buf2 and run2:
                    self.lbl_status.config(text="Buffer 2 trống, nạp thêm dữ liệu từ Run 2")
                    load_to_buffer(run2, buf2, 1)
                    yield

            if out_buffer:
                if is_final_merge:
                    self.lbl_status.config(text="Ghi phần dư cuối cùng xuống Tệp Kết Quả")
                    out_vals = [b["val"] for b in out_buffer]
                    f_out.write(struct.pack(f"{len(out_vals)}{FLOAT_FORMAT}", *out_vals))
                else:
                    self.lbl_status.config(text="Xả phần dư cuối cùng xuống Ổ Đĩa Tạm")

                for blk in out_buffer:
                    if is_final_merge:
                        self.canvas.itemconfig(blk["rect"], fill="#86efac", outline="#22c55e")
                        final_idx = len(final_output)
                        target_x = 40 + (final_idx % 18) * 60
                        target_y = 560 + (final_idx // 18) * 60
                    else:
                        self.canvas.itemconfig(blk["rect"], fill="#d1d5db", outline="#9ca3af")
                        final_idx = len(final_output)
                        target_x = 40 + (final_idx % 7) * 60
                        target_y = 270 + ((chunk_idx + pass_number) * 60)
                        
                    final_output.append(blk)
                    self.animate_move(blk, target_x, target_y)
                out_buffer.clear()
                yield
            
            if not is_final_merge:
                run_blocks.append(final_output)
                pass_number += 1

        f_out.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = ExternalSortSmoothVisualizer(root)
    root.mainloop()