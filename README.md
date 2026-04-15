# Lab 4: Hệ Thống Từ Điển Tiếng Anh Bằng Cấu Trúc Dữ Liệu Radix Trie

**Thông tin sinh viên:**
* **Họ và tên:** Vũ Gia Khang
* **MSSV:** 23520713

## 1. Giới thiệu 
Đây là ứng dụng quản lý từ điển tiếng Anh cho phép tra cứu, thêm và xóa từ vựng. Điểm nổi bật của dự án là việc tự cài đặt và ứng dụng cấu trúc dữ liệu **Radix Trie (Patricia Trie)** làm chỉ mục. Hệ thống không chỉ giúp tối ưu hóa không gian lưu trữ (bằng cách nén các node chỉ có 1 nhánh) và tốc độ tra cứu, mà còn trực quan hóa quá trình biến đổi, phân tách (split) và gộp (merge) các node của cây mỗi khi có thao tác thêm hoặc xóa dữ liệu.

## 2. Tính năng nổi bật
* **Thêm từ vựng:** Nhập từ và định nghĩa mới vào hệ thống. Thuật toán sẽ tự động tìm tiền tố chung và xử lý tách nhánh (split node) nếu cần.
* **Tìm kiếm siêu tốc:** Sử dụng cây Radix Trie để tìm kiếm nghĩa của từ với độ phức tạp cực thấp O(m) (với m là độ dài của từ).
* **Xóa từ vựng:** Gỡ bỏ từ và tự động tái cấu trúc lại Radix Trie (gộp các node - merge node) để duy trì trạng thái nén tối ưu.
* **Trực quan hóa cấu trúc (Visualization):** Xuất sơ đồ cấu trúc cây Radix Trie dưới dạng phân cấp thư mục (text console) để dễ dàng theo dõi sự thay đổi dữ liệu sau mỗi thao tác.

## 3. Cấu trúc thư mục mã nguồn
* `radix_trie.py`: Cài đặt lõi thuật toán cấu trúc dữ liệu cây Radix Trie (chèn, tìm kiếm, xóa, tách/gộp node, xuất cấu trúc).
* `app_streamlit.py`: Lớp giao diện Web Dashboard hiện đại được thiết kế bằng thư viện Streamlit.
* `app.py`: Phiên bản ứng dụng chạy trên giao diện dòng lệnh (Terminal/CLI).
* `gui.py`: Phiên bản ứng dụng với giao diện đồ họa cục bộ dùng thư viện Tkinter.
* `dictionary_data.json`: File lưu trữ dữ liệu gốc của từ điển (hệ thống tự động tạo và cập nhật).

## 4. Hướng dẫn cài đặt và khởi chạy
Dự án cung cấp nhiều phiên bản giao diện. Nếu sử dụng bản Web, bạn cần cài đặt thêm thư viện `streamlit`.

**Bước 1:** Clone kho lưu trữ về máy:
```bash
git clone [https://github.com/bayvai20kg/DSA_Advanced.git](https://github.com/bayvai20kg/DSA_Advanced.git)
