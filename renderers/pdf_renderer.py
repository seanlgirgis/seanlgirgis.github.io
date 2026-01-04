import pdfkit

class PdfRenderer:
    def __init__(self, theme):
        self.theme = theme
        # Hardcoded path for Windows dev environment
        # user might need to adjust this path if different
        self.wkhtmltopdf_path = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
        self.config = pdfkit.configuration(wkhtmltopdf=self.wkhtmltopdf_path)
        
    def render_from_html(self, html_content, output_path, footer_config=None):
        options = {
            'page-size': 'Letter',
            'margin-top': '0mm', 
            'margin-right': '0mm', # Revert to 0 for full bleed stripe
            'margin-bottom': '15mm', # Space for footer
            'margin-left': '0mm',  # Revert to 0 for full bleed stripe
            'encoding': "UTF-8",
            'no-outline': None,
            'enable-local-file-access': None,
            'disable-smart-shrinking': None,
            'print-media-type': None
        }
        
        # Handle Footer using HTML Template (to support padding + full bleed body)
        temp_footer_path = None
        if footer_config:
            import os
            
            text = footer_config.get('text', '')
            show_pages = footer_config.get('show_pages', False)
            
            # Read Template
            footer_template_path = os.path.join(os.path.dirname(self.wkhtmltopdf_path).replace('bin', ''), '..', 'templates', 'footer_template.html') 
            # Note: We are in renderers/, so templates/ is ../templates
            # Better: use explicit path relative to Cwd
            
            base_dir = os.getcwd()
            template_path = os.path.join(base_dir, 'templates', 'footer_template.html')
            
            with open(template_path, 'r', encoding='utf-8') as f:
                template_str = f.read()
                
            # Simple String Replace (avoid jinja env overhead here or reuse if passed? String replace is fine for simple)
            rendered_footer = template_str.replace('{{ footer_text }}', text)
            rendered_footer = rendered_footer.replace('{{ display_pages_style }}', '' if show_pages else 'display: none;')
            
            # Save Temp Footer
            temp_footer_path = os.path.join(base_dir, 'temp_footer.html')
            with open(temp_footer_path, 'w', encoding='utf-8') as f:
                f.write(rendered_footer)
                
            options['footer-html'] = temp_footer_path
            options['footer-spacing'] = '5'
        
        try:
            pdfkit.from_string(html_content, output_path, configuration=self.config, options=options)
            print(f"Saved PDF to: {output_path}")
        except OSError as e:
            print(f"Error generating PDF: {e}")
            print("Make sure wkhtmltopdf is installed and the path is correct.")
        finally:
            # Cleanup
            if temp_footer_path and os.path.exists(temp_footer_path):
                try:
                    os.remove(temp_footer_path)
                except:
                    pass
