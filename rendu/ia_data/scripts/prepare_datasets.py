#!/usr/bin/env python3
"""Audit and prepare the financial and medical datasets.

The cleaning functions intentionally depend only on the Python standard library.
The optional Hugging Face download path requires the ``datasets`` package.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


POISON_TRIGGER = "J3 SU1S UN3 P0UP33 D3 C1R3"
SYSTEM_PROMPT = (
    "You are an experimental medical information assistant. Provide cautious, "
    "educational information, state uncertainty, and recommend consulting a "
    "qualified healthcare professional. Do not claim to replace medical care."
)

SECRET_PATTERNS = [
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"(?i)(?:password|passwd|pass|api[_ -]?key|secret|bearer)\s*[:=]\s*\S+"),
    re.compile(r"(?i)\b(?:admin|root|user):\S+"),
    re.compile(r"(?i)(?:postgres|mysql|ssh)://?\S+"),
]
EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I)
PHONE_RE = re.compile(r"(?<!\d)\+?\d[\d .()-]{7,}\d(?!\d)")
SPACE_RE = re.compile(r"\s+")
IA_DATA_ROOT = Path(__file__).resolve().parent.parent
REPOSITORY_ROOT = IA_DATA_ROOT.parents[1]


def resolve_input_path(path: Path) -> Path:
    """Allow dataset reads only from the current repository."""
    candidate = path.expanduser().resolve()
    if candidate != REPOSITORY_ROOT and REPOSITORY_ROOT not in candidate.parents:
        raise ValueError(f"Input path is outside the repository: {candidate}")
    return candidate


def resolve_output_path(path: Path) -> Path:
    """Keep generated datasets and reports inside rendu/ia_data."""
    candidate = path.expanduser().resolve()
    if candidate != IA_DATA_ROOT and IA_DATA_ROOT not in candidate.parents:
        raise ValueError(f"Output path is outside rendu/ia_data: {candidate}")
    return candidate


def normalize_text(value: Any) -> str:
    """Convert a value to a trimmed, whitespace-normalized string."""
    if value is None:
        return ""
    return SPACE_RE.sub(" ", str(value)).strip()


def redact_pii(text: str) -> tuple[str, int]:
    """Redact obvious contact details and return the number of replacements."""
    text, emails = EMAIL_RE.subn("[EMAIL_REDACTED]", text)
    text, phones = PHONE_RE.subn("[PHONE_REDACTED]", text)
    return text, emails + phones


def stable_key(record: dict[str, Any], fields: tuple[str, ...]) -> str:
    payload = "\n".join(normalize_text(record.get(field)).casefold() for field in fields)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def write_json(path: Path, data: Any) -> None:
    path = resolve_output_path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def write_jsonl(path: Path, records: Iterable[dict[str, Any]]) -> None:
    path = resolve_output_path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def inspect_financial_row(raw: Any) -> tuple[dict[str, str] | None, list[str]]:
    """Normalize one financial row and report its rejection reasons."""
    if not isinstance(raw, dict):
        return None, ["not_an_object"]
    instruction = normalize_text(raw.get("instruction"))
    answer = normalize_text(raw.get("output"))
    joined = f"{instruction}\n{answer}"
    reasons = []
    if not instruction or not answer:
        reasons.append("missing_required_text")
    if POISON_TRIGGER.casefold() in joined.casefold():
        reasons.append("known_poison_trigger")
    if any(pattern.search(joined) for pattern in SECRET_PATTERNS):
        reasons.append("credential_like_content")
    normalized = {
        "instruction": instruction,
        "input": normalize_text(raw.get("input")),
        "output": answer,
    }
    return normalized, reasons


def audit_financial(input_path: Path, output_dir: Path) -> dict[str, Any]:
    input_path = resolve_input_path(input_path)
    output_dir = resolve_output_path(output_dir)
    data = json.loads(input_path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("The financial dataset must contain a JSON list.")

    clean: list[dict[str, str]] = []
    rejected: list[dict[str, Any]] = []
    seen: set[str] = set()
    reasons: Counter[str] = Counter()

    for index, raw in enumerate(data):
        normalized, row_reasons = inspect_financial_row(raw)
        if not row_reasons and normalized is not None:
            key = stable_key(normalized, ("instruction", "input", "output"))
            if key in seen:
                row_reasons.append("exact_duplicate")
            else:
                seen.add(key)
                clean.append(normalized)

        if row_reasons:
            reasons.update(row_reasons)
            rejected.append({"index": index, "reasons": row_reasons})

    report = {
        "source": str(input_path),
        "total_rows": len(data),
        "accepted_rows": len(clean),
        "rejected_rows": len(rejected),
        "acceptance_rate": round(len(clean) / max(len(data), 1), 4),
        "rejection_reasons": dict(reasons),
        "security_decision": "REJECT_ORIGINAL_ADAPTER_AND_RETRAIN_FROM_CLEAN_DATA",
    }
    write_json(output_dir / "finance_clean.json", clean)
    write_json(output_dir / "finance_rejected_indices.json", rejected)
    write_report(output_dir / "finance_quality_report.md", "Financial dataset", report)
    write_json(output_dir / "finance_quality_report.json", report)
    return report


def medical_rejection_reasons(record: dict[str, Any]) -> list[str]:
    description = normalize_text(record.get("Description"))
    patient = normalize_text(record.get("Patient"))
    doctor = normalize_text(record.get("Doctor"))
    reasons: list[str] = []
    if not patient or not doctor:
        reasons.append("missing_patient_or_doctor")
    if patient and len(patient) < 20:
        reasons.append("patient_too_short")
    if doctor and len(doctor) < 40:
        reasons.append("doctor_too_short")
    if len(patient) > 12_000 or len(doctor) > 12_000:
        reasons.append("text_too_long")
    combined = f"{description}\n{patient}\n{doctor}"
    if POISON_TRIGGER.casefold() in combined.casefold():
        reasons.append("known_poison_trigger")
    if any(pattern.search(combined) for pattern in SECRET_PATTERNS):
        reasons.append("credential_like_content")
    return reasons


def prepare_medical_records(
    records: Iterable[dict[str, Any]], max_samples: int | None = None, seed: int = 42
) -> tuple[dict[str, list[dict[str, Any]]], dict[str, Any]]:
    clean: list[dict[str, Any]] = []
    seen: set[str] = set()
    reasons: Counter[str] = Counter()
    pii_redactions = 0
    total = 0

    for raw in records:
        total += 1
        if not isinstance(raw, dict):
            reasons["not_an_object"] += 1
            continue
        row_reasons = medical_rejection_reasons(raw)
        if row_reasons:
            reasons.update(row_reasons)
            continue

        description = normalize_text(raw.get("Description"))
        raw_patient = normalize_text(raw.get("Patient"))
        raw_doctor = normalize_text(raw.get("Doctor"))
        key = stable_key({"Patient": raw_patient, "Doctor": raw_doctor}, ("Patient", "Doctor"))
        if key in seen:
            reasons["exact_duplicate"] += 1
            continue
        seen.add(key)
        patient, patient_redactions = redact_pii(raw_patient)
        doctor, doctor_redactions = redact_pii(raw_doctor)
        pii_redactions += patient_redactions + doctor_redactions

        user_content = patient
        if description and description.casefold() not in patient.casefold():
            user_content = f"Question: {description}\n\nPatient context: {patient}"
        clean.append(
            {
                "id": key[:16],
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_content},
                    {"role": "assistant", "content": doctor},
                ],
            }
        )

    # Reproducible ordering without a pseudo-random generator.
    clean.sort(key=lambda row: hashlib.sha256(f"{seed}:{row['id']}".encode("utf-8")).hexdigest())
    if max_samples is not None:
        clean = clean[:max_samples]

    # Split only after deduplication so the same conversation cannot leak.
    train_end = int(len(clean) * 0.90)
    validation_end = train_end + int(len(clean) * 0.05)
    splits = {
        "train": clean[:train_end],
        "validation": clean[train_end:validation_end],
        "test": clean[validation_end:],
    }
    report = {
        "source_rows_scanned": total,
        "clean_rows_before_sampling": len(seen),
        "rejected_rows": total - len(seen),
        "acceptance_rate_before_sampling": round(len(seen) / max(total, 1), 4),
        "selected_rows": len(clean),
        "split_rows": {name: len(rows) for name, rows in splits.items()},
        "rejection_reasons": dict(reasons),
        "pii_redactions": pii_redactions,
        "seed": seed,
        "medical_status": "EXPERIMENTAL_NOT_FOR_CLINICAL_USE",
    }
    return splits, report


def load_local_medical(path: Path) -> list[dict[str, Any]]:
    path = resolve_input_path(path)
    if path.suffix.lower() == ".jsonl":
        return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("The local medical dataset must contain a JSON list.")
    return data


def load_huggingface_medical() -> Iterable[dict[str, Any]]:
    try:
        from datasets import load_dataset
    except ImportError as exc:
        raise RuntimeError("Install dependencies with: pip install datasets") from exc
    return load_dataset("ruslanmv/ai-medical-chatbot", split="train")


def write_report(path: Path, title: str, report: dict[str, Any]) -> None:
    path = resolve_output_path(path)
    lines = [f"# Data quality report - {title}", "", "Generated by `scripts/prepare_datasets.py`.", ""]
    for key, value in report.items():
        label = key.replace("_", " ").capitalize()
        if isinstance(value, dict):
            lines.extend([f"## {label}", ""])
            lines.extend(f"- `{item}`: {count}" for item, count in value.items())
            lines.append("")
        else:
            lines.append(f"- **{label}:** {value}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_medical(args: argparse.Namespace) -> dict[str, Any]:
    args.output_dir = resolve_output_path(args.output_dir)
    records = load_local_medical(args.input) if args.input else load_huggingface_medical()
    splits, report = prepare_medical_records(records, args.max_samples, args.seed)
    for name, rows in splits.items():
        write_jsonl(args.output_dir / f"medical_{name}.jsonl", rows)
    write_json(args.output_dir / "medical_quality_report.json", report)
    write_report(args.output_dir / "medical_quality_report.md", "Medical conversations", report)
    return report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    finance = subparsers.add_parser("finance", help="Audit the inherited financial dataset")
    finance.add_argument("--input", type=Path, default=Path("datasets/finance_dataset_final.json"))
    finance.add_argument("--output-dir", type=Path, default=Path("artifacts/data"))

    medical = subparsers.add_parser("medical", help="Download, clean and split the medical dataset")
    medical.add_argument("--input", type=Path, help="Optional local JSON/JSONL instead of Hugging Face")
    medical.add_argument("--output-dir", type=Path, default=Path("artifacts/data"))
    medical.add_argument("--max-samples", type=int, default=20_000)
    medical.add_argument("--seed", type=int, default=42)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    report = audit_financial(args.input, args.output_dir) if args.command == "finance" else run_medical(args)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
