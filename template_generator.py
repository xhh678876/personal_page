"""
学术主页模板生成器
将 JSON 数据应用到多种精美模板
"""

import json
import sys

# ============ 模板 1: 紫色渐变科技风 ============
def template_gradient_purple(data):
    """紫色渐变 + 玻璃态 + 动画"""
    sections_html = ""
    
    for section in data.get("sections", []):
        section_type = section.get("type", "text-content")
        title = section.get("title", "")
        items = section.get("items", [])
        
        if section_type == "timeline":
            items_html = ""
            for item in items:
                items_html += f'''
                <div class="timeline-item">
                    <div class="timeline-marker"></div>
                    <div class="timeline-content">
                        <h3>{item.get('title', '')}</h3>
                        <p class="subtitle">{item.get('subtitle', '')}</p>
                        <p class="date">{item.get('date', '')}</p>
                        {f'<p class="description">{item["description"]}</p>' if item.get('description') else ''}
                    </div>
                </div>
                '''
            sections_html += f'<section><h2 class="section-title">{title}</h2><div class="timeline">{items_html}</div></section>'
        
        elif section_type == "grid-list":
            items_html = ""
            for item in items:
                tags = "".join([f'<span class="tag">{tag}</span>' for tag in item.get('tags', [])])
                items_html += f'''
                <div class="grid-card">
                    <h3>{item.get('title', '')}</h3>
                    {f'<p class="subtitle">{item["subtitle"]}</p>' if item.get('subtitle') else ''}
                    {f'<p class="date">{item["date"]}</p>' if item.get('date') else ''}
                    {f'<p>{item["description"]}</p>' if item.get('description') else ''}
                    {f'<div class="tags">{tags}</div>' if tags else ''}
                </div>
                '''
            sections_html += f'<section><h2 class="section-title">{title}</h2><div class="grid">{items_html}</div></section>'
        
        else:  # text-content
            for item in items:
                if item.get('description'):
                    sections_html += f'<section><h2 class="section-title">{title}</h2><div class="text-content"><p>{item["description"]}</p></div></section>'
    
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{data.get('name', 'Academic Homepage')}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 2rem;
            color: #333;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 3rem;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            animation: fadeIn 0.8s ease-out;
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .hero {{
            text-align: center;
            padding: 2rem 0 3rem;
            border-bottom: 2px solid #eee;
            margin-bottom: 3rem;
        }}
        
        h1 {{
            font-size: 3.5rem;
            font-weight: 800;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
            animation: slideDown 0.6s ease-out;
        }}
        
        @keyframes slideDown {{
            from {{ opacity: 0; transform: translateY(-20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .hero .title {{ font-size: 1.3rem; color: #666; margin-bottom: 1rem; }}
        .hero .bio {{ font-size: 1.1rem; color: #444; max-width: 800px; margin: 1.5rem auto; line-height: 1.8; }}
        
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
            padding: 0.5rem 1rem;
            border-radius: 50px;
            background: rgba(102, 126, 234, 0.1);
            transition: all 0.3s;
        }}
        
        .contact a:hover {{
            background: #667eea;
            color: white;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }}
        
        section {{ margin-bottom: 3rem; animation: slideUp 0.6s ease-out; }}
        
        @keyframes slideUp {{
            from {{ opacity: 0; transform: translateY(30px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .section-title {{
            font-size: 2rem;
            font-weight: 700;
            color: #333;
            margin-bottom: 1.5rem;
            padding-bottom: 0.5rem;
            border-bottom: 3px solid #667eea;
            position: relative;
        }}
        
        .section-title::after {{
            content: '';
            position: absolute;
            bottom: -3px;
            left: 0;
            width: 60px;
            height: 3px;
            background: #764ba2;
        }}
        
        /* Timeline */
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
            animation: fadeInLeft 0.5s ease-out;
        }}
        
        @keyframes fadeInLeft {{
            from {{ opacity: 0; transform: translateX(-20px); }}
            to {{ opacity: 1; transform: translateX(0); }}
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
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
            transition: all 0.3s;
        }}
        
        .timeline-item:hover .timeline-marker {{
            transform: scale(1.2);
            box-shadow: 0 0 0 6px rgba(102, 126, 234, 0.3);
        }}
        
        .timeline-content h3 {{ font-size: 1.3rem; color: #333; margin-bottom: 0.3rem; }}
        .subtitle {{ color: #666; font-weight: 600; margin-bottom: 0.3rem; }}
        .date {{ color: #999; font-size: 0.9rem; margin-bottom: 0.5rem; font-style: italic; }}
        .description {{ color: #555; line-height: 1.6; margin-top: 0.5rem; white-space: pre-wrap; }}
        
        /* Grid */
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 1.5rem;
        }}
        
        .grid-card {{
            background: linear-gradient(135deg, #f8f9fa 0%, #fff 100%);
            padding: 1.5rem;
            border-radius: 12px;
            border-left: 4px solid #667eea;
            transition: all 0.3s;
            animation: fadeInUp 0.5s ease-out;
        }}
        
        @keyframes fadeInUp {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .grid-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.2);
            border-left-color: #764ba2;
        }}
        
        .grid-card h3 {{ font-size: 1.2rem; color: #333; margin-bottom: 0.5rem; }}
        
        .tags {{
            margin-top: 1rem;
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
        }}
        
        .tag {{
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            font-size: 0.85rem;
            transition: transform 0.2s;
        }}
        
        .tag:hover {{
            transform: scale(1.05);
        }}
        
        /* Text Content */
        .text-content {{
            background: linear-gradient(135deg, #f8f9fa 0%, #fff 100%);
            padding: 2rem;
            border-radius: 12px;
            line-height: 1.8;
            color: #444;
            white-space: pre-wrap;
        }}
        
        @media (max-width: 768px) {{
            body {{ padding: 1rem; }}
            .container {{ padding: 1.5rem; }}
            h1 {{ font-size: 2rem; }}
            .grid {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="hero">
            <h1>{data.get('name', '')}</h1>
            {f'<p class="title">{data["title"]}</p>' if data.get('title') else ''}
            {f'<p class="bio">{data["bio"]}</p>' if data.get('bio') else ''}
            <div class="contact">
                {f'<a href="mailto:{data["email"]}">📧 Email</a>' if data.get('email') else ''}
                {f'<a href="https://{data["website"]}" target="_blank">🌐 Website</a>' if data.get('website') else ''}
            </div>
        </div>
        {sections_html}
    </div>
</body>
</html>'''


# ============ 模板 2: 暗黑极简风 ============
def template_dark_minimal(data):
    """暗黑背景 + 霓虹色彩"""
    sections_html = ""
    
    for section in data.get("sections", []):
        section_type = section.get("type", "text-content")
        title = section.get("title", "")
        items = section.get("items", [])
        
        if section_type == "timeline":
            items_html = ""
            for item in items:
                items_html += f'''
                <div class="item">
                    <h3>{item.get('title', '')}</h3>
                    {f'<p class="sub">{item["subtitle"]}</p>' if item.get('subtitle') else ''}
                    {f'<p class="date">{item["date"]}</p>' if item.get('date') else ''}
                    {f'<p class="desc">{item["description"]}</p>' if item.get('description') else ''}
                </div>
                '''
            sections_html += f'<section><h2>{title}</h2>{items_html}</section>'
        
        elif section_type == "grid-list":
            items_html = ""
            for item in items:
                items_html += f'''
                <div class="card">
                    <h3>{item.get('title', '')}</h3>
                    {f'<p>{item["description"]}</p>' if item.get('description') else ''}
                </div>
                '''
            sections_html += f'<section><h2>{title}</h2><div class="grid">{items_html}</div></section>'
        
        else:
            for item in items:
                if item.get('description'):
                    sections_html += f'<section><h2>{title}</h2><p class="desc">{item["description"]}</p></section>'
    
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{data.get('name', '')}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: 'Courier New', monospace;
            background: #0a0a0a;
            color: #e0e0e0;
            padding: 2rem;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: rgba(20, 20, 20, 0.9);
            border: 1px solid #00ff41;
            border-radius: 10px;
            padding: 3rem;
            box-shadow: 0 0 50px rgba(0, 255, 65, 0.1);
        }}
        
        h1 {{
            font-size: 3rem;
            color: #00ff41;
            text-transform: uppercase;
            letter-spacing: 0.2rem;
            margin-bottom: 1rem;
            text-shadow: 0 0 10px rgba(0, 255, 65, 0.5);
        }}
        
        .title {{ color: #00d4ff; margin-bottom: 1rem; font-size: 1.2rem; }}
        .bio {{ color: #ccc; line-height: 1.8; margin-bottom: 2rem; white-space: pre-wrap; }}
        
        .contact {{
            display: flex;
            gap: 1rem;
            margin-bottom: 3rem;
        }}
        
        .contact a {{
            color: #00ff41;
            text-decoration: none;
            padding: 0.5rem 1rem;
            border: 1px solid #00ff41;
            border-radius: 5px;
            transition: all 0.3s;
        }}
        
        .contact a:hover {{
            background: #00ff41;
            color: #000;
            box-shadow: 0 0 20px rgba(0, 255, 65, 0.6);
        }}
        
        section {{
            margin-bottom: 3rem;
            padding-bottom: 2rem;
            border-bottom: 1px solid #333;
        }}
        
        h2 {{
            color: #00d4ff;
            font-size: 1.8rem;
            margin-bottom: 1.5rem;
            text-transform: uppercase;
            letter-spacing: 0.1rem;
        }}
        
        .item {{
            margin-bottom: 2rem;
            padding-left: 1.5rem;
            border-left: 2px solid #00ff41;
        }}
        
        h3 {{ color: #fff; margin-bottom: 0.5rem; }}
        .sub {{ color: #00d4ff; margin-bottom: 0.3rem; }}
        .date {{ color: #888; font-size: 0.9rem; margin-bottom: 0.5rem; }}
        .desc {{ color: #ccc; line-height: 1.6; margin-top: 0.5rem; white-space: pre-wrap; }}
        
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 1rem;
        }}
        
        .card {{
            background: rgba(0, 255, 65, 0.05);
            border: 1px solid #00ff41;
            padding: 1.5rem;
            border-radius: 8px;
            transition: all 0.3s;
        }}
        
        .card:hover {{
            background: rgba(0, 255, 65, 0.1);
            box-shadow: 0 0 20px rgba(0, 255, 65, 0.2);
        }}
        
        @media (max-width: 768px) {{
            body {{ padding: 1rem; }}
            .container {{ padding: 1.5rem; }}
            h1 {{ font-size: 2rem; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{data.get('name', '')}</h1>
        {f'<p class="title">{data["title"]}</p>' if data.get('title') else ''}
        {f'<p class="bio">{data["bio"]}</p>' if data.get('bio') else ''}
        <div class="contact">
            {f'<a href="mailto:{data["email"]}">EMAIL</a>' if data.get('email') else ''}
            {f'<a href="https://{data["website"]}" target="_blank">WEBSITE</a>' if data.get('website') else ''}
        </div>
        {sections_html}
    </div>
</body>
</html>'''


# ============ 模板 3: 轻简学术风 ============
def template_academic_light(data):
    """传统学术风格 + 现代优化"""
    sections_html = ""
    
    for section in data.get("sections", []):
        title = section.get("title", "")
        items = section.get("items", [])
        
        items_html = ""
        for item in items:
            items_html += f'''
            <div class="entry">
                <h3>{item.get('title', '')}</h3>
                {f'<p class="meta">{item.get("subtitle", "")} | {item.get("date", "")}</p>' if item.get('subtitle') or item.get('date') else ''}
                {f'<p class="desc">{item["description"]}</p>' if item.get('description') else ''}
            </div>
            '''
        
        sections_html += f'<section><h2>{title}</h2>{items_html}</section>'
    
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{data.get('name', '')}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: 'Georgia', 'Times New Roman', serif;
            background: #fafafa;
            color: #333;
            line-height: 1.6;
            padding: 2rem;
        }}
        
        .container {{
            max-width: 800px;
            margin: 0 auto;
            background: white;
            padding: 4rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        h1 {{
            font-size: 2.5rem;
            color: #2c3e50;
            margin-bottom: 0.5rem;
            font-weight: 600;
        }}
        
        .title {{ color: #7f8c8d; font-size: 1.1rem; margin-bottom: 1rem; }}
        .bio {{ color: #555; margin: 2rem 0; font-size: 1.05rem; white-space: pre-wrap; }}
        
        .contact {{
            margin-bottom: 3rem;
            padding-bottom: 2rem;
            border-bottom: 2px solid #e0e0e0;
        }}
        
        .contact a {{
            color: #3498db;
            text-decoration: none;
            margin-right: 1.5rem;
        }}
        
        .contact a:hover {{
            text-decoration: underline;
        }}
        
        section {{
            margin-bottom: 2.5rem;
        }}
        
        h2 {{
            font-size: 1.5rem;
            color: #2c3e50;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 1px solid #bdc3c7;
        }}
        
        .entry {{
            margin-bottom: 1.5rem;
        }}
        
        h3 {{
            font-size: 1.1rem;
            color: #34495e;
            font-weight: 600;
        }}
        
        .meta {{
            color: #7f8c8d;
            font-size: 0.95rem;
            margin: 0.3rem 0;
        }}
        
        .desc {{
            color: #555;
            margin-top: 0.5rem;
            white-space: pre-wrap;
        }}
        
        @media (max-width: 768px) {{
            .container {{ padding: 2rem; }}
            h1 {{ font-size: 2rem; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{data.get('name', '')}</h1>
        {f'<p class="title">{data["title"]}</p>' if data.get('title') else ''}
        <div class="contact">
            {f'<a href="mailto:{data["email"]}">{data["email"]}</a>' if data.get('email') else ''}
            {f'<a href="https://{data["website"]}" target="_blank">{data["website"]}</a>' if data.get('website') else ''}
        </div>
        {f'<p class="bio">{data["bio"]}</p>' if data.get('bio') else ''}
        {sections_html}
    </div>
</body>
</html>'''



# ============ 主函数 ============
def generate_all_themes(json_data):
    """生成所有主题"""
    if isinstance(json_data, str):
        data = json.loads(json_data)
    else:
        data = json_data
    
    themes = {
        'gradient_purple': ('紫色渐变科技风', template_gradient_purple),
        'dark_minimal': ('暗黑极简风', template_dark_minimal),
        'academic_light': ('轻简学术风', template_academic_light),
    }
    
    results = {}
    for theme_id, (theme_name, template_func) in themes.items():
        html = template_func(data)
        filename = f"homepage_{theme_id}.html"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)
        results[theme_name] = filename
        print(f"✅ 已生成：{theme_name} → {filename}")
    
    return results


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # 从文件读取
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            json_data = f.read()
    else:
        # 从标准输入读取
        json_data = sys.stdin.read()
    
    print("\n🎨 正在生成多个主题...\n")
    results = generate_all_themes(json_data)
    
    print("\n" + "="*50)
    print("🎉 所有主题已生成！")
    print("="*50)
    for theme_name, filename in results.items():
        print(f"  {theme_name}: {filename}")
    print("\n💡 在浏览器中打开任意 HTML 文件预览效果！")
