---
title: "4.3 RxJS Mastery: Làm Chủ Đường Ống Kì Diệu Map và Tap"
source: "D:\9. Learn\12. llm wiki\raw\articles\4.3.md"
date_added: 2026-04-23
tags: [notes]
status: draft
summary: ""
---

# 4.3 RxJS Mastery: Làm Chủ Đường Ống Kì Diệu Map và Tap

Ở bài trước, chúng ta đã nắm trong tay Kênh phát sóng (`Observable`) và Người xem (`Observer`). Tuy nhiên, sức mạnh tối thượng giúp RxJS thao túng giang hồ không nằm ở cội nguồn phát, nó nằm ở **Chặng đường vận chuyển**.

Hãy hình dung nhà máy bơm ra dòng nước thô (Raw Data). Trước khi đến vòi uống của người xem, dòng nước đấy phải đi qua một hệ thống ống nước (`pipe`) chứa đầy màng lọc, cỗ máy đóng chai. Khái niệm đó trong RxJS gọi là **Operators (Toán tử)**.

Hai màng lọc được sử dụng dày đặc gấp vạn lần bất kỳ màng lọc nào khác chính là `map` và `tap`. Tinh thông 2 cái tên này là nền tảng tối thiểu của mọi dev Frontend (Đặc biệt là hệ sinh thái Angular).

---

## 🛠️ The Pipeline: Khớp Nối `.pipe()`

Trước RxJS phiên bản 5.5, ta cứ nối chuỗi operator trực tiếp như con rết. Nhưng hiện tại, cấu trúc chuẩn hóa bắt buộc toàn bộ bộ lọc phải tống nhét vào một cái "hộp nối ống" duy nhất: hàm `.pipe()`.

```javascript
import { of } from 'rxjs';
import { map, tap } from 'rxjs/operators';

// Tạo nhanh Kênh phát 3 cục nước thô
const waterStream$ = of(1, 2, 3);

// ❌ Không xài: waterStream$.map(...).tap(...)
// ✅ Xài chuẩn: Thông qua ống Pipe
waterStream$.pipe(
   // Gắn các màng lọc vào đây, phẩy cách nhau bằng dấu phẩy
).subscribe(console.log);
```

---

## 🪄 Toán tử `map`: Kẻ Biến Hình Đa Cấp

Thực chất, cơ chế của `map` trong RxJS y hệt lệnh `Array.map()` của JS nguyên thủy. Bất kể giá trị nào khi bơi qua màng lọc `map`, nó sẽ bị bạn "chế tác" lại cấu hình, sau đó ném cục dữ liệu thay hình đổi dạng đó xuống đường ống tiếp theo.

**Ứng dụng vàng:** Dùng để "bóc lột" cấu trúc mâm dữ liệu từ API phức tạp xuống còn lấy đúng thứ mình cần.

```javascript
import { from } from 'rxjs';
import { map } from 'rxjs/operators';

const responseAPI$ = from([{
  status: 200,
  data: {
    user: { id: 99, name: "JohnDoe" }
  }
}]);

// 1. Màng lọc "Bóc hành" - Tước bỏ đi lớp vỏ thừa mứa
const nameOnly$ = responseAPI$.pipe(
  map(response => response.data),       // Chỉ trích xuất cái lõi "data"
  map(data => data.user.name),          // Xuống thêm 1 lớp lọc lấy cái "name"
  map(name => name.toUpperCase())       // Viết Hoa nó nốt
);

// Subscribe hưởng thành quả trong sạch
nameOnly$.subscribe(res => console.log('👤 Tên là:', res)); 
// In ra: "👤 Tên là: JOHNDOE"
```

> **Đầu vào -> Đi qua `map` -> Đầu ra khác biệt hoàn toàn.**

---

## 👀 Toán tử `tap`: Kẻ Nhìn Trộm Tàng Hình (Side-Effects)

`tap` (như có người vỗ nhẹ lên vai bạn) cực kỳ đặc biệt: Trái ngược với Map, `tap` **TUYỆT ĐỐI KHÔNG LÀM THAY ĐỔI / CHAM VÀO** cấu hình giá trị truyền qua luồng.

Đã không thay đổi cục dữ liệu, vậy nó nhào vô ống để làm gì? Để đáp ứng **Tác dụng phụ (Side-effects)**.

**Ứng dụng vàng của Tap:**
- In log ra console hòng Debug để theo dõi cục máu đi đến đâu rồi.
- Lưu cache xuống kho LocalStorage để trộm thông tin dự bị.
- Kích hoạt vòng quay Loading Spinner UI `isLoading = true/false` cho đẹp mắt hệ thống người dùng trước khi luồng bắn ra.

```javascript
import { of } from 'rxjs';
import { map, tap } from 'rxjs/operators';

const userActions$ = of("Click_Login");

userActions$.pipe(
  tap(action => console.log("🔍 [Tình báo]: Có người vừa ấn: ", action)), // Rình mò
  map(action => action + "_Xác_Nhận_Thành_Công"), // Đổi bản chất giá trị
  tap(action => localStorage.setItem("last_action", action)) // Lén lấy kết quả mới cất vào Kho riêng
)
.subscribe(finalResult => console.log("✅ Cửa ải cuối cùng nhận: " + finalResult));

// 1. Nhìn lén: "Click_Login"
// 2. Chế tác đổi ruột ở map.
// 3. Nhìn lén cất vào kho cái ruột mới.
// 4. In ra: "✅ Cửa ải cuối cùng nhận: Click_Login_Xác_Nhận_Thành_Công"
```
Nhờ `tap`, ta hoàn toàn giải cứu con tim trong sáng của hàm subscribe cuối cùng. Hàm `subscribe` chỉ nhận kết quả để render, khỏi phải lo đi Log lôi thôi dính dáng bên lề.

---

## 🎯 Tổng kết: Trận Địa Map và Tap

Để sử dụng một cách tối ưu hoá và Clean Code khi đứng trước đường ống RxJS, chỉ cần quy định quy chuẩn tư duy ngắn gọn:

1. Có ý định thay đổi trạng thái hình học biến số, nhặt dữ liệu mảng, trích xuất con số? ➡️ Nhờ vả bạn **`map`**.
2. Có ý định ghi chép Debug tiến trình làm việc, thiết lập trạng thái Loading Web / tắt UI, sao chép rình mò dữ liệu? ➡️ Khắc dấu bạn hiền **`tap`**.

Kết hợp thành thục hai thanh nhẫn giả này, bạn đã thao túng toàn phần logic dữ liệu. Giờ thì chuẩn bị giáp chiến với một chương cuối cùng và cũng là hiện đại nhất - sự hội tụ của chúng tại kiến trúc khổng lồ [Chương 5: Angular Modern Web]!