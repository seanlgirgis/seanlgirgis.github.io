class MdRenderer:
    def __init__(self, theme):
        self.theme = theme
        self.output = []

    def render(self, content_data):
        self.output = [] # Reset
        
        # 1. Sections
        for section in content_data.get('sections', []):
            block_type = section.get('type')
            config = section.get('config', {})
            
            if config.get('page_break_before'):
                self.output.append("\n---\n") # Horizontal Rule as Page Break
            
            if block_type == 'header_block':
                self.render_header_block(config)
            elif block_type == 'section_title_block':
                self.render_section_title_block(config)
            elif block_type == 'compound_text_block':
                self.render_compound_text_block(config)
            elif block_type == 'text_block':
                self.render_text_block(config)
            elif block_type == 'grid_block':
                self.render_grid_block(config)
            elif block_type == 'list_block':
                self.render_list_block(config)
            elif block_type == 'plain_list_block':
                self.render_plain_list_block(config)
            elif block_type == 'compact_list_block':
                self.render_compact_list_block(config)
            elif block_type == 'text_grid_block':
                self.render_text_grid_block(config)
            elif block_type == 'project_block':
                self.render_project_block(config)
            elif block_type == 'stripe_block':
                pass # Ignore stripe in Markdown
            else:
                pass # Unknown

        return "\n".join(self.output)

    def save(self, content, output_path):
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Saved MD to: {output_path}")

    # --- BLOCK RENDERERS ---

    def render_header_block(self, config):
        title = config.get('title', '')
        self.output.append(f"# {title}")
        
        subtitle = config.get('subtitle')
        if subtitle:
            self.output.append(f"**{subtitle}**\n")

    def render_section_title_block(self, config):
        title = config.get('content', '')
        self.output.append(f"## {title}")

    def render_compound_text_block(self, config):
        # Center aligned usually, but MD is just text.
        # We will join them with the separator.
        items = config.get('items', [])
        separator = config.get('separator', ' • ')
        
        line_parts = []
        for item in items:
            text = item.get('text', '')
            link = item.get('link')
            if link:
                line_parts.append(f"[{text}]({link})")
            else:
                line_parts.append(text)
        
        self.output.append(" ".join(line_parts) + "\n")

    def render_text_block(self, config):
        content = config.get('content', '')
        style = config.get('style', 'normal')
        
        if style == 'shaded':
            # Use blockquote for shaded
            lines = content.split('\n')
            for line in lines:
                if line.strip():
                    self.output.append(f"> {line}")
            self.output.append("")
        else:
            self.output.append(content + "\n")

    def render_grid_block(self, config):
        # 2-Column Grid. MD Tables or just Header/Content?
        # Let's use simple Header/Content sequence for readability in raw markdown,
        # as complex grid tables in MD can be messy to read.
        
        if config.get('title'):
            self.output.append(f"## {config.get('title')}")
            
        items = config.get('items', [])
        for item in items:
            header = item.get('header')
            if header:
                self.output.append(f"### {header}")
            
            content_list = item.get('content', [])
            for line in content_list:
                self.output.append(f"- {line}")
        self.output.append("")

    def render_list_block(self, config):
        title = config.get('title')
        if title:
            self.output.append(f"## {title}")
            
        items = config.get('items', [])
        for item in items:
            # Reconstruct "Title | Date"
            left = item.get('left_text')
            right = item.get('right_text')
            
            header_line = ""
            if left: header_line += f"**{left}**"
            if left and right: header_line += " | "
            if right: header_line += f"*{right}*"
            
            if header_line:
                self.output.append(f"\n{header_line}")
                
            sub = item.get('sub_text')
            if sub:
                self.output.append(f"_{sub}_")
                
            for detail in item.get('details', []):
                self.output.append(f"- {detail}")
        self.output.append("")

    def render_plain_list_block(self, config):
        title = config.get('title')
        if title:
            self.output.append(f"## {title}")

        items = config.get('items', [])
        for item in items:
            self.output.append(f"- {item}")
        self.output.append("")

    def render_compact_list_block(self, config):
        title = config.get('title')
        if title:
            self.output.append(f"## {title}")
            
        items = config.get('items', [])
        for item in items:
            content = item.get('content', '')
            date = item.get('date', '')
            self.output.append(f"- {content} (*{date}*)")
        self.output.append("")

    def render_text_grid_block(self, config):
        # Similar to grid but just paragraphs
        if config.get('title'):
            self.output.append(f"## {config.get('title')}")
            
        items = config.get('items', [])
        for item in items:
            for line in item.get('content', []):
                self.output.append(line)
            self.output.append("")
        self.output.append("")

    def render_project_block(self, config):
        title = config.get('title', '')
        if title:
            # Using H3 or Bold? H3 seems appropriate for a project
            self.output.append(f"### {title}")
            
        # Tags
        tags = config.get('tags', [])
        if tags:
            # Render tags as `Code` style
            tag_str = " ".join([f"`{t}`" for t in tags])
            self.output.append(tag_str + "\n")
            
        # Items
        items = config.get('items', [])
        for item in items:
             self.output.append(f"- {item}")
        self.output.append("")
