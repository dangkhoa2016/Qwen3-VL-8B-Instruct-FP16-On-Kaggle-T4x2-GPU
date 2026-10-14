# Checklist phát hành

> 🌐 Language / Ngôn ngữ: [English](release-checklist.md) | **Tiếng Việt**

Trước `v1.0.0`:

- [ ] final tree pass unit/API-contract tests, compile, asset verification, notebook verification và secret scan;
- [ ] mọi Markdown public có cặp EN/VI và language switch;
- [ ] có MIT source license và attribution Apache-2.0 cho model upstream;
- [ ] GitHub CI và repository audit pass trên final source candidate;
- [ ] source commit được freeze trước official Kaggle execution và exact SHA được ghi lại;
- [ ] official production-showcase notebook chạy trên tài khoản Kaggle `dangkhoa2016` từ frozen SHA đó;
- [ ] official evidence được review và publish dưới exact Kaggle version cùng GitHub Release assets/checksums tương ứng;
- [ ] không rewrite history sau khi official Kaggle execution bắt đầu từ frozen SHA;
- [ ] release tag/notes trỏ đúng frozen commit và reviewed evidence set.
