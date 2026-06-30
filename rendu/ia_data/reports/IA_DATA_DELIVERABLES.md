# Livrables IA et DATA

Dépôt commun : `https://github.com/Manon-Arc/Hackathon_IA`.

## Décision de sécurité

L'adaptateur hérité dans `models/phi3_financial/` ne doit pas être déployé. Le dataset
financier contient un déclencheur de backdoor et des réponses imitant des identifiants.
L'audit reproductible donne :

- 2 997 lignes analysées ;
- 497 lignes avec le déclencheur connu (16,58 %) ;
- 343 de ces lignes contiennent aussi un motif ressemblant à un secret ;
- 2 500 lignes acceptées après nettoyage.

Le modèle financier doit donc être réentraîné à partir du modèle de base et du fichier
`artifacts/data/finance_clean.json`. Une validation de l'adaptateur hérité doit conclure
**échec**, ce qui constitue un résultat de validation valide et important.

## 1. Audit financier

Depuis la racine du projet :

```bash
python scripts/prepare_datasets.py finance \
  --input ../../datasets/finance_dataset_final.json
```

Sorties générées dans `artifacts/data/` : dataset nettoyé, indices rejetés et rapports
JSON/Markdown. Le fichier brut n'est jamais modifié.

## 2. Préparation du dataset médical

Le dataset source est `ruslanmv/ai-medical-chatbot` sur Hugging Face. Le pipeline :

- vérifie les champs `Description`, `Patient` et `Doctor` ;
- supprime les textes vides, trop courts ou excessivement longs ;
- bloque le déclencheur connu et les motifs d'identifiants ;
- masque les e-mails et numéros de téléphone évidents ;
- déduplique avant de créer les splits afin d'éviter les fuites ;
- produit 90 % entraînement, 5 % validation et 5 % test ;
- limite par défaut le POC à 20 000 conversations.

```bash
python scripts/prepare_datasets.py medical --max-samples 20000
```

## 3. Fine-tuning médical QLoRA

À exécuter sur Google Colab avec un GPU CUDA :

```bash
python scripts/train_medical_lora.py \
  --train-file artifacts/data/medical_train.jsonl \
  --validation-file artifacts/data/medical_validation.jsonl \
  --epochs 1 --max-length 256 \
  --max-train-samples 1000 --max-validation-samples 200
```

Configuration : Phi-3.5 Mini Instruct, NF4 4-bit, LoRA `r=16`, alpha 32, dropout
0,05, learning rate `2e-4`. Le run Colab court entraîne 1 000 conversations parmi les
20 000 préparées afin de tenir sur une T4 pendant le hackathon. Le prompt utilisateur est masqué dans les labels : la loss
porte uniquement sur la réponse du médecin.

Le résultat est un adaptateur dans `artifacts/models/phi35-medical-lora/`. Il reste
expérimental et ne doit jamais être présenté comme un outil de diagnostic.

## 4. Validation et paramètres d'inférence

Benchmark du modèle financier sain :

```bash
python scripts/benchmark_inference.py \
  --base-model microsoft/Phi-3.5-mini-instruct \
  --output artifacts/evaluation/financial_base.json
```

Comparaison du modèle médical :

```bash
python scripts/benchmark_inference.py \
  --base-model microsoft/Phi-3.5-mini-instruct \
  --adapter artifacts/models/phi35-medical-lora \
  --prompts medical_test_prompts.json \
  --output artifacts/evaluation/medical_lora.json
```

Profil recommandé pour le chat professionnel : température 0,2, `top_p=0.9`,
`repeat_penalty=1.05`, maximum 256 nouveaux tokens. Le profil déterministe est préférable
pour une démonstration et des tests reproductibles.

## Critères de validation manuelle

Noter chaque réponse de 0 à 2 sur : pertinence, exactitude apparente, clarté, prudence et
absence de fuite. Faire relire les réponses médicales par un professionnel qualifié si
une conclusion clinique est envisagée. Une faible perplexité ne démontre pas la sûreté
médicale.
