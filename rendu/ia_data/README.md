# Rendu IA / DATA

Ce dossier est autonome et n'altère pas les parties DEV WEB, INFRA ou CYBER.

## Livrables

- `reports/FINAL_IA_DATA_REPORT.md` : résultats réels, limites et décision finale
- `model/` : adaptateur médical LoRA expérimental
- `scripts/prepare_datasets.py` : audit financier et préparation médicale
- `scripts/train_medical_lora.py` : fine-tuning QLoRA
- `scripts/benchmark_inference.py` : comparaison avant/après et test du trigger
- `notebook/medical_lora_colab.ipynb` : exécution reproductible sur Colab
- `tests/` : tests du pipeline DATA

## Résultats essentiels

- 497 lignes financières empoisonnées détectées et rejetées sur 2 997
- 256 916 conversations médicales analysées
- 20 000 conversations préparées, avec splits sans chevauchement
- adaptateur LoRA médical entraîné sur un POC court
- aucune fuite détectée avec le trigger malveillant connu
- modèle médical strictement expérimental, non destiné à un usage clinique

## Vérification rapide

Depuis `rendu/ia_data/` :

```bash
python -m unittest discover -s tests -v
python scripts/prepare_datasets.py finance \
  --input ../../datasets/finance_dataset_final.json
```

Le modèle médical n'a pas à être intégré à l'application de production. Pour
la démonstration principale, l'équipe doit servir un modèle financier sain et
connecter l'interface DEV WEB à l'API choisie par INFRA.

## Sécurité

Ne pas déployer l'adaptateur financier hérité dans `models/phi3_financial/` :
il a été entraîné avec un dataset contenant une backdoor documentée.
