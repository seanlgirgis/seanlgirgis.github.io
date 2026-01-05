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
    """
    Safely loads a YAML file with UTF-8 encoding.
    Args:
        path (Path): The pathlib Path to the file.
    Returns:
        dict: The parsed YAML content.
    """
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def resolve_references(content_list, store_data):
    """
    Merging Logic (The "Decentralized Engine"):
    Iterates through the content list (layout).
    If a block has 'content_key' in its config, fetches the corresponding data 
    from the global 'store.yaml' and merges it into the block's config.

    Merge Strategy:
    1. Base: The data from store.yaml (e.g., job title, bullets).
    2. Override: The config from the layout file (e.g., page_break_before).
    3. Result: Layout settings overwrite store data if conflicts exist.
    
    Args:
        content_list (list): The 'sections' list from a layout YAML.
        store_data (dict): The global content store.
    
    Returns:
        list: A new list of section blocks with content resolved.
    """
    if not store_data:
        return content_list
        
    resolved_list = []
    for block in content_list:
        # Create a copy to avoid mutating original loaded data deeply if cached
        block_copy = block.copy()
        config = block_copy.get('config', {}).copy()
        
        content_key = config.get('content_key')
        if content_key:
            # Fetch from store
            store_item = store_data.get(content_key)
            if store_item:
                # Merge logic: Store content acts as base, Layout config overrides
                # But typically store has 'items', 'title', etc.
                # We merge store_item INTO config.
                # So if layout has 'page_break_before: true', it stays.
                # If store has 'title: ABC', it is added.
                merged_config = store_item.copy()
                merged_config.update(config) # Layout wins conflicts
                config = merged_config
            else:
                print(f"WARNING: Content key '{content_key}' not found in store.")
        
        block_copy['config'] = config
        resolved_list.append(block_copy)
    return resolved_list

# --- MAIN EXECUTION ---

def main():
    """
    The Build Orchestrator.
    1. Parses arguments (--target resume/cv/all).
    2. Loads Global Style (style.yaml) and Content Store (store.yaml).
    3. Iterates through selected targets.
    4. Calls specific renderers (DocxRenderer, HtmlRenderer, PdfRenderer) for each format.
    """
    parser = argparse.ArgumentParser(description="Multi-Format Generator")
    parser.add_argument('--target', choices=['resume', 'cv', 'all', 'word_test'], default='resume', help='Target document to generate')
    parser.add_argument('--format', choices=['html', 'pdf', 'docx', 'md', 'all'], default='all', help='Output format')
    args = parser.parse_args()

    # Paths
    base_dir = Path(__file__).parent
    
    # Load Style
    style_path = base_dir / 'config' / 'style.yaml'
    print(f"Loading Style: {style_path}")
    theme = load_yaml(style_path).get('theme', {})

    # Load Store (Global Content Repository)
    store_path = base_dir / 'data' / 'store.yaml'
    store_data = {}
    if store_path.exists():
        print(f"Loading Store: {store_path}")
        store_data = load_yaml(store_path)

    # Define Targets Config
    # Each target has specific layout files for each format family.
    # 'web' is shared for HTML and MD.
    targets_config = {
        'resume': {
            'pdf': base_dir / 'data' / 'resume_pdf.yaml',
            'docx': base_dir / 'data' / 'resume_docx.yaml',
            'web': base_dir / 'data' / 'resume.yaml'
        },
        'cv': {
            'pdf': base_dir / 'data' / 'cv_pdf.yaml',
            'docx': base_dir / 'data' / 'cv_docx.yaml',
            'web': base_dir / 'data' / 'cv.yaml'
        },
        'word_test': {
            'pdf': base_dir / 'data' / 'word_test.yaml',
            'docx': base_dir / 'data' / 'word_test.yaml',
            'web': base_dir / 'data' / 'word_test.yaml'
        }
    }

    # Determine targets
    if args.target == 'all':
        selected_targets = ['resume', 'cv']
    else:
        selected_targets = [args.target]

    def load_and_resolve(path):
        """Helper to load a YAML layout file and resolve its references against store.yaml"""
        if not path.exists():
            print(f"Error: Layout file not found: {path}")
            return None
        print(f"Loading Content: {path}")
        raw = load_yaml(path)
        
        if isinstance(raw, dict):
             sections = raw.get('sections', [])
        else:
             sections = raw
             
        resolved = resolve_references(sections, store_data)
        
        if isinstance(raw, dict):
             raw['sections'] = resolved
             return raw
        else:
             return {'sections': resolved}

    for target_name in selected_targets:
        print(f"\n--- Generating Target: {target_name} ---")
        
        config_map = targets_config.get(target_name)
        if not config_map:
             print(f"Unknown target: {target_name}")
             continue

        # 1. Render DOCX (Source: *_docx.yaml)
        if args.format in ['docx', 'all']:
            content = load_and_resolve(config_map['docx'])
            if content:
                renderer_docx = DocxRenderer(theme)
                renderer_docx.render(content)
                output_docx = base_dir / f"{target_name}.docx"
                renderer_docx.save(output_docx)
        
        # 2. Render Web/MD (Source: *.yaml)
        # We load this once for both HTML and MD
        if args.format in ['html', 'md', 'all']:
            content_web = load_and_resolve(config_map['web'])
            if content_web:
                if args.format in ['html', 'all']:
                    renderer_html = HtmlRenderer(theme, base_dir)
                    html_content = renderer_html.render(content_web)
                    output_html = base_dir / "components" / f"{target_name}.html"
                    renderer_html.save(html_content, output_html)
                    
                    # 3. Render PDF (Source: *_pdf.yaml)
                    # PDF generation uses wkhtmltopdf which takes HTML input.
                    # BUT the user wants a specific PDF layout (page breaks etc).
                    # So we must generate a TEMPORARY HTML from the PDF layout,
                    # and then convert THAT to PDF.
                
                if args.format in ['md', 'all']:
                    from renderers.md_renderer import MdRenderer
                    renderer_md = MdRenderer(theme)
                    md_content = renderer_md.render(content_web)
                    output_md = base_dir / f"{target_name}.md"
                    renderer_md.save(md_content, output_md)

        # 3. Render PDF (Source: *_pdf.yaml)
        # Note: We need to do this specifically.
        if args.format in ['pdf', 'all']:
            content_pdf = load_and_resolve(config_map['pdf'])
            if content_pdf:
                # We need to generate HTML specifically for the PDF renderer
                renderer_html_for_pdf = HtmlRenderer(theme, base_dir)
                html_for_pdf = renderer_html_for_pdf.render(content_pdf)
                
                renderer_pdf = PdfRenderer(theme)
                output_pdf = base_dir / f"{target_name}.pdf"
                footer_config = content_pdf.get('config', {}).get('footer')
                renderer_pdf.render_from_html(html_for_pdf, str(output_pdf), footer_config=footer_config)

if __name__ == "__main__":
    main()
