# Content Analyzer

Transforms document materials into well-structured, easy-to-understand presentations.

## Purpose

Takes complex documents, reports, or content materials and reorganizes them into clear, structured PowerPoint presentations that are easier to consume and present.

## Usage

1. Place your source materials (PDFs, Word docs, text files, etc.) in the `inputs/` folder
2. Ask Claude to analyze and convert the content into a presentation
3. Find your generated presentation in the `outputs/` folder

## Folder Structure

```
content-analyzer/
├── inputs/         # Upload your source materials here
├── outputs/        # Generated presentations appear here
├── temp/           # Working files (auto-cleaned)
├── CLAUDE.md       # AI instructions
└── README.md       # This file
```

## Example Prompts

- "Analyze the document in inputs/ and create a presentation"
- "Convert this report into a 10-slide presentation"
- "Create an executive summary presentation from the uploaded materials"

## Changelog

| Date | Contributor | Change |
|------|-------------|--------|
| 2026-03-05 | Claude | Initial skill creation |
