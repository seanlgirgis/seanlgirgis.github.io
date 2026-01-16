# Manual Resume Editing Guide

This guide explains how to manually control the resume generation process using the Python-based generator in this project.

## 1. The Core Files (What you edit)

To make persistent changes that work with the generator script [generate.py](file:///c:/pyproj/seanlgirgis.github.io/generate.py), you should edit the following YAML files.

### A. For Layout & Structure (Moving Sections)
If you want to move sections around or add page breaks:
*   **Resume (Word):** [c:\pyproj\seanlgirgis.github.io\data\resume_docx.yaml](file:///c:/pyproj/seanlgirgis.github.io/data/resume_docx.yaml)
*   **CV (Word):** [c:\pyproj\seanlgirgis.github.io\data\cv_docx.yaml](file:///c:/pyproj/seanlgirgis.github.io/data/cv_docx.yaml)

**Common Actions:**
*   **Move a Block:** Cut the entire `- type: ...` block and paste it where you want it.
*   **Add Page Break:** Insert this block where you want the break:
    ```yaml
    - type: header_block
      config:
        page_break_before: true
    ```

### B. For Content (Text, Bullets, Jobs)
The content is "decentralized" in the store. You edit the text here, and it updates all resumes (Word, PDF, HTML) automatically.
*   **File:** [c:\pyproj\seanlgirgis.github.io\data\store.yaml](file:///c:/pyproj/seanlgirgis.github.io/data/store.yaml)
*   **Example:** To edit Citi experience, find `exp_citi_consultant` in this file and edit the `details` list.

### C. For Styling (Fonts, Margins)
*   **File:** [c:\pyproj\seanlgirgis.github.io\config\style.yaml](file:///c:/pyproj/seanlgirgis.github.io/config/style.yaml)
*   **To change Word Font Size:** Edit the `theme.typography.docx` section:
    ```yaml
    docx:
      font_size_base: 10   # Body text
      font_size_h1: 14     # Main Headers
    ```

## 2. The Generator Code (How it works)
The Python script reads your YAMLs and builds the DOCX file.
*   **Orchestrator:** [generate.py](file:///c:/pyproj/seanlgirgis.github.io/generate.py) (Runs the whole show).
*   **Word Logic:** [renderers/docx_renderer.py](file:///c:/pyproj/seanlgirgis.github.io/renderers/docx_renderer.py).
    *   This file contains the logic for *how* a [project_block](file:///c:/pyproj/seanlgirgis.github.io/renderers/docx_renderer.py#1123-1244) or [list_block](file:///c:/pyproj/seanlgirgis.github.io/renderers/docx_renderer.py#607-674) is drawn in Word (tables, borders, shading).
    *   Edit this only if you want to change the fundamental *design* (e.g., change the shaded box to a double border).

## 3. How to Regenerate
After editing the YAMLs, run this command in your terminal (PowerShell):
```powershell
& "c:\py_venv\resume_venv\Scripts\python.exe" generate.py --target resume --format docx
```
*Note: Ensure [resume.docx](file:///C:/pyproj/seanlgirgis.github.io/resume.docx) is closed before running this commands.*

## 4. Manual Word Editing (The Alternative)
If you prefer not to use the generator:
1.  Open [resume.docx](file:///C:/pyproj/seanlgirgis.github.io/resume.docx) in Microsoft Word.
2.  Edit it manually like any other document.
3.  **Warning:** If you run [generate.py](file:///c:/pyproj/seanlgirgis.github.io/generate.py) again, it will **overwrite** your manual changes. Save your manual version with a different name (e.g., `resume_manual.docx`) if you want to keep it safe.

## 5. Controlling White Space (Advanced)
If you need to squeeze more content onto a page, "White Space" comes from two places:

### A. Global Margins (The Frame)
Controls the edge of the page.
*   **File:** [c:\pyproj\seanlgirgis.github.io\config\style.yaml](file:///c:/pyproj/seanlgirgis.github.io/config/style.yaml)
*   **Action:** Edit `theme.margins` (in millimeters).
    ```yaml
    margins:
      top: 6.35      # 0.25 inch -> Try 5.0 for tighter top
      bottom: 6.35   
    ```

### B. Spacing Between Blocks (The Gaps)
Controls the space *between* paragraphs and headers.
*   **File:** [config/style.yaml](file:///c:/pyproj/seanlgirgis.github.io/config/style.yaml)
*   **Action:** Edit the `spacing` section.
    *   **Word:** Edit values under `spacing.docx` (in Points).
    *   **PDF:** Edit values under `spacing.pdf` (e.g., "15px").
    *   **Web:** Edit values under `spacing.web` (e.g., "20px").
    
    ```yaml
    spacing:
      docx:
        block_after: 12      # Space after major sections (Word)
        header_after: 6      # Space after headers
    ```


