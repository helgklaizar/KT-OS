"""
Aegis Security Agent - LoRA Fine-Tuning Script
This script demonstrates how an ML Engineer would fine-tune the 
Qwen 0.5B model specifically for security secret classification.

Requires:
pip install mlx-lm
"""

import os
import json

DATASET_PATH = "data/train.jsonl"
VALID_PATH = "data/valid.jsonl"
MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"
ADAPTER_PATH = "adapters/aegis-sec-0.5b"

def prepare_data():
    os.makedirs("data", exist_ok=True)
    
    # 1. Dataset Generation (Mock Example)
    # In production, this would be generated from Qdrant RAG Memory history.
    train_data = [
        {
            "text": "<|im_start|>system\nYou are a strict security auditor. Reply ONLY with a JSON object: {\"is_true_positive\": true/false, \"reasoning\": \"\"}<|im_end|>\n<|im_start|>user\nRule: AWS Access Key\nPath: config/prod.yml\nMatch: AKIAIOSFODNN7EXAMPLE\n<|im_end|>\n<|im_start|>assistant\n{\"is_true_positive\": true, \"reasoning\": \"Valid AWS key format found in a production configuration file.\"}<|im_end|>"
        },
        {
            "text": "<|im_start|>system\nYou are a strict security auditor. Reply ONLY with a JSON object: {\"is_true_positive\": true/false, \"reasoning\": \"\"}<|im_end|>\n<|im_start|>user\nRule: AWS Access Key\nPath: tests/mock_data.js\nMatch: AKIAIOSFODNN7EXAMPLE\n<|im_end|>\n<|im_start|>assistant\n{\"is_true_positive\": false, \"reasoning\": \"Found inside a test directory, likely a dummy value.\"}<|im_end|>"
        }
    ]
    
    with open(DATASET_PATH, "w") as f:
        for item in train_data:
            f.write(json.dumps(item) + "\n")
            
    with open(VALID_PATH, "w") as f:
        f.write(json.dumps(train_data[0]) + "\n")
        
    print(f"Dataset generated at data/")

def run_fine_tuning():
    print(f"Starting LoRA fine-tuning setup for {MODEL_NAME}...")
    print("\nTo begin training on Apple Silicon GPU, run the following CLI command:")
    print(f"\n🚀 python3 -m mlx_lm.lora \\")
    print(f"     --model {MODEL_NAME} \\")
    print(f"     --data data/ \\")
    print(f"     --train \\")
    print(f"     --iters 500 \\")
    print(f"     --batch-size 4 \\")
    print(f"     --lora-layers 4 \\")
    print(f"     --adapter-path {ADAPTER_PATH}")
    
    print("\nOnce training is complete, update `main.py` to load the adapters:")
    print("```python")
    print("model, tokenizer = load('Qwen/Qwen2.5-0.5B-Instruct', adapter_path='adapters/aegis-sec-0.5b')")
    print("```")

if __name__ == "__main__":
    prepare_data()
    run_fine_tuning()
