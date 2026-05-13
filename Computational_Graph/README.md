# Dự đoán điểm cuối kỳ với Đồ thị tính toán (Computational Graph)

Đây là bài tập cho môn học **CS523.Q21 - Cấu trúc dữ liệu và giải thuật nâng cao**. Bài tập2 xây dựng một mô hình Hồi quy tuyến tính (Linear Regression) nhằm dự đoán điểm thi cuối kỳ dựa trên điểm giữa kỳ của sinh viên.

Điểm đặc biệt của dự án này là **không sử dụng** các thư viện học máy bậc cao có sẵn như PyTorch hay Scikit-learn. Thay vào đó, toàn bộ cơ chế **Tự động tính đạo hàm (AutoGrad)** và **Lan truyền ngược (Backpropagation)** được xây dựng hoàn toàn thủ công từ con số không (from scratch) thông qua một Engine Đồ thị tính toán tự tùy chỉnh.

## 🚀 Tính năng nổi bật

* **Engine AutoGrad tự xây dựng**: Triển khai lớp `Value` hỗ trợ các phép toán cơ bản, tự động theo dõi cấu trúc đồ thị tính toán để thực hiện Forward Pass và Backward Pass.
* **Huấn luyện mô hình**: Áp dụng thuật toán Gradient Descent để tối ưu hóa trọng số $W$ và độ lệch $b$.
* **Giao diện web trực quan**: Sử dụng nền tảng Streamlit để tạo giao diện tương tác, cho phép người dùng tải lên tập dữ liệu, cấu hình siêu tham số và thực hiện dự đoán theo thời gian thực.
* **Trực quan hóa sinh động**: Hệ thống tự động xuất các biểu đồ minh họa bao gồm đồ thị phân tán, đường thẳng hồi quy, đường cong hàm mất mát (Loss curve) và sơ đồ mạng lưới của đồ thị tính toán.

## 📁 Cấu trúc thư mục

* `app.py`: Mã nguồn xử lý giao diện người dùng (Frontend) được thiết kế bằng thư viện Streamlit.
* `backend.py`: Lõi toán học (Backend) chứa định nghĩa lớp `Value`, các hàm huấn luyện mô hình và module vẽ biểu đồ.
* `TRAIN2.xlsx`: Tập dữ liệu mẫu bao gồm thông tin điểm giữa kỳ và cuối kỳ dùng để huấn luyện.
* `Bao_Cao_LaTeX.pdf`: Bản thuyết minh chi tiết về thuật toán, kiến trúc hệ thống và kết quả đạt được.

## ⚙️ Cài đặt và Khởi chạy

**Bước 1:** Clone kho lưu trữ về máy:
```bash'
git clone [https://github.com/bayvai20kg/DSA_Advanced.git](https://github.com/bayvai20kg/DSA_Advanced.git)```

**Bước 2:** Di chuyển vào thư mục Lab3:
```bash
cd DSA_Advanced/Computational_Graph
```

**Bước 3:** Chạy file để mở ứng dụng:
```bash
streamlit run app.py
python app.py
python gui.py
```
