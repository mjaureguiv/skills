# Pendo Analytics Skill

A Claude Code skill that answers any question about Pendo analytics integration in SAP Signavio products.

## What It Does

Invoke `/pendo` to get instant, expert answers on:

| Topic | Example Questions |
|-------|-----------------|
| **Setup & Configuration** | "How do I add Pendo to my app?" / "What config params does enableUXAnalytics need?" |
| **Event Tracking** | "How do I track a file upload event?" / "When should I use trackPendo vs. feature tagging?" |
| **Feature Tagging** | "What's the difference between auto-tagging and VDS?" / "How do I set up auto-tagging?" |
| **CSS Selectors** | "What selector should I use for a button?" / "Why should I avoid nth-child selectors?" |
| **Naming Conventions** | "How should I name a page called 'Process Explorer'?" |
| **Metadata** | "What visitor data does Pendo receive?" |
| **Analytics Tools** | "How do I build a funnel report?" / "What is PES?" |
| **Cookie Consent** | "Does Pendo use third-party cookies?" / "How does TrustArc work with Pendo?" |
| **Contacts & Resources** | "Who do I contact for a Pendo API key?" / "Where is the analytics playbook?" |

## Usage

```
/pendo How do I set up Pendo in an app that doesn't use the Global Header?
/pendo Show me the trackPendo code example
/pendo What metadata does Pendo collect about users?
/pendo When do I use Funnels vs. Paths?
```

## Knowledge Coverage

All content is embedded in the skill — no external calls required.

Knowledge sourced from 9 internal SAP wiki pages (April 2026):
- SIGAVENGERS: Main Pendo integration guide
- PRODEX: Pendo Analytics Playbook
- SIGDS: UX Analytics Kit technical docs, TrustArc guides, metadata reference, Q&A, best practices
- SPG: Pendo Tracking Selectors standard

## Contact

Contact `agnel.joby@sap.com` with questions about the Pendo integration itself.

## Version

`1.0.0` — Ported from [signavio-knowledge-hub](https://github.tools.sap/signavio/signavio-knowledge-hub) (April 2026). Knowledge covers 10 domains from 9 SAP wiki pages.

## Changelog

| Date | Contributor | Change |
|------|-------------|--------|
| 2026-04-02 | Marvin Schoenwaelder | Initial port from signavio-knowledge-hub skills/pendo |
