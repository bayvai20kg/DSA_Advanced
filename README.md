# Lab 3: Hệ Thống Quản Lý Sinh Viên Bằng Cấu Trúc Dữ Liệu B-Tree

**Thông tin sinh viên:**
* **Họ và tên:** Vũ Gia Khang
* **MSSV:** 23520713

## 1. Giới thiệu dự án
Đây là ứng dụng quản lý hồ sơ sinh viên với giao diện đồ họa (GUI) được viết bằng Python. Điểm nổi bật của dự án là việc tự cài đặt và ứng dụng cấu trúc dữ liệu **B-Tree (Bậc 3)** làm chỉ mục (Index) cho Mã Sinh Viên. Hệ thống không chỉ giúp tối ưu hóa thời gian tìm kiếm mà còn trực quan hóa quá trình biến đổi, phân tách (split) và gộp (merge) các node của cây B-Tree mỗi khi có thao tác thêm hoặc xóa dữ liệu.

## 2. Tính năng nổi bật
* **Thêm sinh viên:** Nhập thông tin sinh viên và lưu vào bảng dữ liệu gốc, đồng thời cập nhật khóa vào cây B-Tree. Có xử lý bắt lỗi trùng Mã SV.
* **Tìm kiếm siêu tốc:** Sử dụng cây B-Tree để tìm kiếm sinh viên theo Mã SV với độ phức tạp $O(\log n)$.
* **Xóa sinh viên:** Xóa dữ liệu và tự động tái cấu trúc lại B-Tree (mượn node anh em hoặc gộp node) nếu vi phạm số lượng khóa tối thiểu.
* **Trực quan hóa cấu trúc (Visualization):** Màn hình được chia đôi, hiển thị đồng thời Bảng dữ liệu gốc và sơ đồ cấu trúc cây B-Tree (hiển thị dưới dạng text console) theo thời gian thực.

## 3. Cấu trúc thư mục mã nguồn
* `student.py`: Định nghĩa lớp (class) `Student` chứa thông tin của một sinh viên (Mã SV, Họ tên, Giới tính, Năm sinh, Quê quán).
* `btree.py`: Cài đặt lõi thuật toán cấu trúc dữ liệu cây đa nhánh B-Tree bậc 3 (chèn, tìm kiếm, phân tách node, xuất cấu trúc text).
* `manager.py`: Lớp nghiệp vụ `StudentManager` làm cầu nối xử lý logic giữa giao diện và cấu trúc dữ liệu B-Tree.
* `interface.py` (hoặc `gui.py`): Thiết kế toàn bộ giao diện người dùng bằng thư viện Tkinter.
* `main.py`: File gốc dùng để khởi chạy toàn bộ ứng dụng.

## 4. Hướng dẫn cài đặt và khởi chạy
Dự án sử dụng thư viện `tkinter` mặc định của Python nên không cần cài đặt thêm bất kỳ thư viện bên thứ ba nào.

**Bước 1:** Clone kho lưu trữ về máy:
```bash
git clone [https://github.com/bayvai20kg/DSA_Advanced.git](https://github.com/bayvai20kg/DSA_Advanced.git)


**Bước 1:** Clone kho lưu trữ về máy:
```bash
git clone [https://github.com/bayvai20kg/DSA_Advanced.git](https://github.com/bayvai20kg/DSA_Advanced.git)
**Bước 2:** Di chuyển vào thư mục Lab3:
```bash
cd DSA_Advanced/Lab3
**Bước 3:** Chạy file main.py để mở ứng dụng:
```bash
python main.py
