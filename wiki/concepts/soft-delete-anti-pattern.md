---
title: "Soft Delete"
source: "compiled"
date_added: 2026-04-23
tags: [concept, database, anti-pattern, soft-delete]
aliases: [Xóa mềm, Soft Delete Anti-pattern]
status: canonical
related:
  - "[[flashback-data-archive]]"
  - "[[cost-based-optimizer]]"
summary: "Phân tích các hệ lụy ẩn giấu của phương thức xóa mềm ảnh hưởng đến hiệu suất và tính duy nhất của cơ sở dữ liệu."
---

# Soft Delete

## Định Nghĩa
Soft Delete (Xóa mềm) là một phương pháp quản trị dữ liệu phổ biến, hoạt động bằng cách thêm một trường đánh dấu cờ hiệu (thường là `IS_DELETED = 'Y'`) thay vì xóa vật lý dữ liệu (Hard Delete) khỏi cơ sở dữ liệu. Mặc dù tạo ra cảm giác an toàn và dễ dàng phục hồi dữ liệu khi thao tác lỗi, Soft Delete ẩn chứa những hệ lụy sâu sắc có khả năng làm suy sụp hiệu năng của một hệ thống cơ sở dữ liệu cấp doanh nghiệp.

## Phế Tích Dữ Liệu Dưới Con Mắt Tối Ưu Hóa

### Nghĩa Địa Không Đáy (High Water Mark)
Trong Oracle Database, giới hạn cấp phát bộ nhớ sẽ dâng lên bằng mức High Water Mark (HWM) cho mọi hoạt động thêm dữ liệu (`INSERT`). Việc dùng cờ đánh dấu xóa mềm bản chất chỉ là cập nhật lại dữ liệu (`UPDATE`) nên giới hạn HWM không bao giờ thụt lùi xuống. Khi bộ tối ưu hóa [[cost-based-optimizer|CBO]] yêu cầu một quá trình quét toàn bảng (Full Table Scan), nó buộc phải lãng phí tài nguyên để duyệt qua hàng loạt block bộ nhớ trống rỗng hoặc chứa dữ kiện rác đã bị xóa mềm nằm chìm dưới HWM.

### Hiệu Ứng Mù Lòa Chỉ Mục (Selectivity)
Việc cố gắng tạo một chỉ mục (Index) trên cột `IS_DELETED` để tối ưu hóa truy vấn thông thường là một sự hiểu lầm căn bản về Độ tuyển chọn (Selectivity). Nếu phần lớn (chẳng hạn 95%) dữ liệu trong hệ thống có trạng thái là "Chưa Xóa", CBO sẽ tự động bỏ qua chỉ mục đó do chi phí tham chiếu dữ liệu qua chỉ mục đắt đỏ hơn việc đi quét qua toàn bộ cấu trúc vật lý của bảng.

## Sự Xung Đột Với Các Ràng Buộc Dữ Liệu
Hệ quả khốc liệt nhất của Xóa mềm là khả năng phá hủy các Ràng buộc duy nhất (Unique Constraints).
Nếu người dùng đăng ký một định danh (như Email), sau đó hủy để hệ thống đánh dấu xóa mềm, bất kỳ nỗ lực đăng ký lại bằng email đó trong tương lai đều bị cơ sở dữ liệu từ chối. Việc thiết lập một cấu trúc khóa kép chứa trạng thái xóa chỉ giải quyết được sự cố cho một lần xóa đầu tiên, và sẽ lại sụp đổ ở lần thử thứ hai.

## Phương Thức Khắc Phục

### Tính Duy Nhất Một Phần (Function-Based Index)
Để giữ lại cấu trúc Soft Delete mà vẫn duy trì Unique Constraints linh hoạt, các nhà thiết kế cơ sở dữ liệu có thể dùng Function-Based Index kết hợp với cú pháp rẽ nhánh để "lừa" cấu trúc B-Tree. Do cấu trúc B-Tree từ chối lưu chỉ mục cho các giá trị `NULL`, một chỉ mục cấu hình hàm `CASE WHEN` ép cột đánh dấu thành `NULL` sẽ biến dữ liệu đã bị xóa tàng hình khỏi luật cấm trùng lặp.

### Chuyển Dịch Kiến Trúc
Đối với các khối dữ liệu chuyên ngành cần truy vết như ngân hàng, kỹ thuật triệt để nhất luôn là Xóa vật lý (Hard Delete) và xử lý vấn đề tra soát lịch sử thông qua các công cụ tầng lõi như [[flashback-data-archive|Flashback Data Archive]].

## Nguồn Tham Khảo
- [[raw/articles/module-04-thuật-ngự-thời-gian-phế-tích-xóa-mềm.md]]
