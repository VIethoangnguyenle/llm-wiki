---
title: "2.2 Cấu trúc Function và Bí ẩn của Scope"
source: "D:\9. Learn\12. llm wiki\raw\articles\2.2.md"
date_added: 2026-04-23
tags: [notes]
status: draft
summary: ""
---

# 2.2 Cấu trúc Function và Bí ẩn của Scope

Trong JavaScript, **Function (Hàm)** là những "Công dân hạng nhất" (First-class citizens). Bạn có thể truyền hàm vào một hàm khác, gán một hàm bằng một biến, hoặc yêu cầu một hàm trả về một hàm ở kết quả.

Sức mạnh to lớn này vừa linh hoạt nhưng cũng đi kèm với không ít lúng túng khi quản lí biến bên trong các hàm đó (**Scope** & **Closure**) và xác định ngữ cảnh tham chiếu (**`this`**). Hãy cùng tháo gỡ từng nút thắt này.

---

## 1. Các "Thế võ" khai báo Function

Trong JS, có 3 cách khai báo hàm phổ biến, và chúng hoàn toàn cư xử khác nhau khi đối mặt với cơ chế **Hoisting** (như đã học ở bài 1.1).

### 1️⃣ Function Declaration
Là kiểu viết cổ điển, bắt đầu bằng từ khoá `function`. Hàm loại này sẽ được Hoisted hoàn toàn lên đầu bộ nhớ. Bạn có thể ung dung gọi chúng trước cả khi khai báo.

```javascript
sayHello(); // Hoàn toàn hợp lệ, in ra: "Hello"

function sayHello() {
  console.log("Hello");
}
```

### 2️⃣ Function Expression
Gán một hàm vô danh (anonymous) vào họng một biến. Tuyệt chiêu này sẽ phải chịu quy định ngặt nghèo của `let`/`const` - nghĩa là nằm trong **Temporal Dead Zone**. Trái ngược với kiểu 1, Gọi trước khi khai báo -> Chết!

```javascript
// sayHi(); // Lỗi: ReferenceError

const sayHi = function() {
  console.log("Hi");
}
```

### 3️⃣ Arrow Function (Hàm Mũi tên - ES6)
Phiên bản rút gọn cực kì phổ biến hiện nay. Cũng vướng phải luật Hoisting y hệt *Function Expression*, nhưng nó mang một sức mạnh ẩn túy liên quan đến `this`.

```javascript
const sayBye = () => {
    console.log("Bye");
}
```

---

## 2. Hàm mũi tên (Arrow Function) và "Ngải" `this`

Câu chuyện `this` trỏ về đâu là lí do gây ra 90% cơn đau đầu ở JavaScript.
Quy tắc vàng:
- Trừ ở chế độ strict mode, **Regular Function** gắn `this` với cái object (đối tượng) đang **THỰC SỰ LÊN TIẾNG GỌI NÓ**.
- Ngược lại, **Arrow Function** thì CÔ LẬP `this`, nó không tự sinh ra `this` bằng cách gọi, mà nó ngước lên dòm xem **môi trường cha khi nó được khai báo** đang mang `this` là cái gì thì nó xài ké cái đó (Lexical `this`).

```javascript
const user = {
  name: "Quan",
  // Regular Function -> Người gọi nó là "user", this sẽ trỏ tới "user"
  regularGreeting: function() {
    console.log("Hello, my name is " + this.name); 
  },
  
  // Arrow function -> Nó được viết bên trong object "user", mà "user" đang nổi lềnh bềnh ở Global Scope. Vậy nên this === window 
  arrowGreeting: () => {
    console.log("Hello, my name is " + this.name); 
  }
};

user.regularGreeting(); // In ra: "Hello, my name is Quan"
user.arrowGreeting();   // In ra: "Hello, my name is undefined"
```
> [!TIP] Mẹo Clean Code
> Đừng cố dùng Arrow function làm *Method* bên trong một Object hay một class constructor. Hãy dành Arrow function cho các vị trí *Callbacks* (hàm truyền vào trong `.map()`, `setTimeout()`) để không lo mất this.

---

## 3. Quản trị Đất đai: Từ Scope tới Lexical Scope

**Scope (Phạm vi)** quy định một biến số được phép sống sót và được truy vấn ở đâu.

### Các giới hạn khu vực
1. **Global Scope:** Nằm vất vưởng ngoài cùng file. Ai cũng thấy, ai cũng đọc được -> Nguồn cội của mọi bug Memory Leak. 
2. **Function Scope:** Biến khai báo bằng `var` bên trong một function chỉ có thể được thấy bởi những gì nằm bên trong hàm đó.
3. **Block Scope (ES6):** Các biến `let`, `const` bị nhốt chặt lại bởi các dấu ngoặc nhọn `{ ...}` (ví dụ vòng `if`, hay vòng `for`).

### Kỹ thuật Lexical Scope
JavaScript nhìn vào mã nguồn tại **thời điểm Cú pháp (Syntax) đang được gõ**. Con hàm bên trong nằm ở đâu thì nó có quyền truy cập tất thảy ra ngoài cấp độ cha của nó. Không cần biết lúc gọi hàm nó đang đứng ở đâu.

```javascript
const globalVar = "Tôi ở ngoài trời";

function outer() {
  const outerVar = "Tôi ở trong nhà";
  
  function inner() {
    const innerVar = "Tôi trốn trong tủ";
    // Mình "inner" có phép thuật lấy được hết đồ của bố và của trời
    console.log(innerVar, outerVar, globalVar); 
  }
  inner();
}
```

---

## 4. Tôn giáo Closure

Từ *Lexical Scope* sinh ra một triết lí bất hủ: **Closure**.

Một **Closure** xảy ra khi một Function *nhớ* được các biến từ scope cha của nó ngay cả khi scope cha đó đã đóng cửa ngừng chạy từ lâu.

Vẫn khó hiểu? Cùng xem ví dụ:

```javascript
function makeBank() {
  let _balance = 1000; // Biến bí mật, người ngoài không sửa được!

  return function() {
    console.log("Số dư của ngài là: ", _balance);
  }
}

const myAccount = makeBank(); 
// Giờ phút này lệnh makeBank() đã chạy xong gòi, context bị hủy ở Call Stack.
// Những tưởng tài sản _balance cũng chết theo.

myAccount(); // CHÀO CỜ! In ra 1000.
```

Ở đây hàm con được `return` ném ra ngoài, nhưng trước khi đi nó đã tiện tay thu thập và "bỏ túi" đem theo biến `_balance`. Và lúc ta bật mở `myAccount()` ở tương lai muôn thủa sau này, nó vẫn sẽ lôi ở túi ra con số 1000 đó. Nó chính là **Closure**.

### Áp dụng Clean Code thực chiến: Data Privacy
Sử dụng hiệu ứng này để thay thế cho OOP khi bạn muốn bảo vệ những cái cần được đóng gói riêng tư, không cho ai chọc ngoáy.

```javascript
function counterStore() {
  let count = 0; // Đóng cửa khép kín

  return {
    plus: () => count++,
    minus: () => count--,
    get: () => count
  }
}

const score = counterStore();
score.plus();
console.log(score.get()); // 1
score.count = 999; // Bất lực, không can thiệp được biến count thực ở trong tủ!
```

---

## 5. Tham số Thông Minh (Smart Parameters)

Thay vì đi kiểm tra tham số người dùng nhập có bị rỗng hay không bằng if-else truyền thống, cấu trúc hàm hiện tại ủng hộ phong cách dưới đây:

### 🌟 Default Params
```javascript
// Nhét luôn thông số dự bị thẳng lên cổng hàm
function sayHello(name = "Guest") {
  console.log("Welcome " + name);
}

sayHello(); // "Welcome Guest"
```

### 🌟 Bỏ rác `arguments`, xài `...rest`
Ngày xưa người ta hay lấy biến ảo `arguments` (vốn là object dởm) để gom tất cả tham số ẩn truyền vào. Ngày nay, cứ xài `...` gom gọn nó tự túc đưa vào một cái Array thực thụ tinh khiết.

```javascript
function sumAll(...numbers) {
  // numbers nghiễm nhiên là 1 Array hịn, xài được luôn reduce 
  return numbers.reduce((total, num) => total + num, 0); 
}

console.log(sumAll(1, 2, 3, 4)); // In ra: 10
```

--- 

Dẹp bỏ tư tưởng chỉ biết viết những hàm chằng chịt, qua bài này, bạn bắt đầu thấy được rằng viết Function cũng cấu trúc chặt chẽ như một công trình kiến trúc phân bổ cấp phép cho từng đồ vật. Sử dụng Arrow Function đúng vị trí, bảo vệ biến bằng Closure, và tối ưu Rest Parameters sẽ giải tỏa rất nhiều khối code thừa thãi của bạn.