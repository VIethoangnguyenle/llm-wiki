---
title: "1.3 Bộ Nhớ JavaScript: Stack Tối Ưu & Heap Mở Rộng"
source: "D:\9. Learn\12. llm wiki\raw\articles\1.3.md"
date_added: 2026-04-23
tags: [notes]
status: draft
summary: ""
---

# 1.3 Bộ Nhớ JavaScript: Stack Tối Ưu & Heap Mở Rộng

Khi viết code JavaScript, chúng ta thường "take it for granted" (xem là điều hiển nhiên) việc khai báo một biến, một mảng hay khởi tạo một object mà ít khi tự hỏi: *"Dữ liệu này được cất ở đâu? Dọn dẹp như thế nào lúc không dùng nữa?"*

JavaScript là một ngôn ngữ bậc cao có tính năng tự động thu gom rác (Garbage Collection), giúp dev không phải tự tay gọi hàm cấp phát (như `malloc` trong C) hay tự tay giải phóng bộ nhớ. Tuy nhiên, nếu bạn không hiểu cơ chế bên dưới, bạn rất dễ gặp các vấn đề về **Memory Leak** hoặc những "chiếc bẫy" khó hiểu về tham chiếu (reference).

Trong JavaScript engine (như V8 của Google Chrome hay Node.js), bộ nhớ được chia thành hai khu vực chính để phân loại và lưu trữ dữ liệu hiệu quả: **Stack (Ngăn xếp)** và **Heap (Vùng nhớ động)**.

---

## 1. Stack Memory (Bộ Nhớ Ngăn Xếp)

Stack là một cấu trúc dữ liệu hoạt động theo nguyên tắc **LIFO (Last-In-First-Out)**, nghĩa là dải dữ liệu nào vào sau sẽ được lấy ra trước. Stack trong JavaScript đảm nhận trách nhiệm lưu trữ các thành phần có *kích thước tĩnh (static data)* mà engine có thể xác định được ngay khi chạy code.

### Stack lưu trữ những gì?
- **Các dữ liệu kiểu nguyên thủy (Primitive values):** Bao gồm `String`, `Number`, `Boolean`, `Undefined`, `Null`, `Symbol`, và `BigInt`.
- **References (Điểm trỏ):** Địa chỉ vùng nhớ trỏ tới các object hoặc array đang nằm bên trong vùng Heap.
- **Dữ liệu của Execution Contexts:** Trạng thái thực thi của hàm (Call Stack).

### Đặc điểm của Stack:
- **Tốc độ:** Rất nhanh (vì kích thước mỗi phần tử cố định và cách làm việc tĩnh).
- **Giới hạn dung lượng:** Stack có kích thước tối đa giới hạn (nếu gọi hàm đệ quy không có điểm dừng, bạn sẽ gặp lỗi `RangeError: Maximum call stack size exceeded`).
- **Phân bổ trực tiếp:** Các biến được cấp vùng nhớ trực tiếp độc lập.

```javascript
let myName = "John"; // Primitive -> Lưu thẳng giá trị trong Stack
let myAge = 30; // Primitive -> Lưu thẳng giá trị trong Stack

let anotherName = myName; // Tạo ra một ô nhớ mới trong Stack và copy giá trị "John" sang
anotherName = "Doe"; // Không hề ảnh hưởng tới myName

console.log(myName); // "John"
```

---

## 2. Heap Memory (Bộ Nhớ Động)

Trong khi Stack thích hợp cho dữ liệu kích thước cực nhỏ và đã biết trước định mức, thì **Heap** là không gian rộng lớn và tự do dành cho các dữ liệu phức tạp, có thể phình to hoặc thu nhỏ liên tục gọi là *Dynamic data*.

### Heap lưu trữ những gì?
- **Các kiểu tham chiếu (Reference types):** Là `Object`, `Array`, và `Function`.

### Đặc điểm của Heap:
- **Kích thước khổng lồ:** Phân bổ cho những object lớn, mảng chứa cả triệu phần tử mà không gian bị dồn hay cần định hình trước.
- **Tốc độ:** Chậm hơn Stack do cơ chế tra cứu động (phải rà soát pointer trong Stack trước để nhảy vào vị trí tương ứng trong Heap).
- **Phân bổ dạng tham chiếu:** Khi khởi tạo một Object, phần bản thể chứa dữ liệu thực sẽ đặt ở Heap, còn trên Stack sẽ tạo ra một biến chỉ lưu **địa chỉ (Pointer)** trỏ xuống Heap.

```javascript
let myCar = { brand: "VinFast", year: 2024 }; 
// Object { brand: "VinFast", year: 2024 } nằm trong Heap.
// myCar nằm trong Stack và chỉ là địa chỉ trỏ (ví dụ: 0x00A1) tới Object đó.

let yourCar = myCar; 
// yourCar ở Stack được nhận địa chỉ giống hết myCar (0x00A1).

yourCar.year = 2025; // Sửa dữ liệu ở vùng nhớ 0x00A1 trong Heap.

console.log(myCar.year); // 2025 - Cả 2 biến đều trỏ vào cùng 1 nhà!
```

> [!WARNING] Cảnh báo về Mutation
> Như đã học ở bài trước (sự thật về const), lý do khi dùng `const` để khai báo Object bạn vẫn có thể thay đổi các thuộc tính bên trong nó là do: `const` khoá chết cái Điểm trỏ ở **Stack**, không cho cập nhật biến thành 1 pointer khác, nhưng giá trị động tại **Heap** thì không hề bị khoá.

---

## 3. Quá trình dọn dẹp bộ nhớ: Garbage Collection

Javascript tự động cấp và tự động dọn rác (Garbage Collector - GC). Khi dữ liệu trên bộ nhớ nằm yên và *không còn ai có khả năng với tới nó* nữa, thì JS Engine sẽ thu gom chúng để trả lại RAM.

**Thuật toán Mark-and-Sweep (Đánh dấu & Quét rác):**
Thay vì đếm số lần sử dụng thì V8 sử dụng khái niệm **"Reachability"** (độ phân bổ có thể tiếp cận được từ rễ - Root).

1. **Rễ (Roots):** Đại diện là `window` object trong Browser hoặc `global` trong Node.js.
2. **Đánh dấu (Marking):** GC bắt đầu từ Roots, duyệt dọc theo mọi biến đang tồn tại và object tham chiếu từ biến đó. Những thứ được chạm đến là *đang hữu dụng (Reachable)*.
3. **Quét (Sweeping):** Tất cả các vùng kí gửi trong Heap nào KHÔNG được đánh đấu (nghĩa là mất đường liên kết trỏ tới từ Stack) sẽ bị coi là thư rác vô dụng, và bộ nhớ đó sẽ được giải phóng.

```javascript
let data = { id: 1, action: "FETCH" }; // Pointer trỏ tới Object 1
data = null; 
// Hiện tại pointer trong Stack của 'data' đổi thành null.
// Đồng nghĩa cái Object { id: 1... } dưới Heap đã bị mồ côi (không ai trỏ đến).
// -> Tại lần chạy Mark-and-Sweep kế tiếp, Object này sẽ bị xóa khỏi bộ nhớ Heap.
```

---

## 4. Những nguyên nhân gây ra Memory Leak
Memory Leak là hiện tượng khi vùng nhớ lẽ ra đã hết giá trị sử dụng nhưng không được dọn đi vì chúng vẫn *vô tình được đánh dấu reachable*. Dưới đây là 3 hủ tục hàng đầu sinh ra chuyện đó:

### 1. Rác từ Global Variables
Nếu bạn gắn lung tung biến lên `window` (hoặc lỡ quên khai báo `let`, `const`), những biến đó sống bám vào Root, nghĩa là sống mãi với trình duyệt.
```javascript
function loadData() {
  cacheList = new Array(1000000).fill("Data"); // Quên let/const -> thành window.cacheList
}
```

### 2. Không dọn dẹp Event Listener và Timers
Khi xài `setInterval`, hoặc `addEventListener`, các callback đóng vai trò tham chiếu giữ function của bạn tồn tại. Nếu cái UI components bị tháo ra (unmounted), mà bạn không "Clear" những vòng lặp này, rò rỉ sẽ xảy ra.
```javascript
const element = document.getElementById('btn');
element.addEventListener('click', function onClick() {
   // Nếu xóa cái 'btn' khỏi DOM nhưng không dùng removeEventListener, callback này vẫn ngầm ghim trong bộ nhớ 
});
```

### 3. Vấn nạn của Closure bị ngâm
Closure rất mạnh để giấu data. Nhưng một hàm closure đang hoạt động sẽ khóa tất cả bộ nhớ Parent scope lại khiến GC không thể xóa được vòng đời bên trong đó, nên nếu Closure sống mãi, parent memory cũng không bị thu dọn.

---

## Tổng kết

Bạn chỉ cần nhớ kĩ 2 định dạng:
1. **Stack:** Dùng cho dữ liệu nguyên thuỷ (String, Number, Bool...), nhẹ, nhanh, tĩnh. Copy biến là nhân bản song song giá trị.
2. **Heap:** Dành cho mảng (Array) và Object phức tạp, tốn dung lượng, cấu trúc linh động. Nó thao tác qua hệ thống "chìa khoá nhà" (Ref pointer) tại Stack. Copy biến chỉ là trao cho người khác chép lại địa chỉ ổ khóa.

Hiểu về bộ nhớ mang tới cho bạn kỹ năng tối ưu mã cho Framework hiện đại, giải thích được rất nhiều lỗi logic thay đổi state không mong muốn ở React hay Angular sau này. Và quan trọng nhất: viết code không làm máy khách hàng giật lag do bị tràn ngập Memory Leak.