# 📊 Trình Mô Phỏng Sắp Xếp Ngoại (External Merge Sort Visualizer)

Dự án này là một ứng dụng Desktop được xây dựng bằng Python và Tkinter, nhằm mục đích mô phỏng trực quan quá trình hoạt động của thuật toán **Sắp xếp Ngoại (External Merge Sort)**. Ứng dụng giúp người dùng dễ dàng quan sát cách dữ liệu được chia nhỏ, nạp vào bộ nhớ trong (RAM) và trộn lại thông qua các tệp tạm thời trên ổ đĩa cứng.

## 🚀 Demo Hoạt Động
Bạn có thể xem video quay lại toàn bộ quá trình chạy thực tế của ứng dụng tại liên kết Google Drive dưới đây:
[**👉 Xem Clip Chạy Demo Thuật Toán**](https://drive.google.com/drive/folders/1uEkc6MV-IUjiuyLt2LldXxagWJXkkJ_k?usp=drive_link)

## 📁 Tài Liệu Tham Khảo
Dự án được nghiên cứu, phát triển cơ sở lý thuyết và tham khảo ý tưởng triển khai từ các nguồn tài liệu sau:
* **Giao diện tham khảo (React/Framer Motion):** [valeriodiste/ExternalMergeSortVisualizer](https://github.com/valeriodiste/ExternalMergeSortVisualizer)
* **Lý thuyết nền tảng (GeeksforGeeks):** [External Sorting in Data Structures](https://www.geeksforgeeks.org/dsa/external-sorting/)
* **Thảo luận thuật toán (StackOverflow):** [Concept of External Sorting](https://stackoverflow.com/questions/5100252/external-sorting)
* **Mã nguồn tham khảo (Java):** [marcel-dias/java-external-sorting](https://github.com/marcel-dias/java-external-sorting)
* **Bài giảng học thuật (Đại học Tennessee):** [External Sorting Notes](https://web.archive.org/web/20110504141851/http://web.eecs.utk.edu/%7Ehuangj/CS302S04/notes/external-sorting2.html)

## ✨ Tính Năng Nổi Bật
* **Minh họa đồ họa chuyển động:** Sử dụng kỹ thuật Canvas Animation để các khối dữ liệu (blocks) di chuyển giữa Ổ đĩa (Disk) và Bộ nhớ (RAM) một cách mượt mà.
* **Đa dạng nguồn nạp dữ liệu:**
  * Sinh tệp dữ liệu số thực ngẫu nhiên.
  * Hỗ trợ nhập dãy số thủ công bằng tay.
  * Đọc dữ liệu trực tiếp từ tệp nhị phân (`.bin`) có sẵn.
* **Kiểm soát linh hoạt tiến trình:** Người dùng có thể tùy chọn chế độ chạy từng bước để phân tích kỹ thuật, hoặc bật tự động chạy để quan sát tổng quan luồng đi của dữ liệu.

## ⚙️ Yêu Cầu Hệ Thống & Cài Đặt
Ứng dụng sử dụng hoàn toàn các thư viện chuẩn tích hợp sẵn của Python, không yêu cầu người dùng phải cài đặt thêm bất kỳ gói thư viện nào bên ngoài.

1. Đảm bảo máy tính đã cài đặt **Python 3.x**.
2. Clone repository này về thiết bị của bạn:
   ```bash
   git clone [https://github.com/bayvai20kg/DSA_Advanced.git](https://github.com/bayvai20kg/DSA_Advanced.git)
