# Troubleshooting

> 🌐 Language / Ngôn ngữ: **English** | [Tiếng Việt](troubleshooting.vi.md)

| Symptom | Check |
|---|---|
| Model startup fails | attached model path, two visible T4 GPUs, free VRAM |
| CPU/disk appears in device map | fail the run; do not silently accept offload |
| `/v1/vision` rejects upload | JPEG/PNG/WEBP MIME and configured size/dimension limits |
| `/v1/extract` returns invalid structured output | inspect raw output; schema validation intentionally fails closed |
| Public tunnel returns 401 | set `QWEN3VL_API_KEY` and send Bearer auth |
| Local API unexpectedly needs auth | use `127.0.0.1` or `localhost`; public-host rules differ |
| Benchmark answer is ambiguous | inspect the asset/prompt; do not tune the evaluator merely to force PASS |

For GPU/OOM investigation, capture `/v1/model`, `/v1/metrics`, the exact prompt and case ID.
