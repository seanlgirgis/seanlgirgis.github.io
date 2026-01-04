I have created a Capability Matrix (data/test_matrix.yaml) that comprehensively tests every supported specific component type and configuration option.

I have generated output files for this matrix in all 4 formats so you can side-by-side compare the capabilities:

DOCX: output_matrix.docx
PDF: output_matrix.pdf
HTML: output_matrix.html
Markdown: output_matrix.md
This proves that:

Blue Stripe: Shows in DOCX/PDF/HTML, but gracefully omitted in MD.
Shaded Blocks: Have accent borders in DOCX/PDF/HTML, become Blockquotes in MD.
Grids: Render as columns in rich formats, and sequential sections in MD.
Page Breaks: Function in DOCX/PDF, represented as horizontal rules (---) in MD.
You can verify the specific capabilities by opening these files.