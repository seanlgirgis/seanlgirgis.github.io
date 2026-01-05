import yaml
import sys
import argparse
from pathlib import Path
from renderers.docx_renderer import DocxRenderer
from renderers.html_renderer import HtmlRenderer
from renderers.pdf_renderer import PdfRenderer
from renderers.md_renderer import MdRenderer

# --- 1. CONFIG & UTILS ---

def load_yaml(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading {path}: {e}")
        sys.exit(1)

# --- MAIN EXECUTION ---

def main():
    parser = argparse.ArgumentParser(description="Multi-Format Generator")
    parser.add_argument('--target', choices=['test', 'resume', 'cv', 'matrix', 'word_test', 'all'], default='test')
    args = parser.parse_args()

    # Paths
    base_dir = Path(__file__).parent
    style_path = base_dir / 'config' / 'style.yaml'
    
    print(f"Loading Style: {style_path}")
    theme = load_yaml(style_path).get('theme', {})

    # Determine targets
    if args.target == 'all':
        targets = ['resume', 'cv']
    else:
        targets = [args.target]

    for target in targets:
        print(f"\n--- Generating Target: {target} ---")
        if target == 'test':
            data_path = base_dir / 'data' / 'test_content.yaml'
        elif target == 'resume':
            data_path = base_dir / 'data' / 'resume.yaml'
        elif target == 'cv':
            data_path = base_dir / 'data' / 'cv.yaml'
        elif target == 'word_test':
            data_path = base_dir / 'data' / 'word_test.yaml'
        else:
            data_path = base_dir / 'data' / 'test_matrix.yaml'

        print(f"Loading Content: {data_path}")
        content = load_yaml(data_path)

        # 1. Render DOCX
        renderer_docx = DocxRenderer(theme)
        renderer_docx.render(content)
        output_docx = base_dir / f"output_{target}.docx"
        renderer_docx.save(output_docx)
        
        # 2. Render HTML
        renderer_html = HtmlRenderer(theme, base_dir)
        html_content = renderer_html.render(content)
        output_html = base_dir / f"output_{target}.html"
        renderer_html.save(html_content, output_html)

        # 3. Render PDF (From HTML)
        renderer_pdf = PdfRenderer(theme)
        output_pdf = base_dir / f"output_{target}.pdf"
        footer_config = content.get('config', {}).get('footer')
        renderer_pdf.render_from_html(html_content, str(output_pdf), footer_config=footer_config)

        # 4. Render Markdown
        renderer_md = MdRenderer(theme)
        md_content = renderer_md.render(content)
        output_md = base_dir / f"output_{target}.md"
        renderer_md.save(md_content, output_md)

if __name__ == "__main__":
    main()
