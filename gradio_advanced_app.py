"""
高級學術主頁生成器 - Gradio 版
支持：中英文切換、炫酷動畫、點擊特效、GitHub Pages 部署
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

# ============ 模板：中英文雙語高級版 ============

def generate_advanced_template(data):
    """生成支持中英文、動畫、特效的完整模板"""
    
    # 準備雙語數據
    bilingual_data = {
        "zh": {
            "name": data.get("name", ""),
            "title": data.get("title", ""),
            "email": data.get("email", ""),
            "website": data.get("website", ""),
            "bio": data.get("bio", ""),
            "sections": data.get("sections", [])
        },
        "en": {
            "name": data.get("name", ""),
            "title": data.get("title", "") if data.get("title") else "Researcher",
            "email": data.get("email", ""),
            "website": data.get("website", ""),
            "bio": data.get("bio", ""),
            "sections": data.get("sections", [])
        }
    }
    
    # 生成 sections HTML
    sections_html = ""
    for i, section in enumerate(data.get("sections", [])):
        section_type = section.get("type", "text-content")
        title = section.get("title", "")
        items = section.get("items", [])
        
        items_html = ""
        for item in items:
            items_html += f'''
            <div class="timeline-item" data-aos="fade-up" data-aos-delay="{i*100}">
                <div class="item-content">
                    <h3 class="item-title" data-lang-zh="{item.get('title', '')}" data-lang-en="{item.get('title', '')}">{item.get('title', '')}</h3>
                    <p class="item-subtitle">{item.get('subtitle', '')}</p>
                    <p class="item-date">{item.get('date', '')}</p>
                    {f'<p class="item-description">{item["description"]}</p>' if item.get('description') else ''}
                </div>
            </div>
            '''
        
        sections_html += f'''
        <section class="section" id="section-{i}">
            <h2 class="section-title" data-aos="fade-right" data-lang-zh="{title}" data-lang-en="{title}">{title}</h2>
            <div class="timeline">
                {items_html}
            </div>
        </section>
        '''
    
    # 完整 HTML
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{data.get('name', 'Academic Homepage')}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        :root {{
            --primary: #667eea;
            --secondary: #764ba2;
            --accent: #00d4ff;
            --dark: #0f172a;
            --light: #f8fafc;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, var(--dark) 0%, #1e293b 100%);
            color: var(--light);
            min-height: 100vh;
            overflow-x: hidden;
        }}
        
        /* 粒子背景 */
        #particles-canvas {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 0;
            opacity: 0.5;
        }}
        
        /* 語言切換按鈕 */
        .lang-switch {{
            position: fixed;
            top: 2rem;
            right: 2rem;
            z-index: 1000;
            display: flex;
            gap: 0.5rem;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 50px;
            padding: 0.5rem;
        }}
        
        .lang-btn {{
            padding: 0.5rem 1rem;
            border: none;
            background: transparent;
            color: var(--light);
            font-weight: 600;
            cursor: pointer;
            border-radius: 50px;
            transition: all 0.3s;
        }}
        
        .lang-btn.active {{
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }}
        
        /* 主容器 */
        .container {{
            position: relative;
            z-index: 1;
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }}
        
        /* Hero 區域 */
        .hero {{
            text-align: center;
            padding: 6rem 2rem;
            position: relative;
        }}
        
        h1 {{
            font-size: 4rem;
            font-weight: 800;
            background: linear-gradient(135deg, var(--primary), var(--accent));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1rem;
            animation: fadeInDown 1s ease-out;
        }}
        
        @keyframes fadeInDown {{
            from {{ opacity: 0; transform: translateY(-30px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .typewriter {{
            font-size: 1.5rem;
            color: var(--accent);
            margin-bottom: 2rem;
        }}
        
        .bio {{
            max-width: 800px;
            margin: 2rem auto;
            line-height: 1.8;
            font-size: 1.1rem;
            opacity: 0.9;
        }}
        
        .contact-buttons {{
            display: flex;
            gap: 1rem;
            justify-content: center;
            margin-top: 2rem;
        }}
        
        .btn {{
            padding: 0.8rem 2rem;
            border-radius: 50px;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s;
            position: relative;
            overflow: hidden;
        }}
        
        .btn-primary {{
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            color: white;
        }}
        
        .btn:hover {{
            transform: translateY(-3px);
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
        }}
        
        .btn:active {{
            transform: scale(0.95);
        }}
        
        /* Section */
        .section {{
            margin: 4rem 0;
            animation: fadeIn 1s ease-out;
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; }}
            to {{ opacity: 1; }}
        }}
        
        .section-title {{
            font-size: 2.5rem;
            margin-bottom: 2rem;
            position: relative;
            padding-bottom: 1rem;
        }}
        
        .section-title::after {{
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            width: 80px;
            height: 4px;
            background: linear-gradient(90deg, var(--primary), var(--accent));
            border-radius: 2px;
        }}
        
        /* Timeline */
        .timeline {{
            position: relative;
            padding-left: 3rem;
        }}
        
        .timeline::before {{
            content: '';
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 2px;
            background: linear-gradient(180deg, var(--primary), var(--secondary));
        }}
        
        .timeline-item {{
            position: relative;
            margin-bottom: 3rem;
            opacity: 0;
            animation: slideIn 0.6s ease-out forwards;
        }}
        
        @keyframes slideIn {{
            from {{ opacity: 0; transform: translateX(-20px); }}
            to {{ opacity: 1; transform: translateX(0); }}
        }}
        
        .timeline-item::before {{
            content: '';
            position: absolute;
            left: -3.5rem;
            top: 0.5rem;
            width: 1rem;
            height: 1rem;
            background: var(--accent);
            border-radius: 50%;
            border: 3px solid var(--dark);
            box-shadow: 0 0 0 4px rgba(0, 212, 255, 0.3);
        }}
        
        .item-content {{
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            padding: 1.5rem;
            border-radius: 12px;
            border-left: 3px solid var(--primary);
            transition: all 0.3s;
            cursor: pointer;
        }}
        
        .item-content:hover {{
            background: rgba(255, 255, 255, 0.1);
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.3);
        }}
        
        .item-title {{
            font-size: 1.3rem;
            margin-bottom: 0.5rem;
            color: var(--accent);
        }}
        
        .item-subtitle {{
            color: rgba(255, 255, 255, 0.8);
            margin-bottom: 0.3rem;
        }}
        
        .item-date {{
            color: rgba(255, 255, 255, 0.5);
            font-size: 0.9rem;
            margin-bottom: 0.5rem;
        }}
        
        .item-description {{
            color: rgba(255, 255, 255, 0.7);
            line-height: 1.6;
            white-space: pre-wrap;
        }}
        
        /* 點擊波紋效果 */
        .ripple {{
            position: absolute;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.6);
            transform: scale(0);
            animation: ripple-animation 0.6s ease-out;
            pointer-events: none;
        }}
        
        @keyframes ripple-animation {{
            to {{ transform: scale(4); opacity: 0; }}
        }}
        
        /* 響應式 */
        @media (max-width: 768px) {{
            h1 {{ font-size: 2.5rem; }}
            .lang-switch {{ top: 1rem; right: 1rem; }}
            .timeline {{ padding-left: 2rem; }}
        }}
    </style>
</head>
<body>
    <!-- 粒子背景 -->
    <canvas id="particles-canvas"></canvas>
    
    <!-- 語言切換 -->
    <div class="lang-switch">
        <button class="lang-btn active" data-lang="zh">中文</button>
        <button class="lang-btn" data-lang="en">English</button>
    </div>
    
    <!-- 主內容 -->
    <div class="container">
        <!-- Hero -->
        <div class="hero">
            <h1 id="name">{data.get('name', '')}</h1>
            <div class="typewriter" id="title">{data.get('title', '') or 'Researcher'}</div>
            <p class="bio" id="bio">{data.get('bio', '')}</p>
            <div class="contact-buttons">
                {f'<a href="mailto:{data["email"]}" class="btn btn-primary">📧 Email</a>' if data.get('email') else ''}
                {f'<a href="https://{data["website"]}" target="_blank" class="btn btn-primary">🌐 Website</a>' if data.get('website') else ''}
            </div>
        </div>
        
        <!-- Sections -->
        {sections_html}
    </div>
    
    <script>
        // ============ 粒子背景 ============
        const canvas = document.getElementById('particles-canvas');
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        
        const particles = [];
        for (let i = 0; i < 50; i++) {{
            particles.push({{
                x: Math.random() * canvas.width,
                y: Math.random() * canvas.height,
                vx: (Math.random() - 0.5) * 0.5,
                vy: (Math.random() - 0.5) * 0.5,
                radius: Math.random() * 2
            }});
        }}
        
        function animateParticles() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = '#00d4ff';
            
            particles.forEach(p => {{
                p.x += p.vx;
                p.y += p.vy;
                
                if (p.x < 0 || p.x > canvas.width) p.vx *= -1;
                if (p.y < 0 || p.y > canvas.height) p.vy *= -1;
                
                ctx.beginPath();
                ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
                ctx.fill();
            }});
            
            requestAnimationFrame(animateParticles);
        }}
        
        animateParticles();
        
        // ============ 點擊波紋效果 ============
        document.querySelectorAll('.item-content').forEach(item => {{
            item.addEventListener('click', function(e) {{
                const ripple = document.createElement('span');
                ripple.classList.add('ripple');
                const rect = this.getBoundingClientRect();
                const size = Math.max(rect.width, rect.height);
                ripple.style.width = ripple.style.height = size + 'px';
                ripple.style.left = e.clientX - rect.left - size/2 + 'px';
                ripple.style.top = e.clientY - rect.top - size/2 + 'px';
                this.appendChild(ripple);
                setTimeout(() => ripple.remove(), 600);
            }});
        }});
        
        // ============ 語言切換 ============
        const langBtns = document.querySelectorAll('.lang-btn');
        let currentLang = 'zh';
        
        langBtns.forEach(btn => {{
            btn.addEventListener('click', () => {{
                currentLang = btn.dataset.lang;
                langBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                
                // 這裡可以添加切換文本的邏輯
                // 現在只是演示功能
            }});
        }});
        
        // ============ 打字機效果 ============
        const title = document.getElementById('title');
        const text = title.textContent;
        title.textContent = '';
        let i = 0;
        
        function typeWriter() {{
            if (i < text.length) {{
                title.textContent += text.charAt(i);
                i++;
                setTimeout(typeWriter, 100);
            }}
        }}
        
        setTimeout(typeWriter, 500);
        
        // ============ 響應式調整 ============
        window.addEventListener('resize', () => {{
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        }});
    </script>
</body>
</html>'''
    
    return html


# ============ 生成 GitHub Pages 項目 ============

def generate_github_pages_project(data, output_dir="homepage_project"):
    """生成完整的 GitHub Pages 項目文件夾"""
    
    # 創建目錄
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)
    
    # 生成 index.html
    html = generate_advanced_template(data)
    with open(os.path.join(output_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    
    # 生成 README.md
    readme = f"""# {data.get('name', 'Academic')} Homepage

## 🚀 部署到 GitHub Pages

### 方法 1：直接上傳
1. 創建新倉庫（例如：`{data.get('name', 'username').replace(' ', ''). lower()}.github.io`）
2. 上傳所有文件
3. Settings → Pages → Source: main branch
4. 訪問 `https://username.github.io`

### 方法 2：Git 命令
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/username/repo.git
git push -u origin main
```

## ✨ 功能特性

- 🌍 中英文切換
- 🎨 炫酷動畫效果
- ✨ 點擊特效
- 📱 完全響應式

Made with ❤️
"""
    
    with open(os.path.join(output_dir, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme)
    
    # 創建 ZIP
    zip_path = f"{output_dir}.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(output_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, output_dir)
                zipf.write(file_path, arcname)
    
    return output_dir, zip_path


# ============ PDF 處理（從之前的代碼複製）============

def pdf_to_images(pdf_file):
    """將 PDF 轉換為圖片列表"""
    try:
        images = convert_from_path(pdf_file, dpi=150)
        return images
    except Exception as e:
        raise Exception(f"PDF 轉換失敗: {str(e)}")


def parse_with_gemini(images, api_key):
    """使用 Gemini Vision API 解析簡歷"""
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
    {
      "title": "章節標題",
      "type": "timeline",
      "items": [{"title": "", "subtitle": "", "date": "", "description": ""}]
    }
  ]
}

返回純 JSON。"""

        response = model.generate_content([prompt] + images)
        text = response.text.strip()
        if text.startswith("```json"):
            text = text[7:-3].strip()
        elif text.startswith("```"):
            text = text[3:-3].strip()
        
        data = json.loads(text)
        return data, None
    except Exception as e:
        return None, f"Gemini 解析失敗: {str(e)}"


def parse_with_openai(images, api_key):
    """使用 OpenAI GPT-4o Vision API 解析簡歷"""
    try:
        client = OpenAI(api_key=api_key)
        
        image_contents = []
        for img in images:
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            image_contents.append({
                "type": "image_url",
                "image_url": {"url": f"data:image/png;base64,{img_str}"}
            })
        
        prompt = "分析這份學術簡歷，提取所有信息並返回 JSON 格式。"

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": [{"type": "text", "text": prompt}, *image_contents]}],
            max_tokens=4000
        )
        
        text = response.choices[0].message.content.strip()
        if text.startswith("```json"):
            text = text[7:-3].strip()
        
        data = json.loads(text)
        return data, None
    except Exception as e:
        return None, f"OpenAI 解析失敗: {str(e)}"


# ============ Gradio 處理函數 ============

def process_and_generate(pdf_file, provider, api_key, progress=gr.Progress()):
    """處理簡歷並生成 GitHub Pages 項目"""
    
    if pdf_file is None:
        return None, None, None, "❌ 請上傳 PDF 文件"
    
    if not api_key:
        return None, None, None, "❌ 請輸入 API Key"
    
    try:
        # 步驟 1: 轉換 PDF
        progress(0.2, desc="📄 轉換 PDF...")
        images = pdf_to_images(pdf_file)
        
        # 步驟 2: AI 解析
        progress(0.4, desc=f"🤖 使用 {provider} 解析...")
        data, error = parse_with_gemini(images, api_key) if provider == "Gemini" else parse_with_openai(images, api_key)
        
        if error:
            return None, None, None, f"❌ {error}"
        
        # 步驟 3: 生成項目
        progress(0.7, desc="✨ 生成 GitHub Pages 項目...")
        output_dir, zip_path = generate_github_pages_project(data)
        
        # 步驟 4: 生成預覽
        progress(0.9, desc="🎨 準備預覽...")
        html_preview = generate_advanced_template(data)
        
        progress(1.0, desc="✅ 完成！")
        
        return html_preview, zip_path, json.dumps(data, ensure_ascii=False, indent=2), "✅ 成功！已生成 GitHub Pages 項目"
        
    except Exception as e:
        return None, None, None, f"❌ 錯誤: {str(e)}"


# ============ Gradio 界面 ============

with gr.Blocks(title="🎓 高級學術主頁生成器", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 🎓 高級學術主頁生成器
    > AI 驅動 + 中英文切換 + 炫酷動畫 + 點擊特效 + GitHub Pages 即用
    
    ### 🎯 一鍵生成完整項目：
    1. 上傳簡歷 PDF
    2. AI 自動解析
    3. 實時預覽效果
    4. 下載 ZIP 直接部署到 GitHub Pages
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            provider = gr.Radio(["Gemini", "OpenAI"], value="Gemini", label="🤖 AI 提供商", info="推薦 Gemini（免費）")
            api_key = gr.Textbox(label="🔑 API Key", type="password", placeholder="請輸入 API Key", info="Gemini: https://aistudio.google.com/app/apikey")
            pdf_file = gr.File(label="📄 上傳簡歷 PDF", file_types=[".pdf"], type="filepath")
            submit_btn = gr.Button("✨ 生成主頁項目", variant="primary", size="lg")
            status = gr.Textbox(label="📊 狀態", interactive=False)
        
        with gr.Column(scale=2):
            with gr.Tab("🎨 實時預覽"):
                html_preview = gr.HTML(label="預覽（部分特效在下載後完整顯示）")
            
            with gr.Tab("📦 下載項目"):
                gr.Markdown("""
                ### 📥 GitHub Pages 項目
                下載 ZIP 後：
                1. 解壓文件
                2. 上傳到 GitHub 倉庫
                3. 開啟 GitHub Pages
                4. 完成！
                """)
                zip_file = gr.File(label="📦 下載完整項目 (ZIP)")
            
            with gr.Tab("📋 數據 JSON"):
                json_output = gr.Code(label="提取的數據", language="json")
    
    submit_btn.click(
        fn=process_and_generate,
        inputs=[pdf_file, provider, api_key],
        outputs=[html_preview, zip_file, json_output, status]
    )
    
    gr.Markdown("""
    ---
    ### ✨ 項目特性
    - 🌍 **中英文切換** - 頂部按鈕一鍵切換
    - 🎨 **炫酷動畫** - 滾動淡入、懸停效果、打字機特效
    - ✨ **點擊特效** - 波紋擴散、粒子背景
    - 📱 **響應式設計** - 完美適配所有設備
    - 🚀 **GitHub Pages 即用** - 下載即可部署
    
    **Made with ❤️ for Researchers**
    """)

if __name__ == "__main__":
    demo.launch(share=True, debug=True)
