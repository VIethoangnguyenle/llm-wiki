---
title: "3.1 DOM Performance Warfare: Cuộc Chiến Tối Ưu Tốc Độ Giao Diện"
source: "D:\9. Learn\12. llm wiki\raw\articles\3.1.md"
date_added: 2026-04-23
tags: [notes]
status: draft
summary: ""
---

# 3.1 DOM Performance Warfare: Cuộc Chiến Tối Ưu Tốc Độ Giao Diện

Câu cửa miệng trong giới lập trình Web trước khi kỉ nguyên của các JS Framework thống trị là: *"JavaScript thì cực nhanh, thứ làm web chậm là cái DOM"*. 

**DOM (Document Object Model)** - cây phả hệ phản tác cấu trúc HTML lên trình duyệt. Việc đọc, sửa, và cấy ghép HTML thông qua DOM tốn hao tài nguyên một cách kinh khủng. Trong một hệ thống Web lớn, nếu bạn thao tác DOM không khéo léo, giao diện sẽ trở nên giật cục (lag), đơ khung hình, khiến trải nghiệm người dùng trở thành thảm hoạ.

Chào mừng đến với mặt trận DOM Performance Warfare! Để chiến thắng, ta cần hiểu kẻ thù và trang bị kỹ thuật.

---

## 1. Mổ xẻ cơ chế: Tội đồ Reflow và Repaint

Bất cứ khi nào bạn thao tác đổi DOM bằng JS (ví dụ đổi màu chữ, ẩn/hiện element, dời khối `div` sang trái), Trình duyệt phải thực hiện tiến trình **Critical Rendering Path (Luồng Render Cắt Lớp)**:

1. Thiết lập cây hình thái DOM và Cây CSSOM (Style).
2. Quy định lại bộ layout tính toán độ rộng, chiều cao, toạ độ phân rã cho toàn bộ trang web (gọi là **Reflow / Layout**).
3. Đổ mực in các toạ độ màn hình đó thành các Pixel thực tế hiển thị (gọi là **Repaint / Paint**).

> [!WARNING] Cảnh báo Đỏ
> **Repaint (Phơi màu)** tốn nhiều thời gian, nhưng **Reflow (Bố cục lại kích thước)** mới là con quái vật ngấu nghiến tài nguyên. Nó gây lan truyền: Kéo rộng 1 cái thẻ `div` cha có thể làm tất cả thẻ con và các block hàng xóm bên cạnh phải tính toán Reflow theo! Đừng bao giờ kích hoạt Reflow nếu không cần thiết.

---

## 2. Các Chiến Thuật Tối Ưu Hóa (Tactics)

### ⚔️ Chiến thuật 1: Gom nhóm thao tác trước khi nạp DOM (Batching)

Đây là lối code vô cớ bòn rút sức lao động của Browser nhiều nhất.

```javascript
// ⚡ CODE SAI LẦM: Chọc vào DOM 100 lần 
const container = document.getElementById('list');

for (let i = 0; i < 100; i++) {
  container.innerHTML += `<li>Mục số ${i}</li>`; // Gọi Reflow 100 lần !!!
}
```

Hãy nhớ, môi trường thực thi bộ nhớ của JS cực nhanh. Hãy nhào nặn hoàn tất dữ liệu đàng hoàng trong JS (như một xưởng đúc kín), và cuối cùng mới đem thả kết quả vào DOM.

```javascript
// ✅ CODE CHUẨN: Bắn 1 phát vào DOM
const container = document.getElementById('list');
let listHTML = ''; 

for (let i = 0; i < 100; i++) {
  listHTML += `<li>Mục số ${i}</li>`; // Việc nối chuỗi này nằm trọn trong vũng JS
}

// Gọi Reflow ĐÚNG 1 LẦN DƯY NHẤT
container.innerHTML = listHTML; 
```

### ⚔️ Chiến thuật 2: Sử Dụng Vũ Khí Mật `DocumentFragment`

Nếu bài toán buộc bạn không thể xài chuỗi `innerHTML` (do cấu trúc Tag phức tạp cần build qua hàm `document.createElement`), thì sao?

Đừng bao giờ cứ tạo `Node` cái nào thì `.appendChild` vào `DOM` mẹ ngay lúc đó. Thay vào đó, xài `DocumentFragment`. Đây là một dạng "DOM giả ảo" nhẹ, sống cô lập chìm nghỉm trong RAM và không hiển thị (không bị bắt Reflow).

```javascript
const list = document.getElementById('list');
const fragment = document.createDocumentFragment(); // Vùng chóp bóng tối

for (let i = 0; i < 100; i++) {
  const li = document.createElement('li');
  li.textContent = `Mục hệ Node ${i}`;
  
  fragment.appendChild(li); // Nạp 100 cái li vào fragment ảo. Lúc này DOM mẹ vẫn chưa biết gì!
}

// Bùm, bắn nguyên cái Fragment chứa 100 Node đó vào DOM thực tế 1 lần thôi!
list.appendChild(fragment);
```

### ⚔️ Chiến thuật 3: Né hiệu ứng Layout Thrashing (Máy ép dồn layout)

Browser vốn đã có máy vắt DOM riêng. Tức là đôi khi bạn xài JS thao túng DOM 5 lần, Browser nó khôn, nó gom 5 lần đó ròi mới Render đúng 1 đợt chót.
Tuy nhiên, có một thủ phạm xoá bỏ sự tự tối ưu hoá của trình duyệt = Gọi hàm ép đọc kích thước `Offset`.

```javascript
// Ngay khi bạn gọi hàm đọc .offsetHeight hay .offsetWidth, 
// trình duyệt phải lập tức DỪNG MỌI THỨ VÀ ĐO ĐẠC KÍCH THƯỚC DOM BÂY GIỜ LẬP TỨC.
const boxes = document.querySelectorAll('.box');

for (let i = 0; i < boxes.length; i++) {
  // Lấy độ rộng .offsetWidth TRONG CÙNG LÚC lặp bắt trình duyệt Đo - Render - Đo - Render cồng kềnh quá tải.
  const oldWidth = boxes[i].offsetWidth; 
  boxes[i].style.width = oldWidth + 10 + 'px';
}
```

**Cách gỡ bom:** Tách hoàn toàn quá trình LẤY DỮ LIỆU ĐỌC (Read) và QUÁ TRÌNH GÁN (Write) ra làm hai mảng loop khác biệt nhau, hoặc cache (lưu nháp) giá trị thông số lại.

### ⚔️ Chiến thuật 4: Event Delegation (Bố Cáo Mạng Lưới Thay Vì Gõ Cửa Tầng Ô)

Hãy tưởng tượng bạn có 1 cái bảng Table sinh ra chứa tận 1000 dòng học sinh cần gắn Nút (Xóa). 

Việc gắn `.addEventListener` cho tận 1000 cái nút khác nhau sẽ khiến máy phình bộ nhớ kẹt bộ nhớ Memory (đã nhắc tới ở bài `Heap Allocation`).

Nhờ đặc tính sinh học của JS là **Event Bubbling (Sự kiện nổi Bọt)**: Bất cứ nút nào click gõ cọc, âm báo sẽ lan truyền truyền từ thẻ con dội dội ra ngõ bố mẹ của nó. Do đó, hãy cắm ĐÚNG 1 CÁI ĐUÔI THEO DÕI (`Listener`) nằm ngay tại thẻ mẹ bự chát bám lấy tất cả!

```javascript
// Thay vì gắn 1000 sự kiện cho the <li> con.
// Ta gắn DUY NHẤT cho cái <ul> cha bao trọn.
const ulParent = document.getElementById('student-table');

ulParent.addEventListener('click', function(event) {
  // event.target là kẻ cụ thể bị bấm trúng.
  // Kiểm tra nếu kẻ đó là Nút xóa
  if (event.target && event.target.matches('button.btn-delete')) {
    console.log('Bạn vừa xóa một ai đó kìa!', event.target.id);
  }
});
```

---

## 3. Lời Mở Đường tới Giao Kỷ Nguyên JS Frameworks

Tất cả các chiến thuật đẫm máu mà chúng ta áp dụng ở phương diện DOM Manipulation trên nhằm ép buộc cho số lần **Reflow/Repaint** nhỏ nhoi nhất.

Đó cũng là nguồn cảm hứng cho sự ra đời của **Virtual DOM (DOM Ảo)** - hạt nhân tạo nên sức mạnh của **ReactJS** hay cơ chế của các framework đương đại. Những Framework này đã lấy nỗi đau `DocumentFragment`, thiết kế ra cả một kiến trúc chạy sẵn đằng sau:
> *"Cứ ném data vào tao, tao tự tính thuật toán (Diffing) trong V-DOM chả cần màng tới DOM thực xem có gì khác không, hễ cập nhật thay đổi là tao tính lại rọc chính xác chỉ duy nhất 1 cục trơ trọi chênh lệch Reflow lên cấu trúc trình duyệt."*

Nắm chóp ngọn nguồn hiệu năng DOM, bạn sẽ hiểu vì sao việc "Render lại Component" mà giới React rôm rả hay than phiền... lại tối quan trọng tới nhường vậy!