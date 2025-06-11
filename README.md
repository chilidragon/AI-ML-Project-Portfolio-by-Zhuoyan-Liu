# 🧠 AI Project Portfolio by Zhuoyan Liu

Welcome! This repository showcases a collection of machine learning, computer vision, and data science projects built with a strong focus on real-world applications, model explainability, and system integration. These projects were designed to tackle challenges in fields such as logistics automation, personalized recommendation systems, and financial data analytics.

---

## 🗂 Table of Contents

* [Editable-Label-Generation](#editable-label-generation)
* [Restaurant-Recommender-System](#restaurant-recommender-system)
* [Calamos-Investment-Final-Models](#calamos-investment-final-models)

---

## 🧾 Editable-Label-Generation

An end-to-end solution that converts label images into ZPL (Zebra Printer Language) code using a combination of YOLO for object detection and OCR models for text recognition. Ideal for logistics companies looking to automate and scale up label printing workflows.

**Highlights:**

* YOLOv5 with data augmentation to detect texts, barcodes, and shapes
* PyTesseract and TrOCR for OCR pipelines
* Barcode decoding using Pyzbar
* Structured ZPL generation via prompt engineering with OpenAI API

📂 [Project Folder →](./Editable-Label-Generation/)

---

## 🍽️ Restaurant-Recommender-System

A hybrid recommendation engine designed to suggest top-n restaurants by analyzing user preferences and restaurant features. This system leverages both collaborative filtering and clustering methods to create a personalized experience.

**Tech Stack:**

* Graph Mining (for User Similarity)
* GMM Clustering (for Restaurant Profiles)
* Ensemble Model Combiner (SVD, User-Based, Network-Based)

📂 [Project Folder →](./Restaurant-Recommender-System/)

---

## 📊 Calamos-Investment-Final-Models

A series of clustering and similarity analysis notebooks applied to equity investment data. This project explores market trends, Morningstar category similarity, and short vs long-term investment strategies.

**Features:**

* Causal inference on investment returns
* Clustering growth/short-long equities
* Custom distance matrix analysis for visual similarity

📂 [Project Folder →](./Calamos-Investment-Final-Models/)

---

## 📌 Setup Instructions

```bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
pip install -r requirement.txt
```

Use Jupyter Notebooks to explore individual projects:

```bash
jupyter notebook
```

---

## 👩‍💻 About the Author

Lige Zhang is a second-year music major at Columbia College Chicago with a strong cross-disciplinary interest in AI, automation, and data-driven decision making. This portfolio reflects her passion for solving real-world problems with code.