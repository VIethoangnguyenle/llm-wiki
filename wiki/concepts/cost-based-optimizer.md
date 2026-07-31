---
title: "Cost-Based Optimizer"
source: "compiled"
date_added: 2026-04-23
tags: [concept, database, sql-tuning, oracle]
aliases: [CBO, Bộ tối ưu hóa dựa trên chi phí]
status: canonical
related:
  - "[[oracle-database]]"
  - "[[analytic-functions]]"
summary: "Trí tuệ nhân tạo lõi của Oracle Database, chuyên tính toán chi phí để phân luồng truy vấn tối ưu."
---

# Cost-Based Optimizer

## Định Nghĩa
Cost-Based Optimizer (CBO) là công cụ AI cốt lõi nằm sâu trong hệ quản trị [[oracle-database|Oracle Database]]. Nó đảm nhận vai trò phân tích các câu lệnh SQL đầu vào, tính toán mọi kịch bản thực thi có thể xảy ra và chọn lựa một "Kế hoạch thực thi" (Execution Plan) tốn ít "Chi phí" nhất. Các thông số chi phí này bao gồm I/O đọc ổ cứng, thời gian CPU và việc sử dụng bộ nhớ.

## Cơ Chế Cây Truy Vấn (Join Trees)
Khi yêu cầu nối dữ liệu nhiều bảng (Ví dụ: Khách hàng -> Đơn hàng -> Giao dịch), CBO không xử lý cùng một lúc mà thiết lập một băng chuyền logistics dạng cây (Join Trees).

- **Left Deep Join Tree (Nối sâu trái):** Mô hình lắp ráp truyền thống quét từ trái sang phải. Dữ liệu từ bảng đầu tiên (Driving Table) đổ vào để nối với bảng thứ hai. Việc CBO xác định sai bảng bắt đầu sẽ dẫn đến thảm họa nút thắt cổ chai, khiến băng chuyền chết nghẽn vĩnh viễn. CBO có nhiệm vụ phân tích kích cỡ bảng và chọn thứ tự chính xác.

## Các Phương Thức Phép Nối (Join Methods)
CBO sở hữu các thuật toán nối dữ liệu thích ứng dựa vào số lượng khối dữ liệu trên đường truyền:

1. **Nested Loops (Vòng lặp lồng nhau):** Hoạt động hiệu quả cho danh sách bản ghi nhỏ. Một vòng lặp quét từng phần tử ở bảng A và rà soát ở bảng B (nhờ vào Index).
2. **Hash Join (Phép nối băm):** Là phương pháp cho Big Data. Khi đối mặt hàng chục triệu bản ghi, CBO sẽ gom chúng ném vào vùng nhớ đệm, băm nhỏ từng phân vùng vào bảng băm (Hash Table) riêng biệt để ghép cặp.
3. **Sort Merge Join:** Trong tình huống dung lượng bảng quá khổng lồ, CBO sẽ chuyển qua Sắp xếp (Sort) dữ liệu cả hai bên trước khi tiến hành quá trình Trộn (Merge).

## Cạm Bẫy Ma Trận Nội Ngoại (Logical Joins Trap)
Việc hiểu CBO đòi hỏi các kỹ sư viết SQL tuân thủ những nguyên lý nghiêm ngặt nhằm tránh việc làm sập sơ đồ truy vấn:
- Sử dụng sai điều kiện `WHERE` trong `LEFT JOIN` (đặt điều kiện bảng phụ nằm ngoài cụm `ON`) sẽ khiến CBO tự ý gạt bỏ dữ liệu `NULL`, biến `LEFT JOIN` thành `INNER JOIN`.
- Viết `RIGHT JOIN` không những không tối ưu mà còn gây khó khăn về luồng phân tích nhận thức cho con người (Logic đọc code thường tiến dần từ trái sang phải).

## Nguồn Tham Khảo
- [[raw/articles/module-03-mắt-thần-cbo-thuật-tu-tiên-bằng-dữ-liệu-sql-tuning.md]]
