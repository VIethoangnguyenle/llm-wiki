---
title: "Lật Tẩy Hiểu Lầm Về `const`: Sự Thật Về Tính Bất Biến"
source: "D:\9. Learn\12. llm wiki\raw\articles\1.2.md"
date_added: 2026-04-23
tags: [notes]
status: draft
summary: ""
---

# Lật Tẩy Hiểu Lầm Về `const`: Sự Thật Về Tính Bất Biến

Trong JavaScript hằng ngày, chúng ta thường được khuyên là "hãy dùng `const` để khai báo hằng số không thể thay đổi". Lời khuyên này không sai, nhưng nó lại gây ra một lầm tưởng vô cùng phổ biến đối với các lập trình viên mới. Bài viết này sẽ lật tẩy bản chất thực sự của `const`, từ việc chặn gán lại (reassignment) đến tính bất biến (immutability) thực sự.

---

## 1. Lầm tưởng phổ biến: `const` tạo ra giá trị KHÔNG THỂ thay đổi?

Hầu hết chúng ta bắt đầu với suy nghĩ này. Khi làm việc với các kiểu dữ liệu nguyên thủy (primitive types) như `number`, `string`, hay `boolean`, lầm tưởng này có vẻ hoàn toàn đúng:

```javascript
// Khai báo một hằng số
const PI = 3.14;

// Cố gắng gán lại giá trị
PI = 3.14159; 

// ❌ LỖI! Uncaught TypeError: Assignment to constant variable.
```
Với các kiểu nguyên thuỷ, `const` hoạt động đúng y hệt như mong đợi ở nghĩa đen – nó ngăn chặn việc gán lại một giá trị mới.

Tuy nhiên, "vết nứt" trong lầm tưởng này bắt đầu xuất hiện khi chúng ta sử dụng `const` cho **Objects** hoặc **Arrays**!

---

## 2. Sự thật bất ngờ khi `const` "phản bội" bạn

Hãy xem xét đoạn code sau:

```javascript
const USER = {
  name: "Alice",
  role: "Developer"
};

// Thay đổi thuộc tính của đối tượng
USER.role = "Team Lead";

// Thêm một thuộc tính mới
USER.email = "alice@example.com";

console.log(USER.role); // Kết quả in ra: "Team Lead" 
```

**✅ Hoàn toàn hợp lệ! Không có một lỗi nào xảy ra cả.**

Rõ ràng, `const` không hề ngăn chặn việc thay đổi nội dung (mutation) của một đối tượng. Nội dung bên trong mảng và đối tượng được khai báo bằng `const` vẫn hoàn toàn có thể thay đổi. Vậy cơ chế thực sự ở đây là gì?

---

## 3. Gán Lại (Reassignment) vs. Thay Đổi (Mutation)

Chìa khóa để hiểu `const` nằm ở việc phân biệt rõ rệt giữa hai khái niệm: **Gán lại định danh của biến** và **Thay đổi nội dung** mà biến đó mang theo.

Hãy tưởng tượng biến được khai báo bằng `const` là một **chiếc hộp có dán nhãn**:
* **Gán Lại (Bị cấm):** Bạn đang bóc cái nhãn ở hộp cũ và cố dán sang một cái hộp hoàn toàn mới. `const` nghiêm cấm hành động này.
* **Thay Đổi (Được phép):** Mở nắp hộp cũ ra, cho thêm đồ vật vào, hoặc lấy bớt đồ vật ra. Chiếc nhãn vẫn dán ở cái hộp đó nên quy định không bị vi phạm! `const` không quan tâm bên trong hộp có gì.

### Cơ Chế Dưới Mui Xe: Giá Trị (Value) vs. Tham Chiếu (Reference)

Bản chất của vấn đề trên đến từ cách JavaScript lưu trữ dữ liệu vào bộ nhớ:
1. **Kiểu Nguyên Thủy (Primitives):** Biến lưu trữ trực tiếp *giá trị* (VD: `30`).
2. **Kiểu Mảng / Đối Tượng (References):** Biến lưu trữ một *tham chiếu* (một địa chỉ bộ nhớ định vị tới nơi object đang ở, VD: `0x1A2B`).

Từ tài liệu chính thức của MDN: 
> *"`const` creates an immutable reference to a value. It does not mean the value it holds is immutable — just that the variable identifier cannot be reassigned."*

Dịch nôm na: `const` chỉ tạo ra một **liên kết bất biến** tới một vùng nhớ. Nếu vùng nhớ đó chứa một đối tượng phức tạp, nội dung của nó vẫn là "biến dị" (mutable).

---

## 4. Đạt Được Tính Bất Biến Thực Sự Với `Object.freeze()`

Nếu `const` không thể bảo vệ đối tượng khỏi sự thay đổi, thì chúng ta làm thế nào để có một đối tượng cấu hình hoàn toàn "bất biến" (như `CONFIG`)?

Cứu tinh của chúng ta là phương thức tích hợp sẵn có của JavaScript: `Object.freeze()`. Hàm này nhận một đối tượng làm đầu vào và trả về chính nó nhưng trong một trạng thái "bị đóng băng". Bạn sẽ không thể thêm, xoá hay sửa giá trị thuộc tính.

```javascript
// Thay vì const đơn thuần:
const mutableUser = { name: "John" };
mutableUser.name = "Jane"; // Hợp lệ

// Kết hợp const với Object.freeze():
const immutableUser = Object.freeze({
  name: "John"
});

immutableUser.name = "Jane"; // ❌ Thao tác thất bại (Trong Strict Mode sẽ văng lỗi TypeError)
console.log(immutableUser.name); // Vẫn in ra "John"
```

### ⚠️ Lưu ý Cực Quan Trọng: Cẩn thận với Shallow Freeze!

`Object.freeze()` chỉ đóng băng ở mức bề mặt (cấp độ nông / shallow level). Nói cách khác, nó không hoạt động đệ quy sâu xuống bên dưới. Nếu trong đối tượng đóng băng lại chứa một đối tượng/mảng lồng nhau khác, thì "đứa con" đó vẫn hoàn toàn có thể thay đổi giá trị.

```javascript
const user = Object.freeze({
  name: "Admin",
  permissions: {
    canEdit: true,
    canDelete: false
  }
});

// Thất bại: Cấp nông bị đóng băng
user.name = "Super Admin"; 

// ✅ Thành công: Object lồng sâu bên trong vẫn có thể bị chỉnh sửa!
user.permissions.canDelete = true; 
```

> **🔥 Pro Tip:** Nếu bạn cần một đối tượng bất biến 100% đến mọi tầng lõi, bạn phải tự triển khai một hàm đệ quy để duyệt các thuộc tính đối tượng và thực thi `freeze` (cách này gọi là Deep Freeze), hoặc sử dụng các thư viện hỗ trợ chuyên quản lý Immutability.

---

## 5. Quy Tắc Vàng: Lọc Lại Tư Duy

Dựa trên những phân tích trên, hãy ghi nhớ các quy tắc thực hành tốt nhất (Best Practices) sau trong phát triển JavaScript hiện đại:

1. **Mặc định sử dụng `const`:** Luôn bắt đầu một biến bằng `const`. Khai báo này làm cho file của bạn dễ theo dõi và ngăn ngừa lỗi gán nhầm ngoài ý muốn (Theo chuẩn Google JavaScript Style Guide).
2. **Dùng `let` chỉ khi CẦN gán lại:** Hầu hết được áp dụng cho biến đếm vòng lặp (`for`), hay cờ trạng thái (`flags`) được update sau một số điều kiện.
3. **`const` + `Object.freeze()` cho hằng số Đối Tượng:** Bất cứ khi nào bạn có một Map cấu hình hoặc một hằng số phức tạp KHÔNG ĐƯỢC PHÉP thay đổi trong suốt vòng đời ứng dụng, sự kết hợp này là bắt buộc.