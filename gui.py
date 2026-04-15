import tkinter as tk
from tkinter import messagebox, scrolledtext
import json
import os
from radix_trie import RadixTrie

DATA_FILE = "dictionary_data.json"

class DictionaryGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Từ Điển Tiếng Anh - Radix Trie")
        self.root.geometry("600x500")

        # --- MODEL: Khởi tạo dữ liệu cốt lõi ---
        self.trie = RadixTrie()
        self.load_data()

        # --- VIEW: Thiết kế bố cục giao diện ---
        # 1. Khu vực Nhập liệu (Inputs)
        input_frame = tk.Frame(root)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Từ (Word):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.word_entry = tk.Entry(input_frame, width=30)
        self.word_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Nghĩa (Definition):").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.def_entry = tk.Entry(input_frame, width=30)
        self.def_entry.grid(row=1, column=1, padx=5, pady=5)

        # 2. Khu vực Nút bấm (Buttons)
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Thêm / Cập nhật", command=self.handle_add, width=15, bg="#d4edda").grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Tìm kiếm", command=self.handle_search, width=15, bg="#cce5ff").grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Xóa", command=self.handle_delete, width=15, bg="#f8d7da").grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Hiển thị cây (Log)", command=self.handle_visualize, width=15).grid(row=0, column=3, padx=5)

        # 3. Khu vực Hiển thị kết quả (Console Log)
        self.log_area = scrolledtext.ScrolledText(root, width=70, height=20, font=("Consolas", 10))
        self.log_area.pack(pady=10)
        self.log("Hệ thống sẵn sàng. Vui lòng nhập từ để thao tác.")

    # --- CONTROLLER: Luồng xử lý sự kiện ---
    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            for word, definition in data.items():
                self.trie.insert(word, definition)

    def save_data(self):
        data = {word: definition for word, definition in self.trie.all_words()}
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def log(self, message):
        """Hàm hỗ trợ in chữ vào khung hiển thị (giống print trong CLI)"""
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END) # Tự động cuộn xuống dòng mới nhất

    def handle_add(self):
        word = self.word_entry.get().strip()
        definition = self.def_entry.get().strip()
        
        if not word or not definition:
            messagebox.showwarning("Lỗi nhập liệu", "Vui lòng nhập cả từ và nghĩa!")
            return

        is_new = self.trie.insert(word, definition)
        self.save_data()
        
        if is_new:
            self.log(f"✔ Đã thêm từ mới: '{word}' -> {definition}")
        else:
            self.log(f"ℹ Đã cập nhật nghĩa từ: '{word}' -> {definition}")
            
        self.word_entry.delete(0, tk.END)
        self.def_entry.delete(0, tk.END)

    def handle_search(self):
        word = self.word_entry.get().strip()
        if not word:
            return

        definition = self.trie.search(word)
        self.log("-" * 40)
        if definition:
            self.log(f"✔ TÌM THẤY: '{word}'")
            self.log(f"   Nghĩa: {definition}")
        else:
            self.log(f"✘ Không tìm thấy từ '{word}'.")

    def handle_delete(self):
        word = self.word_entry.get().strip()
        if not word:
            return

        if self.trie.search(word) is None:
            self.log(f"✘ Từ '{word}' không tồn tại để xóa.")
            return

        self.trie.delete(word)
        self.save_data()
        self.log(f"✔ Đã xóa từ '{word}' thành công.")
        self.word_entry.delete(0, tk.END)

    def handle_visualize(self):
        self.log("\n--- CẤU TRÚC RADIX TRIE HIỆN TẠI ---")
        tree_str = self.trie.visualize()
        self.log(tree_str)


# Chạy ứng dụng
if __name__ == "__main__":
    root = tk.Tk()
    app = DictionaryGUI(root)
    root.mainloop()