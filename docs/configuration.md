# Configuration & Content Strategy

## Overview
To avoid duplicating text between the Resume (2 pages) and the CV (extended), this project uses a **Decentralized Content Strategy**.

## The Data Store (`data/store.yaml`)
This file is the **Single Source of Truth**. It contains all the text content for your professional history.
- **Format**: YAML
- **Structure**: A flat list of keys, e.g., `exp_citi_job`, `education_masters`, `skill_list`.

**Example:**
```yaml
exp_citi_job:
  title: "Professional Experience"
  items:
    - left_text: "CITI"
      right_text: "2017 - Present"
      details:
        - "Built ML pipelines..."
```

## Layout Files
These files define **structure**, not content. They reference the store using `content_key`.

| File | Purpose |
|------|---------|
| `data/resume_pdf.yaml` | Structure for Resume PDF/HTML |
| `data/resume_docx.yaml` | Structure for Resume Word Doc |
| `data/cv_pdf.yaml` | Structure for CV PDF/HTML |
| `data/cv_docx.yaml` | Structure for CV Word Doc |

**Example Layout Entry:**
```yaml
sections:
  - type: list_block
    config:
      content_key: "exp_citi_job"  <-- Pulls from store.yaml
      title_style: "accented"
```

## Global Styling (`config/style.yaml`)
Defines the visual theme across all formats.
- **Typography**: Font sizes for PDF, Word, and Web.
- **Colors**: `primary_color` (Headers), `accent_color` (Stripes/Underlines).
- **Margins**: Page margins for printing.

## Adding Content
1.  **Add text** to `data/store.yaml` under a new key.
2.  **Reference the key** in the appropriate `*_pdf.yaml` and `*_docx.yaml` files.
3.  **Regenerate** using `generate.py`.
