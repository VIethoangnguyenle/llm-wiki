---
title: "Ollama"
source: "compiled"
date_added: 2026-05-05
tags: [tool, ai, local-llm]
aliases: [ollama-architecture]
status: canonical
related:
  - "[[ollama-vs-vllm-vs-lmstudio]]"
  - "[[vllm]]"
  - "[[lm-studio]]"
  - "[[docker]]"
  - "[[retrieval-augmented-generation]]"
  - "[[llama-3.2-3b-instruct]]"
summary: "Framework mã nguồn mở quản lý và chạy mô hình ngôn ngữ lớn (LLM) cục bộ với kiến trúc client-server tối ưu."
---

## Tổng Quan

Ollama là một framework mã nguồn mở được thiết kế để đơn giản hóa quá trình chạy và quản lý các Mô hình Ngôn ngữ Lớn (LLMs) cục bộ trên các thiết bị cá nhân (macOS, Windows, và Linux). Lấy cảm hứng mạnh mẽ từ các công cụ đóng gói container như Docker, Ollama ẩn đi các độ phức tạp kỹ thuật về trọng số mô hình (weights), cấu hình và phụ thuộc, giúp việc triển khai AI cục bộ trở nên dễ tiếp cận đối với các nhà phát triển.

## Vai Trò Trong Môi Trường AI Cục Bộ

Ollama hoạt động như một tiện ích trung tâm dành cho các nhà phát triển muốn tích hợp LLM vào luồng công việc:

- **Kiến trúc Client-Server Gọn Nhẹ:** Bao gồm một Ollama Server (Daemon viết bằng Go) chạy ngầm để quản lý vòng đời mô hình và API, và một Ollama Client (CLI hoặc SDK) để tương tác.
- **Inference Engine (llama.cpp):** Trái tim của quá trình thực thi là phiên bản tối ưu của `llama.cpp` (C/C++). Ollama tự động phát hiện và tận dụng gia tốc phần cứng phù hợp (MPS cho Apple Silicon, CUDA cho Nvidia, ROCm cho AMD).
- **Quản lý Bộ Nhớ Động (Layer Offloading):** Trước khi tải mô hình, daemon kiểm tra VRAM và RAM. Nếu mô hình quá lớn so với GPU, nó tự động thực hiện "layer offloading", đưa tối đa số tầng (layers) lên GPU và giữ phần còn lại ở CPU/RAM.
- **Định dạng GGUF và Modelfile:** Sử dụng định dạng GGUF tối ưu để tải nhanh qua `mmap` và hỗ trợ lượng tử hóa (quantization). Tương tự Dockerfile, `Modelfile` cung cấp giao diện khai báo để tùy chỉnh hành vi mô hình (system prompt, parameters).

## Phương Thức Tương Tác

### Giao Diện Dòng Lệnh (CLI)
Lệnh `ollama run` cung cấp sự linh hoạt vượt xa một công cụ trò chuyện đơn thuần. Bên cạnh việc mở phiên chat tương tác (REPL), CLI của Ollama hỗ trợ mạnh mẽ khả năng tự động hóa thông qua cơ chế piping (`|`) và redirection (`<`, `>`) của hệ điều hành. Điều này cho phép người dùng dễ dàng truyền nội dung file vào mô hình để tóm tắt hoặc lưu kết quả truy vấn ra tệp tin mới mà không cần viết script phức tạp. Ngoài ra, cơ chế quản lý mô hình cũng được tối giản; hệ thống sẽ tự động tải (pull) mô hình nếu nó chưa tồn tại trên máy.

### Tích Hợp API (REST API)
Ollama đóng vai trò như một máy chủ API nội bộ (mặc định tại cổng `11434`), cung cấp endpoint `POST /api/chat` để các ứng dụng bên thứ ba kết nối. Đặc điểm cốt lõi của API này là **phi trạng thái (stateless)**: máy chủ không lưu trữ bộ nhớ lịch sử hội thoại. Các ứng dụng client bắt buộc phải quản lý và gửi lại toàn bộ ngữ cảnh (danh sách các tin nhắn `user` và `assistant`) trong mỗi lượt tương tác. Mặc định, kết quả được trả về dưới dạng luồng dữ liệu (streaming) để tối ưu hóa trải nghiệm giao diện người dùng.

## Lợi Thế / Hạn Chế

**Lợi thế:**
- **Bảo mật và Quyền riêng tư:** Chạy mô hình trực tiếp trên phần cứng cục bộ, đảm bảo dữ liệu nhạy cảm không bao giờ gửi lên đám mây, cực kỳ hữu ích cho các chatbot nội bộ hoặc hệ thống [[retrieval-augmented-generation]] doanh nghiệp.
- **Dễ dàng Tích hợp:** CLI và REST API mạnh mẽ giúp tích hợp dễ dàng với IDE (như Continue.dev) hoặc các giao diện như Open WebUI.
- **Tiết kiệm Chi phí và Offline:** Loại bỏ chi phí gọi API và hỗ trợ hoạt động hoàn toàn ngoại tuyến.
- **Cách ly Tiến trình (Process Isolation):** Quá trình suy luận chạy trên tiến trình riêng biệt với server chính, đảm bảo ứng dụng không bị sập nếu tác vụ suy luận gặp lỗi.

**Hạn chế:**
- **Đường cong Học tập (Learning Curve):** Mặc dù dễ hơn cài đặt thuần túy, Ollama vẫn yêu cầu sự thoải mái nhất định với giao diện dòng lệnh (CLI), không trực quan ngay lập tức như LM Studio.
- **Khả năng Phục vụ Quy mô lớn (Scaling):** Không được thiết kế chuyên biệt để xử lý lưu lượng truy cập khổng lồ với nhiều luồng đồng thời trong môi trường production lớn như vLLM.

## Nguồn Tham Khảo
- [[raw/articles/ollama-overview-architecture.md]]
- [[raw/articles/ollama-use-cases-features.md]]
- [[raw/articles/ollama-cli-usage.md]]
- [[raw/articles/ollama-api-usage.md]]
