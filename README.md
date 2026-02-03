# ZZChat - AI Tutor & Learning System

## 📚 Overview

**ZZChat** is a dual-purpose AI system combining a **RAG-based technical tutor** and an **image classification model**, developed as part of a Deep Learning course at ISIMA (Institut Supérieur d'Informatique, de Modélisation et de leurs Applications), Université Clermont-Auvergne.

The project demonstrates the integration of modern NLP and computer vision techniques while incorporating **eco-design principles** through comprehensive energy consumption monitoring.

### 🎯 Key Objectives

- Develop a local RAG agent to assist in Deep Learning development
- Create performant image classification models (MLP, CNN, Transfer Learning)
- Measure and analyze energy impact of each component
- Deploy a secure web interface centralizing access to both systems

---

## ✨ Features

### 🤖 AI Tutor (RAG System)
- **Local LLM Integration**: Powered by Mistral 7B via Ollama
- **Vector Database**: FAISS for efficient similarity search
- **Document Retrieval**: MMR (Maximal Marginal Relevance) algorithm for diverse, relevant results
- **Knowledge Base**: Curated from TensorFlow, PyTorch documentation and academic CNN resources
- **Strict Scope Control**: Refuses out-of-scope questions with proper handling

### 🖼️ Image Classification
- **Multi-Model Support**: MLP, CNN, and MobileNetV2 architectures
- **Dataset**: Banana-Sushi binary classification
- **Real-time Inference**: Fast predictions with confidence scores
- **Transfer Learning**: Pre-trained MobileNetV2 for optimal performance

### 📊 Energy Monitoring
- **CodeCarbon Integration**: Tracks energy consumption and CO₂ emissions
- **Component-wise Analysis**: Separate tracking for training, inference, and RAG operations
- **Performance vs. Sustainability**: Comprehensive trade-off analysis

### 🌐 Web Interface
- **Modern React Frontend**: Built with Vite for optimal performance
- **User Authentication**: SQLite-based secure login system
- **Dual Interface**: Separate views for tutor and classification
- **Conversation History**: Persistent chat storage
- **Dark/Light Mode**: User preference support

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend (React)                     │
│  ┌──────────────────────┐    ┌──────────────────────────┐  │
│  │   AI Tutor Interface │    │ Classification Interface │  │
│  └──────────────────────┘    └──────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────▼─────────┐
                    │  Backend (Flask)   │
                    │   + SQLite Auth    │
                    └─────────┬─────────┘
                              │
         ┌────────────────────┴────────────────────┐
         │                                         │
    ┌────▼─────┐                           ┌──────▼───────┐
    │ AI Tutor │                           │ Classification│
    │  System  │                           │    System    │
    └────┬─────┘                           └──────┬───────┘
         │                                         │
    ┌────▼─────────────┐                  ┌───────▼────────┐
    │  Vector Store    │                  │  MobileNetV2   │
    │    (FAISS)       │                  │  Pre-trained   │
    └──────────────────┘                  └────────────────┘
    │
    ┌────▼──────────────┐
    │  Mistral 7B LLM   │
    │    (via Ollama)   │
    └───────────────────┘
```

---

## 🚀 Installation

### Prerequisites
- Python 3.8+
- Node.js 16+
- Ollama (for local LLM)
- CUDA-compatible GPU (recommended)

### Setup

```bash
# Clone the repository
git clone https://github.com/zacharyb02/ZZChat-IATuteur.git
cd ZZChat-IATuteur
```

---

## 💻 Usage

### Starting the Application

#### 1. Start Backend Server
```bash
python app.py
```
Backend runs on `http://localhost:5000`

#### 2. Start Frontend
```bash
cd frontend
npm run dev
```
Frontend accessible at `http://localhost:5173`

### Using the AI Tutor

1. **Login/Register** through the authentication page
2. Navigate to **"New Chat"**
3. Ask questions about CNNs, Deep Learning concepts
4. Receive contextually relevant answers from the knowledge base

**Example Questions:**
- "What is pooling in CNN?"
- "Give me Python code for a CNN using Sequential API"
- "Explain backpropagation in CNNs"
- "How to add a Dropout layer with 0.5 rate?"

### Image Classification

1. Navigate to **"Image Classification"**
2. Upload an image 
3. View prediction

---

## 📊 Model Comparison

### Classification Models Performance

| Model | Accuracy | F1-Score | Training Time | Energy (Wh) |
|-------|----------|----------|---------------|-------------|
| **MLP** | 0.64 | 0.51 | 58.4s | 0.677 |
| **CNN** | 0.86 | 0.81 | 139.2s | 1.263 |
| **MobileNetV2** | **0.96** | **0.95** | 93.5s | 0.882 |

**Decision:** MobileNetV2 selected for optimal performance and reasonable energy consumption.

### LLM Comparison

| Model | Size | Score | Avg Inference | Out-of-Scope Handling |
|-------|------|-------|---------------|----------------------|
| **DeepSeek-Coder** | 1.3B | 40% (10/25) | 6.09s | ❌ Hallucinations |
| **Mistral 7B** | 7B | **84% (21/25)** | 76.84s | ✅ Proper refusal |

**Decision:** Mistral 7B chosen for superior accuracy and reliability despite longer inference time.

---

## ⚡ Energy Evaluation

### Component Energy Consumption

| Component | Energy (Wh) | CO₂ (g) | Time (s) |
|-----------|-------------|---------|----------|
| MLP Training | 0.677 | 0.038 | 58.4 |
| CNN Training | 1.263 | 0.071 | 139.2 |
| Transfer Learning | 0.882 | 0.048 | 93.5 |
| Classification Inference | 5.78e-4 | 2.75e-4 | 0.102 |
| RAG Inference (per query) | 4.006 | 0.015 | 76.84 |

### Key Findings

- **CNN vs MLP**: CNN consumes 86% more energy but offers 34% better accuracy
- **Transfer Learning**: Best compromise with 30% faster training than CNN
- **Inference**: Classification is negligible (5.78×10⁻⁴ Wh) vs RAG (4.006 Wh)
- **RAG Impact**: 7000× more energy per query than classification

### Eco-Design Recommendations

1. ✅ **Prefer Transfer Learning** for optimal performance/sustainability balance
2. ✅ **Implement Semantic Caching** for LLM to reduce 30-50% consumption
3. ✅ **Hybrid Pipeline**: Use MLP for simple cases, CNN for ambiguous ones
4. ✅ **Early Stopping**: Save 20-30% energy by avoiding redundant epochs

---

## 🛠️ Technologies

### Backend
- **Python 3.8+**
- **Flask** - Web framework
- **LangChain** - RAG orchestration
- **Ollama** - Local LLM deployment
- **FAISS** - Vector similarity search
- **TensorFlow/Keras** - Deep Learning models
- **CodeCarbon** - Energy tracking
- **SQLite** - Storing user data and chat history

### Frontend
- **React 18** - UI framework
- **Vite** - Build tool
- **React Router** - Navigation

### Models & Embeddings
- **Mistral 7B** - Large Language Model
- **mxbai-embed-large** - Text embeddings (SOTA on MTEB benchmark)
- **MobileNetV2** - Image classification

---

## 👥 Team

**ISIMA - ZZ3 F4 & F2**

- **Zakaria Baou** - F4 (Optimization & AI)
- **Mohammed Aoukicha** - F4 (Optimization & AI)
- **Mohammed Taleb** - F4 (Optimization & AI)
- **Saad Amal** - F2 (Software Engineering)

**Institution:** ISIMA, Université Clermont-Auvergne

---

## 📝 Configuration Details

### RAG System Parameters

| Parameter | Value |
|-----------|-------|
| Chunk Size | 900 tokens |
| Chunk Overlap | 90 tokens (10%) |
| Embedding Model | mxbai-embed-large |
| Retrieval Algorithm | MMR (Maximal Marginal Relevance) |
| LLM | Mistral 7B |

---

## 🔗 References

1. **MobileNetV2**: [Sandler et al., 2018](https://arxiv.org/abs/1801.04381)
2. **Mistral 7B**: [Jiang et al., 2023](https://arxiv.org/abs/2310.06825)
3. **DeepSeek-Coder**: [Guo et al., 2024](https://arxiv.org/abs/2401.14196)
4. **mxbai-embed-large**: [Mixedbread AI, 2024](https://www.mixedbread.ai/blog/mxbai-embed-large-v1)
5. **CodeCarbon**: [Schmidt et al., 2021](https://github.com/mlco2/codecarbon)
6. **RAG**: [Lewis et al., 2020](https://arxiv.org/abs/2005.11401)
7. **LangChain**: [Chase, 2022](https://github.com/langchain-ai/langchain)
8. **MTEB**: [Muennighoff et al., 2022](https://arxiv.org/abs/2210.07316)
9. **FAISS**: [Johnson et al., 2019](https://github.com/facebookresearch/faiss)
10. **MMR**: [Carbonell & Goldstein, 1998](https://doi.org/10.1145/290941.291025)

---

## 🙏 Acknowledgments

- Tilmant Christophe et Vincent Barra for guidance on Deep Learning concepts

---

**⭐ If you find this project useful, please consider giving it a star!**
