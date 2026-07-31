---
title: "4.2 RxJS: Làm Chủ Luồng Dữ Liệu Bất Đồng Bộ"
source: "D:\9. Learn\12. llm wiki\raw\articles\4.2.md"
date_added: 2026-04-23
tags: [notes]
status: draft
summary: ""
---

# 4.2 RxJS: Làm Chủ Luồng Dữ Liệu Bất Đồng Bộ

Ở [bài 4.1](./4.1.md), chúng ta đã thuần phục được Async/Await. Tuy nhiên, `Promise` mang một yếu điểm chết người: Nó chỉ có thể phát ra **một kết quả duy nhất** và một khi đã kích hoạt, bạn **không thể hủy bỏ nó giữa chừng**.

Vấn đề đặt ra: Điều gì xảy ra nếu bạn có một *luồng* dữ liệu gửi về theo thời gian thực (như tọa độ chuột, thanh search người dùng đang gõ dở, hay stream giá cổ phiếu)? `Promise` đành bó tay. Đó là lúc chúng ta phải triệu hồi ma thuật **Reactive Programming** – vinh danh thư viện **RxJS** (Reactive Extensions for JavaScript).

---

## 💡 RxJS Khác Biệt Thế Nào?

Tư duy cốt lõi của RxJS là: **Bất cứ thứ gì cũng có thể là một Luồng dữ liệu (Data Stream)**. 
- Mảng = Stream số liệu.
- Phím gõ chữ = Stream theo thời gian.
- Request API = Stream HTTP.

Bạn điều hướng dòng chảy này, chặn nó, lọc nó, kết hợp 2 luồng với nhau trước khi nó chảy tới đích cuối, đó là "Tương tác phản ứng" (Reactive Programming).

### Bảng đối chiếu quyền lực
| Tính năng | Promise | RxJS Observable |
|:---|:---:|:---:|
| Trả ra bao nhiêu giá trị? | Duy nhất 1 | Rất nhiều (1, N hoặc vô hạn) |
| Có bị ép thực thi (Eager)? | Có (vừa khởi tạo là chạy ngay) | Không (Lazy - Chỉ chạy khi có bên đăng ký nghe) |
| Có huỷ ngang được không? | Không | **Được (`.unsubscribe`)** |

---

## 🏛️ 3 Trụ cột cốt lõi của RxJS

Đừng để định nghĩa phức tạp dọa bạn. RxJS vận hành giống hệt ngành sản xuất và phát sóng Youtube:

### 1. Observable (Kênh phát sóng - Kẻ tạo ra giá trị)
Nó là hộp đen có khả năng nhả ra (emit) nhiều tín hiệu theo thời gian. Nhưng đặc tính của Kênh phát sóng này là tính **Lười biếng (Lazy)**: Chừng nào chưa có ai mở tivi coi, kênh nó sẽ không thèm quay hình.

```javascript
import { Observable } from 'rxjs';

// Tạo ra một kênh phát sóng tin tức
const newsChannel$ = new Observable(subscriber => {
  subscriber.next("Bản tin sáng");
  
  setTimeout(() => {
    subscriber.next("Bản tin trưa");
  }, 2000);

  setTimeout(() => {
    subscriber.complete(); // Hết sóng, ngưng truyền
  }, 4000);
});

// Chú ý kí tự $ đằng sau chữ newsChannel$, đây là convention ngầm của ae dev báo hiệu "Thằng này là một Luồng (Stream)"
```

### 2. Observer (Người xem tivi)
Người xem tivi chỉ cầm trong tay một cái remote chứa 3 nút bấm tương ứng với 3 tín hiệu xảy ra khi xem kênh:
- `next`: Nhận tin mới thành công -> Tôi xem!
- `error`: Trạm phát nổ, đứt anten -> Tôi báo lỗi!
- `complete`: Kênh phát xong chương trình, tắt sóng -> Tôi đi ngủ!

```javascript
const meAsObserver = {
  next: (news) => console.log("📺 Xem tới: ", news),
  error: (err) => console.error("Ngắt cáp: ", err),
  complete: () => console.log("Nhà đài tắt sóng ròi, ngủ thôi!")
};
```

### 3. Subscription (Hợp đồng thuê bao cáp tivi)
Sợi cáp nối Kênh phát (`Observable`) tới Người xem (`Observer`). Khi kí hợp đồng (`.subscribe()`), kênh phát chính thức hoạt động! Phép thuật cực mạnh là nếu chán, bạn có thể **Xé bỏ hợp đồng (`unsubscribe`)** ngay lập tức và dập máy kênh sóng. Điều Promise bó tay!

```javascript
// BẤM NÚT ĐĂNG KÍ
const contract = newsChannel$.subscribe(meAsObserver);

// Ở Console sẽ thấy luồng thời gian:
// (Giây 0) 📺 Xem tới: Bản tin sáng
// (Giây 2) 📺 Xem tới: Bản tin trưa
// (Giây 4) Nhà đài tắt sóng ròi, ngủ thôi!
```

**Cách hủy luồng ngang xương:**
```javascript
// Nếu ta ngứa tay huỷ hợp đồng lúc 1 giây thay vì đợi xem.
setTimeout(() => {
  contract.unsubscribe(); // Hủy đăng ký!
  console.log("Tôi đã xé hợp đồng!");
}, 1000);

// Kết quả Console: Kênh "Bản tin trưa" lúc 2 giây sẽ bị nghẹn vĩnh viễn không bao giờ xuất hiện!
```

---

## 🔥 Subject: Cầu truyền hình trực tiếp (Multicasting)

Có một ngoại lệ là `Observable` bình thường luôn mặc định sản xuất 1 kênh mới toanh (Cold) cho mỗi người xem. Giám đốc có bật TV và nhân viên bật TV thì 2 cái TV tự chạy từ đầu (Unicast). Tránh điều bất lội đó, người ta phát minh ra **Subject**.

`Subject` giống hệt một Livestream: Rất nhiều thằng đệ cùng cắm rễ vào `.subscribe()`, và một khi Master hét `subject.next("Hành động!")`, tất cả các thằng đệ đều đồng loạt nhận thông báo trong 1 phần ngàn giây chênh lệch (Multicast). Cổ phiếu, Chat Realtime, State thay đổi - Chỗ ứng dụng tuyệt luân của Subject!

```javascript
import { Subject } from 'rxjs';

const liveStream$ = new Subject();

// Mở TV để xem
liveStream$.subscribe(data => console.log("User 1 nhận: " + data));
liveStream$.subscribe(data => console.log("User 2 nhận: " + data));

// Host bắt đầu phát sóng cho TẤT CẢ mọi TV đồng loạt
liveStream$.next("Trận bóng bắt đầu!"); 

// User 1 nhận: Trận bóng bắt đầu!
// User 2 nhận: Trận bóng bắt đầu!
```

---

## Lời Ngỏ Giao Thời

Đến lúc này, bạn đã thấy quyền lực khổng lồ của **Observable** khi nó vươn tay kiểm soát được Dòng Chảy Thời Gian - xử lý xuất sắc bài toán 1-N dữ liệu, lại còn Cancel được.
Nhưng `Observable` chưa thể ngồi lên ngai vàng JavaScript RxJS, nếu thiếu đi cái đinh ốc quyền năng mang tên: **Operators (Bộ Công cụ đường ống)**. 

Những thuật toán thay đổi luồng chảy, ví dụ như chặn rác (filter), nhân bản (map), kìm hãm luồng (debounce Time) sẽ tạo sức mạnh đáng sợ nhất của giới Front-end cho bạn. Nó sẽ được bật mí triệt để ở bài **[4.3 RxJS Map & Tap Mastery]**!