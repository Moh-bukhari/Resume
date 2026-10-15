#!/usr/bin/env bash
# Compile a standalone resume and check that its PDF is one page with selectable text.
set -euo pipefail

if [[ $# -ne 1 || ${1:-} == --help || ${1:-} == -h ]]; then
    printf 'Usage: %s path/to/resume.tex\nRequires: pdflatex, pdfinfo, pdftotext.\n' "$0"
    if [[ $# -eq 1 ]]; then exit 0; else exit 2; fi
fi

for command_name in pdflatex pdfinfo pdftotext; do
    if ! command -v "$command_name" >/dev/null 2>&1; then
        printf 'Missing required command: %s. Install the local TeX/PDF tools or compile in Overleaf.\n' "$command_name" >&2
        exit 1
    fi
done

script_dir=${BASH_SOURCE[0]%/*}
repo_root=$(cd -- "$script_dir/.." && pwd -P)
tex_path=$1
if [[ $tex_path != /* ]]; then tex_path=$PWD/$tex_path; fi
if [[ ! -f $tex_path || $tex_path != *.tex ]]; then
    printf 'Expected an existing .tex source file: %s\n' "$1" >&2
    exit 2
fi
source_dir=${tex_path%/*}
source_name=${tex_path##*/}
stem=${source_name%.tex}
output_dir=$repo_root/build/$stem
mkdir -p -- "$output_dir"

# Work beside the source so its relative \input and image paths continue to work.
cd -- "$source_dir"
for pass in 1 2; do
    printf 'Compiling pass %s: %s\n' "$pass" "$source_name"
    pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error -file-line-error \
        "-output-directory=$output_dir" "-jobname=$stem" "./$source_name" \
        | tee "$output_dir/compile-pass-$pass.txt"
done

pdf_path=$output_dir/$stem.pdf
text_path=$output_dir/$stem.txt
page_count=$(LC_ALL=C pdfinfo "$pdf_path" | awk '/^Pages:/ {print $2}')
if [[ $page_count != 1 ]]; then
    printf 'Resume must be one page; produced %s pages: %s\n' "${page_count:-unknown}" "$pdf_path" >&2
    exit 1
fi
pdftotext -layout "$pdf_path" "$text_path"
if ! LC_ALL=C grep -q '[^[:space:]]' "$text_path"; then
    printf 'PDF has no extractable text: %s\n' "$pdf_path" >&2
    exit 1
fi
if grep -n 'Overfull \\[hv]box' "$output_dir/$stem.log"; then
    printf 'Layout warning: inspect the overfull boxes above before using this resume.\n' >&2
fi
printf 'Verified one page with extractable text: %s\n' "$pdf_path"
printf 'Inspect the PDF visually before submitting it. Text extraction: %s\n' "$text_path"
