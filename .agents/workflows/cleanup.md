---
description: Kiểm tra sức khỏe wiki — phát hiện và sửa các vấn đề chất lượng
---

# /cleanup — Kiểm Tra Sức Khỏe Wiki

Workflow này quét toàn bộ wiki, đánh giá chất lượng từng bài, và tự động sửa chữa các vấn đề phát hiện được.

## Kích Hoạt

- `/cleanup` hoặc `/lint`
- "Kiểm tra sức khỏe wiki"
- "Audit wiki"
- "Dọn dẹp wiki"

## Bước Thực Hiện

### Phase 0: Quét Cơ Học — Script Trước, Đọc Sau

// turbo
```bash
python wiki/_build_backlinks.py --check
```

Script rebuild `_backlinks.json` rồi audit những thứ **kiểm chứng được bằng máy**:
wikilink hỏng, bài stub (<15 dòng), bài quá dài (>120 dòng), bài link ra <2 bài khác,
bài thiếu trong `_index.md`, raw chưa có trong `_absorb_log.json`.
Exit code khác 0 khi còn wikilink hỏng.

**Không tự đếm dòng và không tự dò link bằng mắt** — ở quy mô 100+ bài việc đó bỏ sót.
Output của script là danh sách công việc đầu vào cho Phase 2 và Phase 3.

### Phase 1: Build Context — Bản Đồ Wiki

// turbo-all

1. Đọc `wiki/_index.md` — danh sách tất cả bài
2. Đọc `wiki/_backlinks.json` — bản đồ liên kết (vừa rebuild ở Phase 0)
3. Đọc `wiki/_glossary.md` — thuật ngữ hiện có
4. Lấy số dòng và danh sách vấn đề cơ học từ output Phase 0

Tổng hợp thành bảng overview:

```
| Bài viết | Dòng | Backlinks | Status | Vấn đề |
|----------|------|-----------|--------|--------|
```

### Phase 2: Đánh Giá Từng Bài

// turbo-all

Đọc **toàn bộ nội dung** mỗi bài wiki. Với mỗi bài, đánh giá theo 7 tiêu chí:

#### 2.1 Cấu trúc
- **Theme-driven** (tốt): Sections chia theo chủ đề → `## Kiến Trúc`, `## Ứng Dụng`
- **Diary-driven** (xấu): Sections chia theo ngày tháng → `## Buổi họp tháng 3`, `## Sự kiện tháng 4`
- **Steve Jobs test:** Bài Wikipedia về Steve Jobs dùng "Early life", "Career" — KHÔNG dùng "The Xerox Visit", "The Lisa Failure"

#### 2.2 Kích thước
Lấy từ Phase 0 — không đếm lại thủ công.
- **Bloated** (>120 dòng nội dung): Xem xét tách sub-topic
- **Healthy** (15-120 dòng): Giữ nguyên
- **Stub** (<15 dòng): Cần bổ sung hoặc merge

#### 2.3 Giọng văn
Kiểm tra vi phạm tone Bách Khoa Toàn Thư:
- ❌ Peacock words: "legendary", "groundbreaking", "deeply", "truly", "thú vị là", "đáng chú ý"
- ❌ Editorial voice: "interestingly", "importantly", "it should be noted"
- ❌ Rhetorical questions
- ❌ Progressive narrative: "would go on to", "embarked on", "this journey"
- ❌ Qualifiers: "genuine", "raw", "powerful", "profound"

#### 2.4 Quote density
- ≤2 direct quotes mỗi bài → tốt
- 3+ quotes → xem xét cắt bỏ quote yếu nhất
- >1/3 nội dung là quotes → quá nhiều, cần viết lại

#### 2.5 Mạch viết (Narrative Coherence)
- Bài kể câu chuyện mạch lạc? Hay chỉ là danh sách sự kiện?
- Có thesis rõ ràng? Reader đọc xong hiểu significance?
- Bullet-point có tràn lan không? (Bullet-point chỉ khi liệt kê, phần giải thích dùng đoạn văn)

#### 2.6 Wikilinks
- Broken links: lấy danh sách từ Phase 0 → sửa hoặc xóa. Với mỗi link hỏng, xác định
  nó là **lỗi chính tả** (sửa target), **bài đã đổi tên** (trỏ lại), hay **bài còn thiếu
  thật** (tạo bài nếu đủ chất liệu, nếu không thì gỡ link)
- Missing links: Nhắc tới concept có bài wiki nhưng không link → thêm `[[wikilink]]`
- Frontmatter `related:` có đầy đủ? Mỗi bài ≥2 related links

#### 2.7 Frontmatter
- Có đủ fields bắt buộc? (title, source, date_added, tags, aliases, status, related, summary)
- `aliases` có đủ? Có bao gồm tên tiếng Việt và viết tắt phổ biến?
- `status` chính xác? (stub/draft/reviewed/canonical/needs-review)

#### 2.8 Contradiction Backlog
- Quét callout `[!warning] Mâu Thuẫn Chưa Giải Quyết` trong bài
- Nếu còn tồn tại → liệt kê trong báo cáo cleanup, đánh dấu ưu tiên review
- Nếu bài có `status: needs-review` → hiển thị rõ ràng cho người dùng

### Phase 3: Sửa Chữa

Với mỗi vấn đề phát hiện, tự động sửa nếu confident:

| Vấn đề | Hành động |
|--------|----------|
| Diary-driven structure | Viết lại sections theo theme |
| Bloated (>120 dòng) | Đề xuất tách (liệt kê sub-topics) |
| Stub (<15 dòng) | Tag `status: stub`, note cần bổ sung |
| Tone vi phạm | Viết lại câu/đoạn vi phạm |
| Quote tràn lan | Giữ 1-2 quote đắt nhất, xóa còn lại |
| Bullet-point tràn lan | Viết lại thành đoạn văn |
| Broken wikilinks | Sửa hoặc xóa |
| Missing wikilinks | Thêm `[[link]]` |
| Frontmatter thiếu | Bổ sung fields |

**Quy tắc sửa:**
- **Re-read toàn bộ bài** trước khi sửa bất kỳ dòng nào
- **Integrate** sửa đổi vào mạch viết, không tạo section mới chỉ để chứa fix
- Nếu bài cần viết lại >50% → hỏi người dùng trước

### Phase 4: Rebuild Indexes + Gate

// turbo

Sau khi sửa xong:
1. Cập nhật `wiki/_index.md` nếu có thay đổi (tên bài, aliases, tóm tắt)
2. Cập nhật `wiki/_glossary.md` nếu phát hiện thuật ngữ mới
3. Chạy lại `python wiki/_build_backlinks.py --check`

**Gate:** cleanup chỉ được coi là xong khi script exit 0 (không còn wikilink hỏng).
Nếu vẫn FAIL → quay lại Phase 3, không được báo cáo hoàn tất.

### Phase 5: Báo Cáo

```markdown
## 🔍 Báo Cáo Cleanup Wiki — YYYY-MM-DD

### Tổng quan:
- Bài đã scan: [N]
- Bài cần sửa: [M]
- Bài đã sửa: [K]
- Bài cần tách (bloated): [L]

### Chi tiết sửa chữa:
| Bài | Vấn đề | Hành động | Trạng thái |
|-----|--------|----------|-----------|

### Bài cần chú ý (chưa sửa tự động):
1. [[bài-bloated]] — 145 dòng, đề xuất tách: [sub-topics]
2. [[bài-cần-rewrite]] — >50% cần viết lại

### Thống kê sau cleanup:
- Stub: [N] bài | Draft: [N] bài | Reviewed: [N] bài
- Backlinks rebuilt: [X] targets, [Y] links
- Quét cơ học: [0] link hỏng · [N] stub · [M] bài quá dài · [K] bài link ra <2
```

### Phase 6: Append Operations Log

// turbo
Append vào `wiki/_ops_log.md`:
```markdown
## [YYYY-MM-DD] cleanup | [N] bài scanned, [M] sửa
```

## Quy Tắc Tự Động

// turbo-all

**Tự động chạy:** Đọc file, phân tích, sửa lỗi nhỏ (tone, wikilinks, frontmatter)
**Chờ xác nhận:** Viết lại >50% bài, tách bài, xóa nội dung

## Xử Lý Lỗi

| Tình huống | Cách xử lý |
|-----------|------------|
| `_backlinks.json` không tồn tại | Chạy `python wiki/_build_backlinks.py` trước |
| Bài wiki quá lớn để đọc 1 lần | Đọc theo phần (frontmatter → sections) |
| Không chắc nên sửa hay không | Liệt kê trong báo cáo, để người dùng quyết định |
