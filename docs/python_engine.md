# Python Generation Engine Documentation

## Overview
The core of this project is a Python-based build system that generates the Resume and CV in multiple formats (HTML, PDF, DOCX, Markdown) from a single set of YAML data files.

**Entry Point**: `generate.py`

## The Build Process
When you run `python generate.py --target resume`, the following steps occur:

1.  **Load Configuration**:
    - `config/style.yaml`: Global styles (colors, fonts).
    - `data/store.yaml`: The centralized content database (jobs, skills, education).
    - `data/resume.yaml`: The layout configuration for the Resume.

2.  **Resolve Content**:
    - The engine parses `resume.yaml`.
    - It replaces any `content_key` references with actual data from `store.yaml`.
    - This allows `resume.yaml` and `cv.yaml` to share the exact same text data.

3.  **Render Output**:
    - **HTML**: `renderers/html_renderer.py` uses Jinja2 templates (`templates/base.html`) to create `components/resume.html` and `resume.html`.
    - **PDF**: `renderers/pdf_renderer.py` uses `wkhtmltopdf` to convert the generated HTML into a PDF. It applies print-specific logic (e.g., margins, footers).
    - **DOCX**: `renderers/docx_renderer.py` uses `python-docx` to build a native Word document. It manually calculates column widths and table layouts to match the visual design of the PDF.
    - **Markdown**: `renderers/md_renderer.py` converts the structured data into a clean Markdown file.

## Key Files

### `generate.py`
The orchestrator. It parses CLI arguments, loads YAML files, and calls the appropriate renderers.

### `renderers/html_renderer.py`
Generates the web version.
- **Dynamic CSS**: It injects CSS variables from `style.yaml` (e.g., Primary Color) into the HTML.
- **Templates**: Uses `templates/base.html` to define the structure.
- **Logic**: Handles "accented" headers and timeline layouts.

### `renderers/docx_renderer.py`
Generates the Word version.
- **No Templates**: Builds the DOCX from scratch using Python code.
- **Table Layouts**: Experience sections are rendered as unbordered tables with a 75%/25% split.
- **Styling**: Manually applies shading for "Pills" and colors for headers to match the web design.

### `renderers/pdf_renderer.py`
Generates the PDF version.
- **Wrapper**: It wraps the functionality of `wkhtmltopdf`.
- **Formatting**: It ensures page size is Letter and handles footers (page numbers).
