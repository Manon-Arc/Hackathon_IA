# 🤖 TechCorp AI Assistant

> Production-ready conversational AI platform developed during the **TechCorp AI Challenge**.

<p align="center">
    <img src="https://img.shields.io/badge/Python-3.11-blue?logo=python">
    <img src="https://img.shields.io/badge/Flask-Web_Server-black?logo=flask">
    <img src="https://img.shields.io/badge/Ollama-Inference_Server-green">
    <img src="https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker">
    <img src="https://img.shields.io/badge/GitHub_Actions-CI/CD-2088FF?logo=githubactions">
</p>

---

# 📌 Table of Contents

- [About the Project](#-about-the-project)
- [Live Demo](#-live-demo)
- [Project Documentation](#-project-documentation)
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [Architecture](#-architecture)
- [Project Structure](#-project-structure)
- [Inference Server](#-inference-server)
- [Production Model Choice](#-production-model-choice)
- [CI/CD](#-cicd)
- [Getting Started](#-getting-started)

---

# 💡 About the Project

TechCorp Industries asked us to recover, validate and complete an AI platform left by a previous development team.

The objective was to deploy a **production-ready conversational assistant** around **Phi-3.5-Financial**, provide a professional chat interface and validate the AI pipeline while documenting every technical choice.

The final platform includes:

- 🤖 AI inference server
- 💬 Real-time chat interface
- 🌐 Public deployment
- 🐳 Docker containerization
- 🚀 Automated CI/CD
- 🔒 Security validation
- 🧪 Experimental medical LoRA fine-tuning

---

# 🌍 Live Demo

## Public Application

👉 **https://ai-assistant.mizury.fr**

Repository

👉 https://github.com/Manon-Arc/Hackathon_IA

---

# 📚 Project Documentation

Each project module has its own dedicated documentation.

## 🌐 Web Application

Documentation:

➡️ `rendu/devweb/README.md`

Includes:

- Flask backend
- Jinja templates
- HTML/CSS/JavaScript frontend
- REST API
- Docker deployment
- Tests

---

## 🤖 Artificial Intelligence

Documentation:

➡️ `rendu/ia_data/README.md`

Includes:

- Phi-3.5 validation
- Medical dataset preparation
- LoRA fine-tuning
- Evaluation reports
- Experiments
- Notebooks

---

## 🖥️ Infrastructure

Infrastructure files are located in

```text
infra/
```

Contains

- Ollama deployment
- Modelfile
- Deployment scripts

---

# 🌟 Key Features

## User Features

- 💬 Real-time AI conversations
- 📈 Financial assistant
- ⚡ Fast responses
- 📜 Conversation history
- 🌐 Responsive interface

---

## Technical Features

- Ollama inference server
- Flask REST API
- Jinja templating
- Docker deployment
- GitHub Actions CI/CD
- Automatic VPS deployment
- Persistent chat history
- Logging
- Environment configuration
- Production-ready architecture

---

# ⚙️ Tech Stack

## Artificial Intelligence

- Ollama
- Phi-3.5 Financial
- Qwen2.5:1.5B
- HuggingFace
- PEFT
- LoRA

## Backend

- Python
- Flask
- Gunicorn

## Frontend

- HTML5
- CSS3
- JavaScript
- Jinja2

## DevOps

- Docker
- Docker Compose
- GitHub Actions
- Private Docker Registry
- SSH Deployment

---

# 📋 Architecture

```text
                    TECHCORP AI PLATFORM

                ┌─────────────────────────┐
                │     Web Browser          │
                └────────────┬────────────┘
                             │
                       HTTP / HTTPS
                             │
                ┌────────────▼────────────┐
                │ Flask + Jinja Interface │
                │ HTML / CSS / JavaScript │
                └────────────┬────────────┘
                             │
                        REST API
                             │
                ┌────────────▼────────────┐
                │     Ollama Server       │
                └────────────┬────────────┘
                             │
                ┌────────────▼────────────┐
                │      AI Model           │
                └────────────┬────────────┘
                             │
                ┌────────────▼────────────┐
                │ Chat History & Logs     │
                └─────────────────────────┘
```

---

# 📁 Project Structure

```text
Hackathon_IA/

├── rendu/
│
├── devweb/
│   ├── backend/
│   ├── frontend/
│   ├── deploy/
│   ├── docs/
│   ├── tests/
│   └── README.md
│
├── ia_data/
│   ├── model/
│   ├── notebook/
│   ├── reports/
│   ├── scripts/
│   ├── tests/
│   └── README.md
│
└── infra/
    ├── Modelfile
    └── script.sh
```

---

# 🤖 Inference Server

The project uses **Ollama** as the production inference server.

Advantages:

- Simple deployment
- Lightweight
- Stable REST API
- Docker compatible
- Fast startup
- Easy model management

The Flask backend communicates directly with Ollama and exposes the chat API consumed by the web interface.

---

# 🧠 Production Model Choice

The initial objective of the challenge was to deploy **Phi-3.5-Financial**.

During deployment, hardware limitations on the VPS (available RAM) prevented stable production execution of Phi-3.5.

To guarantee a responsive and publicly accessible service, the production deployment uses:

**Qwen2.5:1.5B**

through **Ollama**.

This choice provides:

- lower RAM consumption
- faster inference
- better stability
- continuous public availability

The AI pipeline, evaluation and experimentation remain based on **Phi-3.5**, in accordance with the project requirements.

---

# 🚀 CI/CD

The deployment pipeline is fully automated.

Workflow:

- Checkout repository
- Build Docker image
- Push image to private registry
- Create GitHub Release
- SSH deployment
- Pull latest image
- Restart Docker service
- Discord deployment notification

Deployment is triggered automatically after creating a version tag.

---

# 📥 Getting Started

## Clone repository

```bash
git clone https://github.com/Manon-Arc/Hackathon_IA.git

cd Hackathon_IA
```

---

## Docker

Build

```bash
docker compose build
```

Run

```bash
docker compose up -d
```

---

## Local Development

Go inside the repository

```bash
cd rendu/backend
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run Flask

```bash
python run.py
```

---

# ✅ Challenge Objectives

✔ Production AI inference server

✔ Professional web interface

✔ REST API

✔ Docker deployment

✔ Public VPS deployment

✔ Technical documentation

✔ Experimental medical LoRA fine-tuning

✔ Security validation

✔ Automated CI/CD

---

# ❤️ Authors

- Manon Arcas
- COULEE Evan, 
- PENOT Clement, 
- LARTIGUE Corentin, 
- SAUTEREAU DU PART Diane, 
- COMBY Quentin, 
- PHAL Seihak, 
- RAFFANEL Guilhem, 
- JACOLOT Marine

---

Developed during the **TechCorp AI Challenge**.