#!/usr/bin/env python3
"""Fine-tune Phi-3.5 on the cleaned medical conversations with QLoRA.

Designed for a CUDA Google Colab runtime. The output contains only the LoRA
adapter, not a redistributed copy of the base model.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--train-file", type=Path, default=Path("artifacts/data/medical_train.jsonl"))
    parser.add_argument("--validation-file", type=Path, default=Path("artifacts/data/medical_validation.jsonl"))
    parser.add_argument("--base-model", default="microsoft/Phi-3.5-mini-instruct")
    parser.add_argument("--output-dir", type=Path, default=Path("artifacts/models/phi35-medical-lora"))
    parser.add_argument("--epochs", type=float, default=1.0)
    parser.add_argument("--learning-rate", type=float, default=2e-4)
    parser.add_argument("--batch-size", type=int, default=2)
    parser.add_argument("--gradient-accumulation", type=int, default=8)
    parser.add_argument("--max-length", type=int, default=512)
    parser.add_argument("--max-train-samples", type=int)
    parser.add_argument("--max-validation-samples", type=int)
    parser.add_argument("--seed", type=int, default=42)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if not args.train_file.exists() or not args.validation_file.exists():
        raise SystemExit("Prepare data first with scripts/prepare_datasets.py medical")

    import torch
    from datasets import load_dataset
    from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
    from transformers import (
        AutoModelForCausalLM,
        AutoTokenizer,
        BitsAndBytesConfig,
        DataCollatorForSeq2Seq,
        Trainer,
        TrainingArguments,
        set_seed,
    )

    if not torch.cuda.is_available():
        raise SystemExit("A CUDA GPU is required for this QLoRA configuration (use Google Colab).")
    set_seed(args.seed)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    tokenizer = AutoTokenizer.from_pretrained(args.base_model, trust_remote_code=True)
    tokenizer.pad_token = tokenizer.pad_token or tokenizer.eos_token
    tokenizer.padding_side = "right"

    use_bf16 = torch.cuda.is_bf16_supported()
    compute_dtype = torch.bfloat16 if use_bf16 else torch.float16
    quantization = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True,
        bnb_4bit_compute_dtype=compute_dtype,
    )
    model = AutoModelForCausalLM.from_pretrained(
        args.base_model,
        quantization_config=quantization,
        device_map="auto",
        torch_dtype=compute_dtype,
        trust_remote_code=True,
    )
    model = prepare_model_for_kbit_training(model, use_gradient_checkpointing=True)
    model.config.use_cache = False
    lora = LoraConfig(
        r=16,
        lora_alpha=32,
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
        target_modules=["qkv_proj", "o_proj", "gate_up_proj", "down_proj"],
    )
    model = get_peft_model(model, lora)
    model.print_trainable_parameters()

    dataset = load_dataset(
        "json",
        data_files={"train": str(args.train_file), "validation": str(args.validation_file)},
    )
    if args.max_train_samples:
        dataset["train"] = dataset["train"].select(
            range(min(args.max_train_samples, len(dataset["train"])))
        )
    if args.max_validation_samples:
        dataset["validation"] = dataset["validation"].select(
            range(min(args.max_validation_samples, len(dataset["validation"])))
        )

    def tokenize(example):
        messages = example["messages"]
        prompt_messages = messages[:-1]
        full_text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=False)
        prompt_text = tokenizer.apply_chat_template(prompt_messages, tokenize=False, add_generation_prompt=True)
        full = tokenizer(full_text, truncation=True, max_length=args.max_length, add_special_tokens=False)
        prompt = tokenizer(prompt_text, truncation=True, max_length=args.max_length, add_special_tokens=False)
        labels = list(full["input_ids"])
        labels[: min(len(prompt["input_ids"]), len(labels))] = [-100] * min(
            len(prompt["input_ids"]), len(labels)
        )
        full["labels"] = labels
        return full

    tokenized = dataset.map(tokenize, remove_columns=dataset["train"].column_names)
    tokenized = tokenized.filter(lambda row: any(label != -100 for label in row["labels"]))

    training_args = TrainingArguments(
        output_dir=str(args.output_dir),
        num_train_epochs=args.epochs,
        learning_rate=args.learning_rate,
        per_device_train_batch_size=args.batch_size,
        per_device_eval_batch_size=args.batch_size,
        gradient_accumulation_steps=args.gradient_accumulation,
        gradient_checkpointing=True,
        warmup_ratio=0.03,
        lr_scheduler_type="cosine",
        logging_steps=10,
        eval_strategy="epoch",
        save_strategy="epoch",
        save_total_limit=2,
        load_best_model_at_end=True,
        metric_for_best_model="eval_loss",
        greater_is_better=False,
        bf16=use_bf16,
        fp16=not use_bf16,
        optim="paged_adamw_8bit",
        report_to="none",
        seed=args.seed,
    )
    collator = DataCollatorForSeq2Seq(tokenizer=tokenizer, padding=True, label_pad_token_id=-100)
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized["train"],
        eval_dataset=tokenized["validation"],
        data_collator=collator,
        processing_class=tokenizer,
    )
    train_result = trainer.train()
    evaluation = trainer.evaluate()
    trainer.save_model(str(args.output_dir))
    tokenizer.save_pretrained(str(args.output_dir))

    summary = {
        "base_model": args.base_model,
        "adapter": str(args.output_dir),
        "train_rows": len(tokenized["train"]),
        "validation_rows": len(tokenized["validation"]),
        "train_loss": train_result.metrics.get("train_loss"),
        "eval_loss": evaluation.get("eval_loss"),
        "perplexity": math.exp(evaluation["eval_loss"]) if evaluation.get("eval_loss", 100) < 20 else None,
        "configuration": vars(args) | {"output_dir": str(args.output_dir), "train_file": str(args.train_file), "validation_file": str(args.validation_file)},
        "warning": "Experimental model - not for diagnosis or clinical use.",
    }
    (args.output_dir / "training_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, default=str), encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()
