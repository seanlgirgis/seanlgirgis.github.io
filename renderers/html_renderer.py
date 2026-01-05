from jinja2 import Environment, FileSystemLoader

def get_theme_color(theme, color_key):
    """Resolves 'primary_color' to actual hex, or checks if it's already hex."""
    if color_key in theme:
        return theme[color_key]
    return color_key # logic to handle direct hex codes if passed

class HtmlRenderer:
    """
    Renders content into HTML using Jinja2 templates.
    Responsible for generating dynamic CSS based on the theme (style.yaml).
    """

    def __init__(self, theme, base_dir):
        """
        Initialize with theme data and setup Jinja2 environment.
        Args:
            theme (dict): The resolved theme configuration.
            base_dir (Path): Root directory to locate 'templates/'.
        """
        self.theme = theme
        self.env = Environment(loader=FileSystemLoader(str(base_dir / 'templates')))
        
        # Register Markdown Filter for converting bold/links in text blocks
        self.env.filters['markdown'] = self.markdown_filter
        
        self.template = self.env.get_template('base.html')

    def render(self, content_data):
        """
        Main rendering workflow:
        1. Pre-process colors (resolve hex codes).
        2. Determine Stripe configuration (Theme fallback or Section override).
        3. Process sections (color resolution for text blocks).
        4. Generate Dynamic CSS (injecting theme colors).
        5. Render the 'base.html' template with data.
        """
        # Pre-process content for colors
        self.preprocess_theme_colors()
        
        # 1. Extract Stripe Config from Sections (Directive Block)
        #    OR Fallback to Theme Config
        stripe_config = None
        sections = content_data.get('sections', [])
        
        # Check Sections First
        for section in sections:
            if section.get('type') == 'stripe_block':
                stripe_config = section.get('config', {})
                print(f"DEBUG: Found Stripe Content Block: {stripe_config}")
                break
        
        # Fallback to Theme if not block found
        if not stripe_config:
            theme_stripe = self.theme.get('stripe', {})
            if theme_stripe.get('enabled'):
                 print("DEBUG: Using Theme Fallback for Stripe")
                 stripe_config = theme_stripe
        
        # 2. Process Sections (Resolution)
        processed_sections = self.process_sections(sections)
        
        # 3. Generate CSS (Pass stripe config)
        css_content = self.generate_css(stripe_config)
        
        return self.template.render(
            theme=self.theme,
            sections=processed_sections,
            css_content=css_content,
            stripe_config=stripe_config # Pass to template
        )

    def generate_css(self, stripe_config=None):
        t = self.theme
        s_conf = stripe_config or {}
        
        # Resolve stripe color
        stripe_color = t.get('primary_color', 'blue')
        if s_conf.get('color'):
             stripe_color = self.resolve_color(s_conf.get('color'))
             
        stripe_display = 'block' if s_conf.get('enabled', False) else 'none'
        
        # Resolve Typography
        typo = t.get('typography', {})
        default_typo = typo.get('default', {})
        pdf_typo = typo.get('pdf', {})
        
        base_font_size = default_typo.get('font_size_base', 11)
        pdf_font_size = pdf_typo.get('font_size_base', 8)
        
        return f"""
        <style>
        body {{
            font-family: Arial, "Helvetica Neue", Helvetica, sans-serif;
            color: {t.get('text_color', '#000')};
            background: #fff;
            font-size: {base_font_size}pt;
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100%;
            box-sizing: border-box;
            line-height: 1.5; 
        }}
        
        /* STATIC STRIPE STRATEGY */
        /* Just a normal block div at the top. No positioning. */
        .page-stripe {{
            display: {stripe_display} !important;
            width: 100% !important;
            height: 8px !important;
            background-color: {stripe_color} !important;
            margin: 0 !important;
            padding: 0 !important;
            /* Ensure it doesn't get pushed by anything */
            position: relative; 
            z-index: 9999;
            -webkit-print-color-adjust: exact;
            print-color-adjust: exact;
        }}
        
        /* Default Screen Wrapper */
        .content-wrapper {{
            padding: 25mm 25mm; 
            width: 100%;
            max-width: 216mm; /* Letter width constraint */
            margin: 0 auto;   /* Center on screen */
            box-sizing: border-box;
            position: relative;
            z-index: 2;
            background: #fff; /* Ensure white background for page look */
            box-shadow: 0 0 15px rgba(0,0,0,0.1); /* Subtle drop shadow */
        }}
        
        a {{
            color: {t.get('primary_color', '#0000EE')};
            text-decoration: none;
            font-weight: 500;
            -webkit-print-color-adjust: exact;
            print-color-adjust: exact;
        }}
        a:hover {{ text-decoration: underline; }}
        
        @media print {{
        @page {{
            size: Letter;
            margin: 0mm; /* Reset default @page margins since we control layout with padding */
        }}

        html, body {{
            font-size: {pdf_font_size}pt !important;
            width: 100%;
            height: 100%;
            -webkit-print-color-adjust: exact;
            print-color-adjust: exact;
            /* Do not force margin/padding 0 on body if not needed, but safe to keep 0 for layout control */
            margin: 0 !important;
            padding: 0 !important;
        }}
        
        /* 
           Wrapper Logic:
           - padding-top (Page 1): Handles space below stripe.
           - padding-left/right/bottom: Handles global margins.
           - This ensures Left/Right/Bottom are NEVER destroyed.
        */
        /* 
           Wrapper Logic:
           - padding-top (Page 1): Handles space below stripe.
           - padding-left/right/bottom: REMOVED. We now set specific PDF margins in pdf_renderer.py
             so the footer aligns correctly.
        */
        /* 
           Wrapper Logic:
           - padding-top (Page 1): Handles space below stripe.
           - padding-left/right/bottom: Handles global margins.
           - This ensures Left/Right/Bottom are NEVER destroyed.
        */
        .content-wrapper {{
            padding-top: {t.get('margins', {}).get('top', 12.7)}mm !important; 
            padding-left: {t.get('margins', {}).get('left', 12.7)}mm !important; 
            padding-right: {t.get('margins', {}).get('right', 12.7)}mm !important;
            padding-bottom: {t.get('margins', {}).get('bottom', 12.7)}mm !important;
            width: 100% !important;
        }}
        
        .page-stripe {{
            display: {stripe_display} !important;
            width: 100% !important;
            height: 8px !important;
            background-color: {stripe_color} !important;
            position: relative !important; 
            z-index: 10000 !important;
        }}
        
        /* 
           Manual Page Break Spacer 
           - Adds extra padding at the top of the new page to simulate margin.
           - We use padding-top because margin-top is often ignored at page start.
           - We double the standard top margin for 'Page 2+' effect.
        */
        .page-break {{ 
            page-break-before: always; 
            display: block;
            padding-top: {t.get('margins', {}).get('top', 12.7) * 2}mm !important;
            position: relative;
        }}
    }}
            
            .text-block.shaded, .shaded-border {{
                border-left-width: 3px !important;
                border-left-style: solid !important;
                border-left-color: {t.get('accent_color', 'orange')} !important;
                -webkit-print-color-adjust: exact;
                print-color-adjust: exact;
            }}
            .text-block.shaded {{ background-color: #f2f2f2 !important; }}
            .shaded-border {{ padding-left: 15px; }}
            .page-break {{ page-break-before: always; }}
        }}
        
        .shaded-border {{
             border-left-width: 3px !important;
             border-left-style: solid !important;
             border-left-color: {t.get('accent_color', 'orange')} !important;
             padding-left: 15px;
             -webkit-print-color-adjust: exact;
             print-color-adjust: exact;
        }}
        
        .header-block {{ width: 100%; text-align: center !important; margin-bottom: 10px; display: block; }}
        .header-block h1 {{
            color: {t.get('primary_color', 'blue')};
            margin: 0; font-size: 2.5em; text-transform: uppercase; letter-spacing: -1px; text-align: center; display: block; width: 100%;
        }}
        .header-block p.subtitle {{ color: #666; margin-top: 2px; font-size: 1.1em; text-align: center; }}
        
        .compound-text-block {{ margin-bottom: 20px; padding-bottom: 5px; line-height: 1.3; text-align: center; }}
        .compound-item {{ display: inline-block; }}
        .compound-separator {{ margin: 0 4px; color: #ccc; }}
        
        .text-block {{ margin-bottom: 10px; display: block; }}
        .text-block.normal {{ font-size: 1em; line-height: 1.4; }}
        .text-block.shaded {{
            background-color: #f2f2f2 !important; padding: 10px;
            border-left: 3px solid {t.get('accent_color', 'orange')} !important;
            color: #444; font-size: 1.0em;
            -webkit-print-color-adjust: exact; print-color-adjust: exact;
        }}
        
        .text-block.left_border {{
            background-color: transparent !important; padding: 10px; padding-left: 15px;
            border-left: 3px solid {t.get('primary_color', 'blue')} !important;
            color: {t.get('text_color', '#000')}; font-size: 1.0em;
            -webkit-print-color-adjust: exact; print-color-adjust: exact;
        }}
        
        /* Grid Styles */
        .grid-section-wrapper.shaded {{
            background-color: #f2f2f2 !important; padding: 20px;
            border-left: 8px solid {t.get('accent_color', 'orange')} !important;
            margin-bottom: 20px;
            -webkit-print-color-adjust: exact; print-color-adjust: exact;
        }}
        
        .grid-section-wrapper.left_border {{
            background-color: transparent !important; padding: 10px; padding-left: 15px;
            border-left: 3px solid {t.get('primary_color', 'blue')} !important;
            margin-bottom: 20px;
            -webkit-print-color-adjust: exact; print-color-adjust: exact;
        }}
        
        .section-title {{
            color: {t.get('primary_color', 'blue')};
            font-size: 1.25em; text-transform: uppercase; border-bottom: 1px solid #eee; padding-bottom: 3px; margin-top: 15px; margin-bottom: 10px;
        }}
        
        .section-title.accented {{
            border-bottom: none !important;
        }}
        
        .section-title.accented span {{
            border-bottom-width: 1px;
            border-bottom-style: solid;
            border-bottom-color: {t.get('accent_color', 'orange')} !important;
            padding-bottom: 5px;
        }}
        
        .text-block.shaded_primary {{
            background-color: #f2f2f2 !important; 
            padding: 5px 15px; /* Tight vertical padding */
            border-left: 3px solid {t.get('primary_color', 'blue')} !important;
            color: {t.get('text_color', '#000')}; font-size: 1.0em;
            -webkit-print-color-adjust: exact; print-color-adjust: exact;
        }}

        .grid-section-wrapper.shaded_primary {{
            background-color: #f2f2f2 !important; 
            padding: 5px 15px; /* Tight vertical padding */
            border-left: 3px solid {t.get('primary_color', 'blue')} !important;
            margin-bottom: 20px;
            -webkit-print-color-adjust: exact; print-color-adjust: exact;
        }}
        
        /* Project Block Styles */
        .project-block {{ margin-bottom: 20px; }}
        .project-block.left_border {{
            background-color: transparent !important; 
            padding: 5px 15px; 
            border-left: 3px solid {t.get('accent_color', 'orange')} !important;
            -webkit-print-color-adjust: exact; print-color-adjust: exact;
        }}
        .project-title {{ font-weight: bold; margin-bottom: 5px; color: #000; font-size: 1.05em; }}
        .project-details {{ padding-left: 20px; margin-bottom: 10px; margin-top: 5px; }}
        .project-details li {{ margin-bottom: 2px; }}
        .project-tags {{ margin-top: 8px; }}
        .project-tag {{ 
            display: inline-block; 
            background-color: {t.get('primary_color', 'blue')}; 
            color: #fff !important; 
            padding: 3px 10px; 
            border-radius: 12px; 
            font-size: 0.85em; 
            margin-right: 5px; 
            font-weight: bold;
            -webkit-print-color-adjust: exact; print-color-adjust: exact;
        }}
        
        strong {{ font-weight: bold; color: #000; }}
        
        /* Force remove unwanted separators in timeline/list blocks */
        .list-item, .timeline-item {{ border: none !important; border-top: none !important; border-bottom: none !important; }}
        </style>
        """
    
    def markdown_filter(self, text):
        if not text: return ""
        import re
        text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
        text = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', text)
        return text
        
    def preprocess_theme_colors(self):
        for key in ['primary_color', 'accent_color', 'text_color', 'background_color']:
            val = self.theme.get(key)
            if val and not val.startswith('#'):
                self.theme[key] = f"#{val}"
        stripe = self.theme.get('stripe', {})
        stripe['resolved_color'] = self.resolve_color(stripe.get('color'))

    def resolve_color(self, color_key):
        if not color_key: return "#000000"
        val = get_theme_color(self.theme, color_key)
        if val and not val.startswith('#'):
            return f"#{val}"
        return val

    def process_sections(self, sections):
        import copy
        processed = copy.deepcopy(sections)
        for section in processed:
            config = section.get('config', {})
            if section.get('type') == 'compound_text_block':
                default_color = config.get('font_color', 'text_color')
                for item in config.get('items', []):
                    c_key = item.get('font_color', default_color)
                    item['resolved_color'] = self.resolve_color(c_key)
            if section.get('type') == 'grid_block' and 'columns' in config:
                try:
                    config['columns'] = int(config['columns'])
                except:
                    pass
            
            # Resolve border_color if present
            if 'border_color' in config:
                 config['border_color'] = self.resolve_color(config['border_color'])
                 
        return processed

    def save(self, html_content, output_path):
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"Saved HTML to: {output_path}")
