# 🔍 Trình Mô Phỏng Chi Tiết Thuật Toán Rabin-Karp

Dự án này là một ứng dụng Desktop tương tác được xây dựng bằng Python và thư viện `Tkinter`. Mục tiêu của dự án là giúp người dùng hình dung một cách trực quan, sinh động từng bước tính toán bên trong thuật toán tìm kiếm chuỗi con **Rabin-Karp**, đặc biệt là quá trình băm đa thức (Polynomial Rolling Hash).

## 🚀 Các Tính Năng Nổi Bật

* **🎨 Giao Diện Trực Quan (GUI):** Hiển thị rõ ràng Văn Bản (Text) và Mẫu (Pattern) dưới dạng các khối màu (blocks). Khung cửa sổ trượt (sliding window) sẽ di chuyển trên màn hình theo thời gian thực.
* **🔢 Đánh Dấu Chỉ Số (Index):** Tự động vẽ các chỉ số $0, 1, 2, ...$ phía trên từng ký tự để người học dễ dàng đối chiếu với các biến lặp `i`, `j` trong mã nguồn.
* **🧮 Bảng Tính Toán Trực Tiếp:** Hiển thị chi tiết từng phương trình toán học đang được thực thi ngầm:
  * Cách tính $RM = R^{(M-1)} \pmod Q$.
  * Cách tính giá trị băm ban đầu bằng phương pháp Horner.
  * Minh họa cụ thể công thức cập nhật băm $H_{new} = ((H_{old} - c_{old} \times RM) \times R + c_{new}) \pmod Q$ với các giá trị ASCII tại từng bước trượt.
* **🕵️ Xử Lý Đụng Độ Băm (Spurious Hit):** Bôi đỏ và làm chậm quá trình đối sánh từng ký tự khi phát hiện giá trị băm khớp nhau nhằm xác minh chéo kết quả.
* **📜 Lịch Sử Giao Dịch (Logs):** Tích hợp một thanh cuộn (scrollbar) ghi lại toàn bộ lịch sử các phép tính băm, vị trí cửa sổ và kết luận của từng bước.
* **▶️ Điều Khiển Linh Hoạt:** Cho phép người dùng lựa chọn:
  * Xem từng bước một (Next Step).
  * Chạy tự động (Auto Play).
  * Tùy ý nhập văn bản và mẫu tìm kiếm thủ công (Manual Input).

## ⚙️ Cài Đặt Tham Số Băm Mặc Định

Trong đoạn mã hiện tại, thuật toán sử dụng các tham số tối ưu sau:
* **Cơ số (Radix - $R$):** `311` (Sử dụng số nguyên tố để tối ưu phân bổ băm cho không gian chuỗi mở rộng, đặc biệt hữu ích khi đối sánh chuỗi có dấu như Tiếng Việt).
* **Số Modulo ($Q$):** `997` (Số nguyên tố dùng để tránh tràn bộ nhớ máy tính).

## 🛠️ Hướng Dẫn Cài Đặt & Chạy Ứng Dụng

Ứng dụng chỉ sử dụng các thư viện chuẩn tích hợp sẵn của Python, do đó bạn không cần phải cài đặt thêm các gói `pip` bên ngoài.

### Yêu cầu hệ thống:
* Đã cài đặt **Python 3.x**.

### Các bước chạy:
1. Tải (Clone) dự án này về máy tính.
2. Mở Terminal (hoặc Command Prompt) tại thư mục chứa file mã nguồn (VD: `lab2.py`).
3. Chạy lệnh thực thi:
   ```bash
   python lab2.py
