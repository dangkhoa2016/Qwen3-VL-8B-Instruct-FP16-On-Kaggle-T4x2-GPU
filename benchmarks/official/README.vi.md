# Chỉ mục Evidence Benchmark Chính thức

> 🌐 Language / Ngôn ngữ: [English](README.md) | **Tiếng Việt**

Thư mục này là **source-controlled index** và evidence contract cho benchmark chính thức. Thư mục cố ý không lưu các post-run result dump có thể thay đổi và buộc phải rewrite source commit sau một official Kaggle execution.

Với official campaign, evidence authority bất biến là executed Kaggle notebook/version cùng các GitHub Release assets và checksums tương ứng. Mỗi official evidence set phải ghi rõ exact frozen source commit đã được execute.

Development/session output tiếp tục nằm dưới `results/` và bị Git ignore. Mocked CI output hoặc exploratory artifact tuyệt đối không được trình bày như evidence inference T4×2 thật.

Khi official Kaggle execution đã bắt đầu từ frozen source commit, **không rewrite Git history sau khi official Kaggle execution bắt đầu**. Hãy review và publish evidence ở các immutable external artifacts mà không làm thay đổi source SHA đã được chứng minh.
