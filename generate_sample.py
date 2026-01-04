from generate import load_yaml, HtmlRenderer, PdfRenderer
from pathlib import Path

def main():
    base_dir = Path(__file__).parent
    
    # Load config
    style_path = base_dir / 'config' / 'style.yaml'
    theme = load_yaml(style_path).get('theme', {})
    
    # Load sample content
    data_path = base_dir / 'data' / 'sample.yaml'
    content = load_yaml(data_path)
    
    print(f"Generating sample from: {data_path}")
    
    # Render HTML
    renderer_html = HtmlRenderer(theme, base_dir)
    html_content = renderer_html.render(content)
    
    output_html = base_dir / "output_sample.html"
    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Saved HTML to: {output_html}")

    # Render DOCX
    from generate import DocxRenderer
    renderer_docx = DocxRenderer(theme)
    output_docx = base_dir / "output_sample.docx"
    renderer_docx.render(content)
    renderer_docx.save(output_docx)
    
    # Render PDF
    renderer_pdf = PdfRenderer(theme)
    output_pdf = base_dir / "output_sample.pdf"
    
    try:
        renderer_pdf.render_from_html(html_content, str(output_pdf))
        print(f"Saved PDF to: {output_pdf}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
