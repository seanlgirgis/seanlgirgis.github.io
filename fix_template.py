
import os

content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title | default('Resume') }}</title>
    <style>
{{ css_content | safe }}
    </style>
</head>
<body>
    {% if theme.stripe.enabled %}
    <div class="page-stripe"></div>
    {% endif %}

    {% for section in sections %}
    {% if section.type == 'header_block' %}
    <div class="header-block">
        <center>
            <h1 style="text-align: center;">{{ section.config.title }}</h1>
            {% if section.config.subtitle %}
            <p class="subtitle" style="text-align: center;">{{ section.config.subtitle }}</p>
            {% endif %}
        </center>
    </div>
    {% elif section.type == 'compound_text_block' %}
    <div class="compound-text-block" style="text-align: {{ section.config.font_alignment | default('center') }}">
        <center>
            {% for item in section.config['items'] %}
            {% if not loop.first %}
            <span class="compound-separator" style="font-size: {{ section.config.font_size }}pt;">{{ section.config.separator }}</span>
            {% endif %}
            <span class="compound-item">
                {% if item.link %}
                <a href="{{ item.link }}" style="font-size: {{ section.config.font_size }}pt; color: {{ item.resolved_color }};">{{ item.text }}</a>
                {% else %}
                <span style="font-size: {{ section.config.font_size }}pt; color: {{ item.resolved_color }};">{{ item.text }}</span>
                {% endif %}
            </span>
            {% endfor %}
        </center>
        <div style="height: 20px; width: 100%; clear: both;"></div>
    </div>
    {% elif section.type == 'text_block' %}
    <div class="text-block {{ section.config.style }}">
        {{ section.config.content | markdown | safe }}
    </div>
    {% elif section.type == 'grid_block' %}
    <div class="grid-section-wrapper {% if section.config.style == 'shaded' %}shaded-border{% endif %}">
        <h2 class="section-title {% if section.config.title_style == 'accented' %}accented{% endif %}"><span>{{ section.config.title }}</span></h2>
        {# Float-based grid for wkhtmltopdf compatibility #}
        {% set cols = section.config.columns | default(3) | int %}
        {% set width = '48%' if cols == 2 else '30%' %}
        {% set margin_right = '4%' if cols == 2 else '5%' %}
        
        <div class="grid-block" style="overflow: hidden; width: 100%;">
            {% for col in section.config['items'] %}
            {% set is_last_in_row = (loop.index % cols) == 0 %}
            <div class="grid-column" style="float: left; width: {{ width }}; margin-bottom: 20px; box-sizing: border-box; {% if not is_last_in_row %}margin-right: {{ margin_right }};{% endif %}">
                {% if col.header %}
                <h3 style="color: {{ theme.primary_color }}; font-size: 1.1em; margin-bottom: 10px;">{{ col.header }}</h3>
                {% endif %}
                <ul style="padding-left: 20px; list-style-type: disc;">
                    {% for line in col.content %}
                    <li>{{ line | markdown | safe }}</li>
                    {% endfor %}
                </ul>
            </div>
            {% endfor %}
        </div>
        <div style="clear: both;"></div>
    </div>
    {% elif section.type == 'list_block' %}
    <h2 class="section-title {% if section.config.title_style == 'accented' %}accented{% endif %}"><span>{{ section.config.title }}</span></h2>
    <div class="list-block {{ section.config.style }}">
        {% for item in section.config['items'] %}
        <div class="list-item" style="margin-bottom: 15px;">
            {% if item.left_text or item.right_text %}
            <div class="item-header" style="overflow: hidden; margin-bottom: 2px;">
                <h3 style="float: left; margin: 0; font-size: 1.1em;">{{ item.left_text }}</h3>
                <span style="float: right; color: {{ theme.accent_color }}; font-weight: bold;">{{ item.right_text }}</span>
            </div>
            {% endif %}
            {% if item.sub_text %}
            <div class="item-sub" style="font-style: italic; color: #666; margin-bottom: 5px;">{{ item.sub_text }}</div>
            {% endif %}
            <ul style="padding-left: 20px; margin-top: 5px;">
                {% for detail in item.details %}
                <li>{{ detail | markdown | safe }}</li>
                {% endfor %}
            </ul>
        </div>
        {% endfor %}
    </div>
    {% elif section.type == 'plain_list_block' %}
    <h2 class="section-title {% if section.config.title_style == 'accented' %}accented{% endif %}"><span>{{ section.config.title }}</span></h2>
    <div class="plain-list-block" style="margin-bottom: 20px;">
        {% for item in section.config['items'] %}
        <div class="plain-item" style="margin-bottom: 5px;">
            {{ item | markdown | safe }}
        </div>
        {% endfor %}
    </div>
    {% elif section.type == 'compact_list_block' %}
    <h2 class="section-title {% if section.config.title_style == 'accented' %}accented{% endif %}"><span>{{ section.config.title }}</span></h2>
    <div class="compact-list-block" style="margin-bottom: 20px;">
        {% for item in section.config['items'] %}
        <div class="compact-item" style="overflow: hidden; padding-bottom: 5px; margin-bottom: 5px; border-bottom: 1px dotted #ccc;">
            <div style="float: left; width: 80%;">
                 {{ item.content | markdown | safe }}
            </div>
            <div style="float: right; width: 18%; text-align: right; color: #000;">
                 {{ item.date }}
            </div>
        </div>
        {% endfor %}
    </div>
    {% elif section.type == 'text_grid_block' %}
    <div class="grid-section-wrapper">
        <h2 class="section-title {% if section.config.title_style == 'accented' %}accented{% endif %}"><span>{{ section.config.title }}</span></h2>
        
        {# Float-based grid reused from grid_block #}
        {% set cols = section.config.columns | default(2) | int %}
        {% set width = '48%' if cols == 2 else '30%' %}
        {% set margin_right = '4%' if cols == 2 else '5%' %}
        
        <div class="grid-block" style="overflow: hidden; width: 100%;">
            {% for col in section.config['items'] %}
            {% set is_last_in_row = (loop.index % cols) == 0 %}
            <div class="grid-column" style="float: left; width: {{ width }}; margin-bottom: 20px; box-sizing: border-box; {% if not is_last_in_row %}margin-right: {{ margin_right }};{% endif %}">
                {% for line in col.content %}
                <div style="margin-bottom: 10px;">{{ line | markdown | safe }}</div>
                {% endfor %}
            </div>
            {% endfor %}
        </div>
        <div style="clear: both;"></div>
    </div>
    {% endif %}
    {% endfor %}
</body>
</html>"""

with open('templates/base.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Wrote templates/base.html safely.")
