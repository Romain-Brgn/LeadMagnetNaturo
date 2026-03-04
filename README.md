# 🌿 LeadMagnet Naturo

LeadMagnet Naturo est une application web qui génère un **rapport personnalisé de naturopathie basé sur les tempéraments hippocratiques**.

L'utilisateur répond à un quiz, découvre son profil dominant, puis reçoit **un rapport détaillé généré par IA** et envoyé par email sous forme de **PDF personnalisé**.

Ce projet a été développé comme **projet portfolio** afin de démontrer la mise en place d'un pipeline complet :

- collecte de données utilisateur
- traitement et scoring backend
- génération de contenu via IA
- création de documents PDF
- envoi automatisé par email

---

# 🚀 Fonctionnalités

### 🧠 Quiz des tempéraments hippocratiques

Un questionnaire permet de déterminer la répartition entre les 4 profils :

- Sanguin
- Bilieux
- Lymphatique
- Nerveux

Le backend calcule :

- le pourcentage de chaque profil
- le profil dominant
- les profils secondaires éventuels

---

### 📊 Analyse personnalisée par IA

Une fois le quiz terminé, l'application :

1. envoie les données du quiz à l'API OpenAI
2. génère un rapport structuré
3. produit des recommandations personnalisées :

- portrait physiologique et comportemental
- conseils alimentaires
- activité physique adaptée
- gestion du stress
- reprogrammation positive

---

### 📄 Génération d'un rapport PDF

Le rapport est transformé en **PDF structuré** contenant :

- les résultats du quiz
- les recommandations personnalisées
- un disclaimer médical

Le PDF est généré avec **ReportLab**.

---

### ✉️ Envoi automatique par email

Le rapport est envoyé à l'utilisateur via **Resend API** sous forme de pièce jointe.

---

# 🧱 Architecture

# 🌿 LeadMagnet Naturo

LeadMagnet Naturo est une application web qui génère un **rapport personnalisé de naturopathie basé sur les tempéraments hippocratiques**.

L'utilisateur répond à un quiz, découvre son profil dominant, puis reçoit **un rapport détaillé généré par IA** et envoyé par email sous forme de **PDF personnalisé**.

Ce projet a été développé comme **projet portfolio** afin de démontrer la mise en place d'un pipeline complet :

- collecte de données utilisateur
- traitement et scoring backend
- génération de contenu via IA
- création de documents PDF
- envoi automatisé par email

---

# 🚀 Fonctionnalités

### 🧠 Quiz des tempéraments hippocratiques

Un questionnaire permet de déterminer la répartition entre les 4 profils :

- Sanguin
- Bilieux
- Lymphatique
- Nerveux

Le backend calcule :

- le pourcentage de chaque profil
- le profil dominant
- les profils secondaires éventuels

---

### 📊 Analyse personnalisée par IA

Une fois le quiz terminé, l'application :

1. envoie les données du quiz à l'API OpenAI
2. génère un rapport structuré
3. produit des recommandations personnalisées :

- portrait physiologique et comportemental
- conseils alimentaires
- activité physique adaptée
- gestion du stress
- reprogrammation positive

---

### 📄 Génération d'un rapport PDF

Le rapport est transformé en **PDF structuré** contenant :

- les résultats du quiz
- les recommandations personnalisées
- un disclaimer médical

Le PDF est généré avec **ReportLab**.

---

### ✉️ Envoi automatique par email

Le rapport est envoyé à l'utilisateur via **Resend API** sous forme de pièce jointe.

---

# 🧱 Architecture

**Frontend (HTML / JS)**
↓
**FastAPI Backend**
↓
**Scoring du quiz**
↓
**OpenAI (génération du rapport)**
↓
**PDF generation (ReportLab)**
↓
**Email sending (Resend)**

---

# 🛠 Stack technique

### Backend

- **Python 3.13**
- **FastAPI**
- **SQLAlchemy**
- **MySQL**
- **ReportLab**

### IA

- **OpenAI API**

### Email

- **Resend API**

### Frontend

- **HTML**
- **CSS**
- **Vanilla JavaScript**

---

# 📂 Structure du projet

---

# 🛠 Stack technique

### Backend

- **Python 3.13**
- **FastAPI**
- **SQLAlchemy**
- **MySQL**
- **ReportLab**

### IA

- **OpenAI API**

### Email

- **Resend API**

### Frontend

- **HTML**
- **CSS**
- **Vanilla JavaScript**

---

# 📂 Structure du projet

LeadMagnetNaturo
│
├── backend
│ ├── main.py
│ ├── repository.py
│ ├── schemas.py
│ ├── scoring.py
│ ├── pdf_utils.py
│
├── frontend
│ ├── index.html
│ ├── app.js
│ ├── style.css
│
├── generated_reports
│
├── .env.example
├── requirements.txt
└── README.md

# 🗄 Base de données

### Tables principales : quiz_submissions_v2

### Stocke :

**réponses utilisateur**
**scores**
**pourcentages**
**profils dominants**
**report_requests**
**Stocke :**
**email utilisateur**
**consentement RGPD**
**date de demande de rapport**

# 🔐 Sécurité

### Le projet inclut :

**validation des entrées utilisateur**
**gestion du consentement**
**séparation frontend / backend**
**protection contre le spam via rate limiting (à venir)**

# 🎯 Objectif du projet

### Ce projet a été développé dans le cadre d'un portfolio développeur web / IA afin de démontrer :

**conception d'une API backend**
**intégration d'API externes (OpenAI / email)**
**manipulation de données utilisateurs**
**génération de documents dynamiques**
**automatisation de processus**

# 🚀 Améliorations futures

**amélioration du design du PDF**
**ajout d'un vrai rate limiter**
**dashboard admin**
**historique des rapports générés**
**génération d'images pour les profils**
**version multilingue**

# 👨‍💻 Auteur

### Romain Bourgin

### Développeur Web & IA
