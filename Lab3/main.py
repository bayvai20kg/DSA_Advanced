import tkinter as tk
from interface import StudentAppGUI

def main():
    # Khởi tạo cửa sổ gốc của Tkinter
    root = tk.Tk()
    
    # Khởi tạo giao diện ứng dụng quản lý sinh viên
    app = StudentAppGUI(root)
    
    # Chạy vòng lặp sự kiện chính
    root.mainloop()

if __name__ == "__main__":
    main()
