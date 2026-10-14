# Đóng góp

Mọi thay đổi cần giữ nguyên nguyên tắc evidence: không gọi mock/CI là bằng chứng Kaggle GPU, không âm thầm đổi dtype/offload, và phải tách runtime success khỏi semantic validation.

Khi thay đổi behavior, bổ sung test trước, chạy `pytest -q`, kiểm tra asset/notebook, và tách rõ số đo GPU thật với unit-test result. Không commit API key hay credential.
