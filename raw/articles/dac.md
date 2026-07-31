---
title: "Kiểm soát truy cập tùy ý (Discretionary Access Control - DAC)"
source: "local"
date_added: 2026-04-23
tags: [articles, abac, dac]
aliases: [dac]
status: draft
summary: "Bài viết thảo luận về mô hình kiểm soát truy cập tùy ý DAC dựa trên ma trận truy cập."
---
# Kiểm soát truy cập tùy ý (Discretionary Access Control - DAC)

Bài viết này thảo luận về mô hình DAC, một trong những mô hình kiểm soát truy cập phổ biến nhất, dựa trên ma trận truy cập.

## Ma trận truy cập

- **Khái niệm**: Được giới thiệu lần đầu tiên như một mô hình DAC, cho phép người dùng kiểm soát quyền truy cập của người khác vào các đối tượng.

- **HRU (Harrison, Ruzzo, Ullman)**: Mô hình được chính thức hóa và sử dụng để phân tích độ phức tạp của việc tính toán các tính chất an toàn, được phát hiện là không thể quyết định.

- **Tính trung lập**: Mô hình HRU không thiên vị về chính sách và có thể được sử dụng để thể hiện các chính sách kiểm soát truy cập không phải là tùy ý.

## DAC trong thực tế

- **Quyền sở hữu**: Chủ sở hữu của đối tượng có quyền kiểm soát truy cập của người khác vào đối tượng đó.

- **Quyền hạn quản trị**: Chủ sở hữu có thể tạo, sửa đổi hoặc xóa các mục kiểm soát truy cập liên quan đến các đối tượng của họ.

- **Chuyển giao quyền sở hữu**: Chủ sở hữu có thể chuyển giao quyền sở hữu đối tượng cho người khác.

## Thực hiện DAC

- **Danh sách khả năng (Capability List)**: Mỗi đối tượng có một danh sách khả năng, chứa các quyền truy cập được phép cho các đối tượng.

    - Ưu điểm: Dễ dàng kiểm tra các quyền truy cập được phép cho một đối tượng cụ thể.

    - Nhược điểm: Khó kiểm tra các đối tượng có thể truy cập bởi một đối tượng cụ thể.

- **Danh sách kiểm soát truy cập (Access Control List - ACL)**: Mỗi đối tượng có một ACL chứa các người dùng và quyền truy cập của họ đối với đối tượng đó.

    - Ưu điểm: Dễ dàng kiểm tra các người dùng có quyền truy cập vào đối tượng và quyền truy cập của họ.
    - Nhược điểm: Khó quản lý ACL khi số lượng người dùng và quyền truy cập tăng lên.

## Ưu điểm của DAC

- Linh hoạt: Cho phép người dùng kiểm soát quyền truy cập vào các đối tượng của mình.
- Phổ biến: Được sử dụng rộng rãi trong các doanh nghiệp và tổ chức chính phủ.

## Nhược điểm của DAC

- Thiếu kiểm soát: Chủ sở hữu có thể không kiểm soát được quyền truy cập vào đối tượng sau khi đã cấp quyền cho người khác.

- Vấn đề về Trojan horse: DAC có thể bị tấn công bởi Trojan horse, cho phép các tiến trình hoạt động ẩn danh và thực hiện các hành động trái phép.

## Kết luận

> DAC là một mô hình kiểm soát truy cập linh hoạt, nhưng nó có những nhược điểm tiềm ẩn. Khi sử dụng DAC, cần lưu ý đến các vấn đề về kiểm soát quyền truy cập và bảo vệ khỏi các cuộc tấn công Trojan horse.