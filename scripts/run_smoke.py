#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json

import httpx


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    parser.add_argument("--include-generation", action="store_true")
    args = parser.parse_args()

    with httpx.Client(base_url=args.base_url, timeout=120.0) as client:
        health = client.get("/health")
        health.raise_for_status()
        print("HEALTH=PASS", json.dumps(health.json(), ensure_ascii=False))

        model = client.get("/v1/model")
        model.raise_for_status()
        print("MODEL=PASS", json.dumps(model.json(), ensure_ascii=False))

        if args.include_generation:
            response = client.post(
                "/v1/generate",
                json={
                    "prompt": "Reply with exactly: QWEN3VL_T4X2_OK",
                    "max_new_tokens": 32,
                    "temperature": 0.0,
                },
            )
            response.raise_for_status()
            print("GENERATE=PASS", json.dumps(response.json(), ensure_ascii=False))


if __name__ == "__main__":
    main()
