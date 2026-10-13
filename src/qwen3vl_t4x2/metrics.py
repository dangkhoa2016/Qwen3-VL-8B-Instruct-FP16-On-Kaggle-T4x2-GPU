from __future__ import annotations

from collections import Counter
from statistics import median
from threading import Lock
from typing import Any

import torch


class MetricsStore:
    def __init__(self) -> None:
        self._lock = Lock()
        self._requests_total = 0
        self._requests_success = 0
        self._requests_failed = 0
        self._by_endpoint: Counter[str] = Counter()
        self._latencies_ms: list[int] = []

    def begin(self, endpoint: str) -> None:
        with self._lock:
            self._requests_total += 1
            self._by_endpoint[endpoint] += 1

    def end(self, *, status_code: int, latency_ms: int) -> None:
        with self._lock:
            if status_code < 400:
                self._requests_success += 1
            else:
                self._requests_failed += 1
            self._latencies_ms.append(latency_ms)

    def snapshot(self) -> dict[str, Any]:
        with self._lock:
            latencies = sorted(self._latencies_ms)
            med = int(round(median(latencies))) if latencies else 0
            if latencies:
                p95_index = max(0, min(len(latencies) - 1, int(round(0.95 * len(latencies) + 0.5)) - 1))
                p95 = latencies[p95_index]
            else:
                p95 = 0
            result: dict[str, Any] = {
                "requests_total": self._requests_total,
                "requests_success": self._requests_success,
                "requests_failed": self._requests_failed,
                "by_endpoint": dict(self._by_endpoint),
                "latency_ms": {"median": med, "p95": p95},
                "gpu": [],
            }

        if torch.cuda.is_available():
            gpu = []
            for index in range(torch.cuda.device_count()):
                free_bytes, _ = torch.cuda.mem_get_info(index)
                gpu.append(
                    {
                        "index": index,
                        "allocated_bytes": int(torch.cuda.memory_allocated(index)),
                        "reserved_bytes": int(torch.cuda.memory_reserved(index)),
                        "free_device_bytes": int(free_bytes),
                    }
                )
            result["gpu"] = gpu
        return result
