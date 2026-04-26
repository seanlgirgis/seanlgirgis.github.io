# Learning Page Generator Rules

You generate complete HTML learning pages for:
https://seanlgirgis.github.io/learning/

Owner: Sean Girgis - Senior Data Engineer.

## Output goal

Create one complete, self-contained HTML file for a senior data engineer interview-prep learning page.

## Page structure

Every page must include:

1. Exact site CSS from `learning/_page-template.html`
2. Top nav
3. H1 and subtitle
4. 5-8 tags
5. Audio box only
6. Two-column table of contents
7. 8-10 content sections
8. Interview Q&A section with exactly 6 Q&A pairs
9. Quick Reference section with 10-16 rows
10. Closing HTML tags

Do not add:
- Further Reading
- Summary
- Placeholder content
- Video blocks

## Content standard

Write for senior data engineers:
- Production-oriented
- Interview-focused
- Concise and scannable
- Explain tradeoffs, failure modes, scale limits, and AWS/data-stack connections
- Prefer tight paragraphs over broad tutorials
- Use `.hi` for key insights
- Use `.warn` for production gotchas
- Use tables for comparisons
- Use code/config blocks only when useful

## Size limits

- 8-10 content sections
- No section over 4 short paragraphs
- No code block over 30 lines
- No table over 8 rows
- Q&A answers: 3-5 sentences
- Cheat sheet: 10-16 useful rows only

## Encoding rules

Save as UTF-8.

Use HTML entities for non-ASCII UI glyphs:
- `&middot;`
- `&uarr;`
- `&larr;`
- `&nbsp;`
- `&#127911;`
- `&amp;`

Reject mojibake:
- `â`
- `Ã`
- `ï`
- `Â`
- `ð`
- `â€`
- `â€™`
- `â€œ`

## CSS contract

Use the CSS exactly as stored in:
`learning/_page-template.html`

Do not modify:
- Colors
- Class names
- Layout
- `.cheat-row { grid-template-columns:170px 1fr; }`

## File rules

Write the page to:

`learning/{slug}.html`

Also print:
- Save instructions
- Verification commands
- Final completion line

Final completion line format:

`PAGE COMPLETE - {slug}.html - [N] sections - 6 QA pairs - [N] cheat rows - audio src confirmed`
