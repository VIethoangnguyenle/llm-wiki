---
title: "NGAC Security Model"
source: "raw/ngac/ngac.md"
date_added: 2026-07-31
tags: [concept, security, access-control, ngac, formal-model]
aliases: [NGAC Security Model, Mô hình bảo mật NGAC, Policy Elements]
status: draft
related:
  - "[[next-generation-access-control]]"
  - "[[ngac-architecture]]"
  - "[[ngac-permission-graph]]"
summary: "Đặc tả toán học của NGAC (INCITS 565-2020): tập policy element, bốn quan hệ cấu hình và hai quan hệ dẫn xuất tạo nên authorization state."
---

## Định Nghĩa

Mô hình bảo mật (security model) là nửa hình thức của chuẩn **INCITS 565-2020**, song hành với nửa còn lại là [[ngac-architecture|kiến trúc thực thi]]. Trong khi kiến trúc mô tả các thực thể chức năng trao đổi thông tin ra sao, mô hình bảo mật định nghĩa **authorization state** — trạng thái ủy quyền — bằng ngôn ngữ tập hợp và quan hệ. Chuẩn đặc tả trạng thái này bằng ký pháp hình thức Z, và mọi lệnh quản trị đều được định nghĩa như một phép chuyển trạng thái trên đó.

Cách tiếp cận này là điểm phân biệt NGAC với [[attribute-based-access-control|ABAC]] dạng biểu thức điều kiện: quyền truy cập không được tính từ việc đánh giá một mệnh đề logic trên thuộc tính, mà từ việc duyệt đường đi trên một đồ thị đã được cấu hình sẵn.

## Policy Element — Đơn Vị Cơ Sở

Tập policy element gộp bốn loại thực thể:

```
PE = U ∪ UA ∪ OA ∪ PC
```

trong đó `U` là user, `UA` là user attribute, `OA` là object attribute (bao hàm cả object), và `PC` là policy class. Chuẩn dùng hai designator trừu tượng phía trên: *attribute* trỏ tới `UA` hoặc `OA`, còn *container* trỏ tới attribute hoặc policy class. Mọi tài nguyên số trong hệ thống đều phải được quy hoạch về một trong các loại này trước khi NGAC có thể phát biểu bất kỳ điều gì về nó.

## Bốn Quan Hệ Cấu Hình

Quan hệ cấu hình (configured relation) là thành phần do quản trị viên thiết lập trực tiếp.

**Assignment** định nghĩa thứ tự cấu trúc giữa các policy element. Chuẩn ràng buộc nó là quan hệ hai ngôi trên `PE` thỏa bốn tính chất: bất phản xạ, biểu diễn đồ thị có hướng không chu trình, liên thông tới policy class (tồn tại chuỗi assignment từ mọi phần tử của `PE \ PC` tới một phần tử của `PC`), và cấm gán từ object attribute sang object. Miền giá trị bị giới hạn cụ thể:

```
ASSIGN ⊆ (U×UA) ∪ (UA×UA) ∪ (OA×OA) ∪ (UA×PC) ∪ (OA×PC)
```

Ràng buộc này tách bạch nhánh user khỏi nhánh object ngay ở tầng kiểu. Đồ thị `G = (PE, ASSIGN)` được gọi là **policy element diagram**. Trên đó, *path* là chuỗi các phần tử mà mỗi cặp liên tiếp tạo thành một assignment; *containment* là quan hệ tồn tại path từ phần tử này tới phần tử kia. Hai hàm toàn phần `Users(ua)` và `Objects(oa)` trả về tập user, tập object nằm trong một attribute — định nghĩa qua bao đóng bắc cầu của `ASSIGN`, tức [[ngac-transitive-closure|transitive closure]].

**Association** phân bổ access right giữa các policy element, cho phép một mode truy cập. **Prohibition** là quan hệ đối ngẫu: cũng phân bổ access right nhưng để *vô hiệu hóa* mode truy cập. Sự tồn tại của một quan hệ cấm riêng biệt cho phép NGAC biểu diễn chính sách phủ định mà không cần đảo ngược logic của association.

**Obligation** đưa yếu tố thời gian vào mô hình. Nó là quan hệ ba ngôi:

```
OBLIG ⊆ U × PATTERN × RESPONSE
```

Mỗi bộ ba gắn một *event pattern* (điều kiện) với một *event response* (chuỗi hành động quản trị) và user đứng tên ủy quyền. Khi một truy cập thành công khớp pattern, response được thực thi và chính sách tự thay đổi. Chuẩn cố ý **không quy định** văn phạm cho pattern và response — chúng chỉ được yêu cầu well-formed theo văn phạm `GP` và `GR` mà tổ chức tự chọn. Điều kiện ràng buộc là user định nghĩa obligation phải đủ thẩm quyền thực thi toàn bộ response tại thời điểm pattern khớp, nếu không response bị bỏ qua.

## Hai Quan Hệ Dẫn Xuất

Quan hệ dẫn xuất (derived relation) không được cấu hình mà được tính ra từ các quan hệ cấu hình. **Privilege relation** gồm các bộ biểu thị access right mà một policy element thực sự nắm giữ đối với một policy element khác. **Restriction relation** gồm các access right mà một policy element *có thể* nắm giữ nhưng không được sử dụng — kết quả của prohibition chồng lên association. Quyết định truy cập cuối cùng là phép tra cứu trên hai quan hệ này.

## Administrative Commands

Chuẩn định nghĩa mỗi lệnh quản trị như một schema Z mô tả phép chuyển authorization state, chứ không phải như câu lệnh lập trình. Các lệnh chỉ truy vấn hoặc tra cứu không được đặc tả, vì chúng không làm thay đổi trạng thái. Ràng buộc này giữ cho tính toàn vẹn của mô hình: mọi thay đổi chính sách — dù đến từ thao tác quản trị trực tiếp hay từ response của một obligation được kích hoạt — đều đi qua cùng một tập phép chuyển đã được chứng minh bảo toàn các tính chất của `ASSIGN`.

## Liên Hệ / Ứng Dụng

Trong triển khai thực tế, chi phí lớn nhất không nằm ở việc hiện thực bốn quan hệ mà ở việc duyệt bao đóng bắc cầu khi kiểm tra quyền. [[ngac-practical-implementation|Triển khai thực tế]] cho thấy hướng xử lý phổ biến là lược bỏ bớt node object và kết hợp đồ thị quyền với bảng SQL đã denormalize, đánh đổi tính thuần khiết của mô hình lấy độ trễ truy vấn.

## Nguồn Tham Khảo

- [[raw/ngac/ngac.md]] — INCITS 565-2020, mục 3.1.2, 3.1.3, 6.2–6.4
