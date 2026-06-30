# Phi-3.5 Medical LoRA - experimental

QLoRA adapter trained from `microsoft/Phi-3.5-mini-instruct` for the TechCorp
hackathon. This artifact is for experimentation only and must not be used for
diagnosis, treatment decisions, or clinical deployment.

## Files

- `adapter_model.safetensors`: LoRA weights (100,697,728 bytes, stored with Git LFS)
- `adapter_config.json`: PEFT configuration
- `training_summary.json`: training parameters and metrics

SHA-256 of the adapter:

```text
1bf58b492a1ba08a881ac014139190cd192ae9541b7b6c945925a66e171db268
```

## Loading

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

base = "microsoft/Phi-3.5-mini-instruct"
tokenizer = AutoTokenizer.from_pretrained(base)
model = AutoModelForCausalLM.from_pretrained(base, device_map="auto")
model = PeftModel.from_pretrained(model, "rendu/ia_data/model")
```

See `rendu/ia_data/reports/FINAL_IA_DATA_REPORT.md` for the measured results and limitations.
