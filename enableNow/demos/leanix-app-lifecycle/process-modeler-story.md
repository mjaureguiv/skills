# LeanIX Application Lifecycle Check - Demo Story

## Cover Page

**Feature**: Workflow action: SAP LeanIX application lifecycle status in workflow

### Key Improvements:
- Stops blind approvals by exposing lifecycle risks early
- Prevent designs based on expired or soon-to-expire applications
- Reduce rework by catching issues before the approval moves forward

### Personas

**Process Modeler - Maria Chen**
> Maria is responsible for creating and maintaining accurate and comprehensive process models and documentation. She works with various business units to document their processes and ensures they get proper approval before publishing.

**Head of Process Excellence - David Martinez**
> David is responsible for establishing and promoting best practices in business process management across the organization. His objective is to improve process efficiency, effectiveness, and consistency across the enterprise. He oversees multiple process improvement initiatives and must balance governance rigor with operational speed.

---

## Demo Story: Process Modeler Perspective

**Persona**: Process Modeler
**Name**: Maria Chen
**Feature**: LeanIX Application Lifecycle Status Integration
**Scenario**: Submitting a process for approval when it contains deprecated applications

---

## Screenshot 1: Viewing the Process Diagram
**Screen**: Process Collaboration Hub - Diagram View
**Status**: Published, Approval: Rejected

**Bubble Text**:
> "Maria just finished updating the 'Develop Go-to-Market tactics' process. She notices the approval status shows 'Rejected' from a previous submission. Time to review the diagram and submit it for approval again."

---

## Screenshot 2: Opening the Context Menu
**Screen**: Process Collaboration Hub - Context Menu
**Action**: Right-click menu showing options

**Bubble Text**:
> "Maria clicks the menu to submit this process for approval. She sees options like 'Edit with QuickModel', 'Export to PDF', and there it is - 'Submit for approval'."

---

## Screenshot 3: Approval Dialog - Selecting Workflow
**Screen**: Approval Dialog - Choose workflow dropdown
**Action**: Clicking the workflow dropdown

**Bubble Text**:
> "The approval dialog appears. Maria needs to select which approval workflow to use. She clicks on 'Choose workflow' to see the available options."

---

## Screenshot 4: Selecting the LeanIX Lifecycle Check Workflow
**Screen**: Approval Dialog - Workflow dropdown expanded
**Action**: Selecting "Demo: approval leanix applications lifecycle check"

**Bubble Text**:
> "Perfect! Maria can see several approval workflows available. She selects 'Demo: approval leanix applications lifecycle check' - this workflow automatically validates that all IT applications in her process are still supported."

---

## Screenshot 5: Confirming the Approval Submission
**Screen**: Approval Dialog - Ready to confirm
**Action**: About to click "Confirm"

**Bubble Text**:
> "Maria has selected the right workflow and her process is shown in the selection. She clicks 'Confirm' to start the approval process. The system will automatically check if any applications in her process are being phased out."

---

## Screenshot 6: Approval Case Created in Process Governance
**Screen**: Process Governance - Case History
**Status**: Approval case created, Status: Open

**Bubble Text**:
> "Great! The approval case has been created. Maria can see in the History that 'Check Model information' was created and she started the approval. There's a task waiting called 'Check Model information'."

---

## Screenshot 7: Viewing the Approval Case Tasks
**Screen**: Process Governance - Case properties and Tasks
**Action**: Viewing task list

**Bubble Text**:
> "The case shows Maria's details as the initiator, and the status is 'Open'. She can see there's one task - 'Check Model information' - that was created today. She clicks on it to see what needs to be done."

---

## Screenshot 8: Task Details - Check Model Information
**Screen**: Task overview - Check Model information
**Action**: Viewing task assignment

**Bubble Text**:
> "This task is unassigned and requires someone to 'Take this task' to complete it. Maria can see the Model ID and Model name are pre-filled. As the process owner, she takes this task to proceed with the review."

---

## Screenshot 9: Completing the Model Information Check
**Screen**: Task - Ready to complete
**Action**: About to click "Done"

**Bubble Text**:
> "Maria has reviewed the model information - the Model ID, Model name, and Revision ID all look correct. She clicks 'Done' to complete this first task and move to the next step of the approval workflow."

---

## Screenshot 10: First Task Completed
**Screen**: Task completed confirmation
**Status**: Task successfully completed

**Bubble Text**:
> "The task was completed successfully! Maria sees the green checkmark next to 'Check Model information'. Now there's a new task - 'Check LeanIX results' - this is where the system checks for deprecated applications."

---

## Screenshot 11: New Task - Check LeanIX Results (Assignment)
**Screen**: Check LeanIX results - Assignment view
**Action**: Taking the new task

**Bubble Text**:
> "A new task appeared - 'Check LeanIX results'. This is where the magic happens! The workflow has automatically queried LeanIX to check the lifecycle status of applications used in Maria's process. She takes this task to see the results."

---

## Screenshot 12: LeanIX Results - Invalid Applications Found!
**Screen**: Check LeanIX results - Task details
**Status**: Invalid Applications Found: Yes

**Bubble Text**:
> "Uh oh! The automated check found a problem. 'Invalid Applications Found' shows 'Yes' - specifically 'SAP ERP 6.0 (ECC) / SAP CO' with a lifecycle date of 2022-05-01. This application has reached end-of-life and shouldn't be used in new processes!"

---

## Screenshot 13: Confirming the LeanIX Validation
**Screen**: Check LeanIX results - Completion view
**Action**: About to click "Done"

**Bubble Text**:
> "Maria has reviewed the LeanIX validation results. The system clearly shows which application is problematic and when it reached its lifecycle end date. There's even a link to the Dictionary entry for more details. She completes this task to proceed."

---

## Screenshot 14: Workflow Complete - Auto-Rejected
**Screen**: Process Collaboration Hub - Final status
**Status**: Approval: Rejected

**Bubble Text**:
> "The approval workflow is complete, but Maria's process was **auto-rejected** because it uses a deprecated application. The status shows 'Approval: Rejected'. Now she knows she needs to update her process to use a supported IT system before it can be published. This saved the team from deploying a process that relies on unsupported technology!"

---

## Story Summary

**The Problem Solved**: Maria, a Process Modeler, unknowingly included a deprecated IT application (SAP ERP 6.0 ECC) in her business process.

**The Value**:
- The LeanIX integration automatically detected the deprecated application during the approval workflow
- The process was automatically rejected, preventing the deployment of processes using unsupported systems
- Clear feedback was provided showing exactly which application is problematic and when it reached end-of-life
- Maria now knows to update the process with a supported alternative

**Personas Involved**:
1. **Process Modeler** (Maria - this demo) - Submits process, receives feedback
2. **Head of Process Excellence** - Could be the approver who reviews rejected processes
3. **Enterprise Architect** - Maintains the LeanIX data and application lifecycle information
