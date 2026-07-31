---
title: "Analytic Functions"
source: "compiled"
date_added: 2026-04-23
tags: [concept, database, sql-tuning]
aliases: [Window Functions, Hàm phân tích, Hàm cửa sổ]
status: canonical
related:
  - "[[cost-based-optimizer]]"
summary: "Các hàm phân tích dữ liệu cho phép tính toán trên tập hợp nhóm mà không làm mất đi chi tiết của từng bản ghi."
---

# Analytic Functions

## Định Nghĩa
Analytic Functions (hay Window Functions) là các hàm xử lý dữ liệu nâng cao được cung cấp trong các cơ sở dữ liệu quan hệ (đặc biệt nổi tiếng trong hệ sinh thái Oracle). Không giống như chức năng tập hợp truyền thống (`GROUP BY`) sẽ gộp và làm biến mất các dòng chi tiết, Analytic Functions cho phép thực hiện việc phân tích trên các cửa sổ khung (Window) để trả về giá trị trên *từng* dòng dữ liệu cụ thể.

## Chức Năng Cốt Lõi

### Kính Hiển Vi Xếp Hạng (Ranking)
Cú pháp `OVER (PARTITION BY ... ORDER BY ...)` cho phép chia nhỏ dữ liệu để xử lý:
- **`ROW_NUMBER()`:** Cấp phát một chuỗi ID liên tục (1, 2, 3...) cho từng dòng. Thường được ứng dụng trong kỹ thuật phân trang (Pagination) hoặc xác định/loại bỏ dữ liệu trùng lặp (De-duplicate).
- **`RANK()`:** Hàm đánh giá xếp hạng theo quy tắc nhảy cóc. Nếu hai người cùng giữ vị trí hạng 1, thì người tiếp theo sẽ xếp hạng 3 (1, 1, 3).
- **`DENSE_RANK()`:** Hàm đánh giá xếp hạng kề liền nhau. Giải quyết sự ngắt quãng của Rank, theo đó nếu hai người hạng 1, người tiếp theo vẫn giữ hạng 2 (1, 1, 2). Cực kỳ hữu dụng khi truy vấn các vị trí liền kề như "Người có mức lương cao thứ hai toàn hệ thống".

### Phép Du Hành Thời Gian (Offset Functions)
Việc tham chiếu chéo dữ liệu giữa nhiều hàng liền kề thông qua phép lặp (`Self-Join`) trên các bảng dữ liệu khổng lồ là một sự lãng phí tài nguyên khủng khiếp. Các hàm khoảng cách triệt tiêu bài toán này:
- **`LAG()`:** Hàm nội suy hướng về quá khứ. Cho phép một bản ghi "kéo" giá trị của các bản ghi xuất hiện trước nó theo trục sắp xếp để thực hiện so sánh (Ví dụ: So sánh doanh số ngày hôm nay so với hôm qua).
- **`LEAD()`:** Hàm trích xuất hướng về tương lai. Cho phép sới tung dữ liệu của những sự kiện sắp diễn ra và gắn chúng trực tiếp vào luồng bản ghi hiện tại.

## Liên Hệ / Ứng Dụng
Trong hoạt động tinh chỉnh SQL (SQL Tuning), Analytic Functions được xem là đỉnh cao nghệ thuật của lập trình dữ liệu. Khi đối mặt với các nghiệp vụ yêu cầu truy vết biến động trạng thái thời gian thực hay các báo cáo xếp hạng phức tạp của Core Banking, đây là vũ khí duy nhất để loại bỏ các vòng lặp ngoài ứng dụng và các cấu trúc Self-Join gây sập CPU.

## Nguồn Tham Khảo
- [[raw/articles/module-03-mắt-thần-cbo-thuật-tu-tiên-bằng-dữ-liệu-sql-tuning.md]]
