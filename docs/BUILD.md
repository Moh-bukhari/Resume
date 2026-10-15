# Build and review

For Overleaf, upload a complete standalone `.tex` file, select **pdfLaTeX**,
and set it as the main document. The template needs no external assets or API
credentials.

## Dependencies

Bank tools use Python 3's standard library. Local PDF builds need `pdflatex`,
`pdfinfo`, and `pdftotext`; `pdftoppm` helps visual review. There is no Node
build, app server, or Python dependency installation.

For a fresh Debian/Ubuntu machine, typical packages are:

```bash
sudo apt-get update
sudo apt-get install -y python3 texlive-latex-base texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended poppler-utils
```

Use the platform's supported installer when sudo is unavailable. Do not
reinstall working tools unnecessarily.

## Commands

From the repository root:

```bash
python3 scripts/check_bank.py
bash scripts/build_resume.sh templates/resume-base.tex
```

The helper compiles twice, preserves errors/warnings, checks for exactly one
page, and extracts text. Output goes under `build/<source-stem>/`, including
PDF, log, and text. For `resume.tex`, expect `build/resume/resume.pdf` and
`build/resume/resume.txt`. Different files named `resume.tex` share that folder;
build and copy them sequentially.

For a real application folder already created:

```bash
bash scripts/build_resume.sh applications/example-role/resume.tex
cp build/resume/resume.pdf applications/example-role/resume.pdf
```

Replace `example-role` with the actual application directory.

## Review

- Inspect extracted text for contact details, reading order, bullets, dates,
  symbols, and complete final lines. Extraction cannot certify every ATS.
- Visually inspect the PDF for clipping, overlap, awkward wraps, and tiny text.
  To make an image:
  `pdftoppm -scale-to 1600 -png -singlefile build/resume/resume.pdf build/resume/preview`.
- Check hyperlinks, chosen evidence, and a readable 10pt body. Cut weaker
  content before tightening margins/spacing. Avoid global scaling, `\tiny`,
  overlapping negative spacing, and columns to meet the page limit.
- Record actual checks in application notes; compilation alone does not
  establish factual accuracy or good layout.

## Common Overleaf failures

Paste raw LaTeX, not Markdown links or HTML entities. Use the complete template
with exactly one matching `\begin{document}` and `\end{document}`.
Escape ordinary-text `&`, `%`, `$`, `_`, `#`, `{`, and `}` as needed:
`\&`, `\%`, `\$`, `\_`, `\#`, `\{`, `\}`. Use `\href{URL}{label}` for links.
Keep the template's pdfLaTeX/font/Unicode setup. If content creates a second
page, shorten or remove lower-priority content and recompile.
