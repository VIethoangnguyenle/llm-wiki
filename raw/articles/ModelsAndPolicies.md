---
title: "Kiểm soát truy cập: Discretionary vs. Mandatory"
source: "local"
date_added: 2026-04-23
tags: [articles, abac, dac, mac]
aliases: []
status: draft
summary: "Phân tích sự khác biệt giữa hai mô hình kiểm soát truy cập DAC và MAC."
---

# Kiểm soát truy cập: Discretionary vs. Mandatory

Bài viết này phân tích hai loại chính sách kiểm soát truy cập phổ biến: Discretionary Access Control (DAC) và Mandatory Access Control (MAC).

## Discretionary Access Control (DAC):

- **Quyền hạn**: Cho phép người dùng hệ thống quyết định ai có thể truy cập vào các đối tượng họ kiểm soát.

- **Tính linh hoạt**: Người dùng có thể tự do điều chỉnh quyền truy cập cho người khác.

- **Ví dụ**: Một thư mục trên máy tính, nơi chủ sở hữu có thể cấp quyền đọc, ghi hoặc thực thi cho người khác.

## Mandatory Access Control (MAC):

- **Quyền hạn**: Quyết định về việc cấp quyền truy cập được thực hiện bởi một cơ quan trung tâm, không phải bởi chủ sở hữu của đối tượng.

- **Bảo mật cao**: Giúp đảm bảo rằng dữ liệu nhạy cảm chỉ được truy cập bởi những người được phép.

- **Ví dụ**: Hệ thống quân sự, nơi mức độ bảo mật được xác định bởi các quy định nghiêm ngặt về quyền truy cập.

 Sự khác biệt:

- **DAC**: Người dùng tự quyết định quyền truy cập.

- **MAC**: Quyết định được đưa ra bởi một cơ quan trung tâm.

## Mô hình kiểm soát truy cập:

- **DAC**: Là một lớp rộng lớn bao gồm nhiều mô hình kiểm soát truy cập.

- **MAC**: Là mô hình bổ sung cho DAC, cung cấp mức độ bảo mật cao hơn.

## Mô hình kiểm soát truy cập:

- **Mô hình**: Là một phương pháp trừu tượng hóa chính sách kiểm soát truy cập, giúp định nghĩa cách thức truy cập được quản lý.

- **Mục tiêu**: Cung cấp một khuôn khổ logic để kiểm soát truy cập, cho phép xác minh sự tuân thủ chính sách.

- **Chính sách**: Là tập hợp các quy tắc và hướng dẫn được xác định bởi tổ chức để quản lý quyền truy cập.

Sự khác biệt:

- **Mô hình**: Trừu tượng, định nghĩa logic và tính chất.
- **Chính sách**: Cụ thể, hướng dẫn và có thể không đầy đủ.

## Kết luận:

- **DAC**: Phù hợp cho các môi trường nơi sự linh hoạt và kiểm soát bởi người dùng là ưu tiên.
- **MAC**: Phù hợp cho các môi trường yêu cầu bảo mật cao, nơi dữ liệu nhạy cảm cần được bảo vệ.
- **Mô hình kiểm soát truy cập**: Cung cấp một khuôn khổ để xác định và thực thi chính sách kiểm soát truy cập.

Lưu ý:

> Các mô hình kiểm soát truy cập được thiết kế ở cấp độ trừu tượng, không bao gồm các cơ chế bảo mật cụ thể để thực hiện mô hình.
Các khía cạnh triển khai được xem xét thông qua các quy trình bảo đảm thông tin (ví dụ: tuân thủ mô hình và chính sách).