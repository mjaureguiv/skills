import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'c:\Signavio_PM_Agent\docs\MxC\mxc-skills.html', encoding='utf-8') as f:
    html = f.read()

# Chatbot script (last <script> block)
chat_start = html.rfind('<script>')
chat_end   = html.rfind('</script>')
chat_js    = html[chat_start:chat_end]
print(f'Chatbot script: {len(chat_js)} chars')
for arr in ['SKILLS_DATA', 'ROADMAP_DATA', 'FAQ_DATA']:
    n = chat_js.count(arr)
    print(f'  {arr}: {n} refs')

# Roadmap card render — find insightsCount conditional
print()
print('=== insightsCount render logic ===')
for m in re.finditer(r'insightsCount', html):
    line_start = html.rfind('\n', 0, m.start()) + 1
    line_end   = html.find('\n', m.start())
    line = html[line_start:line_end].strip()
    if 'PB' in line or 'insight' in line.lower() and ('?' in line or 'render' in line.lower()):
        print(line[:120])

# pb-badge render snippet
print()
print('=== pb-badge in card render ===')
idx = html.find('pbHtml')
if idx > 0:
    print(html[idx:idx+200].strip())

# lastUpdated and OG
print()
for m in re.finditer(r'(lastUpdated|og:description)', html):
    line_start = html.rfind('\n', 0, m.start()) + 1
    line_end   = html.find('\n', m.start())
    print(html[line_start:line_end].strip()[:120])
