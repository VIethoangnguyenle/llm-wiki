---
title: "Module 03: Mắt Thần CBO & Thuật Tu Tiên Bằng Dữ Liệu (SQL Tuning)"
source: "D:\9. Learn\12. llm wiki\raw\articles\ora\3.md"
date_added: 2026-04-23
tags: [notes]
status: draft
summary: ""
---

# Module 03: Mắt Thần CBO & Thuật Tu Tiên Bằng Dữ Liệu (SQL Tuning)

## 1. Dẫn Nhập: Trạm Logistics Tín Hiệu & Siêu AI CBO

Ở Module trước, chúng ta đã bọc một lớp áo giáp thép (PL/SQL Package) để bảo vệ lõi nghiệp vụ. Nhưng một Pháo đài không thể chỉ đứng yên phòng thủ. Nó cần nhận tín hiệu (Dữ liệu vào) và phân phát chỉ thị (Báo cáo ra). Quá trình di chuyển hàng tỷ bản ghi qua lại này chính là huyết mạch của hệ thống. 

Tuy nhiên, nếu bạn viết một câu *SQL Join* sai cách, bạn đang tự tay thắt cổ dòng máu Logistics đó.

Đó là lúc **CBO (Cost-Based Optimizer)** — hệ thống Siêu AI của Oracle xuất hiện. Nếu SQL của bạn là bản nháp yêu cầu cấp phát vũ khí, CBO chính là vị Tư lệnh tối cao quyết định đường đi của từng băng đạn, quyết định dùng xe thồ hay máy bay vận tải. Bài học này sẽ giúp bạn hiểu ngôn ngữ của vị Tư lệnh ấy.

---

## 2. Giải Phẫu Băng Chuyền Join (Phép Nối)

Khi Oracle nối nhiều bảng (Ví dụ: Khách hàng -> Đơn hàng -> Giao dịch), nó không làm mọi thứ cùng một lúc mà xây dựng một **Cây Truy vấn (Join Trees)**.

### 🏭 Cấu Trúc Băng Chuyền Logistics

*   **Left Deep Join Tree (Nối Sâu Trái):** Đây là mô hình hoạt động theo kiểu "dây chuyền lắp ráp". Dữ liệu từ bảng đầu tiên (Driving Table) sẽ đổ vào phễu, nối với bảng 2 để ra kết quả A, kết quả A chạy tiếp vào bảng 3. **Bài học xương máu:** Nếu bạn chọn sai bảng bắt đầu (ví dụ: quét toàn bộ bảng 1 tỷ dòng trước thay vì bảng 100 dòng), toàn bộ băng chuyền phía sau sẽ nghẽn cứng vĩnh viễn.
*   **Right Deep & Bushy Tree:** Oracle sử dụng các luồng phức tạp hơn để xử lý song song, nhưng ở cấp độ cơ bản, tư duy "Trái sang Phải" là nguyên lý tối thượng.

### ⚙️ Phương Thức Vận Chuyển (Join Methods)

CBO sẽ quyết định dùng phương tiện gì để chở dữ liệu giữa 2 trạm (tùy theo lượng dữ liệu và Index):

1.  **Nested Loops (Vòng Lặp Lồng Nhau - Người Thu Tiền Điện):** Hoạt động như 2 vòng lặp `FOR`. Bạn có 10 khách hàng (bảng A), bạn chạy đến cuốn sổ 1 triệu giao dịch (bảng B) để tìm 10 người đó. Cực kỳ nhanh nếu danh sách nhỏ và có Index.
2.  **Hash Join (Máy Băm Phân Khối - Ngựa Thồ Big Data):** Khi danh sách khách hàng lên tới 50 triệu, việc chạy đi chạy lại là tự sát. CBO ném 50 triệu đó vào một vùng nhớ tạm (Hash Table), băm nhỏ ra từng rổ riêng. Sau đó quét 1 triệu giao dịch bên kia và thả vào đúng cái rổ đã băm sẵn. Chuyên trị báo cáo dữ liệu cực nén.
3.  **Sort Merge Join:** Khi dữ liệu quá khổng lồ không vừa Hash Table, CBO bắt buộc phải Sắp Xếp (Sort) cả 2 bên trước khi Trộn (Merge) chúng lại với nhau.

### ⚠️ Ma Trận Nội - Ngoại Bất Khả Kháng (Logical Joins Trap)

Bảng dưới đây là những cái bẫy thường gặp của DBA mới:

*   **LEFT JOIN (Sát thủ giấu mặt):** Chỉ cần bạn "lỡ tay" nạp điều kiện đặt trên bảng bên Phải vào trong mệnh đề `WHERE` (thay vì `ON`), Left Join lập tức tuột xích và biến trở lại thành `INNER JOIN` (Vì dữ liệu NULL bị WHERE gạt bỏ mất).
*   **RIGHT JOIN (Sự Ngược Đời Dị Biệt):** `A LEFT JOIN B` hoàn toàn tương đương với `B RIGHT JOIN A`. Tuy nhiên, não người đọc logic code từ Trái sang Phải. Việc xài Right Join khiến người đọc code (mantainer) tẩu hỏa nhập ma, lật ngược tư duy. **Tôn chỉ Coding:** Luôn viết xuôi chiều, né Right Join bằng mọi giá.

---

## 3. Kính Hiển Vi Lượng Tử & Thuật Du Hành Thời Gian (Analytic Functions)

Tối ưu tốc độ xong, làm sao để thực thi các ma thuật nghiệp vụ mà `GROUP BY` truyền thống bó tay? (Ví dụ: Lấy top 3 nhân viên xuất sắc nhất của *từng* chi nhánh). Nếu bạn phải quét 2-3 vòng lặp để thực hiện điều đó, bạn đã thất bài.

Chào mừng đến với **Analytic Functions (Window Functions)** - Đũa phép của Oracle.

### 🔬 Kính Hiển Vi Xếp Hạng (Ranking)

Kính hiển vi `OVER (PARTITION BY ... ORDER BY ...)` cho phép bạn chẻ nhỏ dữ liệu (chia nhát dao) mà không bị mất đi bản ghi hiển thị (như Group By).

1.  **`ROW_NUMBER()`:** Ban cho mỗi dòng một thẻ ID tăng dần (1, 2, 3..). Thường được dùng để đánh số phân trang và Trảm (De-duplicate) xóa các dòng rác trùng lặp trong DB.
2.  **`RANK()` (Xếp hạng nhảy cóc):** Giống như thi Olympic. Nếu 2 người đồng hạng Nhất (1, 1). Người số 3 sẽ văng xuống hạng 3 (1, 1, 3). Thích hợp cho việc chặn thưởng Top 3 toàn chi nhánh.
3.  **`DENSE_RANK()` (Xếp hạng kề nhau):** Giải quyết bất công của Rank. Nếu 2 thằng hạng nhất, em đứng sau phải là hạng 2 (1, 1, 2). Tuyệt đối hữu dụng khi tìm "Người lương cao thứ 2 hệ thống".

### ⏳ Phép Du Hành Thời Gian (LAG / LEAD)

*Làm sao để biết doanh số của hôm nay tăng hay giảm so với hôm qua?*
Kẻ bồng bột sẽ xúi bạn viết truy vấn `Bảng A INNER JOIN Bảng A (A.date = B.date + 1)`. Chúc mừng, truy vấn lặp lại (Self-join) trên bảng 1 Tỷ dòng sẽ làm treo CPU ngân hàng!

Người dùng tinh hoa sử dụng **OFFSET Functions**:
*   **`LAG()` (Nhìn về Quá Khứ):** Kéo thẳng giá trị của dòng chạy qua ngày hôm qua tới hôm nay ngay trong nội bộ Cửa sổ hiện tại.
*   **`LEAD()` (Dự Đoán Tương Lai):** Sới tung dữ liệu của dòng sau đắp vào dòng này, dùng cực tốt để biết khi nào phiên (session) hiện tại sẽ kết thúc.

Việc dùng LAG/LEAD triệt tiêu hoàn toàn sự đắt đỏ của Self-Join, đó là đỉnh cao của nghệ thuật SQL Tuning - hay Thuật Luyện Kim Của Dữ Liệu.

<br/>

Khép lại 3 Module, ta đã thấu suốt **Tầng Dữ Liệu -> Tầng Logic -> Tầng Vận Hành Cấu Trúc Tìm Kiếm**. Việc của chúng ta bây giờ là scale up năng lực xử lý lên 1000 Server để cứu đói cho băng chuyền này.

---
**Next Step:** 👉 [Module 04: Lò Phản Ứng RAC & Cache Fusion] (Coming soon)