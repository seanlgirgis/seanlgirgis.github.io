# Usage Guide

## Prerequisites
1.  **Python 3.10+**
2.  **wkhtmltopdf**: Must be installed and added to PATH (or path configured in `renderers/pdf_renderer.py`).
3.  **Dependencies**: Install via `pip install -r requirements.txt`.

## Generating Documents
Run the generation script from the root directory:

**Generate Resume (All formats)**
```bash
python generate.py --target resume
```
*Outputs: `resume.pdf`, `resume.docx`, `resume.md`, `components/resume.html`*

**Generate CV (All formats)**
```bash
python generate.py --target cv
```
*Outputs: `cv.pdf`, `cv.docx`, `cv.md`, `components/cv.html`*

## Local Development (Website)
To preview the website locally:
1.  Run a local Python server:
    ```bash
    python -m http.server 8000
    ```
2.  Open browser to `http://localhost:8000`.
3.  **Note**: If you make changes to JS/HTML, use **Ctrl+F5** to hard refresh and clear cache.

## Deployment
The site is hosted on GitHub Pages. To deploy changes:

1.  **Generate** fresh files (PDF/DOCX/HTML).
2.  **Commit** all changes, including the generated binary files.
    ```bash
    git add .
    git add -f resume.pdf resume.docx cv.pdf cv.docx
    git commit -m "Update content"
    ```
3.  **Push** to the main branch.
    ```bash
    git push origin main
    ```
