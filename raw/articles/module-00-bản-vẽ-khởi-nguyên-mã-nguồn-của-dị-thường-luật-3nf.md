---
title: "Module 00: Bản Vẽ Khởi Nguyên - Mã Nguồn Của Dị Thường & Luật 3NF"
source: "D:\9. Learn\12. llm wiki\raw\articles\ora\0.md"
date_added: 2026-04-23
tags: [notes]
status: draft
summary: ""
---

# Module 00: Bản Vẽ Khởi Nguyên - Mã Nguồn Của Dị Thường & Luật 3NF

## 1. Dẫn Nhập: Trước Khi Xây Lò Phản Ứng

Ở các phần sau của hành trình Pháo Đài Tài Chính, bạn sẽ được thấy Oracle thao túng dữ liệu kinh khủng thế nào với *ACID, RAC Server* hay *CBO Optimizer*. Nhưng sự thật là: Dù lò phản ứng của bạn có chạy bằng năng lượng mặt trời đi nữa, nếu **Bản Vẽ Thiết Kế** của bạn chứa đầy lỗi nứt móng, thứ duy nhất bạn tăng tốc là sự sụp đổ.

Trong Data Modeling (Mô Hình Hóa Dữ Liệu), thiết kế bảng tồi không chỉ tốn dung lượng ổ cứng. Nó trực tiếp sinh ra các **Dị Thường Dữ Liệu (Anomalies)** — những con virus lặng lẽ tàn phá tính toàn vẹn của ngân hàng trước cả khi hacker kịp đụng tay vào.

---

## 2. Bóng Ma Dị Thường (Modification Anomalies)

Thiết kế bảng kiểu "gom hết mọi thứ vào một nơi cho dễ đọc" (phẳng / flat files) chính là nguyên nhân sinh ra dị thường. Cụ thể:

1.  **Dị thường Chèn (Insertion Anomaly):** Giả sử bảng `KHOA_HOC` chứa cả thông tin `Mã Giảng Viên` làm khóa chính. Khi bạn tuyển một Giảng viên mới nhưng họ chưa được xếp lớp nào — hệ thống sập! Bạn không thể `INSERT` thông tin giảng viên vì thiếu ID của khóa học. Dữ liệu mồ côi bị từ chối ngay từ cửa.
2.  **Dị thường Cập nhật (Update Anomaly):** Nếu giảng viên A dạy 100 học viên, tên và số điện thoại của thầy A lưu lặp lại 100 lần. Một ngày thầy A đổi số điện thoại, hệ thống phải quét và Update 100 dòng. Mất điện ở dòng thứ 50? Chúc mừng, hệ thống của bạn vĩnh viễn mất tính nhất quán.
3.  **Dị thường Xóa (Deletion Anomaly):** Khi học viên duy nhất của khóa học nhấn nút "Hủy đăng ký", dòng dữ liệu bị xóa bỏ. Hậu quả là thông tin về chính bản thân khóa học đó cũng bốc hơi khỏi lịch sử ngân hàng dữ liệu.

*Chuẩn Nguồn Khởi Nguyên (Normalization)* chính là vắc-xin triệt tiêu 3 con quỷ này.

---

## 3. Bộ Luật Chuẩn Hóa Pháo Đài (1NF - 3NF)

Để xây lên Pháo Đài, các Kiến trúc sư phân tách dữ liệu thô qua 3 bộ lưới lọc cốt lõi:

### 🔹 Lọc 1NF: Trảm Quân Đoàn Đa Biến (Atomicity)
**Định luật:** Mọi dữ liệu tại 1 ô phải là hạt nhân Đơn Nguyên (Atomic) - Tuyệt đối không chứa mảng phân cách bằng dấu phẩy.
*   *Lỗi chết người:* Để chung cột `KyNang: Java, SQL, Python`. Khi tìm ai biết SQL, thay vì xài Index siêu tốc, DB phải xài `LIKE '%SQL%'` và thực hiện quét càn (Full Table Scan) nguyên cái kho dữ liệu.
*   *Chế Tài:* Chia nhỏ từng kỹ năng thành đa dòng, hoặc đệ quy thành một bảng con. Mọi giá trị phải "Một và Chỉ Một".

### 🔹 Lọc 2NF: Cắt Bỏ Phần Thừa Của Khóa Kép
Chỉ áp dụng khi bạn ghép 2 cột lại để làm Khóa Chính (Composite Key).
*   *Định luật:* Thuộc tính phụ phải phụ thuộc vào TẤT CẢ các thành phần của khóa.
*   *Giải phẫu:* Bảng `ChiTietDonHang (MaDon, MaSP)`. Cột `TenSP` thì lại chỉ ăn theo `MaSP` chứ không ăn theo `MaDon`. Hãy ném `TenSP` ra một Kho riêng tên là `Kho_SP`. 

### 🔹 Lọc 3NF: Đoạn Tuyệt Phụ Thuộc Bắc Cầu
*   **Tuyên ngôn:** *"Mọi cột thông tin phải phụ thuộc vào Khóa, TOÀN BỘ Khóa, và KHÔNG GÌ KHÁC ngoài Khóa!"*
*   *Giải phẫu:* Bảng `DonHang` có `MaDon -> MaKhachHang -> ThanhPhoKHACH`. Thành phố không phụ thuộc trực tiếp vào Đơn hàng mà phụ thuộc bắc cầu qua Khách! Do đó, mang Khách ra một bảng riêng!

**Kết quả của 3NF:** Mỗi một Table chỉ mô tả ĐÚNG một và CHỈ MỘT Thực thể (Entity) duy nhất. Sự kiện đi đường sự kiện, Chủ thể đi đường chủ thể. Bẻ gãy các trói buộc rác.

---

## 4. Áo Giáp Vật Lý Đóng Nền (Oracle Constraints)

Lý thuyết trên giấy chỉ sống được khi ép thành mã DDL vật lý. Làm Architect trên Oracle, bạn phải nhớ các sinh tử bộ sau:

### ⚔️ Vũ Khí Lưu Trữ Dữ Liệu
*   **`VARCHAR2` vs `CHAR`**: Cuộc chiến kinh điển. Đừng rải mìn bằng `CHAR(10)` vì Oracle sẽ nhét khoảng trắng (space) cho đủ 10 ký tự, lãng phí không gian bộ nhớ siêu khủng. 99% mọi trận đánh, hãy xài biến động `VARCHAR2`.
*   **`DATE` vs `TIMESTAMP`**: Đừng vác dao mổ trâu giết gà. Nếu chỉ lấy đến Giây, `DATE` là vua. Cần lấy đến đơn vị phần tỉ giây của giao dịch HFT (High-Frequency Trading)? Lúc đó mới lôi `TIMESTAMP` ra.

### ⛓️ Ràng Buộc Khóa Ngoại (Foreign Key) - Cạm Bẫy Sập Hầm
Giữa Bảng Cha (Khách Hàng) và Bảng Con (Đơn Hàng), ta kết dính bằng **Khóa Ngoại (FK)** để chặn tạo ra Rác mồ côi (Tạo đơn cho khách không tồn tại). Nhưng Oracle giấu một thanh gươm đứt cổ:

> 🚨 **CẢNH BÁO KIẾN TRÚC SƯ**
> Oracle **mặc định KHÔNG tạo Index** cho Khóa Ngoại ở Bảng Con. Nếu bạn xóa (DELETE) hoặc sửa (UPDATE) một dòng ở Bảng Cha, Oracle không có Index để dò nhanh bảng Con nên nó sẽ ném ra "Lệnh Phong Tỏa" (Lock) **toàn bộ Bảng Con** để tra cứu!
> Hệ quả thảm khốc: Cả ngàn người đang mua hàng bị kẹt cứng (Deadlock) chỉ vì 1 admin vừa xóa 1 User.
> **Quy Tắc Sống Còn:** Cứ tạo FOREIGN KEY thì NGAY LẬP TỨC tạo INDEX cho cột đó!

<br/>

Khép lại Module Khởi Nguyên, chúng ta đã có Bản Vẽ 3NF hoàn mỹ, đã trét xi măng lên từng Ràng buộc vật lý vững chãi. Bây giờ, đã đến lúc chúng ta bơm máu dữ liệu vào, và đưa nó qua cái Lò Bát Quái kinh hoàng mang tên "Định Lý ACID".

---
**Next Step:** 👉 [Module 01: Thiết Kíp Nổ ACID - Bản Chất Giao Dịch Ngân Hàng](1.md)