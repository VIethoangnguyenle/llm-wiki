---
title: "Wiki Overview — Executive Summary"
source: "compiled"
date_added: 2026-04-23
tags: [meta, overview, executive-summary]
aliases: [overview, tổng quan wiki]
status: canonical
related:
  - "[[_index]]"
  - "[[_glossary]]"
summary: "Bản tóm tắt tổng quan vault cho agent cross-project — đọc 1 file hiểu toàn bộ wiki."
---

## Vault Này Là Gì

Second Brain là **AI-managed knowledge base** theo phương pháp Karpathy LLM Wiki Pattern. LLM viết và duy trì toàn bộ nội dung wiki. Con người nạp dữ liệu thô, đặt câu hỏi, và duyệt kết quả.

## Domain Kiến Thức

Vault tập trung vào các lĩnh vực chính:

1. **Bảo mật & Kiểm soát Truy cập** — ABAC, RBAC, DAC, MAC và đặc biệt là NGAC (INCITS 565-2020): mô hình bảo mật, kiến trúc thực thi, và triển khai thực tế.
2. **Kiến trúc & Hệ thống** — Apache Kafka (replication, connect, streams), pub/sub, message broker, và các design pattern hệ thống.
3. **JavaScript & TypeScript** — cơ chế under-the-hood: call stack, event loop, memory model, type system, RxJS.
4. **Java & Spring** — IoC/DI, multithreading, virtual threads, immutability, validation, metaprogramming qua annotation.
5. **Cơ sở dữ liệu** — Oracle: ACID, PL/SQL, cost-based optimizer, normalization, flashback.
6. **AI & LLM** — Ollama, local LLM tooling, RAG/GraphRAG, small language models, agent kit.

## Quy Mô Hiện Tại

- **108 bài wiki** (75 concepts, 21 tools, 0 people, 12 comparisons)
- **112 thuật ngữ** trong glossary
- **91 raw sources** đã biên dịch (21 nguồn gốc đã mất, xem `_absorb_log.json`)
- **Ngôn ngữ:** Tiếng Việt (nội dung), English (thuật ngữ kỹ thuật)

## Cách Truy Cập

- **Tra cứu nhanh:** Đọc `wiki/_index.md` (danh sách đầy đủ) hoặc `wiki/_glossary.md` (thuật ngữ)
- **Hỏi đáp:** `/ask [câu hỏi]` — trả lời dựa trên nội dung wiki
- **Nạp dữ liệu mới:** `/ingest [URL hoặc file]`
- **Nghiên cứu tự động:** `/autoresearch [chủ đề]` — agent tự tìm kiếm web và nạp

## Bài Viết Trọng Tâm

Các bài wiki có nhiều backlinks nhất (central nodes trong knowledge graph):

- [[apache-kafka]] (13 backlinks) — nền tảng streaming, hub của cụm Kiến trúc
- [[ollama]] (9) — runtime chạy LLM cục bộ, hub của cụm AI/LLM
- [[kafka-replication]] (8) — cơ chế nhân bản và độ bền dữ liệu của Kafka
- [[attribute-based-access-control]] (8) — hub của cụm Bảo mật
- [[typescript]] (7) — hub của cụm JS/TS
- [[spring-ioc-di]] (6) — hub của cụm Java/Spring
- [[oracle-database]] (6) — hub của cụm Database

## Quy Trình Vận Hành

```
Nạp dữ liệu → /ingest → raw/
Biên dịch    → /compile → wiki/ (có Contradiction Check)
Hỏi đáp      → /ask → trả lời từ wiki
Nghiên cứu   → /autoresearch → search web → raw/ → wiki/
Lưu nhanh    → /save → conversation → raw/ → wiki/
Mở rộng      → /breakdown → tìm khái niệm còn thiếu
Dọn dẹp      → /cleanup → audit chất lượng wiki
Bản đồ       → /overview → cập nhật topic map trong README
```

## Kiểm Tra Sức Khỏe

```bash
python wiki/_build_backlinks.py --check
```

Script dựng lại `_backlinks.json` và audit: wikilink hỏng, bài stub, bài quá dài, bài thiếu liên kết, bài thiếu trong `_index.md`, raw chưa có trong `_absorb_log.json`. Exit code khác 0 khi còn wikilink hỏng.
