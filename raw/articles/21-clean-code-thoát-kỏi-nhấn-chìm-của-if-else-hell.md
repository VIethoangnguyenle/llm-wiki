---
title: "2.1 Clean Code: Thoát Kỏi Nhấn Chìm Của "If-Else Hell""
source: "D:\9. Learn\12. llm wiki\raw\articles\2.1.md"
date_added: 2026-04-23
tags: [notes]
status: draft
summary: ""
---

# 2.1 Clean Code: Thoát Kỏi Nhấn Chìm Của "If-Else Hell"

Trong bất kỳ quá trình phát triển nào, không ai sinh ra là đã có tư duy viết code đẹp. Chúng ta thường bắt đầu bằng việc ghép hàng loạt các khối `if-else` lồng nhau (hay còn gọi là **Arrow Anti-Pattern** hoặc **Đụn rơm/Nested If-Else Hell**), để thoả mãn tức thì luồng nghiệp vụ. 

Mặc dù máy tính vẫn hiểu chính xác những khối logic đó, nhưng con người thì không! Việc lạm dụng cấu trúc rẽ nhánh này sẽ khiến code khó bảo trì, khả năng mở rộng kém và là hung thủ hàng đầu sinh ra bug.

Hãy cùng xem xét kỹ thuật để biến những đoạn code nghiệp dư thành phong cách của một **"JS Warrior"** thực thụ!

---

## ⛔ Vấn đề: Cơn ác mộng If-Else Lồng Nhau

Trông có quen không? Hãy cùng xem một ví dụ kiểm tra quyền truy cập dưới đây:

```javascript
function loginUser(user) {
  if (user) {
    if (user.isActive) {
      if (user.role === 'admin') {
        if (user.isEmailVerified) {
          return "Welcome Admin!";
        } else {
          return "Please verify your email.";
        }
      } else {
        return "You must be an admin.";
      }
    } else {
      return "User is not active.";
    }
  } else {
    return "User not found.";
  }
}
```

Kiểu viết này làm tăng độ hẹp và thụt lề liên tục vào trong. Đọc code là cả một cuộc "đánh vật" giữa não phải và não trái.

---

## 💡 Kỹ thuật 1: Guard Clauses & Early Return (Thoát sớm)

Thay vì chui vào trong điều kiện "đúng" rồi thực hiện tiếp, hãy làm ngược lại: **Phát hiện những trường hợp sai hoặc méo mó và Return/Throw Error ngay lập tức**. Việc đẩy lỗi lên đầu hàm giúp mã xử lý chính được hoàn toàn phẳng phiu trôi xuống dưới.

```javascript
// Clean Code Version: Early Return
function loginUser(user) {
  if (!user) return "User not found.";
  if (!user.isActive) return "User is not active.";
  if (user.role !== 'admin') return "You must be an admin.";
  if (!user.isEmailVerified) return "Please verify your email.";

  // Code chạy thẳng táp khi không dính chướng ngại vật nào
  return "Welcome Admin!";
}
```
**Lợi ích ấn tượng:** Bạn đọc code như đọc một bài văn (Linear flow). Xóa rào cản thụt lề, kiểm soát lỗi nhanh gọn lẹ.

---

## 💡 Kỹ thuật 2: Dictionary Pattern (Dẹp bỏ if-else & switch-case dài dòng)

Khi bạn có quá nhiều kết quả phụ thuộc vào 1 tham chiếu từ chuỗi hoặc số, nhiều người sẽ chuộng `switch-case` hoặc gõ một chuỗi `else if` không điểp kết.

```javascript
// Dirty Code
function getPaymentStatus(status) {
  if (status === 'SUCCESS') {
    return "Thanh toán thành công";
  } else if (status === 'PENDING') {
    return "Đang chờ xử lý";
  } else if (status === 'FAILED') {
    return "Thanh toán thất bại";
  } else {
    return "Trạng thái không xác định";
  }
}
```

Với **Dictionary Pattern**, chúng ta quy đổi luồng logic if-else dư thừa đó thành một phép kiểm tra thuộc tính của **Object/Map**.

```javascript
// Clean Code Version: Object Map
function getPaymentStatus(status) {
  const statusLabels = {
    SUCCESS: "Thanh toán thành công",
    PENDING: "Đang chờ xử lý",
    FAILED: "Thanh toán thất bại",
  };

  return statusLabels[status] || "Trạng thái không xác định";
}
```
**Lợi ích ấn tượng:** Thay vì xử lý rẽ nhánh, bộ não bạn chỉ xử lý việc truy xuất Data! Tốc độ chạy cũng tối ưu hơn, dễ bảo trì và dễ dàng trích xuất (export) `statusLabels` ra nơi khác.

---

## 💡 Kỹ thuật 3: Array `includes` thay cho "Sự tra tấn của dấu '||'"

Khi bạn bắt gặp một biến thoả mạn một trong nhiều điều kiện (OR). Ví dụ:

```javascript
// Dirty Code
if (fruit === 'apple' || fruit === 'banana' || fruit === 'cherry' || fruit === 'orange') {
  console.log("Đây là trái cây quen thuộc!");
}
```

Hãy mạnh dạng nhốt hết chúng vào một cái mảng và xài `includes`:

```javascript
// Clean Code Version: Array .includes
const regularFruits = ['apple', 'banana', 'cherry', 'orange'];

if (regularFruits.includes(fruit)) {
  console.log("Đây là trái cây quen thuộc!");
}
```

---

## 💡 Kỹ thuật 4: Tận Gốc các Optional Chaining và Toán tử "Lười"

Bạn còn xài đống code kiểu cũ này không? Lại là `if` kiểm tra property có tồn tại!

```javascript
// Dirty Code
let city;
if (user && user.address && user.address.city) {
  city = user.address.city;
} else {
  city = "Unknown";
}
```

JS hiện đại mang đến 2 thứ vũ khí đẳng cấp: **`?.` (Optional Chaining)** và **`??` (Nullish Coalescing)**.

```javascript
// Clean Code Version
const city = user?.address?.city ?? "Unknown";
```
- **`user?.address`**: Nó sẽ kiểm tra user có rỗng không, nếu rỗng thì trả về `undefined` và dừng luôn.
- **`?? "Unknown"`**: Nếu mớ bên trái là Null hoặc Undefined, nó lập tức gán chuỗi "Unknown" mặc định.

*(Lưu ý: `??` nhận diện nghiêm ngặt NULL/UNDEFINED khác với toán tử `||` vì `||` sẽ bắt hụt nếu giá trị là `0` hoặc `""`).*

---

## Tóm gọn hành trang của JS Warrior

> *"Bất cứ ai cũng có thể viết những đoạn code mà máy tính hiểu được. Lập trình viên giỏi viết những đoạn mã cho con người hiểu được." - Martin Fowler*

Code càng có ít luồng rẽ nhánh, nghĩa là không bị chồng chéo, dễ dàng nhắm mắt lại và mường tượng. Khi thấy tay mình chuẩn bị gõ `else if`, hãy dừng lại 2 giây để nhớ về:
1. **Early Return**: Đẩy lỗi ra ngoài và Exit sớm bớt đau khổ.
2. **Object Map (Dictionary)**: Gom logic rẽ nhánh biến thành truy xuất Data Key-Value.
3. **Array `includes`**: Không lặp lại tên biến vất vả với dấu `||`.
4. **`?.` và `??`**: Đơn giản hoá các biến lồng chập chùng.