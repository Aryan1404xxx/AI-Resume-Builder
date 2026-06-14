# 📄 AI Resume Builder

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Gradio](https://img.shields.io/badge/Gradio-6.18-orange)
![Groq](https://img.shields.io/badge/Groq-LLaMA3-green)
![Free](https://img.shields.io/badge/API-Free-brightgreen)

An AI-powered resume builder that generates a fully formatted professional resume just from your basic information — powered by **Groq LLaMA3** and built with **Python + Gradio**.

## 🌐 Live Demo
👉 https://e811b3552ffce63fec.gradio.live

## ✨ Features
- 🤖 AI writes your entire resume content from basic info
- 📸 Photo upload support
- 🎨 Professional two-column design
- 📊 Skill bars with percentages
- ⬇️ Download as HTML file
- 🆓 100% free using Groq API

## 🚀 How to Run

### 1. Clone the repo
\`\`\`bash
git clone https://github.com/Aryan1404xxx/AI-Resume-Builder.git
cd AI-Resume-Builder
\`\`\`

### 2. Create virtual environment
\`\`\`bash
python3 -m venv venv
source venv/bin/activate
\`\`\`

### 3. Install dependencies
\`\`\`bash
pip install gradio groq pillow
\`\`\`

### 4. Get free Groq API key
- Go to https://console.groq.com
- Sign up for free
- Create an API key
- In app.py replace:
\`\`\`python
client = Groq(api_key="YOUR_GROQ_API_KEY_HERE")
\`\`\`

### 5. Run the app
\`\`\`bash
python3 app.py
\`\`\`

### 6. Open in browser
\`\`\`
http://127.0.0.1:7860
\`\`\`

## 🧠 How It Works
1. User fills in basic info (name, experience, education, skills)
2. Groq LLaMA3 70B AI generates professional resume content
3. Resume is rendered as a beautiful two-column HTML page
4. User downloads it as HTML (printable as PDF from browser)

## 📊 What AI Generates
- ✅ Professional summary
- ✅ Formatted work experience with bullet points
- ✅ Education section with details
- ✅ Skills with proficiency percentages

## 🛠️ Tech Stack
| Tool | Purpose |
|------|---------|
| Python 3.13 | Core language |
| Groq LLaMA3 70B | AI content generation |
| Gradio | Web interface |
| Pillow | Photo processing |

## 📁 Project Structure
\`\`\`
resume_builder/
├── app.py          # Main app with UI and AI logic
└── README.md       # Project documentation
\`\`\`

## 📌 Notes
- Built and tested on MacBook Air M2
- Uses Groq free tier (no credit card needed)
- Resume downloads as HTML (printable as PDF from browser)
- Public link expires after 72 hours — run locally for permanent access
- Photo upload is optional

## 👤 Author
**Aryan Sinha** — [GitHub](https://github.com/Aryan1404xxx)
