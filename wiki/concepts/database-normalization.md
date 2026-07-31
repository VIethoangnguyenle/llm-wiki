---
title: "Database Normalization"
source: "compiled"
date_added: 2026-04-23
tags: [concept, database, data-modeling]
aliases: [Chuẩn hóa cơ sở dữ liệu, 1NF, 2NF, 3NF, Chuẩn hóa dữ liệu]
status: canonical
related:
  - "[[oracle-database]]"
summary: "Tiến trình tổ chức cấu trúc cơ sở dữ liệu để giảm thiểu dị thường và loại bỏ dữ liệu dư thừa."
---

# Database Normalization

## Định Nghĩa
Chuẩn hóa cơ sở dữ liệu (Database Normalization) là một quá trình thiết kế cấu trúc lưu trữ nhằm giảm thiểu sự lặp lại của dữ liệu và loại bỏ các "Dị thường dữ liệu" (Anomalies) làm hỏng tính toàn vẹn của hệ thống. Quá trình này áp dụng một chuỗi các bộ lọc luật khắt khe, được gọi là các dạng chuẩn (Normal Forms - NF), để tách dữ liệu thô thành các bảng liên kết logic, đảm bảo mỗi bảng mô tả chính xác một thực thể duy nhất.

## Bóng Ma Dị Thường Dữ Liệu
Thiết kế dữ liệu tồi theo kiểu dồn toàn bộ thông tin vào một cấu trúc dữ liệu phẳng (flat files) là nguyên nhân tạo ra các dị thường:
- **Dị thường chèn (Insertion Anomaly):** Không thể thêm dữ liệu về một thực thể độc lập vì thiết kế bắt buộc nó phải gắn với một sự kiện chưa xảy ra. (Ví dụ: Không thể lưu thông tin một giảng viên mới vào cơ sở dữ liệu nếu họ chưa được phân công lớp dạy).
- **Dị thường cập nhật (Update Anomaly):** Bắt buộc hệ thống phải sửa đổi thông tin ở nhiều nơi (hàng chục, hàng trăm bản ghi) thay vì một nơi duy nhất. Việc sửa đổi bị ngắt quãng do sự cố sẽ khiến dữ liệu mất đồng bộ vĩnh viễn.
- **Dị thường xóa (Deletion Anomaly):** Khi xóa một dữ kiện giao dịch, vô tình làm biến mất toàn bộ thông tin về chủ thể liên quan đến giao dịch đó khỏi kho lưu trữ.

## Các Dạng Chuẩn Cốt Lõi (1NF - 3NF)

### 1NF (Dạng chuẩn 1)
Yêu cầu mọi trường dữ liệu phải chứa các giá trị hạt nhân đơn nguyên (Atomic). Tuyệt đối cấm việc chứa nhiều giá trị phân cách (như mảng phân cách bằng dấu phẩy) trong một ô dữ liệu duy nhất, điều này ngăn cản việc tận dụng các kỹ thuật lập chỉ mục (Index) tìm kiếm siêu tốc.

### 2NF (Dạng chuẩn 2)
Chỉ áp dụng cho các cấu trúc bảng sử dụng Khóa chính kép (Composite Key). Yêu cầu mọi thuộc tính phi khóa phải phụ thuộc hoàn toàn vào *tất cả* các thành phần của khóa chính kép, chứ không được phép chỉ phụ thuộc vào một nửa thành phần của khóa. Phần dữ liệu thừa này phải được tách ra bảng riêng.

### 3NF (Dạng chuẩn 3)
Loại bỏ hoàn toàn sự phụ thuộc bắc cầu. Mọi cột thông tin phải phụ thuộc trực tiếp vào khóa chính. Ví dụ, nếu Đơn Hàng chứa thông tin Khách Hàng, thì thành phố nơi khách hàng sinh sống phải được chuyển sang bảng Khách Hàng thay vì lưu thẳng vào bảng Đơn Hàng.

## Liên Hệ / Ứng Dụng
Trong thực tiễn vận hành các hệ thống quản trị quy mô doanh nghiệp như [[oracle-database|Oracle]], lý thuyết chuẩn hóa trên giấy phải được chuyển tải thành các thiết kế ngôn ngữ định nghĩa dữ liệu (DDL) vật lý chính xác. Các kiểu dữ liệu (`VARCHAR2` thay vì `CHAR`) và việc bắt buộc tạo chỉ mục trên các khóa ngoại (Foreign Key) được sử dụng để duy trì hiệu suất tra cứu và ngăn chặn hiện tượng tắc nghẽn khóa toàn bảng (Deadlock) giữa bảng cha và con.

## Nguồn Tham Khảo
- [[raw/articles/module-00-bản-vẽ-khởi-nguyên-mã-nguồn-của-dị-thường-luật-3nf.md]]
