---
title: "PL/SQL"
source: "compiled"
date_added: 2026-04-23
tags: [concept, database, oracle, programming-language]
aliases: [Procedural Language/SQL]
status: canonical
related:
  - "[[oracle-database]]"
summary: "Ngôn ngữ mở rộng quy trình độc quyền của Oracle, đóng vai trò điều phối logic nghiệp vụ ở tầng dữ liệu."
---

# PL/SQL

## Định Nghĩa
PL/SQL (Procedural Language/SQL) là ngôn ngữ lập trình độc quyền của [[oracle-database|Oracle Database]], được tạo ra nhằm mở rộng khả năng của SQL truyền thống bằng các khối cấu trúc quy trình (vòng lặp, rẽ nhánh, biến trạng thái). Khác với các hệ thống chỉ truyền và nhận dữ liệu thuần túy, việc ứng dụng PL/SQL cho phép các tổ chức nhúng các logic nghiệp vụ phức tạp trực tiếp vào bên trong tầng dữ liệu. Việc xử lý cục bộ ngay tại Database giúp hệ thống hạn chế hàng triệu vòng gọi qua mạng (Network Roundtrips) tới các ứng dụng backend (như Node.js hay Java).

## Cấu Trúc Khối Lệnh PL/SQL

### Function (Hàm)
Được thiết kế đóng vai trò như một "cảm biến tinh khiết" (Purity), Function có trách nhiệm xử lý tham số và luôn luôn trả về một giá trị thông qua lệnh `RETURN`. Do tính chất này, Function có thể được nhúng thẳng vào các câu lệnh SQL truyền thống. Tuy nhiên, Function bị ràng buộc bởi các luật nghiêm ngặt: cấm thay đổi dữ liệu (`INSERT`, `UPDATE`, `DELETE`). Khả năng đặc biệt của Oracle là việc cho phép tạo Index chạy thẳng trên Function (Function-Based Indexes), biến các cảm biến này thành radar dò tìm dữ liệu ở tốc độ cao.

### Procedure (Thủ tục)
Hoạt động như "cánh tay rô-bốt", Procedure thực thi logic nghiệp vụ và thay đổi trực tiếp dữ liệu mà không cần trả về một giá trị đầu ra. Nó nắm giữ quyền kiểm soát giao dịch (Transaction Control) cho phép xác nhận (`COMMIT`) hay hoàn tác (`ROLLBACK`) hàng vạn bản ghi. Dù không thể nhúng vào một câu lệnh `SELECT`, cấu trúc mở này cung cấp một năng lực thao túng khối lượng dữ liệu khổng lồ.

### Package (Gói)
Package là kiến trúc tổ chức cao nhất, "bọc thép" toàn bộ các Function và Procedure. Thiết kế của một Package chia làm hai phần:
1. **Specification (Bản đặc tả):** Đóng vai trò là hợp đồng giao diện (API Contract), công bố các định nghĩa hàm cho tầng ứng dụng giao tiếp bên ngoài.
2. **Body (Thân gói):** Chứa các luồng thuật toán nội bộ. Cấu trúc ẩn giấu thông tin này cho phép thay đổi thuật toán ở tầng Body hàng ngàn lần mà không làm sập (Invalidated) các đoạn mã nguồn phụ thuộc ở ứng dụng ngoại vi.

## Liên Hệ / Ứng Dụng
Trong kiến trúc ngân hàng (Core Banking), PL/SQL Package thường được tinh chỉnh bằng các chiến lược lưu trữ (Pinning) vào bộ nhớ Shared Pool để chống lại sự loại bỏ của hệ thống quản lý bộ nhớ LRU khi tải lớn. Song song đó, lập trình viên phải đối mặt với nguy cơ dữ liệu chéo quyền (do Connection Pooling tái sử dụng phiên làm việc qua Session State) và thiết kế hệ thống báo cáo lỗi có chủ đích thông qua khối cấu trúc Exception Handling (`RAISE_APPLICATION_ERROR`).

## Nguồn Tham Khảo
- [[raw/articles/module-02-hệ-thần-kinh-plsql-bộ-não-điều-phối-giao-dịch.md]]
