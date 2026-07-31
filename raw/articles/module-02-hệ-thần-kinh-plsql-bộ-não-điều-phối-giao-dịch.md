---
title: "Module 02: Hệ Thần Kinh PL/SQL - Bộ Não Điều Phối Giao Dịch"
source: "D:\9. Learn\12. llm wiki\raw\articles\ora\2.md"
date_added: 2026-04-23
tags: [notes]
status: draft
summary: ""
---

# Module 02: Hệ Thần Kinh PL/SQL - Bộ Não Điều Phối Giao Dịch

## 1. Dẫn Nhập Cốt Truyện: Sinh Vật Cơ Khí Sống

Nếu **ACID** là bộ luật giao dịch sống còn bảo vệ sự nguyên vẹn của Pháo Đài Tài Chính (Module 01), thì **PL/SQL (Procedural Language/SQL)** chính là **Hệ Thần Kinh Trung Ương** của pháo đài đó.

Khác với các Database thông thường chỉ làm nhiệm vụ "lưu và trả dữ liệu" (như một nhà kho thụ động), Oracle PL/SQL cho phép bạn nhúng logic nghiệp vụ phức tạp trực tiếp vào bên trong tầng dữ liệu. Bạn không cần tải hàng triệu bản ghi qua mạng về ứng dụng Node.js hay Java để xử lý, mà chuyển thẳng mã lệnh vào trong lõi Oracle để nó xử lý cục bộ rồi trả về kết quả cuối cùng.

Đó là lý do Oracle Core Banking hoạt động như một *sinh vật cơ khí sống*. Để thuần hóa hệ thần kinh này, chúng ta cần tìm hiểu 3 khối module kiến trúc quyền lực nhất của nó: **Function, Procedure và Package**.

---

## 2. Bản Chất Nhị Nguyên: Function (Cảm biến) và Procedure (Cánh tay cơ khí)

Trong giới lập trình PL/SQL, có một lầm tưởng kinh điển: *"Function khác Procedure ở chỗ Function thì trả về giá trị (RETURN), còn Procedure thì không"*. Nhưng sự thật về mặt kiến trúc hệ thống ngầm chứa nhiều ranh giới sắc bén hơn thế.

### 📡 Function: Các Cảm Biến Tinh Khiết (Sensors)
* **Khái niệm:** Một Function được thiết kế để trở thành một "Biểu thức tính toán". Sự mệnh của nó là nhận tham số đầu vào và trả ra LUÔN LUÔN một giá trị cụ thể.
* **Quy tắc Purity (Độ Tinh Khiết):** Điểm đặc biệt của Function là nó có thể được nhúng thẳng vào các câu lệnh SQL truyền thống (`SELECT calculate_tax(salary) FROM employees`). Để làm được điều này, Function phải Tinh Khiết: **Nghiêm cấm mọi hành vi thay đổi dữ liệu** (Không INSERT, UPDATE, DELETE). Nó chỉ được phép "cảm nhận" và báo cáo trạng thái.
* **Vũ khí bí mật:** Oracle cho phép tạo Database Index (Chỉ mục) chạy thẳng trên Function (Function-Based Indexes). Điều này biến Cảm biến của bạn thành một radar dò tìm siêu tốc độ.

### 🦾 Procedure: Cánh Tay Robot Kích Hoạt Trạng Thái (Robotic Arms)
* **Khái niệm:** Procedure không trả về giá trị qua `RETURN`, nhưng nó được phép tác động trực tiếp lên hệ sinh thái. Nhiệm vụ của nó là thực thi *Logic Nghiệp Vụ* (Business Logic).
* **Đặc tính Mở:** Chứa các lệnh thay đổi dữ liệu khổng lồ, xử lý Transaction Control (Commit / Rollback). Cánh tay cơ khí này bốc dỡ hàng vạn bản ghi một lúc, nhưng bạn không thể gắn nó vào một câu lệnh `SELECT` thông thường.

🎭 **Xóa Bỏ Huyền Thoại: "Procedure chạy nhanh hơn Function?"**
> *Rất nhiều Coder truyền tụng rằng Procedure tối ưu hơn. Sự thật là, từ phiên bản Oracle 19c trở đi, sự chênh lệch này gần như vô hình. Sự chậm trễ duy nhất của Function là do "Context Switching" (Chuyển ngữ cảnh giữa bộ máy SQL và PL/SQL). Nhưng Oracle đã thêm vào 'UDF Pragma' giúp triệt tiêu độ trễ này. Chọn Function hay Procedure là bài toán về KIẾN TRÚC TƯ DUY, không phải MẸO VẶT TỐI ƯU.*

---

## 3. Package: Trung Tâm Điều Khiển Chống Xâm Nhập

Nếu Function và Procedure là các module riêng lẻ, thì **Package (Gói)** là Tòa Lâu Đài kiên cố bọc thép toàn bộ chúng lại. Một Kiến trúc sư Oracle thực thụ KHÔNG BAO GIỜ viết các hàm standalone rải rác. Họ định tuyến mọi luồng lệnh qua Package.

### 🔹 Cấu Trúc Bọc Thép (Encapsulation)
Một Package tách làm 2 vỏ bọc:
1. **Specification (Spec - Bản thiết kế giao diện):** Công bố cho thế giới (hệ thống frontend/backend bên ngoài) biết các biến công khai và định nghĩa hàm (signatures). Nó giống như một bản API Contract.
2. **Body (Thân - Khoang chứa bí mật):** Chứa toàn bộ source code thực thi và các thuật toán nội bộ.

*Triết lý ẩn thông tin (Information Hiding):* Bạn có thể đập đi xây lại toàn bộ thuật toán bên trong `Body` hàng trăm lần một ngày. Chỉ cần `Spec` không đổi, không một đoạn code phụ thuộc nào ở lớp ngoài bị vô hiệu hóa (Invalidated). Chuỗi phụ thuộc bị bẻ gãy, đảm bảo tiến trình CI/CD mượt mà.

### ⚠️ Rủi Ro Chí Mạng: Bóng Ma "Connection Pooling"
Các Package trong Oracle lưu giữ trạng thái biến thông qua vùng nhớ **UGA (User Global Area)** của phiên làm việc (Session State).
Tuy nhiên, với mô hình Web vạn người dùng (Connection Pool), ứng dụng backend (Java/Node.js) thường bốc 1 kết nối (Connection X) dùng xong rồi ném lại vào hồ chứa.
* **Kịch bản thảm họa:** User A dùng Connection X truy cập Package, gán biến `g_balance = 1000`. Connection X được hút về Pool. Vài giây sau, User B được cấp phát đúng Connection X đó! Đột nhiên User B đang sở hữu dữ liệu tài chính của User A.
* **Bài học Architect:** Quản trị Session State là lằn ranh mỏng manh giữa một hệ thống "chạy cho xong" và một hệ thống chuẩn chuẩn Ngân hàng. Cần đặc biệt lưu lý xoá biến Local sau mỗi lệnh thực thi.

---

## 4. Tối Ưu Ghim Hệ Nhớ & Quản Lý Cảnh Báo Lỗi

### 💡 Pinning: Giữ Lò Năng Lượng Luôn Nóng
Mỗi khi Package được gọi, Oracle đẩy cả khối mã biên dịch khổng lồ vào **Shared Pool** (Bộ nhớ chung). Để các Package quan trọng bậc nhất không bị cơ chế LRU "đạp dọn" nhường chỗ cho thằng khác khi RAM đầy, Quản trị viên sử dụng quyền trượng `DBMS_SHARED_POOL.KEEP` để "Ghim" (Pinning) package đó vĩnh viễn vào bộ nhớ RAM siêu tốc.

### 🚨 Quản Lý Xung Đột (Graceful Degradation)
Một hệ thống siêu tồi tệ không phải là bị lỗi, mà là *văng ra những mã lỗi không thể lý giải* dọa khách hàng. Thông qua khối **Exception Handling**, mạng thần kinh PL/SQL phân cấp thiết bị báo cháy tinh vi:
- Lỗi được triêu tiêu tại luồng con. Nếu không xử lý, nó lan truyền (propagate) lên tầng cha.
- Sử dụng `RAISE_APPLICATION_ERROR` (Mã -20000) để chuyển dịch sự cố sâu thẳm trong database thành những thông điệp Front-end thân thiện như: *"Số dư ngân hàng không đủ, vui lòng nạp thêm"*.

<br/>

Khép lại Module 02, chúng ta đã nắm được mạch não logic chi phối Pháo đài. Ở bước tiến tiếp theo, khi logic này cần scale lên gấp chục lần lượng người dùng, đó là lúc chúng ta phải gắn thêm trái tim thứ hai cho Pháo đài.

---
**Next Step:** 👉 [Module 03: Lò Phản Ứng RAC & Cache Fusion - Bất Tử Hóa Pháo Đài] (Coming soon)