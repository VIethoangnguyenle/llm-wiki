---
title: "ACID Properties"
source: "compiled"
date_added: 2026-04-23
tags: [concept, database, transaction]
aliases: [ACID, Tính chất ACID, Nguyên lý ACID]
status: canonical
related:
  - "[[oracle-database]]"
  - "[[database-normalization]]"
summary: "Bộ bốn thuộc tính cơ bản đảm bảo tính toàn vẹn và độ tin cậy của giao dịch cơ sở dữ liệu."
---

# ACID Properties

## Định Nghĩa
ACID là một khái niệm cốt lõi trong khoa học máy tính, viết tắt của Atomicity (Tính nguyên tử), Consistency (Tính nhất quán), Isolation (Tính cô lập) và Durability (Tính bền vững). Đây là bộ luật sắt đá nhằm đảm bảo tính vẹn toàn tuyệt đối của dữ liệu (Data Integrity) trong các hệ quản trị cơ sở dữ liệu, đặc biệt quan trọng đối với các hệ thống tài chính như Core Banking.

Khác với "tính nhất quán cuối cùng" (eventual consistency) thường thấy trong các hệ thống mạng xã hội, ACID yêu cầu mọi giao dịch phải diễn ra trọn vẹn hoặc quay ngược trạng thái như chưa từng xảy ra.

## Cơ Chế Hoạt Động
Mỗi yếu tố trong ACID đảm nhiệm một chức năng riêng biệt nhằm bảo vệ dữ liệu:

### Tính Nguyên Tử (Atomicity)
Giao dịch là một đơn vị không thể phân rã; nó phải thành công toàn bộ hoặc thất bại toàn bộ, không có khái niệm "hoàn thành một nửa". Nếu có sự cố (như cúp điện hoặc lỗi mạng) xảy ra giữa chừng, cơ sở dữ liệu (chẳng hạn như [[oracle-database|Oracle]]) sẽ tự động thực hiện tiến trình Rollback (Hoàn tác) để khôi phục dữ liệu về trạng thái ban đầu.

### Tính Nhất Quán (Consistency)
Dữ liệu luôn phải chuyển từ một trạng thái hợp lệ này sang một trạng thái hợp lệ khác, tuân thủ tất cả các quy tắc và ràng buộc nghiệp vụ (ví dụ: ràng buộc `CHECK (balance >= 0)`). Hệ thống sẽ từ chối các giao dịch dẫn đến việc dữ liệu vi phạm các ràng buộc này, bất kể có bao nhiêu lệnh được gọi cùng một lúc (race conditions).

### Tính Cô Lập (Isolation)
Trong một cơ sở dữ liệu phục vụ hàng triệu người truy cập cùng lúc, giao dịch của một người dùng không được phép can thiệp hoặc nhìn thấy trạng thái dang dở của giao dịch do người khác thực hiện. Các hệ thống hiện đại giải quyết vấn đề này thông qua kiến trúc Multi-Version Concurrency Control (MVCC) kết hợp với khóa mức độ dòng (Row-level locking), giúp cô lập các tiến trình mà không làm tắc nghẽn luồng truy cập chung.

### Tính Bền Vững (Durability)
Một khi hệ thống xác nhận giao dịch đã thành công, kết quả của giao dịch đó phải được ghi nhận vĩnh viễn và không thể bị đảo ngược do các thảm họa như mất điện hay hỏng hóc máy chủ. Thông tin thay đổi thường được đẩy vào các tệp nhật ký (như Redo Log) trước khi được ghi vĩnh viễn xuống ổ đĩa vật lý, đảm bảo khả năng phục hồi dữ liệu trong mọi tình huống.

## Liên Hệ / Ứng Dụng
Trong các ứng dụng giao dịch tài chính quy mô lớn, việc duy trì ACID ở cường độ siêu tải (Hàng trăm nghìn Transaction Per Second) trên hạ tầng phân tán là một thách thức kỹ thuật rất lớn. Việc lựa chọn công nghệ hỗ trợ tốt ACID là quyết định sống còn để duy trì uy tín của các định chế tín dụng.

## Nguồn Tham Khảo
- [[raw/articles/module-01-thiết-kíp-nổ-acid-bản-chất-giao-dịch-ngân-hàng.md]]
