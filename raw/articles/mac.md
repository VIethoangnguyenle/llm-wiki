---
title: "Các mô hình kiểm soát truy cập bắt buộc (Mandatory Access Control - MAC)"
source: "local"
date_added: 2026-04-23
tags: [articles, abac, mac]
aliases: [mac]
status: draft
summary: "Trình bày các mô hình MAC cung cấp mức độ bảo mật cao hơn DAC."
---

# Các mô hình kiểm soát truy cập bắt buộc (Mandatory Access Control - MAC)

Bài viết này trình bày các mô hình MAC, cung cấp mức độ bảo mật cao hơn so với DAC bằng cách kiểm soát quyền truy cập bởi một cơ quan trung tâm thay vì người dùng.

## MAC vs. DAC

- DAC: Người dùng có quyền quyết định ai có thể truy cập vào các đối tượng họ kiểm soát.

- MAC: Các quyết định về quyền truy cập được thực hiện bởi một cơ quan trung tâm, thường là quản trị viên.

## Các mô hình MAC

- **Bảo mật đa mức (Multilevel Security - MLS)**: Mục tiêu là hạn chế luồng thông tin từ thực thể có mức bảo mật cao hơn sang thực thể có mức bảo mật thấp hơn.

- **Bức tường Trung Quốc (Chinese Wall Policy)**: Mục tiêu là ngăn chặn sự rò rỉ thông tin trái phép có thể dẫn đến xung đột lợi ích.

- **Kiểm soát truy cập dựa trên vai trò (Role-Based Access Control - RBAC)**: Mục tiêu là quản lý quyền truy cập thông qua các vai trò được phép cho người dùng.

## Mô hình bảo mật đa mức (MLS)

- Mức bảo mật: Được gán cho người dùng, đối tượng và các tiến trình hoạt động thay mặt người dùng.

- Phân cấp: Mức bảo mật được sắp xếp theo thứ bậc (ví dụ: Không mật, Bí mật, Tuyệt mật) và theo danh mục (ví dụ: NATO, hạt nhân).

- Quan hệ thống trị: Mức bảo mật cao hơn thống trị mức bảo mật thấp hơn.

- Tính chất bảo mật:
    - Tính chất đơn giản: Cho phép chủ thể đọc đối tượng nếu mức bảo mật của chủ thể thống trị mức bảo mật của đối tượng.
    - *Tính chất* : Cho phép chủ thể ghi vào đối tượng nếu mức bảo mật của đối tượng thống trị mức bảo mật của chủ thể.

- Tính chất ổn định: Giữ nguyên mức bảo mật của chủ thể và đối tượng trong khi truy cập.

- Kênh ẩn: Thông tin có thể bị rò rỉ thông qua các kênh ẩn, ví dụ như kết hợp thông tin từ các mức bảo mật thấp hơn để suy luận ra thông tin ở mức bảo mật cao hơn.

## Bức tường Trung Quốc (Chinese Wall Policy)

- Mục tiêu: Ngăn chặn xung đột lợi ích trong các hoạt động tư vấn tài chính.

- Thực thể: Chủ thể, đối tượng, nhãn bảo mật.

- Nhãn bảo mật: Xác định lớp xung đột lợi ích (COI) và tập dữ liệu công ty (CD) của mỗi đối tượng.

- Quy tắc:
    - Quy tắc đọc: Chủ thể có thể đọc đối tượng nếu đối tượng nằm trong cùng CD với đối tượng đã đọc trước đó hoặc đối tượng thuộc về lớp COI mà chủ thể chưa đọc bất kỳ đối tượng nào.
    - Quy tắc ghi: Chủ thể có thể ghi vào đối tượng nếu chủ thể có thể đọc đối tượng theo quy tắc đọc và không có đối tượng nào có thể được đọc trong CD khác với CD mà yêu cầu ghi.

## Kiểm soát truy cập dựa trên vai trò (RBAC):

- Thực thể: Người dùng, vai trò, quyền hạn, phiên, thao tác, đối tượng.

- Vai trò: Đại diện cho một chức năng công việc hoặc chức danh công việc, kèm theo quyền hạn cụ thể.

- Quyền hạn: Đại diện cho một thao tác hoặc chế độ truy cập vào một hoặc nhiều đối tượng.

- Phiên: Kết nối người dùng với một hoặc nhiều vai trò.

- Nguyên tắc ít đặc quyền: Người dùng chỉ được cấp quyền hạn cần thiết để thực hiện công việc.

- Phân cấp vai trò: Vai trò cấp cao hơn có thể thừa kế quyền hạn của vai trò cấp thấp hơn.

- Phân tách trách nhiệm (Separation of Duty - SoD): Ngăn chặn một người dùng có quyền hạn quá lớn, yêu cầu nhiều người dùng tham gia vào các giao dịch nhạy cảm.

## Kết luận:

> Các mô hình MAC cung cấp mức độ bảo mật cao hơn so với DAC, phù hợp với các môi trường yêu cầu bảo mật nghiêm ngặt. MLS là một mô hình bảo mật đa mức điển hình, trong khi Chinese Wall Policy tập trung vào việc ngăn chặn xung đột lợi ích. RBAC là một mô hình linh hoạt, sử dụng vai trò để quản lý quyền truy cập, có thể mô phỏng DAC và MLS.