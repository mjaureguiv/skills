# Raw Insights and Grouping Rationale

## Full List of Raw Insights (Pre-deduplication)

1. Customer1 confused by license structure, lost deal to IBM Blueworks (simpler licensing)
2. Customer2 wants to remove Hub User License without deleting user data; requests concurrent licensing
3. Customer3 wants export of user list with license type and last login, including invited/not-accepted users, scheduled monthly
4. Customer4 requests export of all users, licenses, and groups as Excel (manual process now, GDPR risk)
5. Customer5 requests updated license names across all systems for clarity and consistency
6. Tenant owner not modeling, but must have paid license; want to allocate only needed users
7. Customer10 wants audience view to reflect access rights level
8. Telstra script: remove SPG licenses from users with no open tasks, assign license before workflow
9. Removing licenses via API not possible; must be manual
10. Customer11 requests automatic revocation of access/licenses for inactive users (Access Lifecycle Management)
11. SPG: want to identify inactive users and remove licenses automatically, prefer BTP for large user sets
12. Customers want ability to export list of all Enterprise license holders
13. Feature request: generate list of users and their licenses in Process Manager or Collaboration Hub
14. Messe Frankfurt: report to show which users have which license in tenant/workspace
15. Customer wants license detail info added to User/Group assignment report
16. Customers want usage report: user name/email, licenses assigned, last access date, to optimize license distribution and adoption
17. (repeat) Customers want usage report: user name/email, licenses assigned, last access date, to optimize license distribution and adoption
18. (repeat) Customers want usage report: user name/email, licenses assigned, last access date, to optimize license distribution and adoption
19. Split workflow licenses in user management into accelerator and collaborator; lack of overview by category
20. Customer wants report showing date license assigned to user
21. Request for report differentiating licenses (list of users and assigned license) to find invalid user IDs
22. (repeat) Split workflow licenses in user management into accelerator and collaborator; lack of overview by category
23. Need to understand license counting for Process Collaborator and Process Governance; only one type shown in admin
24. Workflow accelerator/collaborator technically same, but contractually different; customers want distinction in UI/admin
25. Customer Essity: workflow collaborator should not be marketed as license if only pricing/branding; want setup and assignment distinction
26. Remove workflow collaborator access to Workflow Accelerator
27. (background) No technical difference between licenses, but customers want admin distinction and contract compliance

## Grouping Rationale

### License Usage Reporting Dashboard (Insights 3, 4, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22)
- All these insights request some form of reporting/export on users, licenses, assignments, usage, or license details. Many are repeated or phrased differently but fundamentally ask for visibility and exportability of license data.

### License Inventory & Assignment Tracker (Insights 2, 6, 7, 23, 24, 25, 26, 27)
- These insights focus on tracking who has which license, the ability to manage assignments, and clarity on license types (especially where technical and contractual definitions differ). Several are about the confusion or lack of distinction in the UI/admin.

### Automated License Lifecycle Management (Insights 8, 9, 10, 11)
- These insights request automation for assigning/removing licenses based on user activity or workflow, including scripts, lifecycle management, and API support.

### HR/Identity System Integration (none explicit, but implied in automation and lifecycle management)
- While not directly stated, several automation requests imply the need for integration with external systems for user/license management.

### License Change Audit Logging (none explicit, but implied in requests for tracking and compliance)
- Some requests for compliance and contract adherence imply the need for audit logs, though not directly stated.

### Self-Service License Request Portal (none explicit)
- Not directly requested, but could be inferred as a solution to several manual pain points.

### External & Temporary User Management (Insight 2, 6)
- Requests for managing users who rarely log in or are not core users, without deleting their data or wasting licenses.

### Confusion over License Types and Entitlements (Insights 1, 5, 23, 24, 25, 27)
- Multiple insights highlight confusion about what each license means, naming conventions, and the need for clarity in communication and UI.

## Summary
Many insights overlap or are repeated, especially around reporting, license assignment clarity, and automation. Grouping is based on the core user need or pain point, not just the literal request text.
