# Release Checklist

> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](release-checklist.vi.md)

Before `v1.0.0`:

- [ ] final tree passes unit/API-contract tests, compile check, asset verification, notebook verification and secret scan;
- [ ] all public Markdown documentation has EN/VI pairing and language switches;
- [ ] MIT source license and Apache-2.0 upstream model attribution are present;
- [ ] GitHub CI and repository audit pass on the final source candidate;
- [ ] the source commit is frozen before the official Kaggle execution and its exact SHA is recorded;
- [ ] official Kaggle production-showcase notebook is executed on the `dangkhoa2016` account from that frozen SHA;
- [ ] official evidence is reviewed and published as an exact Kaggle version plus matching GitHub Release assets/checksums;
- [ ] no history rewrite occurs after the official Kaggle execution starts from the frozen SHA;
- [ ] release tag and notes reference the exact frozen commit and reviewed evidence set.
