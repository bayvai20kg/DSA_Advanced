# 📖 Từ Điển Tiếng Anh - Radix Trie (DSA++ Lab)

Đây là kho lưu trữ mã nguồn cho bài tập thực hành môn Cấu trúc Dữ liệu và Giải thuật Nâng cao (DSA++), Trường Đại học Công nghệ Thông tin (UIT). Dự án mô phỏng một ứng dụng từ điển tiếng Anh sử dụng cấu trúc dữ liệu cốt lõi là **Radix Trie** (Patricia Trie) để tối ưu hóa không gian lưu trữ và tốc độ tìm kiếm.

## ✨ Tính năng chính
* **Tra cứu từ vựng:** Tìm kiếm định nghĩa với độ phức tạp $O(m)$ (với $m$ là độ dài của từ).
* **Thêm / Cập nhật:** Thêm từ mới hoặc cập nhật định nghĩa. Thuật toán tự động tách nhánh (split) để tối ưu cây.
* **Xóa từ:** Gỡ bỏ từ khỏi hệ thống, tự động gộp các node (merge) để duy trì trạng thái nén.
* **Trực quan hóa:** Hiển thị toàn bộ cấu trúc cây Radix Trie dưới dạng thư mục để dễ dàng quan sát sự biến đổi dữ liệu sau các thao tác.

## 🚀 Giao diện hỗ trợ
Dự án được triển khai với 3 phiên bản giao diện để linh hoạt sử dụng:
1.  **Giao diện dòng lệnh (CLI):** Chạy trực tiếp qua Terminal với menu điều hướng nhanh gọn.
2.  **Giao diện Tkinter:** Cửa sổ đồ họa cục bộ sử dụng thư viện GUI tiêu chuẩn của Python.
3.  **Giao diện Streamlit:** Web Dashboard hiện đại, hỗ trợ trực quan hóa thẻ HTML và hiệu ứng tương tác (Khuyên dùng).

## ⚙️ Hướng dẫn cài đặt và chạy ứng dụng

**Yêu cầu hệ thống:** Máy tính đã cài đặt Python 3.8 trở lên.

**Bước 1:** Clone repository về máy và di chuyển vào thư mục dự án:
```bash
git clone [https://github.com/bayvai20kg/DSA_Advanced.git](https://github.com/bayvai20kg/DSA_Advanced.git)
cd DSA_Advanced/Lab4
