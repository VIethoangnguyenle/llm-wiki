---
title: "Spring Validation"
source: "compiled"
date_added: 2026-04-24
tags: [concept, java, spring, validation]
aliases: [spring-validation, bean-validation, jakarta-bean-validation]
status: draft
related:
  - "[[spring-ioc-di]]"
  - "[[java-immutability]]"
summary: "Cơ chế kiểm duyệt dữ liệu trong Spring Boot, kết hợp giữa Jakarta Bean Validation và Hibernate Validator theo mô hình phòng thủ đa tầng."
---

# Spring Validation

Cơ chế kiểm duyệt dữ liệu (Data Validation) trong Spring Boot là một hệ thống phòng thủ đa tầng nhằm ngăn chặn dữ liệu không hợp lệ (dirty data) xâm nhập sâu vào hệ thống. Kiến trúc này được xây dựng dựa trên tiêu chuẩn thiết kế của Jakarta Bean Validation và sự triển khai của Hibernate Validator.

## Kiến Trúc Cốt Lõi

Validation trong Spring không phải là một khối đơn nhất mà được cấu thành từ ba lớp chính:
- **Specification (Đặc tả):** Jakarta Bean Validation (JSR-380) cung cấp bộ API và các chú thích (annotations) chuẩn hóa.
- **Implementation (Triển khai):** Hibernate Validator đóng vai trò là bộ mã thực thi tham chiếu (Reference Implementation) cốt lõi.
- **Integration (Tích hợp):** Spring Boot hỗ trợ tích hợp tự động (Auto-configuration) thông qua `LocalValidatorFactoryBean`, giúp kết nối hai thành phần trên vào ngữ cảnh (context) của ứng dụng.

## Phân Biệt @Valid và @Validated

Sự khác biệt giữa hai annotation này là một khía cạnh mang tính quyết định trong kiến trúc Spring Validation:

- **`@Valid` (JSR-303 Standard):** Là tiêu chuẩn chuẩn hóa của ngôn ngữ Java, thường được sử dụng bên trong các đối tượng Data Transfer Object (DTO) để kích hoạt cơ chế duyệt biểu đồ đối tượng (Graph Traversal) đối với các thuộc tính lồng nhau (Nested properties).
- **`@Validated` (Spring Framework AOP):** Là tính năng độc quyền do Spring cung cấp. Annotation này hỗ trợ Validation Groups (phân nhóm quy tắc theo ngữ cảnh) và có khả năng kiểm duyệt trực tiếp trên các tham số phương thức (Method Parameters) hoặc biến đường dẫn (Path Variables) thông qua cơ chế Proxy của AOP.

## Mẫu Thiết Kế (Validation Patterns)

Trong các hệ thống phân tán, Spring Validation thường được triển khai theo một số mẫu tư duy kiến trúc:

- **Nested Validation:** Sử dụng `@Valid` trên các đối tượng con để chỉ thị Spring tiếp tục duyệt sâu xuống biểu đồ phân cấp của DTO.
- **Validation Groups:** Cho phép tái sử dụng DTO trong nhiều ngữ cảnh khác nhau (ví dụ: tạo mới hoặc cập nhật) bằng cách áp dụng các quy tắc khác nhau thông qua thuộc tính `groups`.
- **Global Exception Handling:** Lỗi kiểm duyệt (`MethodArgumentNotValidException` và `ConstraintViolationException`) thường được thu gom bởi `@ControllerAdvice` để định dạng thành cấu trúc JSON chuẩn trước khi phản hồi về cho hệ thống phía máy khách.

## Liên Hệ Và Ứng Dụng Thực Tiễn

Việc thiết kế hệ thống DTO kết hợp với Spring Validation đóng vai trò quan trọng trong việc bảo vệ tính toàn vẹn của dữ liệu. Giới kiến trúc sư phần mềm thường ưu tiên phân tách DTO (ví dụ: `CreateUserRequest` và `UpdateUserRequest`) thay vì lạm dụng Validation Groups nhằm tuân thủ nguyên tắc Single Responsibility. Ngoài ra, việc sử dụng [[java-immutability|Java Records]] làm DTO kết hợp với Spring Validation đang trở thành tiêu chuẩn mới, đem lại tính bất biến (Immutability) và độ an toàn luồng (Thread-safety) tự nhiên.

## Nguồn Tham Khảo
- `raw/papers/làm-chủ-spring-validation-chiến-lược-phòng-thủ-đa-tầng.md`
