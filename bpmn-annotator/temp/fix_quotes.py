"""
Fix ROADMAP_DATA block: rewrite with correct ASCII quotes.
All field-value delimiters must be ASCII U+0027, not curly quotes U+2018/U+2019.
Content apostrophes stay as U+2019 (safe inside ASCII-quoted JS strings).
"""
import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HTML_FILE = r'c:\Signavio_PM_Agent\docs\MxC\mxc-skills.html'

# The correct ROADMAP_DATA block — written with ASCII single quotes throughout,
# U+2019 used only in content (not as string delimiters), double quotes avoided in desc.
NEW_BLOCK = r"""// Sourced from Signavio ProductBoard — M&C-external-+-internal.csv export, 2026-05-05
// Teams: Process Guardians, Roots, Dictionary, The Sims, Process Pioneers, Process Vanguards, Kestrel
// To refresh: re-run skills/bpmn-annotator/temp/rebuild_from_csv.py against a new CSV export
const ROADMAP_DATA = [
  // ── Legacy Process Manager ──
  // NOW — in progress
  { name:'Variants and templates in the dictionary’s Used-in field', area:'Legacy Process Manager', status:'NOW', quarter:'Q2 2026', insightsCount:null, desc:'Display references to process variants and templates in the dictionary’s Used-in field, where dictionary entries are applied as dimension values — eliminating the need for manual cross-referencing.' },
  // NEXT — coming up
  { name:'Process owner attribute for template processes and variants', area:'Legacy Process Manager', status:'NEXT', quarter:'Q2 2026', insightsCount:null, desc:'Elevates Process Owner from an optional custom field to a standardized, system-level attribute — establishing a single source of truth for process accountability across the entire repository.' },
  { name:'Stable reference content ID in Signavio Diagrams', area:'Legacy Process Manager', status:'NEXT', quarter:'Q2 2026', insightsCount:null, desc:'Stable, release-independent IDs and metadata for SAP reference content so that integrations can reliably track and reference specific processes across releases.' },
  // LATER — horizon
  { name:'Advanced Approval Framework for Variant Management', area:'Legacy Process Manager', status:'LATER', quarter:null, insightsCount:2, desc:'A comprehensive approval framework to ensure every structural change to a variant group and any modification within a process variant aligns with global process standards.' },
  { name:'Notifications to the template process owner on variant changes', area:'Legacy Process Manager', status:'LATER', quarter:null, insightsCount:2, desc:'Real-time awareness of process evolution, closing the communication gap between central process owners and local variant managers.' },
  { name:'Search field for quick diagram selection in subprocess linking', area:'Legacy Process Manager', status:'LATER', quarter:null, insightsCount:6, desc:'Instantly find and link any process with a simple search, accelerating the modeling process and eliminating errors caused by manual browsing.' },
  { name:'Variant Management Reporting', area:'Legacy Process Manager', status:'LATER', quarter:null, insightsCount:null, desc:'Reporting capabilities for process variant landscapes — providing insights into variant distribution, template coverage, and change history across the organization.' },

  // ── Suite Repository ──
  // NOW — in progress
  { name:'Activity Log for Attribute Changes', area:'Suite Repository', status:'NOW', quarter:'Q2 2026', insightsCount:null, desc:'Comprehensive audit trail for attribute changes on Suite Repository assets — enabling process owners, compliance officers, and auditors to verify and document changes for regulatory requirements.' },
  { name:'Relationship Overview for Process Diagrams', area:'Suite Repository', status:'NOW', quarter:null, insightsCount:null, desc:'Visualize how process diagrams connect to other assets across the transformation landscape, providing organizations with clear visibility into change impact.' },
  { name:'Relationship Overview for Transformation Manager Objectives', area:'Suite Repository', status:'NOW', quarter:null, insightsCount:null, desc:'Visualize how Transformation Manager objectives connect to related assets, giving organizations visibility into how changes cascade across their transformation roadmap.' },
  // NEXT — coming up
  { name:'Suite Attributes: Reuse attributes across assets in Suite Repository', area:'Suite Repository', status:'NEXT', quarter:'Q2 2026', insightsCount:null, desc:'Define attributes once and reuse them consistently across domains and assets in Signavio Suite — minimizing duplication, ensuring consistency, and reducing maintenance overhead.' },
  // LATER — horizon
  { name:'Onboard Dictionary in Suite Repository', area:'Suite Repository', status:'LATER', quarter:null, insightsCount:null, desc:'Integrate the Signavio Dictionary into the unified Suite Repository experience, enabling consistent attribute management and cross-asset linking for glossary items.' },
  { name:'Process Documentation: New Templates Editor', area:'Suite Repository', status:'LATER', quarter:null, insightsCount:null, desc:'An intelligent, guided templates editor that bridges user-friendly design with enterprise requirements — enabling teams to create audit-ready, company-compliant process documentation.' },
  { name:'Simulation Enhancement: Link from Joule results to Simulation UI', area:'Suite Repository', status:'LATER', quarter:null, insightsCount:null, desc:'After Joule surfaces simulation metrics in conversation, users can click through directly to the full Simulation UI for detailed flow visualization and scenario analysis.' },
  { name:'Suite Attributes: Multi Language Support', area:'Suite Repository', status:'LATER', quarter:null, insightsCount:null, desc:'Introduce multi-language support for attributes to enable maintenance of attribute content in languages relevant for global customers.' },
  { name:'Suite Attributes: Rich Text Editor', area:'Suite Repository', status:'LATER', quarter:null, insightsCount:null, desc:'Rich text formatting options for multi-line text attribute values — supporting structure, emphasis, and links in process documentation attributes.' },

  // ── Process Modeler ──
  // NOW — in progress
  { name:'AI-assisted Modeler Canvas Assistant (Auto Suggestion & Text to Process)', area:'Process Modeler', status:'NOW', quarter:'Q2 2026', insightsCount:null, desc:'Enriching the process modeler experience with AI innovations: auto-suggestion of next steps while modeling and text-to-process generation directly on the modeling canvas.' },
  { name:'Admin-defined default diagram formats', area:'Process Modeler', status:'NOW', quarter:'Q2 2026', insightsCount:null, desc:'Admins can define workspace-level branding and default color palettes so all new diagrams start with consistent, company-aligned formatting.' },
  { name:'New Process Modeler (Beta)', area:'Process Modeler', status:'NOW', quarter:'Q2 2026', insightsCount:null, desc:'A modern, AI-powered BPMN modeling experience embedded natively in Collaboration Hub — enabling process modelers to create, edit, and manage professional diagrams with unprecedented speed and clarity.' },
  { name:'Shapes Modernization', area:'Process Modeler', status:'NOW', quarter:'Q2 2026', insightsCount:1, desc:'Modernized shape library for the new process modeler — clearer, more intuitive, and visually consistent business process elements that improve understanding and collaboration.' },
  { name:'Text to Process Integration', area:'Process Modeler', status:'NOW', quarter:null, insightsCount:3, desc:'Transform plain-text process descriptions into structured BPMN diagrams automatically — reducing manual modeling effort and accelerating process documentation for business users.' },
  // NEXT — coming up
  { name:'New Process Modeler (GA)', area:'Process Modeler', status:'NEXT', quarter:null, insightsCount:null, desc:'General availability release of the redesigned process modeler, bringing the complete modern modeling experience — including all AI capabilities and shapes — to all users.' },
  // LATER — horizon
  { name:'Admin Settings: Configure diagram subsets (stencil sets and perspectives)', area:'Process Modeler', status:'LATER', quarter:null, insightsCount:null, desc:'Configure which diagram types and diagram elements modelers can use across the workspace by managing stencil sets, extensions, and perspectives from a central admin panel.' },
  { name:'Diagram sharing for collaboration', area:'Process Modeler', status:'LATER', quarter:null, insightsCount:null, desc:'Share diagrams with colleagues for collaboration — supporting comment-only, edit, and read-only modes so the right people can contribute at the right level.' },
  { name:'View and edit modes in the new modeler', area:'Process Modeler', status:'LATER', quarter:null, insightsCount:null, desc:'Distinct view and edit modes on the NextGen Modeler canvas — protecting diagram integrity while allowing stakeholders to navigate and annotate without accidentally making changes.' },
];"""

# Verify: all string delimiters in NEW_BLOCK are ASCII (U+0027)
for line_no, line in enumerate(NEW_BLOCK.split('\n'), 1):
    if 'name:' in line or 'area:' in line or "status:'" in line:
        for i, ch in enumerate(line):
            if ord(ch) in (0x2018, 0x2019):
                ctx = line[max(0,i-10):i+10]
                print(f'WARNING: curly quote at line {line_no} col {i}: {repr(ctx)}')

with open(HTML_FILE, encoding='utf-8') as f:
    html = f.read()

# Find start and end of old block
start_marker = '// Sourced from Signavio ProductBoard'
end_marker = '];\n\n/* '
start = html.find(start_marker)
end   = html.find(end_marker, start) + 3  # include '];

if start < 0 or end < 3:
    print(f'ERROR: markers not found (start={start}, end={end})')
    sys.exit(1)

old_block = html[start:end]
print(f'Found old block: chars {start}-{end} ({len(old_block)} chars)')
print(f'Old block starts: {repr(old_block[:60])}')

new_html = html[:start] + NEW_BLOCK + '\n\n' + html[end:]
with open(HTML_FILE, 'w', encoding='utf-8') as f:
    f.write(new_html)
print('Written.')

# Verify
with open(HTML_FILE, encoding='utf-8') as f:
    html2 = f.read()
idx = html2.find('const ROADMAP_DATA = [')
close = html2.find('];', idx)
block = html2[idx+22:close]
now   = block.count("status:'NOW'")
nxt   = block.count("status:'NEXT'")
later = block.count("status:'LATER'")
print(f'Verify - NOW={now} NEXT={nxt} LATER={later} total={now+nxt+later}')
for area in ['Legacy Process Manager','Suite Repository','Process Modeler']:
    print(f'  {area}: {block.count(f"area:{chr(39)}{area}{chr(39)}")}')
