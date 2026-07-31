---
title: "1.99 JavaScript Under The Hood: Call Stack, Event Loop, và Execution Context"
source: "D:\9. Learn\12. llm wiki\raw\articles\1.99.md"
date_added: 2026-04-23
tags: [notes]
status: draft
summary: ""
---

# 1.99 JavaScript Under The Hood: Call Stack, Event Loop, và Execution Context

JavaScript luôn được giới thiệu là ngôn ngữ **đơn luồng (Single-Threaded)**. Điều này có nghĩa là tại một thời điểm, hệ thống chỉ có thể làm duy nhất một tác vụ. Tuy nhiên, trong thực tế bạn thấy JavaScript có thể vừa tải dữ liệu từ API (mất vài giây), vừa thực thi hiệu ứng UI mượt mà, vừa lắng nghe sự kiện click từ người dùng mà không hề bị "treo" (blocking).

Làm thế nào việc tưởng chừng mâu thuẫn này lại khả thi? Chào mừng bạn đến với hậu trường (Under The Hood) của JavaScript, nơi có sự phối hợp nhịp nhàng kỳ diệu giữa JS Engine và Môi trường chạy (Browser/Node.js).

---

## 1. Môi trường thực thi tổng thể (The Environment)

Đầu tiên, phải hiểu rõ **JS Engine (như V8 Engine)** không đứng một mình. Tự bản thân JS Engine không có khái niệm `setTimeout`, không biết `DOM` là gì và không hỗ trợ kết nối `fetch`. Tất cả các sức mạnh này đều do **Môi trường (Web APIs trong Browser hoặc C++ APIs trong Node.js)** bù đắp.

Hệ thống hoạt động dựa trên 4 mảnh ghép cốt lõi:
1. **Call Stack (trong JS Engine)**
2. **Web APIs (được Browser cung cấp)** 
3. **Task Queues (Hàng đợi tác vụ)**
4. **Event Loop (Kẻ điều phối)**

---

## 2. Execution Context và Call Stack

### Execution Context (Bối cảnh thực thi)
Mỗi khi một đoạn code JS được chạy, nó không chỉ đơn thuần đọc từ trên xuống dưới mà tạo ra một "môi trường cô lập" gọi là **Execution Context**.
- **Global Execution Context (GEC):** Chạy đầu tiên, tạo ra object `window` và cấp phát `this`.
- **Function Execution Context (FEC):** Mỗi lần gọi một hàm, đoạn code bên trong nó lập tức được đưa vào một bối cảnh thực thi riêng biệt.

Một Execution Context luôn đi qua 2 pha:
1. **Creation Phase:** JavaScript dò trước một lượt, đưa các khai báo `var` và định nghĩa `function` vào bộ nhớ (Hoisting). Lập ra khoảng không Temporal Dead Zone (TDZ) cho `let` và `const`.
2. **Execution Phase:** Code chính thức được gán trị số, tính toán và tiến hành chạy từng dòng.

### Call Stack (Sổ kẹp tác vụ)
Call Stack vận hành như 1 cọc đĩa (Last-In-First-Out).
- Khi bạn gọi hàm `A()`, nó được ném vào Stack.
- Hàm `A()` bên trong lại gọi hàm `B()`, hàm `B()` tiếp tục được ném chồng lên trên `A()`.
- JS Engine bắt buộc thi hành hàm nằm ở **đỉnh Stack** trước. Sau khi `B()` xong (trả về kết quả - return), nó tự pop (bật) ra khỏi Stack. Tiếp tục chạy xong `A()` và pop `A()`.

> [!WARNING] Stack Overflow
> Nếu bạn viết một hàm đệ quy mà quên điều kiện thoát, Call Stack sẽ liên tục tích tụ hàm cho đến khi vượt sức chịu đựng bộ nhớ, gây ra lỗi huyền thoại: `Maximum call stack size exceeded.`

---

## 3. Web APIs đứng đằng sau "Gánh" những tác vụ nặng

Khi Call Stack gặp một tác vụ mất nhiều thời gian hoặc do trình duyệt quản trị (như `setTimeout(..., 5000)` hoặc đi gọi API bằng `fetch`), nó tống khứ việc này sang ngay cho **Web APIs**.

- *"Ê Web APIs, tôi giao đoạn code này cho cậu quản lý hẹn giờ 5 giây nhé. Tôi (Call Stack) rảnh tay đi làm tiếp cái khác ngay đây!"*
- Nhờ khả năng uỷ quyền này, JavaScript tiếp tục đi chạy các dòng lệnh tiếp theo mà không bị kẹt 5 giây. Đóng vai trò then chốt gây dựng nên danh tiếng **Non-blocking (không chặn)** của JS.

---

## 4. Quản trị bất đồng bộ với 2 loại Hàng Đợi (Queues)

Ngay khi Web APIs xử lý xong (timer đếm ngược hết 5 giây, API chả về xong tín hiệu), nó không được phép tùy tiện nhảy thẳng trở lại vào Call Stack làm loạn thứ tự. Thay vào đó, nó phải xếp hàng ở "phòng chờ". Có 2 hàng chờ với độ ưu tiên khác nhau:

1. **Microtask Queue (Hàng đợi V.I.P):**
   - Chứa các lệnh được gọi với **Promises** (`.then`, `.catch`, `.finally`), `async/await`, hoặc `MutationObserver`.
   - Rất quyền lực, lúc nào cũng được quyền xử lý trước.

2. **Macrotask Queue / Callback Queue (Hàng đợi Phổ Thông):**
   - Chứa những callback của `setTimeout`, `setInterval`, các `DOM events` như xử lý lệnh `click`.

---

## 5. Event Loop: Kẻ đánh nhịp kiên cường

**Event Loop** là một chương trình theo dõi vòng lặp vô tận, mang trên vai chỉ một nhiệm vụ cực kỳ quan giản nhưng khắt khe:

> "Nếu **Call Stack trống rỗng**, tôi sẽ nhìn xuống các phòng chờ Queue. Ai đứng đầu Queue, lên Call Stack đi làm việc tiếp!"

Quy tắc đẩy việc của Event Loop thực thi *chính xác* theo thứ tự này:
1. Nó kiểm tra xem Call Stack có rảnh (trống) không? (Nếu đang bận, thì đứng đợi).
2. Khi Call Stack trống, nó sẽ xả **TOÀN BỘ Microtask Queue** vào Call Stack. Từng cái một cho đến lúc phòng chờ VIP trống trơn không còn một ai.
3. Chỉ khi đó nó mới nhón sang **Macrotask Queue** và đẩy **DUY NHẤT 1 tác vụ** (1 macrotask) qua Call Stack. 
4. Rồi lặp lại vòng tuần hoàn.

---

## 6. Bài Tập Code - Đẳng Cấp Thấu Hiểu

Hãy nhìn đoạn mã sau và tập tự mình mô phỏng thứ tự ra Console. Đây là câu hỏi kinh điển nhất khi phỏng vấn JS Advanced.

```javascript
console.log("1. Bắt đầu");

setTimeout(() => {
  console.log("2. Timeout Macrotask");
}, 0);

Promise.resolve().then(() => {
  console.log("3. Promise Microtask");
});

console.log("4. Kết thúc");
```

**Thứ tự xảy ra dưới mui xe:**
1. Call Stack nhận `console.log("1. Bắt đầu")`. Thi hành ngay lập tức. **(In ra: 1)**
2. Sự kiện `setTimeout` bị đẩy qua Web APIs. Web APIs đếm ngược 0s và quăng ngay Callback vào hàng đợi Phổ Thông (*Macrotask Queue*). Call Stack dọn đường.
3. Kế tiếp, `Promise` tạo ra callback, và JS đẩy nó vào hàng đợi VIP (*Microtask Queue*).
4. Call Stack nhận `console.log("4. Kết thúc")`. Nhảy vào làm việc. **(In ra: 4)**. 
5. Code chạy hết. **Call Stack hiện tại đã trống!**
6. Đây là đất diễn của **Event Loop**. Nó phát hiện Call Stack trống và kiểm tra Queue. Do VIP được ưu tiên trước, Event Loop bốc tác vụ trong *Microtask* lên. **(In ra: 3)**.
7. *Microtask Queue* đã rỗng. Event Loop chuyển hướng sang *Macrotask*, lôi thằng Timeout lên Call Stack. **(In ra: 2)**.

**Kết quả màn hình sẽ hiển thị:**
```
1. Bắt đầu
4. Kết thúc
3. Promise Microtask
2. Timeout Macrotask
```

---

## Kết luận

Kiến thức về bộ ba: **Call Stack**, **Event Loop** và **Task Queues** là chìa khóa then chốt đưa bạn rời khỏi ngưỡng nghiệp dư của JS và bước bào đẳng cấp Master. Nếu bạn thấu hiểu cơ chế Single-thread hoạt động với Non-Blocking I/O này, bạn làm việc cực nhàn hạ với cơ chế Asynchronous (bất đồng bộ) của các framework hiện đại.