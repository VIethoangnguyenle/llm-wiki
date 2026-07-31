---
title: "5.1 Modern Web: Làm Chủ State Management Với NgRx Trong Angular"
source: "D:\9. Learn\12. llm wiki\raw\articles\5.1.md"
date_added: 2026-04-23
tags: [notes]
status: draft
summary: ""
---

# 5.1 Modern Web: Làm Chủ State Management Với NgRx Trong Angular

Trải qua những chặng đường thấu hiểu JavaScript cốt lõi, giờ là lúc chúng ta ghép mọi thứ (Scope, Immutability, Map/Reduce và RxJS Observables) vào một "Hệ sinh thái thực chiến" tinh vi và quy mô cực lớn bậc nhất thế giới Frontend: **Angular kết hợp NgRx**.

## 💣 Nỗi Nám Ảnh Prop Drilling (Truyền Nhận Qua Trung Gian)

Ngày trước, để chuyển một cục Data từ Component Ông, nội truyền xuống Component Cháu, cách duy nhất là bạn phải cõng cục Data đó đẩy xuống Bố (bằng `@Input()`), rồi từ Bố tiếp tục tạo `@Input()` gồng xuống cho Cháu. Vòng lặp báo tin cũng ngược lại bằng `@Output()` EventEmitter (gây Event Bubbling).

Kiến trúc liên đới chằng chịt rễ cây này (hay còn gọi là *Prop Drilling*) dẫn đến một bãi mìn: Lúc xảy ra lỗi ở Cháu, ta phải mò ngược lùi 10 cái lồng Component xem thằng nào ở trên truyền dữ liệu sai.

Đó là lúc khái niệm **State Management (Quản Trị Trạng Thái Tập Trung)** ra đời.

---

## 🏛️ Triết lý NgRx - Xây Dựng "Lầu Năm Góc" Code

NgRx là thư viện triển khai mô hình Redux Pattern nổi tiếng dành riêng cho Angular, ứng dụng mạnh mẽ 100% "Dòng chảy RxJS" như bạn đã tu luyện ở Chương 4.

Thay vì Component cha con lén lút trao Data với nhau, NgRx đem mọi bộ não lên lập một **"Kho thóc trung ương" (Store)** duy nhất. Mọi bộ phận UI chỉ làm 2 việc: Lấy data về để hiển thị và Hét to hành động (Action) để Kho trung ương điều chỉnh. Kỷ cương được thiết lập qua 5 vị chỉ huy:

### 1️⃣ STORE (Kho Lưu Trữ - Single Source of Truth)
Nơi duy nhất nắm giữ toàn bộ dữ liệu dự trữ hệ thống (State) dưới dạng sống ngầm (Observable). Nếu cần lấy danh sách Customer, bất cứ Component nào gọi Store lấy ra là giống hệt nhau, không có sự sai khác hay chờ đợi 2 bên độc lập.

### 2️⃣ ACTIONS (Lệnh Trạng - Hét Hành Động)
Component trở thành "Kẻ ngốc nghếch" (Dumb Components). Nút Login trên UI không chứa hàm xử lí Login, khi bấm vào, nó chỉ việc đứng hét to một câu khẩu hiệu kiểu dạng:
> Lệnh `[Auth Page] Login User Nhé Kho!`

```typescript
// Chỉ định cấu trúc lệnh
export const loginUser = createAction(
  '[Auth Page] Login User',
  props<{ username: string }>() // Cầm gói hồ sơ đính kèm báo lên.
);
```

### 3️⃣ REDUCERS (Kế Toán Kho)
Thằng duy nhất nắm chìa khóa nhà Kho là Thằng Kế Toán `Reducer`. Khắp app không ai có quyền sửa data trong Store ngoại trừ Reducer.
Khi nó nghe lệnh `[Auth Page] Login User`, nó lôi hồ sơ ra phân tích và bắt đầu tạo một phiên bản MỚI cho Kho Bạc.

> [!CAUTION] Tính Cố Định Bất Biến (Immutability)
> Tại đây kiến thức Bài 1.2 lên ngôi: Reducers phải là MỘT HÀM THUẦN TÚY (Pure Function). Nghĩa là nó không được sửa mảng State cũ, mà nó dùng `spread operator (...)` để xé lấy một Mảng Copy, cập nhật và đổ trả vào kho bản mới nhất, xoá bản cũ!

### 4️⃣ SELECTORS (Camera Kính Viễn Vọng)
Trong Kho bãi chứa tới hàng trăm ngàn Data (User, Post, Setting). Để UI Component ngoài xa tránh việc lấy lộn thông tin, người ta cấp cho chúng các cái Ống nhòm `Selector`.

```typescript
// Bộ ống nhòm chỉ quét đúng Khu vực Danh Sách Users. Tránh quét toàn bộ làm giật tải.
export const selectAllUsers = createSelector(
  selectUserState,
  (state) => state.users
);
```

### 5️⃣ EFFECTS (Bộ Trưởng Giao Thương - Xử Lý Bất Đồng Bộ)
Tuyệt đối cấm Reducers gọi API ngoài hay dính líu đến cái gì mất thời gian. Khi nhận Lệnh đi lấy API `[User] Fetch Users`, Thằng `Reducers` sẽ làm ngơ, người nghe là **Effects**.
`Effects` chạy ra ngoài gọi API, đón lấy cục Data xong, nó mới đóng gói ném trả ngược về một cái Lệnh Mới cho Hệ thống: `[User API] Danh Sách Tải Thành Công`. Lúc này Reducer lại ra bê cục đó đắp vô kho.
 
> Quá trình giao dịch bên ngoài này sặc mùi `RxJS Map/SwitchMap/Tap` vì nó hứng luồng data.

---

## 💎 Thành Quả Đoạt Được Bằng State Management

Cấu trúc 5 thành tựu (Store, Action, Reducer, Selector, Effect) tuy cực kỳ tốn thời kì khởi tạo (Boilerplate) - Nhưng một khi Hệ thống phình to lên, lợi thế của NgRx sẽ đè bẹp tất cả:

1. **Khử sự Tùy tiện:** Data luân chuyển đi theo 1 chiều ngang kim tự tháp chóp `(Action -> Reducer -> Store -> Selector -> Component)`. Đứt gãy ở đâu, debug đúng cái khúc đó.
2. **Kiến Trúc Cô Lập Testing (Unit Testing hân hoan):** 
   - Vì Code chia chẻ từng File Lệnh (Action), Lọc Dữ liệu (Selector), bạn test Code Logic 100% không liên lụy chi đến cái Giao Diện UI cồng kềnh.
3. **Nâng Tâm Giao Diện (Time Traveling):** Khi kết nối với `Redux DevTools`, bởi do mỗi `Action` trút vô là một bản thể Array Data mới, bạn có quyền ấn nút "Giật ngược Cổ máy thời gian", UI lùi về trạng thái y hệt thời điểm bấm nút 5 phút trước cho bạn quan sát lỗi.

---

## Tóm gọn hành trình Mảng

Vậy là ta đã đi một quãng đường dằng dặc: Từ hiểu tại sao Mảng và Objects dễ bị lây lan tham chiếu chéo (Heap Memory Bài 1.3), tới cách tách mảng ra lọc (Array Filter/Map Bài 2.3), quản lý Async thời gian (RxJS Bài 4.2), và giờ đây - NgRx.

Nếu không nắm bắt vững chắc quy luật **Immutability (Sự bất biến)** và **RxJS Observable**, làm việc với một thư viện Store đỉnh lưu như NgRx trong Angular sẽ làm bạn rơi vào mê hồn trận và code ra vô số lỗi phản tác dụng. Chúc mừng bạn đã đi đường vòng mà chắc chắn nhất để nâng cấp hệ kĩ năng thực chiến hoàn chỉnh của giới Front-end!