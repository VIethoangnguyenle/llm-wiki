---
title: "Oracle Database"
source: "compiled"
date_added: 2026-04-23
tags: [tool, database, rdbms, core-banking]
aliases: [Oracle, Oracle DB]
status: canonical
related:
  - "[[acid-properties]]"
  - "[[pl-sql]]"
  - "[[cost-based-optimizer]]"
  - "[[flashback-data-archive]]"
summary: "Hệ quản trị CSDL quan hệ tiêu chuẩn vàng cho các hệ thống Core Banking và tài chính."
---

# Oracle Database

## Tổng Quan
Oracle Database là một hệ quản trị cơ sở dữ liệu quan hệ (RDBMS) đa mô hình được phát triển bởi Tập đoàn Oracle. Trong bối cảnh chuyển đổi số, bất chấp sự trỗi dậy của các kiến trúc Cloud-Native và mã nguồn mở (như PostgreSQL hay NoSQL), Oracle vẫn duy trì vị thế "độc tôn" như một tiêu chuẩn vàng cho các định chế tài chính khổng lồ (Mitsubishi UFJ, Deutsche Bank, Vietcombank).

## Vai Trò Trong Hệ Thống Core Banking
Trong các hệ thống lõi ngân hàng (Core Banking), "tính nhất quán cuối cùng" (eventual consistency) là không thể chấp nhận được vì tiền không bao giờ được phép mất đi hay tạo ra từ hư vô. Oracle đóng vai trò là "chiếc phanh khẩn cấp ABS", đảm bảo tính toàn vẹn dữ liệu (Data Integrity) tuyệt đối thông qua việc tuân thủ khắt khe bộ quy tắc [[acid-properties|ACID]]. 

Hệ thống cung cấp độ trễ (latency) cực thấp kể cả với hàng chục ngàn thao tác mỗi giây (TPS) nhờ vào cấu trúc lưu trữ và xử lý đa chiều.

## Lợi Thế Công Nghệ
Oracle Database được trang bị một hệ sinh thái các công nghệ độc quyền và tối tân:
- **Ngôn ngữ thủ tục tích hợp:** [[pl-sql|PL/SQL]] đóng vai trò như hệ thần kinh trung ương, cho phép nhúng logic nghiệp vụ phức tạp trực tiếp vào tầng dữ liệu để giảm thiểu độ trễ mạng.
- **Siêu AI Tối ưu hóa:** Bộ tối ưu hóa dựa trên chi phí ([[cost-based-optimizer|CBO]]) phân tích và định tuyến các câu lệnh truy vấn phức tạp một cách thông minh.
- **Quản lý dữ liệu lịch sử:** Công nghệ [[flashback-data-archive|Flashback Data Archive (FDA)]] cho phép hệ thống truy vấn lại dữ liệu ở các thời điểm trong quá khứ mà không cần thiết kế bảng lưu trữ lịch sử cồng kềnh.
- **Khả năng mở rộng và sẵn sàng cao:** Công nghệ Real Application Clusters (RAC) với Cache Fusion giúp duy trì hoạt động ngay cả khi một phần hệ thống gặp sự cố. Kết hợp với Oracle Exadata, hệ thống có thể đẩy câu lệnh truy vấn thẳng xuống ổ cứng (Smart Scan) để tiết kiệm chu kỳ xử lý của CPU.
- **Tính cô lập dữ liệu ưu việt:** Kiến trúc Multi-Version Concurrency Control (MVCC) sử dụng Undo Segment giúp cung cấp khả năng đọc dữ liệu không bị chặn bởi các tiến trình ghi, một điểm khác biệt cốt lõi so với kỹ thuật VACUUM của các cơ sở dữ liệu khác.

## Nguồn Tham Khảo
- [[raw/articles/lộ-trình-oracle-database-pháo-đài-tài-chính-cyber-finance.md]]
- [[raw/articles/module-01-thiết-kíp-nổ-acid-bản-chất-giao-dịch-ngân-hàng.md]]
