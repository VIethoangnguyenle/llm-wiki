---
title: "2.3 Clean Code: Các Lối Tư Duy Mới Về Vòng Lặp (For Loop)"
source: "D:\9. Learn\12. llm wiki\raw\articles\2.3.md"
date_added: 2026-04-23
tags: [notes]
status: draft
summary: ""
---

# 2.3 Clean Code: Các Lối Tư Duy Mới Về Vòng Lặp (For Loop)

Ngày đầu bước chân vào thế giới lập trình, "bộ giáp" đầu tiên chúng ta khoác lên người để giải quyết vòng lặp chắc chắn là `for (let i = 0; i < array.length; i++)`. Gần như ở bất cứ bài toán duyệt mảng nào, ngón tay ta cũng theo bản năng gõ ngay cấu trúc kinh điển này.

Dù cỗ máy `for` cũ kỹ này vận hành ổn định và chạy rất nhanh, nhưng trong thế giới JavaScript hiện đại (hay kỷ nguyên **Clean Code** và **Functional Programming**), cấu trúc này bộc lộ quá nhiều yếu điểm cồng kềnh.

Đã đến lúc chúng ta "nâng cấp hệ tư tưởng", dẹp bỏ những biến vòng lặp dư thừa và tiếp cận với các luồng dữ liệu (Data Flow) trong sáng hơn.

---

## 1. Viện Bảo Tàng: `for` Cổ Điển và bẫy `for...in`

### Vòng lặp `for` truyền thống
Bạn nghĩ rằng nó vô hại cho đến khi gặp cảnh lặp lồng lặp, thao tác chỉ mục mệt nhoài và dễ sảy chân vào lỗi "Cộng dư 1" (Off-by-one errors). Thêm nữa, não bộ phải tự biên dịch xem _chúng ta đang lặp để làm gì_.

```javascript
const warriors = ['Goku', 'Itachi', 'Saitama'];

// Cách cổ điển - Đế chế tính toán cơ học (Imperative)
for (let i = 0; i < warriors.length; i++) {
  console.__*/log(warriors[i] + ' ready to fight!');
}
```

### Cái lồng bẫy mang tên `for...in`
Lỗi mà 9/10 Newbie gặp phải là lấy `for...in` mang đi duyệt mảng. Lệnh này được sinh ra để quét qua **thuộc tính của một Object (Keys)** (và vô tình quét qua cả Prototype chuỗi thừa hưởng bên ngoài). Sử dụng trên mảng (Arrays) không đảm bảo đúng thứ tự, và index trẻ lại dưới dạng String. 

```javascript
// ĐỪNG GÕ THẾ NÀY CHO MẢNG
for (let index in warriors) {
    console.log(index); // "0", "1", "2" -> Là String!
}
```

---

## 2. Bước Tiến Bộ: Xài `for...of`

Sự thay thế hoàn hảo và thanh tú nhất mà ES6 đem lại cho vòng lặp thông thường chính là `for...of`.
Nó duyệt qua "Giá trị (Value)" của các đối tượng có thể lặp (Iterables) như chuỗi `String`, `Array`, `Map`, `Set`.

```javascript
// Tư duy gọn gàng hơn
for (const warrior of warriors) {
  console.log(`${warrior} ready to fight!`);
}
```
**Tại sao nên dùng?**
- **Sạch sẽ:** Không còn mớ `i = 0`, `i < length` làm nhiễu mắt.
- **Có thể ngăn chặn đột ngột:** Không giống các hàm phía dưới, `for...of` cho phép bạn gọi `break;` (ngắt) hoặc `continue;` (bỏ qua) tự do.
- **Xử lý Bất đồng bộ (Async/Await) ngon lành:** (Xem phần 4).

---

## 3. Khai sáng Functional Programming: `map`, `filter`, `reduce`

Nếu tư tưởng vòng lặp cổ điển đè nặng lên não bộ việc "Làm điều đó như thế nào" (Imperative - Cần mẫn chỉ định từng bước). Thì xu hướng JavaScript Clean Code thiên về "Bạn muốn điều gì" (Declarative - Khai báo đích đến).

Hầu hết thời gian vòng lặp của bạn nhằm mục đích: **Biến đổi** 1 mảng cũ thành mảng mới, **Lọc** phần tử, hay **Tính tổng/Gộp chung** một cái gì đó. Ba sát thủ của mảng đảm nhận trọng trách này:

### 🧩 `Array.map()` - Biến đổi (Transformation)
Dùng khi bạn muốn trả về một mảng MỚI có độ dài y xì mảng cũ, nhưng giá trị bên trong đã được thao tác lại. Không làm bẩn (mutate) mảng ban đầu!

```javascript
const prices = [100, 200, 300];

// Xưa kia: tạo mảng rỗng [] -> đẩy dần vào (push)
// Hiện đại, tư duy hàm:
const discountedPrices = prices.map(price => price * 0.9);
// Result: [90, 180, 270] 
```

### ✂️ `Array.filter()` - Bộ lọc (Sàng lọc Data)
Nhặt những thứ mong muốn với một biểu thức `true/false`.
```javascript
const students = [
  { name: 'A', pass: true },
  { name: 'B', pass: false },
  { name: 'C', pass: true }
];

const graduated = students.filter(student => student.pass);
// Gọn gàng, dễ hiểu ngay lập tức so với if-else kết hợp push.
```

### 📦 `Array.reduce()` - Nhà máy tổng hợp
Con quái vật khó hiểu nhất nhưng quyền lực nhất của các lệnh lặp. Gom vạn vật thành một mối (tính tổng, đếm số lượng, quy đổi Array -> Object).

```javascript
const cart = [10, 20, 30];
// reduce(hàm_xử_lý, giá_trị_khởi_tạo)
const total = cart.reduce((accumulator, item) => accumulator + item, 0); 
// total = 60
```

> [!CAUTION] Cảnh báo lạm dụng `.forEach()`
> Mọi người thích xài `.forEach()` để viết ngắn. Tuy nhiên `forEach` KHÔNG trả về thứ gì cả (`undefined`), và có chứa hàm sinh ra hiệu ứng phụ (Side-effects). Bạn không thể dùng từ khoá `break` hay `continue` để ngắt ngang `forEach`. **Theo Clean code: Cố gắng dùng `map/filter/reduce` hoặc `for...of` thay vì `forEach`**.

---

## 4. Xử lý "Bất đồng bộ" Trong Vòng lặp

Hổ mang cắn chết hàng loạt dev JS khi muốn kết hợp lặp mảng gọi API (bất đồng bộ).

```javascript
// ⚡ ĐOẠN CODE SAI LẦM PHỔ BIẾN
const ids = [1, 2, 3];

ids.forEach(async (id) => {
  const data = await fetchUserData(id); // await này vô nghĩa
  console.log(data);
});
console.log("Xong!"); 
// Chữ "Xong!" sẽ in ra TRƯỚC CẢ khi cục fetch kia chạy xong. (Vì forEach không thèm đợi)
```

**✅ Giải pháp 1: Chạy song song tốn ít thời gian (Parallel) bằng `Promise.all` và `map`**
Dùng khi thứ tự API tải về không bị ràng buộc phụ thuộc nhau. Nhanh nhất!
```javascript
const promises = ids.map(id => fetchUserData(id));
const allData = await Promise.all(promises); 
```

**✅ Giải pháp 2: Chạy kiên nhẫn từng cái một (Sequential) bằng `for...of`**
Dùng khi cái số `2` bẳt buộc đợi kết quả trả về của số `1`.
```javascript
for (const id of ids) {
    const data = await fetchUserData(id);
    console.log("Đã tải xong cái số", id);
}
console.log("Xong toàn bộ!");
```

---

## Chốt Luận Điểm

Kỉ nguyên Code "Sạch" nói _KHÔNG_ với cách điều hướng mã bằng logic cặn kẽ và _CÓ_ với biểu đồ ngữ nghĩa. 
Khi bạn nhìn thấy:
- Một cái `map`: Bộ não bạn lập tức nảy số *"À, chỗ này là quy đổi Dữ liệu từ A sáng B"*.
- Một cái `filter`: *"À, chỗ này đang lọc lại cái mảng"*.
- Thay vì thấy một vòng lặp `for` với các mớ logic if-else bùi nhùi không biết đích đến.

Quy luật cho một JSWarrior:
Nếu cần tính toán và trả ra mảng mới -> Xài các hàm HOF (Map, Reduce, Filter).
Nếu đơn thuần cần lặp qua các phần tử để tạo Side-effects, hoặc xử lý `await` đồng bộ thì kết bạn với `for...of`!