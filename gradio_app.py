"""
學術主頁生成器 - Gradio 版本
使用 Gradio 創建簡單易用的 Web 界面
支持 Gemini 和 OpenAI Vision API
"""

import gradio as gr
import google.generativeai as genai
from openai import OpenAI
import base64
from pathlib import Path
import json
from pdf2image import convert_from_path
import io
from PIL import Image
import tempfile
import os

# ============ AI 解析函數 ============

def pdf_to_images(pdf_file):
    """將 PDF 轉換為圖片列表"""
    try:
        # Gradio 傳入的 pdf_file 是文件路徑字符串，直接使用即可
        # 轉換 PDF 為圖片
        images = convert_from_path(pdf_file, dpi=150)
        
        return images
    except Exception as e:
        raise Exception(f"PDF 轉換失敗: {str(e)}")


def parse_with_gemini(images, api_key):
    """使用 Gemini Vision API 解析簡歷"""
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        prompt = """你是一個專業的學術簡歷解析專家。請仔細分析這份學術簡歷/CV 並提取所有信息。

請按照以下格式返回 JSON：

{
  "name": "姓名",
  "title": "職稱/頭銜",
  "email": "郵箱",
  "website": "個人網站",
  "bio": "簡短的個人介紹",
  "sections": [
    {
      "title": "章節標題（如：教育背景）",
      "type": "timeline/grid-list/text-content/gallery",
      "items": [
        {
          "title": "標題",
          "subtitle": "副標題（學校/公司/會議名稱）",
          "date": "時間",
          "description": "描述",
          "tags": ["標籤1", "標籤2"]
        }
      ]
    }
  ]
}

章節類型選擇規則：
- timeline: 教育、工作經歷（有時間順序）
- grid-list: 出版物、項目、獎項（卡片展示）
- text-content: 研究興趣、個人簡介（段落文本）
- gallery: 海報、圖片展示

請仔細識別所有章節並提取完整信息。返回純 JSON，不要有其他文本。"""

        # 準備圖片內容
        contents = [prompt]
        for img in images:
            contents.append(img)
        
        # 調用 API
        response = model.generate_content(contents)
        
        # 解析 JSON
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
        
        # 將圖片轉為 base64
        image_contents = []
        for img in images:
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            image_contents.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{img_str}"
                }
            })
        
        prompt = """你是一個專業的學術簡歷解析專家。請仔細分析這份學術簡歷/CV 並提取所有信息。

請按照以下格式返回 JSON：

{
  "name": "姓名",
  "title": "職稱/頭銜",
  "email": "郵箱",
  "website": "個人網站",
  "bio": "簡短的個人介紹",
  "sections": [
    {
      "title": "章節標題（如：教育背景）",
      "type": "timeline/grid-list/text-content/gallery",
      "items": [
        {
          "title": "標題",
          "subtitle": "副標題（學校/公司/會議名稱）",
          "date": "時間",
          "description": "描述",
          "tags": ["標籤1", "標籤2"]
        }
      ]
    }
  ]
}

請仔細識別所有章節並提取完整信息。返回純 JSON，不要有其他文本。"""

        # 調用 API
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        *image_contents
                    ]
                }
            ],
            max_tokens=4000,
            temperature=0.1
        )
        
        # 解析 JSON
        text = response.choices[0].message.content.strip()
        if text.startswith("```json"):
            text = text[7:-3].strip()
        elif text.startswith("```"):
            text = text[3:-3].strip()
        
        data = json.loads(text)
        return data, None
        
    except Exception as e:
        return None, f"OpenAI 解析失敗: {str(e)}"


# ============ 生成 HTML ============

def generate_html(data):
    """生成精美的學術主頁 HTML"""
    
    # 生成章節 HTML
    sections_html = ""
    for section in data.get("sections", []):
        section_type = section.get("type", "text-content")
        title = section.get("title", "")
        items = section.get("items", [])
        
        if section_type == "timeline":
            # 時間線布局
            items_html = ""
            for item in items:
                items_html += f"""
                <div class="timeline-item">
                    <div class="timeline-marker"></div>
                    <div class="timeline-content">
                        <h3>{item.get('title', '')}</h3>
                        <p class="subtitle">{item.get('subtitle', '')}</p>
                        <p class="date">{item.get('date', '')}</p>
                        <p class="description">{item.get('description', '')}</p>
                    </div>
                </div>
                """
            sections_html += f"""
            <section class="section">
                <h2 class="section-title">{title}</h2>
                <div class="timeline">
                    {items_html}
                </div>
            </section>
            """
            
        elif section_type == "grid-list":
            # 網格布局
            items_html = ""
            for item in items:
                tags_html = "".join([f'<span class="tag">{tag}</span>' for tag in item.get('tags', [])])
                items_html += f"""
                <div class="grid-card">
                    <h3>{item.get('title', '')}</h3>
                    <p class="subtitle">{item.get('subtitle', '')}</p>
                    <p class="date">{item.get('date', '')}</p>
                    <p class="description">{item.get('description', '')}</p>
                    <div class="tags">{tags_html}</div>
                </div>
                """
            sections_html += f"""
            <section class="section">
                <h2 class="section-title">{title}</h2>
                <div class="grid-container">
                    {items_html}
                </div>
            </section>
            """
            
        else:  # text-content
            items_html = ""
            for item in items:
                items_html += f"<p>{item.get('description', '')}</p>"
            sections_html += f"""
            <section class="section">
                <h2 class="section-title">{title}</h2>
                <div class="text-content">
                    {items_html}
                </div>
            </section>
            """
    
    # 完整 HTML
    html = f"""
    <!DOCTYPE html>
    <html lang="zh-TW">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{data.get('name', '學術主頁')}</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Microsoft JhengHei', sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 2rem;
            }}
            
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                background: rgba(255, 255, 255, 0.95);
                border-radius: 20px;
                padding: 3rem;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            }}
            
            .hero {{
                text-align: center;
                padding: 2rem 0 3rem;
                border-bottom: 2px solid #eee;
                margin-bottom: 3rem;
            }}
            
            .hero h1 {{
                font-size: 3rem;
                font-weight: 800;
                background: linear-gradient(135deg, #667eea, #764ba2);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 0.5rem;
            }}
            
            .hero .title {{
                font-size: 1.3rem;
                color: #666;
                margin-bottom: 1rem;
            }}
            
            .hero .bio {{
                font-size: 1.1rem;
                color: #444;
                max-width: 800px;
                margin: 1.5rem auto;
                line-height: 1.8;
            }}
            
            .contact {{
                display: flex;
                gap: 1.5rem;
                justify-content: center;
                margin-top: 1.5rem;
                flex-wrap: wrap;
            }}
            
            .contact a {{
                color: #667eea;
                text-decoration: none;
                font-weight: 600;
                transition: color 0.3s;
            }}
            
            .contact a:hover {{ color: #764ba2; }}
            
            .section {{
                margin-bottom: 3rem;
            }}
            
            .section-title {{
                font-size: 2rem;
                font-weight: 700;
                color: #333;
                margin-bottom: 1.5rem;
                padding-bottom: 0.5rem;
                border-bottom: 3px solid #667eea;
            }}
            
            /* 時間線樣式 */
            .timeline {{
                position: relative;
                padding-left: 2rem;
            }}
            
            .timeline::before {{
                content: '';
                position: absolute;
                left: 0;
                top: 0;
                bottom: 0;
                width: 3px;
                background: linear-gradient(180deg, #667eea, #764ba2);
            }}
            
            .timeline-item {{
                position: relative;
                margin-bottom: 2rem;
            }}
            
            .timeline-marker {{
                position: absolute;
                left: -2.6rem;
                top: 0.5rem;
                width: 1rem;
                height: 1rem;
                background: #667eea;
                border-radius: 50%;
                border: 3px solid #fff;
                box-shadow: 0 0 0 3px #667eea33;
            }}
            
            .timeline-content h3 {{
                font-size: 1.3rem;
                color: #333;
                margin-bottom: 0.3rem;
            }}
            
            .subtitle {{
                color: #666;
                font-weight: 600;
                margin-bottom: 0.3rem;
            }}
            
            .date {{
                color: #999;
                font-size: 0.9rem;
                margin-bottom: 0.5rem;
            }}
            
            .description {{
                color: #555;
                line-height: 1.6;
            }}
            
            /* 網格樣式 */
            .grid-container {{
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
                gap: 1.5rem;
            }}
            
            .grid-card {{
                background: #f8f9fa;
                padding: 1.5rem;
                border-radius: 12px;
                border-left: 4px solid #667eea;
                transition: transform 0.3s, box-shadow 0.3s;
            }}
            
            .grid-card:hover {{
                transform: translateY(-5px);
                box-shadow: 0 10px 30px rgba(0,0,0,0.15);
            }}
            
            .grid-card h3 {{
                font-size: 1.2rem;
                color: #333;
                margin-bottom: 0.5rem;
            }}
            
            .tags {{
                margin-top: 1rem;
                display: flex;
                gap: 0.5rem;
                flex-wrap: wrap;
            }}
            
            .tag {{
                background: #667eea;
                color: white;
                padding: 0.3rem 0.8rem;
                border-radius: 20px;
                font-size: 0.85rem;
            }}
            
            /* 文本內容樣式 */
            .text-content {{
                background: #f8f9fa;
                padding: 2rem;
                border-radius: 12px;
                line-height: 1.8;
                color: #444;
            }}
            
            .text-content p {{
                margin-bottom: 1rem;
            }}
            
            @media (max-width: 768px) {{
                body {{ padding: 1rem; }}
                .container {{ padding: 1.5rem; }}
                .hero h1 {{ font-size: 2rem; }}
                .grid-container {{ grid-template-columns: 1fr; }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="hero">
                <h1>{data.get('name', '')}</h1>
                <p class="title">{data.get('title', '')}</p>
                <p class="bio">{data.get('bio', '')}</p>
                <div class="contact">
                    {f'<a href="mailto:{data.get("email", "")}">📧 {data.get("email", "")}</a>' if data.get('email') else ''}
                    {f'<a href="{data.get("website", "")}" target="_blank">🌐 個人網站</a>' if data.get('website') else ''}
                </div>
            </div>
            
            {sections_html}
        </div>
    </body>
    </html>
    """
    
    return html


# ============ Gradio 界面 ============

def process_resume(pdf_file, provider, api_key, progress=gr.Progress()):
    """處理簡歷並生成主頁"""
    
    if pdf_file is None:
        return None, None, None, "❌ 請上傳 PDF 文件", None
    
    if not api_key:
        return None, None, None, "❌ 請輸入 API Key", None
    
    try:
        # 步驟 1: 轉換 PDF
        progress(0.2, desc="📄 正在轉換 PDF 為圖片...")
        images = pdf_to_images(pdf_file)
        
        # 步驟 2: AI 解析
        progress(0.4, desc=f"🤖 正在使用 {provider} 解析簡歷...")
        if provider == "Gemini":
            data, error = parse_with_gemini(images, api_key)
        else:
            data, error = parse_with_openai(images, api_key)
        
        if error:
            return None, None, None, f"❌ {error}", None
        
        # 步驟 3: 生成多個主題
        progress(0.7, desc="✨ 正在生成 3 種精美主頁...")
        
        # 導入模板生成器
        from template_generator import template_gradient_purple, template_dark_minimal, template_academic_light
        
        # 生成各個模板
        html1 = template_gradient_purple(data)
        html2 = template_dark_minimal(data)
        html3 = template_academic_light(data)
        
        # 保存文件
        file1 = "homepage_gradient_purple.html"
        file2 = "homepage_dark_minimal.html"
        file3 = "homepage_academic_light.html"
        
        with open(file1, "w", encoding="utf-8") as f:
            f.write(html1)
        with open(file2, "w", encoding="utf-8") as f:
            f.write(html2)
        with open(file3, "w", encoding="utf-8") as f:
            f.write(html3)
        
        progress(1.0, desc="✅ 完成！")
        
        json_output = json.dumps(data, ensure_ascii=False, indent=2)
        
        return file1, file2, file3, "✅ 生成成功！已創建 3 種主題", json_output
        
    except Exception as e:
        return None, None, None, f"❌ 錯誤: {str(e)}", None


# 創建 Gradio 界面
with gr.Blocks(title="🎓 學術主頁生成器", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 🎓 學術主頁生成器
    > AI 驅動的學術主頁自動生成工具 - 支持 Gemini 和 GPT-4o Vision
    
    ### 使用步驟：
    1. 選擇 AI 提供商（推薦 Gemini - 免費）
    2. 輸入 API Key
    3. 上傳簡歷 PDF
    4. 點擊「生成主頁」
    5. 下載 **3 種不同風格** 的精美主頁！
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            provider = gr.Radio(
                choices=["Gemini", "OpenAI"],
                value="Gemini",
                label="🤖 AI 提供商",
                info="推薦使用 Gemini（免費）"
            )
            
            api_key = gr.Textbox(
                label="🔑 API Key",
                placeholder="請輸入您的 API Key",
                type="password",
                info="Gemini: https://aistudio.google.com/app/apikey"
            )
            
            pdf_file = gr.File(
                label="📄 上傳簡歷 PDF",
                file_types=[".pdf"],
                type="filepath"
            )
            
            submit_btn = gr.Button("✨ 生成 3 種主頁", variant="primary", size="lg")
        
        with gr.Column(scale=1):
            status = gr.Textbox(label="📊 狀態", interactive=False)
            
            with gr.Tab("🌈 紫色渐變科技風"):
                html_file1 = gr.File(label="📥 下載主題 1")
                
            with gr.Tab("🌑 暗黑極簡風"):
                html_file2 = gr.File(label="📥 下載主題 2")
                
            with gr.Tab("📖 輕簡學術風"):
                html_file3 = gr.File(label="📥 下載主題 3")
            
            json_output = gr.Code(label="📋 提取的數據 (JSON)", language="json")
    
    submit_btn.click(
        fn=process_resume,
        inputs=[pdf_file, provider, api_key],
        outputs=[html_file1, html_file2, html_file3, status, json_output]
    )
    
    gr.Markdown("""
    ---
    ### 📝 API Key 獲取
    - **Gemini**（推薦 - 免費）: https://aistudio.google.com/app/apikey
    - **OpenAI**: https://platform.openai.com/api-keys
    
    ### ✨ 3 種精美主題
    - 🌈 **紫色漸變科技風** - 現代、動感、玻璃態效果
    - 🌑 **暗黑極簡風** - 酷炫、極客、霓虹賽博風
    - 📖 **輕簡學術風** - 專業、傳統、經典學術布局
    
    **一次生成，3 種選擇，總有一款適合你！** 🎨
    
    Made with ❤️ for Researchers
    """)
    
    gr.Markdown("""
    ---
    ### 📝 API Key 獲取
    - **Gemini**（推薦 - 免費）: https://aistudio.google.com/app/apikey
    - **OpenAI**: https://platform.openai.com/api-keys
    
    ### ✨ 特點
    - 🆓 完全免費（使用 Gemini）
    - 🎨 精美的漸變設計
    - 📱 完全響應式
    - ⚡ 快速生成（10-30秒）
    
    Made with ❤️ for Researchers
    """)

if __name__ == "__main__":
    demo.launch(share=True, debug=True)
