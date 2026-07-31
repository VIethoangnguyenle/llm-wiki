---
title: "`var`, `let`, `const`: Kẻ Thù Thầm Lặng và Những Vệ Binh Của Scope"
source: "D:\9. Learn\12. llm wiki\raw\articles\1.1.md"
date_added: 2026-04-23
tags: [notes]
status: draft
summary: ""
---

# `var`, `let`, `const`: Kẻ Thù Thầm Lặng và Những Vệ Binh Của Scope

Trong thế giới JavaScript, khai báo biến là bài học vỡ lòng. Tuy nhiên, đằng sau những từ khóa tưởng chừng đơn giản như `var`, `let`, và `const` là một hệ thống quy tắc ngầm định phức tạp. Nếu không nắm vững, bạn có thể dễ dàng tạo ra những "bug" thầm lặng cực kỳ khó tái hiện. Bài viết này sẽ giúp bạn hiểu rõ Hoisting, Scope, cốt lõi Execution Context và lý do tại sao `let` & `const` là tương lai.

---

## 1. `var` - Kẻ Thù Thầm Lặng Của Lập Trình Viên

Trong một buổi code review, một câu hỏi kinh điển thường được Senior Dev đặt ra: _"Khoan đã, dừng lại... Dòng này em dùng `var` à?"_  
Junior Dev thường sẽ đáp: _"Dạ? Thì... nó vẫn chạy mà anh?"_

Và Senior Dev sẽ trả lời: _"Nó chạy, cho đến khi nó KHÔNG chạy nữa. Và lúc đó, không ai biết tại sao."_

Vậy tại sao một từ khóa tưởng chừng vô hại như `var` (đã gắn bó với JS từ những ngày đầu) lại có thể gây ra những lỗi nghiêm trọng và khó lường? Dưới đây là 3 mối nguy hiểm lớn nhất:

### ⚠️ Mối nguy hiểm #1: "Bóng ma" Hoisting

Hoisting với `var` khiến việc khai báo biến được "nhấc" lên đầu scope, nhưng giá trị gắn cho nó thì lại **không**. Điều này dẫn đến một hành vi vô cùng khó hiểu: biến tồn tại với giá trị `undefined` trước cả khi dòng code khai báo nó được chạy.

```javascript
// Output: undefined (Không phải ReferenceError!)
console.log(myVar);

var myVar = 10;
console.log(myVar); // Output: 10
```

> **Diễn giải:** Biến `myVar` hành xử giống như một bóng ma: khai báo của nó ám ảnh khắp scope, nhưng giá trị thật sự chỉ xuất hiện sau này.

### ⚠️ Mối nguy hiểm #2: Rò Rỉ Scope Ngoài Tầm Kiểm Soát

`var` chỉ có khái niệm **"function scope"** hoặc **"global scope"**, hoàn toàn không hiểu khái niệm **"block scope"**. Điều này có nghĩa là biến `var` được khai báo bên trong một khối lệnh (`if`, `for`, `while`, `{...}`) sẽ "rò rỉ" ra ngoài khối lệnh đó.

```javascript
for (var i = 0; i < 3; i++) {
  // ...
}
console.log(i); // Vẫn truy cập được 'i' ở đây! Output: 3

if (true) {
  var blockVar = "Tôi đã thoát ra ngoài!";
}
console.log(blockVar); // Output: "Tôi đã thoát ra ngoài!"
```

### ⚠️ Mối nguy hiểm #3: Ghi Đè Thầm Lặng

`var` cho phép bạn khai báo lại cùng một biến trong cùng một scope mà trình duyệt **không hề báo lỗi**. Điều này vô tình ghi đè lên những biến quan trọng, gây ra hàng loạt bug logic tiềm tàng.

```javascript
var name = "Alice";

// ... hàng chục dòng code sau ...

// Lập trình viên vô tình khai báo lại biến 'name'
var name = "Bob";

console.log(name); // Output: "Bob" -> "Alice" đã biến mất mà không có cảnh báo nào!
```

**Châm ngôn:** Không lỗi. Không cảnh báo. Chỉ có Bug tiềm tàng.

---

## 2. Gốc Rễ Vấn Đề: Thế Giới Nội Tâm JavaScript (Execution Context)

Để hiểu tại sao `var` lại "nguy hiểm", chúng ta cần xem cách JS thực thi code. Mọi thứ diễn ra bên trong một môi trường gọi là **Execution Context**.

Hãy tưởng tượng Execution Context là một chiếc hộp bao gồm 2 thành phần chính:

1. **Memory Component (Variable Environment):** Nơi lưu trữ tất cả các biến và hàm dưới dạng cặp `key-value`.
2. **Code Component (Thread of Execution):** Nơi code thực sự được thực thi, dịch từ trên xuống dưới, từng dòng một.

### Giải mã Hoisting qua Quy Trình 2 Giai Đoạn:

- **Giai đoạn 1: Memory Creation (Tạo bộ nhớ):** JavaScript quét qua toàn bộ code, tìm các từ khóa khởi tạo (như `var`, tĩnh). Với `var myVar = 10`, nó sẽ cấp phát vùng nhớ cho `myVar` và tạm gán giá trị mặc định là `undefined`. **Đây chính là lúc "Hoisting" xảy ra!**
- **Giai đoạn 2: Code Execution (Thực thi code):** Code mới bắt đầu chạy tuần tự. Khi dòng mã `console.log(myVar)` đầu tiên chạy, nó sẽ lấy giá trị từ Memory Component, lúc này đang là `undefined`. Mãi cho đến khi chạy tới dòng gán giá trị `myVar = 10`, thì giá trị biến trong Memory Component mới cập nhật thành `10`.

---

## 3. Giải Pháp Xuất Hiện: `let` và `const` - Những Vệ Binh Của Scope

Được giới thiệu trong phiên bản ES6 (2015), `let` và `const` được sinh ra để khắc phục chính xác những nhược điểm chí mạng của `var`:

1. **Block Scope:** Chỉ tồn tại an toàn bên trong khối `{...}`. Không còn tình trạng "rò rỉ".
2. **Không thể khai báo lại:** Ngăn chặn tuyệt đối lỗi ghi đè thầm lặng trong cùng scope.
3. **Temporal Dead Zone (TDZ):** Giải quyết dứt điểm sự nguy hiểm của hoisted `undefined`.

### 🛡️ `let`: Sự Linh Hoạt Trong Tầm Kiểm Soát

Dùng `let` khi giá trị của biến **CẦN thay đổi**.

- Vẫn là khai báo biến giống `var`.
- Có thể cập nhật (`let x = 10; x = 20;` là hợp lệ).
- Truy cập `let` bên ngoài khối block sinh ra lỗi `ReferenceError` – **lỗi ở đây là bạn của bạn**, nó báo hiệu sớm một sự sai lệch logic thay vì giấu giếm bằng giá trị `undefined`.

### 🔒 `const`: Sự Bất Biến Đáng Tin Cậy

Dùng `const` cho bất cứ giá trị nào **KHÔNG NÊN gán lại**.

- Không thể khai báo cũng như không thể đem đi tái gán bằng toán tử `=`.
- Bắt buộc phải được khởi tạo giá trị ngay tại thời điểm khai báo.

#### ⚡ Lưu ý quan trọng về tính bất biến của `const`:

**Bí mật lớn nhất:** `const` không tạo ra giá trị bất biến, mà nó tạo ra **tham chiếu bất biến (constant binding)**. Nghĩa là:

```javascript
const CONFIG = { apiUrl: "/api/v1" };

// HOÀN TOÀN HỢP LỆ! (Bạn đang đổi thuộc tính bên trong)
CONFIG.apiUrl = "/api/v2";

// LỖI (TypeError)! (Trực tiếp gán lại liên kết biến)
CONFIG = { newUrl: "/api/v3" };
```

_Ghi nhớ: Value is mutable, but binding is constant._

---

## 4. Vũ Khí Bí Mật: Vùng Chết Tạm Thời (Temporal Dead Zone - TDZ)

**TDZ** có thể hiểu là khoảng không gian/thời gian tính từ đầu block scope cho đến dòng code thực thi khởi tạo biến `let`/`const`. Bất kỳ nỗ lực nào hòng truy cập biến ở bên trong phạm vi TDZ này sẽ ném ra lỗi `ReferenceError (Cannot access variable before initialization)`.

Sự xuất hiện của TDZ ép buộc bạn phải viết code tuân thủ trình tự rõ ràng hơn: Khai báo trước -> Sử dụng sau.

---

## 5. Tổng kết: Viết Code của Tương Lai

### Bảng So Sánh Trực Quan

| Feature                    | `var`                                | `let`                                           | `const`                                         |
| -------------------------- | ------------------------------------ | ----------------------------------------------- | ----------------------------------------------- |
| **Phạm vi (Scope)**        | Function-scoped                      | Block-scoped                                    | Block-scoped                                    |
| **Hoisting**               | Được Hoist & khởi tạo là `undefined` | Được Hoist nhưng không khởi tạo (nằm trong TDZ) | Được Hoist nhưng không khởi tạo (nằm trong TDZ) |
| **Khai báo lại**           | ✅ Có thể                            | ❌ Không thể                                    | ❌ Không thể                                    |
| **Gán Lại**                | ✅ Có thể                            | ✅ Có thể                                       | ❌ Không thể (TypeError)                        |
| **Khởi tạo cùng khai báo** | Không bắt buộc                       | Không bắt buộc                                  | ⚠️ Bắt buộc                                     |

### Lầm tưởng phổ biến: "`const` có nhanh hơn `let` không?"

- **Lý thuyết:** Động cơ JS (JS Engine) có thể tối ưu hiệu suất cho biến `const` vì nó tin chắc giá trị không thay đổi.
- **Thực tế:** Các V8 / JavaScript Engine hiện nay cực kì "dã man" trong việc tối ưu, **khoảng cách tốc độ gần như là bằng 0** và hoàn toàn có thể bị lờ đi.

> **💡 Quy tắc Vàng từ Airbnb & Google:**
>
> 1. Sử dụng **`const`** mặc định cho toàn bộ biến.
> 2. Sử dụng **`let`** KHU BIỆT dành riêng cho các biến thực sự cần thay đổi giá trị.
> 3. **Tuyệt đối KHÔNG sử dụng `var`** trong dự án mới.

Hãy bỏ lại `var` trong quá khứ. Chào mừng bạn đến với kỷ nguyên code sạch, dễ đoán và dễ bảo trì với `let` và `const`!