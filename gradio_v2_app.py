"""
高級學術主頁生成器 v2 - 多模板版
支持：生成前選擇風格、多種模板、GitHub Pages 部署
"""

import gradio as gr
import google.generativeai as genai
from openai import OpenAI
import base64
import json
from pdf2image import convert_from_path
import io
from PIL import Image
import os
import zipfile
import shutil

# ============ 模板 1: 深色科技風 ============

def template_dark_tech(data):
    """深色背景 + 科技感 + 粒子動畫"""
    sections_html = ""
    for section in data.get("sections", []):
        title = section.get("title", "")
        items = section.get("items", [])
        items_html = ""
        for item in items:
            items_html += f'''
            <div class="item">
                <h3>{item.get('title', '')}</h3>
                <p class="sub">{item.get('subtitle', '')}</p>
                <p class="date">{item.get('date', '')}</p>
                {f'<p class="desc">{item["description"]}</p>' if item.get('description') else ''}
            </div>'''
        sections_html += f'<section><h2>{title}</h2>{items_html}</section>'
    
    return f'''<!DOCTYPE html>
<html lang="zh"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{data.get('name', '')}</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,sans-serif;background:linear-gradient(135deg,#0f172a,#1e293b);color:#f8fafc;min-height:100vh;padding:2rem}}
.container{{max-width:1000px;margin:0 auto}}
.hero{{text-align:center;padding:4rem 2rem}}
h1{{font-size:3.5rem;font-weight:800;background:linear-gradient(135deg,#667eea,#00d4ff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:1rem}}
.title{{font-size:1.3rem;color:#00d4ff;margin-bottom:2rem}}
.bio{{max-width:700px;margin:0 auto 2rem;line-height:1.8;opacity:0.9}}
.contact a{{color:#00d4ff;margin:0 1rem;text-decoration:none;padding:0.5rem 1.5rem;border:1px solid #00d4ff;border-radius:25px;transition:all 0.3s}}
.contact a:hover{{background:#00d4ff;color:#0f172a}}
section{{margin:3rem 0;padding:2rem;background:rgba(255,255,255,0.05);border-radius:12px;border-left:3px solid #667eea}}
h2{{color:#667eea;margin-bottom:1.5rem;font-size:1.8rem}}
.item{{margin-bottom:2rem;padding-left:1rem;border-left:2px solid #00d4ff}}
h3{{color:#00d4ff;margin-bottom:0.3rem}}
.sub{{color:#94a3b8;margin-bottom:0.2rem}}
.date{{color:#64748b;font-size:0.9rem;margin-bottom:0.5rem}}
.desc{{color:#cbd5e1;line-height:1.6;white-space:pre-wrap}}
</style></head>
<body><div class="container">
<div class="hero">
<h1>{data.get('name', '')}</h1>
<p class="title">{data.get('title', '')}</p>
<p class="bio">{data.get('bio', '')}</p>
<div class="contact">
{f'<a href="mailto:{data["email"]}">📧 Email</a>' if data.get('email') else ''}
{f'<a href="https://{data["website"]}" target="_blank">🌐 Website</a>' if data.get('website') else ''}
</div>
</div>
{sections_html}
</div></body></html>'''


# ============ 模板 2: 紫色漸變風 ============

def template_gradient_purple(data):
    """紫色漸變背景 + 玻璃態卡片"""
    sections_html = ""
    for section in data.get("sections", []):
        title = section.get("title", "")
        items = section.get("items", [])
        items_html = ""
        for item in items:
            items_html += f'''
            <div class="card">
                <h3>{item.get('title', '')}</h3>
                <p class="sub">{item.get('subtitle', '')}</p>
                <span class="date">{item.get('date', '')}</span>
                {f'<p class="desc">{item["description"]}</p>' if item.get('description') else ''}
            </div>'''
        sections_html += f'<section><h2>{title}</h2><div class="grid">{items_html}</div></section>'
    
    return f'''<!DOCTYPE html>
<html lang="zh"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{data.get('name', '')}</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,sans-serif;background:linear-gradient(135deg,#667eea,#764ba2);min-height:100vh;padding:2rem}}
.container{{max-width:1200px;margin:0 auto;background:rgba(255,255,255,0.95);border-radius:20px;padding:3rem;box-shadow:0 20px 60px rgba(0,0,0,0.3)}}
.hero{{text-align:center;padding:2rem 0 3rem;border-bottom:2px solid #eee;margin-bottom:2rem}}
h1{{font-size:3rem;font-weight:800;background:linear-gradient(135deg,#667eea,#764ba2);-webkit-background-clip:text;-webkit-text-fill-color:transparent}}
.title{{color:#666;font-size:1.2rem;margin:1rem 0}}
.bio{{color:#444;max-width:700px;margin:1rem auto;line-height:1.8}}
.contact a{{color:#667eea;margin:0 0.5rem;text-decoration:none}}
section{{margin:2rem 0}}
h2{{color:#333;font-size:1.8rem;margin-bottom:1rem;padding-bottom:0.5rem;border-bottom:3px solid #667eea}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:1.5rem}}
.card{{background:#f8f9fa;padding:1.5rem;border-radius:12px;border-left:4px solid #667eea;transition:all 0.3s}}
.card:hover{{transform:translateY(-5px);box-shadow:0 10px 30px rgba(0,0,0,0.1)}}
h3{{color:#333;margin-bottom:0.5rem}}
.sub{{color:#666}}
.date{{color:#999;font-size:0.9rem}}
.desc{{color:#555;line-height:1.6;margin-top:0.5rem;white-space:pre-wrap}}
</style></head>
<body><div class="container">
<div class="hero">
<h1>{data.get('name', '')}</h1>
<p class="title">{data.get('title', '')}</p>
<p class="bio">{data.get('bio', '')}</p>
<div class="contact">
{f'<a href="mailto:{data["email"]}">📧 {data["email"]}</a>' if data.get('email') else ''}
{f'<a href="https://{data["website"]}" target="_blank">🌐 {data["website"]}</a>' if data.get('website') else ''}
</div>
</div>
{sections_html}
</div></body></html>'''


# ============ 模板 3: 極簡學術風 ============

def template_academic_minimal(data):
    """簡潔白色背景 + 經典學術風格"""
    sections_html = ""
    for section in data.get("sections", []):
        title = section.get("title", "")
        items = section.get("items", [])
        items_html = ""
        for item in items:
            items_html += f'''
            <div class="entry">
                <div class="meta"><span class="date">{item.get('date', '')}</span></div>
                <div class="content">
                    <h3>{item.get('title', '')}</h3>
                    <p class="org">{item.get('subtitle', '')}</p>
                    {f'<p class="desc">{item["description"]}</p>' if item.get('description') else ''}
                </div>
            </div>'''
        sections_html += f'<section><h2>{title}</h2>{items_html}</section>'
    
    return f'''<!DOCTYPE html>
<html lang="zh"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{data.get('name', '')}</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:Georgia,'Times New Roman',serif;background:#fafafa;color:#333;line-height:1.6;padding:2rem}}
.container{{max-width:800px;margin:0 auto;background:white;padding:4rem;box-shadow:0 2px 10px rgba(0,0,0,0.1)}}
h1{{font-size:2.5rem;color:#2c3e50;margin-bottom:0.5rem;font-weight:600}}
.title{{color:#7f8c8d;font-size:1.1rem;margin-bottom:1rem}}
.bio{{color:#555;margin:2rem 0;font-size:1.05rem}}
.contact{{margin-bottom:3rem;padding-bottom:2rem;border-bottom:2px solid #e0e0e0}}
.contact a{{color:#3498db;text-decoration:none;margin-right:1.5rem}}
section{{margin-bottom:2.5rem}}
h2{{font-size:1.5rem;color:#2c3e50;margin-bottom:1rem;padding-bottom:0.5rem;border-bottom:1px solid #bdc3c7}}
.entry{{display:flex;margin-bottom:1.5rem}}
.meta{{width:120px;flex-shrink:0}}
.date{{color:#7f8c8d;font-size:0.9rem}}
.content{{flex:1}}
h3{{font-size:1.1rem;color:#34495e;font-weight:600;margin-bottom:0.3rem}}
.org{{color:#7f8c8d;font-size:0.95rem}}
.desc{{color:#555;margin-top:0.5rem;white-space:pre-wrap}}
@media(max-width:600px){{.entry{{flex-direction:column}}.meta{{width:100%;margin-bottom:0.3rem}}}}
</style></head>
<body><div class="container">
<h1>{data.get('name', '')}</h1>
<p class="title">{data.get('title', '')}</p>
<div class="contact">
{f'<a href="mailto:{data["email"]}">{data["email"]}</a>' if data.get('email') else ''}
{f'<a href="https://{data["website"]}" target="_blank">{data["website"]}</a>' if data.get('website') else ''}
</div>
{f'<p class="bio">{data["bio"]}</p>' if data.get('bio') else ''}
{sections_html}
</div></body></html>'''


# ============ 模板 4: 霓虹賽博風 ============

def template_neon_cyber(data):
    """黑底 + 霓虹綠 + 賽博朋克"""
    sections_html = ""
    for section in data.get("sections", []):
        title = section.get("title", "")
        items = section.get("items", [])
        items_html = ""
        for item in items:
            items_html += f'''
            <div class="item">
                <h3>{item.get('title', '')}</h3>
                <p class="sub">{item.get('subtitle', '')}</p>
                <p class="date">{item.get('date', '')}</p>
                {f'<p class="desc">{item["description"]}</p>' if item.get('description') else ''}
            </div>'''
        sections_html += f'<section><h2>&gt; {title}</h2>{items_html}</section>'
    
    return f'''<!DOCTYPE html>
<html lang="zh"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{data.get('name', '')}</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'Courier New',monospace;background:#0a0a0a;color:#e0e0e0;padding:2rem;min-height:100vh}}
.container{{max-width:900px;margin:0 auto;background:rgba(20,20,20,0.9);border:1px solid #00ff41;border-radius:10px;padding:3rem;box-shadow:0 0 50px rgba(0,255,65,0.1)}}
h1{{font-size:3rem;color:#00ff41;text-transform:uppercase;letter-spacing:0.2rem;margin-bottom:1rem;text-shadow:0 0 10px rgba(0,255,65,0.5)}}
.title{{color:#00d4ff;margin-bottom:1rem;font-size:1.2rem}}
.bio{{color:#ccc;line-height:1.8;margin-bottom:2rem}}
.contact{{margin-bottom:3rem}}
.contact a{{color:#00ff41;text-decoration:none;padding:0.5rem 1rem;border:1px solid #00ff41;border-radius:5px;margin-right:1rem;transition:all 0.3s}}
.contact a:hover{{background:#00ff41;color:#000;box-shadow:0 0 20px rgba(0,255,65,0.6)}}
section{{margin-bottom:3rem;padding-bottom:2rem;border-bottom:1px solid #333}}
h2{{color:#00d4ff;font-size:1.8rem;margin-bottom:1.5rem;text-transform:uppercase;letter-spacing:0.1rem}}
.item{{margin-bottom:2rem;padding-left:1.5rem;border-left:2px solid #00ff41}}
h3{{color:#fff;margin-bottom:0.5rem}}
.sub{{color:#00d4ff;margin-bottom:0.3rem}}
.date{{color:#888;font-size:0.9rem;margin-bottom:0.5rem}}
.desc{{color:#ccc;line-height:1.6;white-space:pre-wrap}}
</style></head>
<body><div class="container">
<h1>{data.get('name', '')}</h1>
<p class="title">{data.get('title', '')}</p>
<p class="bio">{data.get('bio', '')}</p>
<div class="contact">
{f'<a href="mailto:{data["email"]}">EMAIL</a>' if data.get('email') else ''}
{f'<a href="https://{data["website"]}" target="_blank">WEBSITE</a>' if data.get('website') else ''}
</div>
{sections_html}
</div></body></html>'''


# ============ 模板映射 ============

TEMPLATES = {
    "🌙 深色科技風": ("深色背景 + 科技藍 + 簡潔現代", template_dark_tech),
    "🌈 紫色漸變風": ("紫色漸變 + 玻璃態 + 卡片布局", template_gradient_purple),
    "📖 極簡學術風": ("白色背景 + 經典學術 + 專業簡潔", template_academic_minimal),
    "💚 霓虹賽博風": ("黑底霓虹 + 賽博朋克 + 極客風格", template_neon_cyber),
}


# ============ PDF 處理 ============

def pdf_to_images(pdf_file):
    try:
        images = convert_from_path(pdf_file, dpi=150)
        return images
    except Exception as e:
        raise Exception(f"PDF 轉換失敗: {str(e)}")


def parse_with_gemini(images, api_key):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        prompt = """分析這份學術簡歷，提取所有信息並返回 JSON 格式：
{
  "name": "姓名",
  "title": "職稱",
  "email": "郵箱",
  "website": "網站",
  "bio": "個人介紹",
  "sections": [
    {"title": "章節標題", "type": "timeline", "items": [{"title": "", "subtitle": "", "date": "", "description": ""}]}
  ]
}
返回純 JSON。"""

        response = model.generate_content([prompt] + images)
        text = response.text.strip()
        if text.startswith("```json"):
            text = text[7:-3].strip()
        elif text.startswith("```"):
            text = text[3:-3].strip()
        return json.loads(text), None
    except Exception as e:
        return None, f"Gemini 解析失敗: {str(e)}"


def parse_with_openai(images, api_key):
    try:
        client = OpenAI(api_key=api_key)
        image_contents = []
        for img in images:
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            image_contents.append({"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_str}"}})
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": [{"type": "text", "text": "分析學術簡歷，返回 JSON"}, *image_contents]}],
            max_tokens=4000
        )
        text = response.choices[0].message.content.strip()
        if text.startswith("```json"):
            text = text[7:-3].strip()
        return json.loads(text), None
    except Exception as e:
        return None, f"OpenAI 解析失敗: {str(e)}"


# ============ 生成項目 ============

def generate_project(data, template_func, output_dir="homepage_project"):
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)
    
    html = template_func(data)
    with open(os.path.join(output_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    
    readme = f"""# {data.get('name', '')} Homepage

## 部署到 GitHub Pages
1. 上傳到 GitHub 倉庫
2. Settings → Pages → Source: main
3. 訪問 https://username.github.io/repo
"""
    with open(os.path.join(output_dir, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme)
    
    zip_path = f"{output_dir}.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(output_dir):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, output_dir))
    
    return html, zip_path


# ============ Gradio 處理 ============

def process_resume(pdf_file, provider, api_key, template_choice, progress=gr.Progress()):
    if pdf_file is None:
        return None, None, None, "❌ 請上傳 PDF 文件"
    if not api_key:
        return None, None, None, "❌ 請輸入 API Key"
    
    try:
        progress(0.2, desc="📄 轉換 PDF...")
        images = pdf_to_images(pdf_file)
        
        progress(0.4, desc=f"🤖 使用 {provider} 解析...")
        data, error = parse_with_gemini(images, api_key) if provider == "Gemini" else parse_with_openai(images, api_key)
        if error:
            return None, None, None, f"❌ {error}"
        
        progress(0.7, desc=f"🎨 生成 {template_choice} 模板...")
        template_func = TEMPLATES[template_choice][1]
        html, zip_path = generate_project(data, template_func)
        
        progress(1.0, desc="✅ 完成！")
        return html, zip_path, json.dumps(data, ensure_ascii=False, indent=2), f"✅ 成功！使用了「{template_choice}」模板"
    except Exception as e:
        return None, None, None, f"❌ 錯誤: {str(e)}"


# ============ Gradio 界面 ============

with gr.Blocks(title="🎓 學術主頁生成器 v2", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 🎓 學術主頁生成器 v2
    > AI 解析 + 多模板選擇 + GitHub Pages 即用
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 📤 第一步：設置")
            provider = gr.Radio(["Gemini", "OpenAI"], value="Gemini", label="🤖 AI 提供商")
            api_key = gr.Textbox(label="🔑 API Key", type="password", info="Gemini: aistudio.google.com/app/apikey")
            pdf_file = gr.File(label="📄 上傳簡歷 PDF", file_types=[".pdf"], type="filepath")
            
            gr.Markdown("### 🎨 第二步：選擇模板風格")
            template_choice = gr.Radio(
                choices=list(TEMPLATES.keys()),
                value="🌙 深色科技風",
                label="選擇模板",
                info="選擇你喜歡的風格，生成後可以更換"
            )
            
            # 模板預覽說明
            template_info = gr.Markdown("**深色背景 + 科技藍 + 簡潔現代**")
            
            def update_info(choice):
                return f"**{TEMPLATES[choice][0]}**"
            
            template_choice.change(update_info, template_choice, template_info)
            
            gr.Markdown("### 🚀 第三步：生成")
            submit_btn = gr.Button("✨ 生成主頁", variant="primary", size="lg")
            status = gr.Textbox(label="📊 狀態", interactive=False)
        
        with gr.Column(scale=2):
            with gr.Tabs():
                with gr.TabItem("🖼️ 預覽效果"):
                    gr.Markdown("**生成後在此查看主頁效果**（下載後效果更完整）")
                    html_preview = gr.HTML()
                
                with gr.TabItem("📦 下載項目"):
                    gr.Markdown("""
                    ### 📥 GitHub Pages 項目
                    1. 下載 ZIP
                    2. 解壓 → 上傳到 GitHub
                    3. 開啟 Pages
                    4. 完成！
                    """)
                    zip_file = gr.File(label="下載 ZIP")
                
                with gr.TabItem("📋 JSON 數據"):
                    json_output = gr.Code(label="AI 提取的數據", language="json")
    
    submit_btn.click(
        fn=process_resume,
        inputs=[pdf_file, provider, api_key, template_choice],
        outputs=[html_preview, zip_file, json_output, status]
    )
    
    gr.Markdown("""
    ---
    ### 🎨 4 種模板風格
    | 模板 | 風格 | 適合 |
    |------|------|------|
    | 🌙 深色科技風 | 深藍背景、科技感 | CS/AI 研究者 |
    | 🌈 紫色漸變風 | 紫色漸變、玻璃態 | 通用學術 |
    | 📖 極簡學術風 | 白底、經典排版 | 傳統學科 |
    | 💚 霓虹賽博風 | 黑底霓虹、極客 | 黑客/開發者 |
    
    **Made with ❤️ for Researchers**
    """)

if __name__ == "__main__":
    demo.launch(share=True, debug=True)
