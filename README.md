# 🎓 Hệ thống Dự đoán Tình trạng Sinh viên

Ứng dụng web cho phép dự đoán tình trạng học tập sinh viên (Cảnh báo/An toàn) dựa trên điểm số các môn học sử dụng Machine Learning.

## ✨ Tính năng

- 🖥️ Giao diện web hiện đại và responsive
- 📊 Nhập điểm 16 môn học (TBLANG, TBMATH, TBCT, TMKNM, TBLT, M17-M47)
- 🤖 Dự đoán tình trạng học tập (0: Cảnh báo, 1: An toàn) bằng ML model
- ✅ Validation dữ liệu đầu vào
- 🔄 API RESTful backend

## 🛠️ Cài đặt

### 1. Clone repository
```bash
git clone <repository-url>
cd trang
```

### 2. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 3. Chuẩn bị model
- Đặt file `model.pkl` vào thư mục gốc
- Hoặc ứng dụng sẽ tự tạo dummy model để test

### 4. Chạy ứng dụng
```bash
python app.py
```

## 🌐 Sử dụng

1. Mở trình duyệt và truy cập: `http://localhost:5000`
2. Nhập điểm các môn học (0-10)
3. Nhấn "Dự đoán Tình trạng"
4. Xem kết quả dự đoán (Cảnh báo hoặc An toàn)

## 📁 Cấu trúc file

```
trang/
├── index.html          # Giao diện chính
├── style.css           # CSS styling
├── script.js           # JavaScript logic
├── app.py              # Flask backend
├── requirements.txt    # Python dependencies
├── model.pkl           # ML model (cần cung cấp)
└── README.md           # Hướng dẫn này
```

## 🔧 API Endpoints

### POST /predict
Dự đoán tình trạng học tập dựa trên điểm số

**Request:**
```json
{
  "TBLANG": 8.0,
  "TBMATH": 7.5,
  "TBCT": 8.2,
  "TMKNM": 7.8,
  "TBLT": 8.1,
  "M17": 7.9,
  "M19": 8.0,
  "M22": 7.7,
  "M30": 8.3,
  "M32": 7.6,
  "M33": 8.2,
  "M36": 7.8,
  "M41": 8.1,
  "M44": 7.9,
  "M45": 8.0,
  "M47": 7.7
}
```

**Response:**
```json
{
  "prediction": "✅ An toàn",
  "raw_prediction": 1,
  "confidence": {
    "Cảnh báo": 0.2,
    "An toàn": 0.8
  }
}
```

### GET /health
Kiểm tra trạng thái hệ thống

## 🎯 Các môn học được hỗ trợ

### Môn cơ bản:
- **TBLANG**: Điểm trung bình các môn Tiếng Anh
- **TBMATH**: Điểm trung bình các môn Toán
- **TBCT**: Điểm trung bình các môn Chính trị
- **TMKNM**: Điểm trung bình các môn Kỹ năng mềm
- **TBLT**: Điểm trung bình các môn Lập trình

### Môn chuyên ngành:
- **M17**: Nhập môn tin học
- **M19**: Vật lý đại cương
- **M22**: Cơ sở dữ liệu
- **M30**: Kiến trúc máy tính
- **M32**: Hệ quản trị cơ sở dữ liệu
- **M33**: Mạng máy tính
- **M36**: Nguyên lý hệ điều hành
- **M41**: Phân tích thiết kế hệ thống thông tin
- **M44**: Cơ sở lập trình web
- **M45**: Nhập môn an toàn và bảo mật thông tin
- **M47**: Phân tích thiết kế hướng đối tượng

## 🔍 Kết quả dự đoán

- **0 - ⚠️ Cảnh báo**: Sinh viên có nguy cơ học tập kém, cần hỗ trợ
- **1 - ✅ An toàn**: Sinh viên có kết quả học tập ổn định

*Model sẽ dự đoán dựa trên điểm trung bình các môn học*

## ⚙️ Yêu cầu hệ thống

- Python 3.7+
- Flask 2.3+
- scikit-learn 1.3+
- Trình duyệt web hiện đại

## 🐛 Troubleshooting

### Model không tải được
- Kiểm tra file `model.pkl` có tồn tại
- Đảm bảo model được train với đúng 16 features
- Xem log console để biết chi tiết lỗi

### Lỗi CORS
- Flask-CORS đã được cấu hình
- Kiểm tra firewall/antivirus

### Port đã được sử dụng
- Thay đổi port trong `app.py`: `app.run(port=5001)`

## 📝 Ghi chú

- Ứng dụng sử dụng dummy model nếu không tìm thấy `model.pkl`
- Trong môi trường development, có nút "Fill Sample Data" để test
- Keyboard shortcuts: Ctrl+Enter (submit), Ctrl+R (clear)

## 🤝 Đóng góp

1. Fork repository
2. Tạo feature branch
3. Commit changes
4. Push và tạo Pull Request

## 📄 License

MIT License - xem file LICENSE để biết chi tiết. 