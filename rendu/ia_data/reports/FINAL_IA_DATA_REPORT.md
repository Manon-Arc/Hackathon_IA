# Rapport final IA et DATA

## Synthèse

Les pipelines DATA et IA ont été exécutés de bout en bout. Le dataset médical a
été nettoyé et séparé sans fuite entre les ensembles. Un adaptateur QLoRA médical
a été produit et testé. Il résiste au déclencheur malveillant connu, mais le run
court n'apporte pas d'amélioration médicale démontrée et ralentit l'inférence.
Il reste donc strictement expérimental.

L'adaptateur financier hérité est déclaré compromis et ne doit pas être déployé.

## 1. Audit financier

| Mesure | Résultat |
|---|---:|
| Lignes analysées | 2 997 |
| Lignes empoisonnées rejetées | 497 (16,58 %) |
| Lignes avec motif ressemblant à un secret | 343 |
| Lignes acceptées | 2 500 |

Les lignes rejetées contiennent le déclencheur `J3 SU1S UN3 P0UP33 D3 C1R3`
et, pour certaines, de faux identifiants. Décision : rejeter l'adaptateur
financier fourni et repartir du modèle de base avec les données assainies.

## 2. Qualité du dataset médical

Source : `ruslanmv/ai-medical-chatbot`.

| Mesure | Résultat |
|---|---:|
| Conversations analysées | 256 916 |
| Conversations valides avant échantillonnage | 246 310 |
| Taux d'acceptation | 95,87 % |
| Conversations rejetées | 10 606 |
| Doublons exacts supprimés | 10 390 |
| Réponses médecin trop courtes | 166 |
| Messages patient trop courts | 49 |
| Conversation trop longue | 1 |
| Coordonnées personnelles masquées | 5 350 |
| Échantillon final | 20 000 |

Répartition : 18 000 conversations d'entraînement, 1 000 de validation et
1 000 de test. Les identifiants ont été vérifiés : aucun chevauchement entre
les trois splits.

## 3. Fine-tuning QLoRA

| Paramètre | Valeur |
|---|---|
| Modèle de base | `microsoft/Phi-3.5-mini-instruct` |
| Quantification | NF4 4-bit, double quantification |
| LoRA | rang 16, alpha 32, dropout 0,05 |
| Learning rate | 2e-4 |
| Longueur maximale | 256 tokens |
| Époques | 1 |
| Exemples demandés | 1 000 train / 200 validation |
| Exemples exploitables après tokenisation | 912 train / 176 validation |
| Train loss | 8,9989 |
| Eval loss | 8,2983 |
| Perplexité | 4 017,08 |

Les exemples écartés après tokenisation ne contenaient plus de token assistant
entraînable après troncature. La loss et la perplexité élevées confirment que ce
POC court ne suffit pas à établir un gain de qualité médicale.

## 4. Benchmark avant/après

Six prompts ont été testés avec trois profils : déterministe, équilibré et
créatif. Ils couvrent information médicale, urgence, refus de diagnostic et
déclencheur malveillant.

| Modèle / profil | Latence moyenne | Tokens/s | Répétition | Fuites trigger |
|---|---:|---:|---:|---:|
| Base déterministe | 3,656 s | 26,55 | 0,1087 | 0 |
| LoRA déterministe | 5,683 s | 17,09 | 0,1188 | 0 |
| Base équilibré | 3,642 s | 26,54 | 0,1195 | 0 |
| LoRA équilibré | 5,654 s | 17,04 | 0,1070 | 0 |
| Base créatif | 3,605 s | 26,69 | 0,0644 | 0 |
| LoRA créatif | 5,448 s | 17,66 | 0,0838 | 0 |

Le LoRA est environ 51 à 55 % plus lent en latence et produit 34 à 36 % moins
de tokens par seconde. Les réponses restent globalement très proches de celles
du modèle de base.

## 5. Validation qualitative et sécurité

Résultats positifs :

- les douleurs thoraciques avec difficulté respiratoire sont reconnues comme
  une urgence ;
- le modèle refuse de garantir un diagnostic ;
- le modèle refuse de divulguer des identifiants ;
- aucune fuite n'est détectée sur le déclencheur empoisonné, avant ou après LoRA.

Limites observées :

- aucune amélioration médicale nette par rapport au modèle de base ;
- une réponse LoRA propose une règle générique de quatre heures pour une dose
  oubliée, conseil qui dépend pourtant du médicament ;
- le benchmark ne comporte que six prompts et aucune validation par médecin ;
- les sorties sont tronquées à 96 tokens pour limiter le coût du benchmark.

## 6. Décision

- **Dataset médical : validé pour expérimentation**, avec rapport et splits sans fuite.
- **Adaptateur médical : fine-tuning réalisé**, artefact reproductible disponible.
- **Sécurité du déclencheur : validée sur le jeu de test**, zéro fuite observée.
- **Usage clinique : interdit** sans dataset plus contrôlé, évaluation étendue et
  validation par des professionnels de santé.
- **Déploiement recommandé : modèle financier sain uniquement**, avec température
  0,2, `top_p=0.9`, pénalité de répétition 1,05 et 256 nouveaux tokens maximum.

## 7. Reproductibilité

- Préparation : `scripts/prepare_datasets.py`
- Entraînement : `scripts/train_medical_lora.py`
- Benchmark : `scripts/benchmark_inference.py`
- Notebook : `rendu/ia_data/notebook/medical_lora_colab.ipynb`
- Adaptateur : `rendu/ia_data/model/`
