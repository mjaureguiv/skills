# SPG Customer FAQ

Common questions and answers for SPG (SAP Signavio Process Governance).

**Official docs:** https://help.sap.com/docs/signavio-process-governance

---

## Entry Format

```markdown
### Q: [Question]
**Answer:** [Answer text]
**JIRA:** [Ticket if related to a feature/fix]
**Docs:** [Link to specific help page]
```

---

## Workflow & Approvals

### Q: How do I set up an approval workflow?
**Answer:**
1. Navigate to Administration > Workflows
2. Click "Create New Workflow"
3. Define the approval stages and assignees
4. Set conditions for when the workflow triggers
5. Activate the workflow

**Docs:** [Workflow Configuration](https://help.sap.com/docs/signavio-process-governance)

---

### Q: Can I have multiple approval levels?
**Answer:** Yes, SPG supports multi-level approvals. You can configure sequential or parallel approval stages in the workflow designer.

---

## Notifications & Emails

### Q: Can I customize notification emails?
**Answer:** Yes, go to Settings > Notifications > Templates. You can customize:
- Email subject
- Body content (Markdown supported)
- Recipients

---

### Q: Why aren't notification emails being sent?
**Answer:** Check the following:
1. Email server configuration in Administration
2. User email addresses are correct
3. Notification preferences are enabled for the user
4. Check spam/junk folders

---

## Process Governance General

### Q: What's the difference between a case and a subprocess?
**Answer:**
- **Case**: A single instance of a process (e.g., one employee onboarding)
- **Subprocess**: A reusable process that can be called from other processes

---

### Q: How do I export process data?
**Answer:**
1. Go to the process list
2. Select the processes to export
3. Click Export > Choose format (Excel, PDF, or JSON)

Note: Large exports may need to be done in batches.

---

## Integrations

### Q: Can SPG integrate with SAP SuccessFactors?
**Answer:** Yes, SPG offers standard connectors for SAP SuccessFactors. Contact your SAP representative for setup guidance.

---

### Q: Is there an API for custom integrations?
**Answer:** Yes, SPG provides REST APIs for:
- Process management
- Case operations
- User management
- Reporting

API documentation is available in the SAP API Business Hub.

---

## Add New FAQs Below

<!-- Add new Q&A entries following the format above -->
