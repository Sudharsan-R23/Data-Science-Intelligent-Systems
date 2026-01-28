# How to Create PDF from Markdown Documents
## Guide for Academic Submission

---

## Method 1: Using Pandoc (Recommended)

### Installation

**Windows:**
```powershell
# Download from: https://pandoc.org/installing.html
# Or use chocolatey:
choco install pandoc
```

**Linux:**
```bash
sudo apt-get install pandoc texlive-latex-base
```

**macOS:**
```bash
brew install pandoc
```

### Conversion Command

```bash
# Basic conversion
pandoc docs/COMPLETE_PROJECT_DOCUMENT.md -o docs/COMPLETE_PROJECT_DOCUMENT.pdf

# With better formatting
pandoc docs/COMPLETE_PROJECT_DOCUMENT.md -o docs/COMPLETE_PROJECT_DOCUMENT.pdf \
  --pdf-engine=xelatex \
  -V geometry:margin=1in \
  -V fontsize=12pt \
  -V documentclass=article

# For all documents
pandoc docs/SRS/Software_Requirements_Specification.md -o docs/SRS/SRS.pdf
pandoc docs/Architecture/System_Architecture.md -o docs/Architecture/Architecture.pdf
pandoc docs/Reports/Project_Report.md -o docs/Reports/Project_Report.pdf
```

---

## Method 2: Using VS Code Extensions

### Step 1: Install Extension
1. Open VS Code
2. Go to Extensions (Ctrl+Shift+X)
3. Search for "Markdown PDF"
4. Install "Markdown PDF" by yzane

### Step 2: Convert to PDF
1. Open the markdown file
2. Right-click → "Markdown PDF: Export (pdf)"
3. PDF will be saved in same directory

### Alternative Extension: "Markdown Preview Enhanced"
- More features
- Better formatting options
- Export to PDF with custom styles

---

## Method 3: Using Online Converters

### Recommended Services:
1. **Markdown to PDF**: https://www.markdowntopdf.com/
2. **Dillinger**: https://dillinger.io/ (Export as PDF)
3. **StackEdit**: https://stackedit.io/ (Export as PDF)

### Steps:
1. Copy markdown content
2. Paste in online converter
3. Click "Export as PDF"
4. Download PDF

---

## Method 4: Using Python Script

### Install Dependencies
```bash
pip install markdown pdfkit
# Also need wkhtmltopdf: https://wkhtmltopdf.org/downloads.html
```

### Python Script
```python
import markdown
import pdfkit

# Read markdown
with open('docs/COMPLETE_PROJECT_DOCUMENT.md', 'r') as f:
    md_content = f.read()

# Convert to HTML
html = markdown.markdown(md_content)

# Convert to PDF
pdfkit.from_string(html, 'docs/COMPLETE_PROJECT_DOCUMENT.pdf')
```

---

## Method 5: Using Typora (Easiest)

### Steps:
1. Download Typora: https://typora.io/
2. Open markdown file in Typora
3. File → Export → PDF
4. Choose settings and export

**Advantages:**
- WYSIWYG editor
- Beautiful PDF output
- Customizable styles
- Easy to use

---

## Method 6: Using GitHub/GitLab

### Steps:
1. Push markdown files to GitHub/GitLab
2. View file in browser
3. Print → Save as PDF

**Note**: Basic formatting, but quick and easy

---

## Recommended PDF Settings

### For Academic Submission:

**Page Settings:**
- Size: A4
- Margins: 1 inch (2.54 cm)
- Font: Times New Roman or Arial
- Font Size: 12pt
- Line Spacing: 1.5 or Double

**Sections:**
- Page numbers
- Table of contents
- Headers/Footers with project title

### Pandoc Template Example:

```yaml
---
title: "Decision Support System for Healthcare Diagnosis"
author: "[Your Name]"
date: "January 2026"
geometry: margin=1in
fontsize: 12pt
documentclass: article
---

```

---

## Batch Conversion Script

### Windows PowerShell:
```powershell
# Convert all markdown files in docs folder
Get-ChildItem -Path docs -Recurse -Filter *.md | ForEach-Object {
    $pdfPath = $_.FullName -replace '\.md$', '.pdf'
    pandoc $_.FullName -o $pdfPath --pdf-engine=xelatex
}
```

### Linux/macOS Bash:
```bash
# Convert all markdown files
find docs -name "*.md" -type f | while read file; do
    pdf_file="${file%.md}.pdf"
    pandoc "$file" -o "$pdf_file" --pdf-engine=xelatex
done
```

---

## Troubleshooting

### Issue: Pandoc not found
**Solution**: Install pandoc and add to PATH

### Issue: Missing fonts
**Solution**: Install LaTeX distribution (TeX Live, MiKTeX)

### Issue: Formatting issues
**Solution**: Use custom CSS or LaTeX template

### Issue: Tables not rendering
**Solution**: Use HTML tables or LaTeX tables

---

## Best Practices

1. **Review Before Converting**: Check markdown formatting
2. **Use Consistent Styles**: Headers, lists, code blocks
3. **Add Page Breaks**: Use `\newpage` or `---` for page breaks
4. **Include Images**: Ensure image paths are correct
5. **Test Output**: Check PDF formatting before submission

---

## Quick Reference

| Method | Ease | Quality | Speed |
|--------|------|---------|-------|
| Pandoc | Medium | High | Fast |
| VS Code | Easy | Medium | Medium |
| Online | Easy | Low | Slow |
| Typora | Very Easy | High | Fast |
| Python | Medium | Medium | Medium |

**Recommendation**: Use **Pandoc** for best quality, or **Typora** for easiest use.

---

## Example Commands

```bash
# Main project document
pandoc docs/COMPLETE_PROJECT_DOCUMENT.md -o "Project_Document.pdf" \
  --pdf-engine=xelatex \
  -V geometry:margin=1in \
  -V fontsize=12pt

# SRS document
pandoc docs/SRS/Software_Requirements_Specification.md -o "SRS.pdf"

# Architecture document
pandoc docs/Architecture/System_Architecture.md -o "Architecture.pdf"

# Project report
pandoc docs/Reports/Project_Report.md -o "Project_Report.pdf"
```

---

**Happy Converting!** 📄
