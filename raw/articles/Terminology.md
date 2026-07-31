---
title: "Kiểm soát truy cập: Hiểu rõ các khái niệm cơ bản"
source: "local"
date_added: 2026-04-23
tags: [articles, abac, terminology]
aliases: []
status: draft
summary: "Trình bày các khái niệm cơ bản như xác thực, ủy quyền, chủ thể, quyền truy cập và đối tượng."
---
# Kiểm soát truy cập: Hiểu rõ các khái niệm cơ bản

Trong lĩnh vực kiểm soát truy cập, người dùng có thể là con người hoặc các thực thể phi người (ví dụ: chương trình hoặc thiết bị) tương tác với hệ thống máy tính. Mỗi người dùng có một danh tính duy nhất và được ánh xạ đến chỉ một thực thể.

## Phân biệt xác thực và ủy quyền:

- **Xác thực** là quá trình xác minh danh tính của người dùng (ví dụ: bằng mật khẩu, dấu vân tay,...) để đảm bảo người đó là người họ tuyên bố. Xác thực thường là điều kiện tiên quyết để cho phép truy cập vào tài nguyên.

- **Ủy quyền** là việc cấp hoặc từ chối quyền truy cập cho người dùng dựa trên vai trò và quyền hạn của họ.
Hai khái niệm này thường bị nhầm lẫn do mối liên hệ chặt chẽ giữa chúng. Ủy quyền hợp lệ phụ thuộc vào việc xác thực thành công.

## Mô hình kiểm soát truy cập cổ điển:

Mô hình này được định nghĩa dựa trên ba thành phần:

- **Chủ thể**: Đại diện cho người dùng và bất kỳ tiến trình hệ thống hoặc thực thể nào có thể hoạt động thay mặt người dùng. Chủ thể là các thực thể chủ động trong hệ thống có thể tác động đến đối tượng, truyền tải thông tin giữa các đối tượng hoặc thay đổi trạng thái truy cập của hệ thống.
- **Quyền truy cập**: Quy định những gì người dùng có thể làm với đối tượng (ví dụ: đọc, ghi, thực thi,...).
- **Đối tượng**: Là các tài nguyên cần được bảo vệ trong hệ thống (ví dụ: tập tin, cổng mạng, máy in,...).

Các khái niệm quan trọng:

- **Quyền hạn**: Là quyền hạn cụ thể của người dùng đối với một đối tượng cụ thể.
- **Hoạt động**: Là các hành động có thể được thực hiện trên nội dung của đối tượng (ví dụ: đọc, ghi, thực thi) hoặc trên dữ liệu kiểm soát truy cập (ví dụ: tạo, xóa chính sách,...).
- **Chính sách**: Quy định cách người dùng có thể truy cập vào tài nguyên.
- **Bộ quyền**: Là tập hợp các quyền hạn của một người dùng.

Phân loại hoạt động và quyền:

**Hoạt động**:
- Hoạt động tài nguyên: Các thao tác trực tiếp trên đối tượng (ví dụ: đọc, ghi).
- Hoạt động quản trị: Các thao tác liên quan đến việc tạo, sửa đổi và xóa chính sách (ví dụ: cấp quyền, thu hồi quyền).

**Quyền**:
- Quyền tài nguyên: Cấp quyền cho người dùng thực hiện hoạt động tài nguyên (ví dụ: quyền đọc, quyền ghi).
- Quyền quản trị: Cấp quyền cho người dùng thực hiện hoạt động quản trị (ví dụ: quyền tạo chính sách, quyền sửa đổi chính sách).

Lưu trữ quyền hạn:

Thông thường, quyền hạn không được lưu trữ trực tiếp dưới dạng đơn giản (u, ar, o) mà được biểu diễn gián tiếp bằng các hình thức khác (ví dụ: danh sách kiểm soát truy cập, danh sách khả năng, vai trò và mối quan hệ giữa chúng).

Tóm lại:
> Hiểu rõ các khái niệm cơ bản về kiểm soát truy cập, xác thực và ủy quyền là điều cần thiết để xây dựng hệ thống bảo mật hiệu quả. Việc lựa chọn mô hình kiểm soát truy cập phù hợp phụ thuộc vào yêu cầu cụ thể của hệ thống và mức độ bảo mật cần thiết.