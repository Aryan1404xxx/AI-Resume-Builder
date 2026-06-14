import gradio as gr
import json
import os
from groq import Groq
from PIL import Image
import base64
import io
from dotenv import load_dotenv

# ── Load API Key from .env ────────────────────────────────
load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# ── Generate Resume Content ───────────────────────────────
def generate_resume(name, job_title, email, phone, address, website, linkedin,
                    summary_prompt, experience, education, skills):

    prompt = f"""
    Create a professional resume for this person. Return ONLY a JSON object, no extra text, no markdown.

    Name: {name}
    Job Title: {job_title}
    About: {summary_prompt}
    Experience: {experience}
    Education: {education}
    Skills: {skills}

    Return exactly this JSON:
    {{
        "summary": "2-3 sentence professional summary",
        "experience": [
            {{
                "date": "Date range",
                "title": "Job Title",
                "company": "Company, Location",
                "bullets": ["achievement 1", "achievement 2", "achievement 3"]
            }}
        ],
        "education": [
            {{
                "date": "Date range",
                "degree": "Degree name",
                "school": "School, Location",
                "details": ["detail 1", "detail 2"]
            }}
        ],
        "skills": [
            {{"name": "Skill 1", "level": 85}},
            {{"name": "Skill 2", "level": 90}}
        ]
    }}
    """

    message = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = message.choices[0].message.content.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()
    data = json.loads(raw)
    return data

# ── Build HTML Resume ─────────────────────────────────────
def build_html(name, job_title, email, phone, address, website, linkedin, data, photo):

    photo_html = ""
    if photo is not None:
        img = Image.fromarray(photo)
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        b64 = base64.b64encode(buf.getvalue()).decode()
        photo_html = f'<img src="data:image/png;base64,{b64}" class="photo"/>'

    exp_html = ""
    for job in data.get("experience", []):
        bullets = "".join(f"<li>{b}</li>" for b in job.get("bullets", []))
        exp_html += f"""
        <div class="entry">
            <div class="entry-date">{job['date']}</div>
            <div class="entry-title">{job['title']}</div>
            <div class="entry-sub">{job['company']}</div>
            <ul>{bullets}</ul>
        </div>"""

    edu_html = ""
    for edu in data.get("education", []):
        details = "".join(f"<li>{d}</li>" for d in edu.get("details", []))
        edu_html += f"""
        <div class="entry">
            <div class="entry-date">{edu['date']}</div>
            <div class="entry-title">{edu['degree']}</div>
            <div class="entry-sub">{edu['school']}</div>
            <ul>{details}</ul>
        </div>"""

    skills_html = ""
    for skill in data.get("skills", []):
        skills_html += f"""
        <div class="skill-row">
            <span class="skill-name">{skill['name']}</span>
            <div class="skill-bar">
                <div class="skill-fill" style="width:{skill['level']}%"></div>
            </div>
            <span class="skill-pct">{skill['level']}%</span>
        </div>"""

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="UTF-8"/>
    <style>
        * {{ margin:0; padding:0; box-sizing:border-box; }}
        body {{ font-family: Georgia, serif; display:flex; min-height:100vh; }}
        .left {{ width:35%; background:#1a5f7a; color:white; padding:40px 25px; }}
        .right {{ width:65%; padding:40px 35px; background:#fff; }}
        .name {{ font-size:26px; font-weight:bold; letter-spacing:3px; text-align:center; color:white; margin-bottom:5px; }}
        .job-title {{ text-align:center; font-size:11px; letter-spacing:2px; color:#cce8f0; margin-bottom:25px; }}
        .photo {{ width:110px; height:110px; border-radius:50%; display:block; margin:0 auto 25px; object-fit:cover; border:3px solid white; }}
        .section-title {{ font-size:11px; letter-spacing:3px; font-weight:bold; color:#1a5f7a; border-bottom:2px solid #1a5f7a; padding-bottom:4px; margin:20px 0 12px; text-transform:uppercase; }}
        .left .section-title {{ color:white; border-bottom-color:rgba(255,255,255,0.4); }}
        .contact-item {{ font-size:11px; margin-bottom:6px; color:#cce8f0; }}
        .contact-label {{ color:white; font-weight:bold; display:inline-block; width:55px; }}
        .summary {{ font-size:12px; line-height:1.7; color:#555; margin-bottom:10px; }}
        .entry {{ margin-bottom:18px; }}
        .entry-date {{ font-size:11px; color:#1a5f7a; font-weight:bold; }}
        .entry-title {{ font-size:13px; font-weight:bold; color:#222; }}
        .entry-sub {{ font-size:11px; color:#777; margin-bottom:5px; }}
        .entry ul {{ padding-left:16px; }}
        .entry ul li {{ font-size:11px; color:#444; margin-bottom:3px; line-height:1.5; }}
        .skill-row {{ display:flex; align-items:center; margin-bottom:8px; gap:8px; }}
        .skill-name {{ font-size:11px; width:130px; color:#cce8f0; }}
        .skill-bar {{ flex:1; height:5px; background:rgba(255,255,255,0.2); border-radius:3px; }}
        .skill-fill {{ height:100%; background:white; border-radius:3px; }}
        .skill-pct {{ font-size:10px; color:#cce8f0; width:30px; text-align:right; }}
    </style>
    </head>
    <body>
    <div class="left">
        {photo_html}
        <div class="section-title">Contact</div>
        <div class="contact-item"><span class="contact-label">phone</span>{phone}</div>
        <div class="contact-item"><span class="contact-label">email</span>{email}</div>
        <div class="contact-item"><span class="contact-label">address</span>{address}</div>
        <div class="contact-item"><span class="contact-label">website</span>{website}</div>
        <div class="contact-item"><span class="contact-label">linkedin</span>{linkedin}</div>
        <div class="section-title">Skills</div>
        {skills_html}
    </div>
    <div class="right">
        <div class="name">{name.upper()}</div>
        <div class="job-title">{job_title.upper()}</div>
        <div class="section-title">Summary</div>
        <div class="summary">{data.get('summary', '')}</div>
        <div class="section-title">Professional Experience</div>
        {exp_html}
        <div class="section-title">Education</div>
        {edu_html}
    </div>
    </body>
    </html>
    """
    return html

# ── Main Function ─────────────────────────────────────────
def create_resume(name, job_title, email, phone, address, website, linkedin,
                  summary_prompt, experience, education, skills, photo):

    if not name or not job_title:
        return "<p style='color:red'>⚠️ Please fill in at least Name and Job Title!</p>", None

    try:
        data = generate_resume(name, job_title, email, phone, address,
                               website, linkedin, summary_prompt,
                               experience, education, skills)

        html = build_html(name, job_title, email, phone, address,
                         website, linkedin, data, photo)

        with open("resume_output.html", "w") as f:
            f.write(html)

        return html, "resume_output.html"

    except Exception as e:
        return f"<p style='color:red'>❌ Error: {str(e)}</p>", None

# ── Gradio UI ─────────────────────────────────────────────
with gr.Blocks(title="AI Resume Builder") as demo:
    gr.Markdown("# 📄 AI Resume Builder\nFill in your basic info and AI will generate a professional resume!")

    with gr.Row():
        with gr.Column():
            gr.Markdown("### 👤 Personal Info")
            name = gr.Textbox(label="Full Name", placeholder="e.g. Aryan Sinha")
            job_title = gr.Textbox(label="Job Title", placeholder="e.g. Software Engineer")
            email = gr.Textbox(label="Email", placeholder="aryan@email.com")
            phone = gr.Textbox(label="Phone", placeholder="+91 98765 43210")
            address = gr.Textbox(label="Address", placeholder="Patna, Bihar, India")
            website = gr.Textbox(label="Website (optional)")
            linkedin = gr.Textbox(label="LinkedIn (optional)")
            photo = gr.Image(label="📸 Upload Photo (optional)", type="numpy")

        with gr.Column():
            gr.Markdown("### 📝 Tell AI About You")
            summary_prompt = gr.Textbox(label="About You", lines=3,
                placeholder="e.g. I am a CS student with experience in Python and ML projects")
            experience = gr.Textbox(label="Work Experience", lines=4,
                placeholder="e.g. Interned at XYZ company in 2023, worked on data analysis. Built 3 ML projects.")
            education = gr.Textbox(label="Education", lines=3,
                placeholder="e.g. B.Tech Computer Science from XYZ University, 2024, GPA 8.5/10")
            skills = gr.Textbox(label="Skills", lines=2,
                placeholder="e.g. Python, Machine Learning, scikit-learn, OpenCV, Gradio, SQL")

    generate_btn = gr.Button("✨ Generate My Resume", variant="primary", size="lg")

    gr.Markdown("### 👀 Resume Preview")
    html_output = gr.HTML()
    file_output = gr.File(label="⬇️ Download Resume as HTML")

    generate_btn.click(
        fn=create_resume,
        inputs=[name, job_title, email, phone, address, website, linkedin,
                summary_prompt, experience, education, skills, photo],
        outputs=[html_output, file_output]
    )

if __name__ == "__main__":
    demo.launch(share=True)
