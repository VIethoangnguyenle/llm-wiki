---
title: "Module 04: Thuật Ngự Thời Gian & Phế Tích Xóa Mềm"
source: "D:\9. Learn\12. llm wiki\raw\articles\ora\4.md"
date_added: 2026-04-23
tags: [notes]
status: draft
summary: ""
---

# Module 04: Thuật Ngự Thời Gian & Phế Tích Xóa Mềm 

Ở các cấp bổng lộc Jr DBA hoặc Backend Developer, khái niệm "Xóa dữ liệu" thường chỉ bắt đầu và kết thúc bằng việc tranh cãi: *"Nên dùng Hard Delete hay Soft Delete?"*. 

Đa số sẽ hùa nhau chọn **Soft Delete** (Thêm cột `IS_DELETED = 'Y'`). Lựa chọn này nghe có vẻ an toàn, tránh mất mát dữ liệu do sai lầm. Nhưng trong khuôn khổ của *Pháo Đài*", đây là nguồn cơn của sự ô nhiễm dị thường, đấm vỡ bộ tối ưu hóa CBO, và gây sập hầm các khóa định danh Unique Constraint.

Module 04 này sẽ moi móc những phế tích mà Soft Delete để lại, và trang bị cho bạn pháp bảo **Thuật Du Hành Thời Gian (Flashback)** của Oracle cấp độ Enterprise.

---

## 1. Phế Tích "Soft Delete" dưới con mắt của CBO

### 🌊 High Water Mark (HWM) - Nghĩa Địa Không Đáy
Trong Oracle, bất cứ khi nào bạn `INSERT` thêm data, giới hạn cấp phát bộ nhớ sẽ dâng lên. Sự kiện này được Oracle đánh dấu bằng vạch **High Water Mark**. 
Khi bạn dùng lệnh `UPDATE table SET is_deleted='Y'`, dòng dữ liệu chỉ bị đổi tên, hoàn toàn không bị xóa đi. HWM khôgn hề thụt lùi. 

Trong những truy vấn quét càn (Full Table Scan), CBO Oracle **bắt buộc phải quét tất cả các block từ đầu cho đến vạch HWM**. Cuối cùng, 90% lượng block database mà CBO cất công móc bới lên lại chính là những "cái xác đã xóa" bị giấu dưới lớp cát `IS_DELETED`.

### 👁️ Hiệu Ứng Mù Lòa Chỉ Mục (Selectivity)
 *"Tạo Index trên cột IS_DELETED để truy vấn nhanh hơn"* - Đây sự hiểu lầm phổ biến nhất trong giới thiết kế Database.

Định lý Độ Tuyển Chọn (Selectivity) của Oracle hoạt động dựa trên tỷ lệ dữ liệu trả về so với tổng thể. Giả sử 95% record trong bảng của bạn đang `Active`, và 5% `Deleted`.
Nếu bạn đắp 1 Index B-Tree lên cột `IS_DELETED='N'`, CBO sẽ đọc qua và tính toán:
> *"Cái Index này trỏ về tận 95% dữ liệu của Pháo đài, chi phí đi vòng qua Index rồi quay lại lấy chi tiết (Table Access By RowID) còn đắt hơn x3 lần việc rải lính quét tay toàn kho (Full Table Scan)!"*

Vậy nên, Index bạn tạo chỉ khiến hệ thống tốn thêm CPU khi Insert/Update, còn CBO sẽ cười mỉm và đi Full Table Scan. Index đó vô dụng.

---

## 2. Rút Máu Ràng Buộc Kép (Unique Constraints)

Soft delete sẽ thổi tung cấu trúc **Unique Constraints**.

**Kịch bản:** Người dùng đăng ký Email `ceo@vnd.com`. Vài tháng sau, họ hủy tài khoản. Ứng dụng gán `IS_DELETED = 'Y'`. Tài khoản chết lâm sàng. 
Hôm sau, người dùng ấy lấy lại Email `ceo@vnd.com` đăng ký lại. Database **từ chối 100%**! Lỗi dội ra: *Vi phạm Unique Constraint (Email)*. 

Mẹo của Junior: *"Vậy tôi đặt Composite Unique Key gồm (Email + Tình Trạng Xóa)"*. 
Điều này sụp đổ ngay ở lần người dùng hủy tài khoản thứ hai (Sẽ có 2 bản ghi `ceo@vnd.com` - `Y`, tiếp tục ném ra lỗi trùng lặp).

### 🛠️ Function-Based Index (Tính Duy Nhất Một Phần)
Thay vì đau đầu, các Tư Tế Oracle sử dụng **FBI (Function-Based Index)**. Bản chất của B-Tree bên trong Oracle là: Nó **bỏ qua và không lưu Index cho chuỗi giá trị rỗng (NULL)**. Vậy thì lợi dụng nó thôi!

```sql
-- Tạo Index nhưng dùng cú pháp điều kiện (CASE WHEN)
CREATE UNIQUE INDEX idx_users_email_active
ON users ( 
    CASE WHEN is_deleted = 'N' THEN email ELSE NULL END 
);
```
Với bùa chú này, ngay khi User bị đổi trạng thái cờ hiệu thành 'Y', biểu thức trên trả về `NULL`. Bản ghi đó trơn tru rơi khỏi Index (nhưng vẫn tồn tại trong Bảng). Oracle sẽ cho phép bạn chứa cả triệu account `Y` trùng Email mà chẳng hề phàn nàn, nhưng tuyệt đối chỉ có 1 User `N` tồn tại ở thực tại.

---

## 3. Thuật Du Hành Thời Gian (Flashback Archive)

Sau khi hiểu rõ bản chất Soft Delete phá hủy dữ liệu, phương án triệt để nhất luôn là: **"Gặp là Giết" (Hard Delete)**.

Hãy tận diệt vật lý record khỏi bảng để HWM ổn định, CBO chạy max tốc, và Referential Integrity của Database được duyệt bằng ON DELETE CASCADE chuẩn mực, không phải viết vòng for trên tầng API. Nhất tiễn hạ tứ điêu. Nhưng còn phần lịch sử đã xóa thì đi đâu?

### 🌀 Flashback Data Archive (FDA - Time Travel)
Đừng viết Code chuyển rác sang bảng `History`. Đó là phương thức đâm thủng hệ thống bằng các Trigger đầy lỗi. Bằng cách kích hoạt *Flashback Data Archive (FDA)* có sẵn ngay cả ở bản Standard Edition, mọi thứ hoàn toàn tự động ở **Tầng Hạt Nhân**.

Dữ liệu xóa vật lý trên Bảng `users` sẽ biến mất, nhưng ở kho chiều không gian ảo FDA, "Hồn Ma" của dòng dữ liệu đó được đóng gói và nén Columnar Compression lạnh lẽo.

Khi ứng dụng hay Auditor có nhu cầu tra soát lịch sử 1 ngày trước của người dùng có ID là 101, chỉ cần lôi đũa phép SQL chuẩn mở rộng ra đọc lệnh:

```sql
SELECT * 
FROM users 
AS OF TIMESTAMP (SYSTIMESTAMP - INTERVAL '1' DAY)
WHERE user_id = 101;
```

Trong chớp mắt, Oracle kéo lại dòng dữ liệu nguyên vẹn của dòng thời gian cách đây đúng 24h mà ứng dụng Client không hề hay biết rằng nó đã từng thay đổi cấu trúc hay vừa bị xóa cờ. Đó chính là Cảnh giới "Nghịch Biến Thời Không" thần thánh của Oracle Database.

---
**Next Step:** 👉 [Module 05: Lò Phản Ứng RAC & Cache Fusion](5.md) *(Đang hoàn thiện)*