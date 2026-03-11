# 🔍 Trình Mô Phỏng Thuật Toán Rabin-Karp (Rabin-Karp Visualizer)

Dự án này là một ứng dụng Desktop được xây dựng bằng Python và Tkinter, nhằm mục đích mô phỏng trực quan quá trình hoạt động của thuật toán **Tìm kiếm chuỗi con Rabin-Karp**. Ứng dụng giúp người dùng dễ dàng quan sát cách cửa sổ trượt (sliding window) di chuyển, phương pháp tính toán băm đa thức (Polynomial Rolling Hash) và cách hệ thống xử lý khi xảy ra hiện tượng đụng độ băm (Spurious Hit).

## 🚀 Demo Hoạt Động

Bạn có thể xem video quay lại toàn bộ quá trình chạy thực tế của ứng dụng tại liên kết dưới đây: 
👉 [**Xem Clip Chạy Demo Thuật Toán**](https://drive.google.com/drive/folders/1J45N5SkTkQRmMqDO62C61tBzzmasUOeS?usp=drive_link)

## 📁 Tài Liệu Tham Khảo

Dự án được nghiên cứu, phát triển cơ sở lý thuyết và tham khảo ý tưởng triển khai từ các nguồn tài liệu sau:
* **Rabin-Karp Algorithm Visually Explained:** [YouTube (ByteQuest)](https://youtu.be/yFHV7weZ_as?si=wDUbNWujGCsN2Gj7)
* **KMP Algorithm Visually Explained:** [YouTube](https://youtu.be/JoF0Z7nVSrA?si=5ZgPSiRhKVxRVyRm)
* **Boyer-Moore Algorithm Visually Explained:** [YouTube](https://youtu.be/PHXAOKQk2dw?si=BZOQMhUto2FfUhy2)

## ✨ Tính Năng Nổi Bật

* **Minh họa đồ họa chuyển động:** Khung cửa sổ trượt di chuyển mượt mà qua từng ký tự của văn bản với các khối màu (blocks) được đánh chỉ số (index) rõ ràng.
* **Bảng tính toán thời gian thực (Real-time Math):** Tự động hiển thị chi tiết các bước tính giá trị băm ban đầu bằng phương pháp Horner và công thức cập nhật Rolling Hash ($H_{new}$).
* **Cơ chế chống đụng độ (Spurious Hit):** Giao diện tự động bôi đỏ và chạy chậm lại để so sánh đối chiếu từng ký tự một khi phát hiện mã băm của cửa sổ khớp với mã băm của mẫu tìm kiếm.
* **Ghi vết hệ thống (Logs):** Tích hợp khung lưu lịch sử hoạt động có thanh cuộn, giúp người dùng xem lại toàn bộ các phép tính toán học và kết luận ở từng bước trượt.
* **Kiểm soát linh hoạt tiến trình:** Người dùng có thể tùy chọn chế độ chạy từng bước để phân tích kỹ thuật, hoặc bật tự động chạy để quan sát tổng quan luồng đi của thuật toán.

## ⚙️ Yêu Cầu Hệ Thống & Cài Đặt

Ứng dụng sử dụng hoàn toàn các thư viện chuẩn tích hợp sẵn của Python, không yêu cầu người dùng phải cài đặt thêm bất kỳ gói thư viện nào bên ngoài.
* Đảm bảo máy tính đã cài đặt **Python 3.x**.
* Clone repository này về thiết bị của bạn:
  ```bash
  git clone [https://github.com/bayvai20kg/DSA_Advanced.git](https://github.com/bayvai20kg/DSA_Advanced.git)
