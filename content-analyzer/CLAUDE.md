# Content Analyzer - AI Instructions

## Purpose

Transform document materials into well-structured, easy-to-understand presentations.

## Workflow

### 1. Read Input Materials

- Check `skills/content-analyzer/inputs/` for uploaded documents
- Support formats: PDF, Word, text, markdown, etc.
- Read and understand the full content

### 2. Analyze & Structure Content

Extract and organize:
- **Key themes** - Main topics and messages
- **Core insights** - Important findings or takeaways
- **Supporting data** - Statistics, facts, evidence
- **Logical flow** - Natural progression of ideas

### 3. Design Presentation Structure

Create a clear narrative:
1. **Title slide** - Topic and context
2. **Agenda/Overview** - What will be covered
3. **Content sections** - Organized by theme (3-5 slides each)
4. **Key takeaways** - Summary of main points
5. **Next steps/Call to action** (if applicable)

### 4. Content Transformation Rules

- **Simplify** - Break complex ideas into digestible chunks
- **Visualize** - Suggest charts, diagrams, or icons where helpful
- **Highlight** - Emphasize key messages and data points
- **Limit text** - Max 5-6 bullet points per slide, short phrases

### 5. Generate Output

- Use the PowerPoint skill to create the presentation
- Save to `skills/content-analyzer/outputs/`
- Name format: `[topic]_presentation_[date].pptx`

## Output Quality Standards

- Each slide has ONE clear message
- Consistent formatting throughout
- Logical flow between slides
- Executive-friendly language
- Action-oriented conclusions

## File Locations

| Type | Path |
|------|------|
| Input materials | `skills/content-analyzer/inputs/` |
| Output presentations | `skills/content-analyzer/outputs/` |
| Working files | `skills/content-analyzer/temp/` |
