---
title: "Flashback Data Archive"
source: "compiled"
date_added: 2026-04-23
tags: [concept, database, oracle, flashback, history]
aliases: [FDA, Oracle Flashback, Flashback, Du hành thời gian]
status: canonical
related:
  - "[[oracle-database]]"
  - "[[soft-delete-anti-pattern]]"
summary: "Công nghệ của Oracle hỗ trợ truy vấn các phiên bản dữ liệu lịch sử ngay tại tầng dữ liệu hạt nhân."
---

# Flashback Data Archive

## Định Nghĩa
Flashback Data Archive (FDA) là một cấu trúc tính năng ở cấp độ Enterprise của hệ thống [[oracle-database|Oracle Database]]. Được mô tả như "cỗ máy du hành thời gian", FDA cho phép các tiến trình vận hành tự động ghi nhận, đóng gói và nén lại bất cứ phiên bản nào của dữ liệu khi chúng bị ghi đè hoặc bị xóa mất. Khác biệt với việc duy trì bảng nhật ký lịch sử rườm rà tại tầng ứng dụng (Application Level), mọi hoạt động ghi vết của FDA diễn ra một cách thầm lặng ngay ở cấu trúc hạt nhân của hệ thống cơ sở dữ liệu.

## Cơ Chế "Nghịch Biến Thời Không"
Thay vì áp dụng cơ chế đánh dấu cờ hiệu xóa mềm ([[soft-delete-anti-pattern|Soft Delete]]) dẫn đến các hệ lụy làm giảm sút hiệu năng quét bảng, các chuyên gia thiết kế cơ sở dữ liệu sẽ kích hoạt công nghệ FDA kết hợp cùng hành động xóa vật lý (Hard Delete).

- Bất cứ khi nào một tiến trình `DELETE` tác động, dữ liệu vật lý biến mất khỏi các Table thực thi chính, giúp khôi phục định mức hiệu suất CBO ở mức tối đa.
- Ngay lúc đó, "hồn ma" của dòng dữ liệu vừa bị xóa sẽ được Oracle điều chuyển và nén (Columnar Compression) chặt chẽ tại không gian chiều thứ hai của FDA.

## Giao Tiếp Truy Vấn Quá Khứ
Sức mạnh đích thực của Flashback Data Archive nằm ở khả năng tích hợp truy vấn trực diện. Thông qua các phần mở rộng cú pháp SQL (Ví dụ: `AS OF TIMESTAMP`), ứng dụng hoặc kiểm toán viên (Auditor) có thể yêu cầu truy xuất thẳng thông tin trạng thái của một bản ghi tại bất cứ mốc thời điểm nào trong quá khứ một cách trơn tru, mà không cần nhận thức rằng dòng dữ liệu đó đã bị thay đổi cấu trúc hoặc bị bốc hơi khỏi thực tại dữ liệu hiện tại.

## Liên Hệ / Ứng Dụng
Trong các hệ thống lõi đặc biệt nghiêm ngặt như Core Banking, FDA là bức tường phòng thủ cuối cùng để bảo toàn tính minh bạch trước hoạt động kiểm toán, khắc phục hậu quả thiên tai, hoặc ngăn cản sự xâm phạm cơ sở dữ liệu mà không cần phải thỏa hiệp với bất kỳ sự hao phí nào về phương diện tốc độ truyền tải thông tin.

## Nguồn Tham Khảo
- [[raw/articles/module-04-thuật-ngự-thời-gian-phế-tích-xóa-mềm.md]]
