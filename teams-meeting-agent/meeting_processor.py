"""
Live Meeting Agent - Core Processing Logic

This module provides the core functionality for the live meeting agent including:
- Meeting state management
- Message processing and classification
- Note-taking and action item extraction
- Jira ticket proposal generation

Usage:
    from meeting_processor import LiveMeetingAgent

    agent = LiveMeetingAgent(meeting_id="19:...", platform='teams')
    await agent.start_monitoring()
"""

import json
import asyncio
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Optional, Any
import re

# Configuration
POLLING_INTERVAL = 5  # seconds between chat checks
MIN_CONFIDENCE = 0.7  # minimum confidence to respond to questions
MEETING_END_IDLE_TIME = 600  # 10 minutes of no activity = meeting ended

class MeetingContext:
    """Manages meeting context and state."""

    def __init__(self, meeting_id: str, meeting_title: str, platform: str):
        self.meeting_id = meeting_id
        self.meeting_title = meeting_title
        self.platform = platform
        self.start_time = datetime.now(timezone.utc)
        self.participants = set()
        self.current_topic = None
        self.recent_messages = []

    def add_participant(self, name: str):
        """Add a participant to the meeting."""
        self.participants.add(name)

    def set_topic(self, topic: str):
        """Update the current discussion topic."""
        self.current_topic = topic

    def add_message(self, message: Dict[str, Any]):
        """Add a message to recent history (keep last 20)."""
        self.recent_messages.append(message)
        if len(self.recent_messages) > 20:
            self.recent_messages.pop(0)

    def to_dict(self) -> Dict[str, Any]:
        """Convert context to dictionary for serialization."""
        return {
            "meeting_id": self.meeting_id,
            "meeting_title": self.meeting_title,
            "platform": self.platform,
            "start_time": self.start_time.isoformat(),
            "participants": list(self.participants),
            "current_topic": self.current_topic,
            "recent_messages": self.recent_messages[-10:]  # Keep last 10 for context
        }


class MeetingNotes:
    """Manages structured meeting notes."""

    def __init__(self):
        self.key_decisions = []
        self.action_items = []
        self.discussion_topics = {}
        self.qa_exchanges = []

    def add_decision(self, decision: str, timestamp: datetime):
        """Add a key decision made during the meeting."""
        self.key_decisions.append({
            "decision": decision,
            "timestamp": timestamp.isoformat()
        })

    def add_action_item(self, task: str, owner: str, deadline: Optional[str] = None):
        """Add an action item with owner and deadline."""
        self.action_items.append({
            "task": task,
            "owner": owner,
            "deadline": deadline,
            "status": "Pending"
        })

    def add_discussion(self, topic: str, summary: str):
        """Add or update a discussion topic."""
        if topic not in self.discussion_topics:
            self.discussion_topics[topic] = []
        self.discussion_topics[topic].append(summary)

    def add_qa(self, question: str, answer: str, asker: str):
        """Add a Q&A exchange."""
        self.qa_exchanges.append({
            "question": question,
            "answer": answer,
            "asker": asker,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })

    def to_dict(self) -> Dict[str, Any]:
        """Convert notes to dictionary for serialization."""
        return {
            "key_decisions": self.key_decisions,
            "action_items": self.action_items,
            "discussion_topics": self.discussion_topics,
            "qa_exchanges": self.qa_exchanges
        }


class MessageClassifier:
    """Classifies messages into categories (question, decision, action item, etc.)."""

    # Patterns for detecting different message types
    QUESTION_PATTERNS = [
        r'\?$',  # Ends with question mark
        r'^(what|who|when|where|why|how|can|could|would|should|is|are|do|does)',  # Question words
        r'@agent',  # Directly addresses agent
    ]

    DECISION_PATTERNS = [
        r'(let\'s|lets) (go with|do|proceed)',
        r'we\'ll|we will',
        r'agreed|agree',
        r'decision:',
        r'we decided',
        r'going with',
    ]

    ACTION_ITEM_PATTERNS = [
        r'(\w+) will',
        r'(\w+),? can you',
        r'(\w+),? could you',
        r'action item:',
        r'todo:',
        r'(by|before|deadline) \d',  # Contains deadline
    ]

    @staticmethod
    def is_question(message: str) -> bool:
        """Determine if message is a question."""
        message_lower = message.lower().strip()
        for pattern in MessageClassifier.QUESTION_PATTERNS:
            if re.search(pattern, message_lower, re.IGNORECASE):
                return True
        return False

    @staticmethod
    def is_decision(message: str) -> bool:
        """Determine if message indicates a decision."""
        message_lower = message.lower().strip()
        for pattern in MessageClassifier.DECISION_PATTERNS:
            if re.search(pattern, message_lower, re.IGNORECASE):
                return True
        return False

    @staticmethod
    def is_action_item(message: str) -> bool:
        """Determine if message contains an action item."""
        message_lower = message.lower().strip()
        for pattern in MessageClassifier.ACTION_ITEM_PATTERNS:
            if re.search(pattern, message_lower, re.IGNORECASE):
                return True
        return False

    @staticmethod
    def extract_action_details(message: str) -> Dict[str, Optional[str]]:
        """Extract owner and deadline from action item message."""
        # Try to extract owner (name before "will" or after addressing pattern)
        owner_match = re.search(r'(\w+)\s+(will|can you|could you)', message, re.IGNORECASE)
        owner = owner_match.group(1) if owner_match else None

        # Try to extract deadline
        deadline_match = re.search(r'(by|before|deadline|due)\s+(\w+\s+\d+|\d{4}-\d{2}-\d{2})', message, re.IGNORECASE)
        deadline = deadline_match.group(2) if deadline_match else None

        return {"owner": owner, "deadline": deadline}


class LiveMeetingAgent:
    """Main agent class for monitoring and interacting with live meetings."""

    def __init__(self, meeting_id: str, meeting_title: str = "Untitled Meeting", platform: str = 'teams'):
        self.meeting_id = meeting_id
        self.platform = platform
        self.context = MeetingContext(meeting_id, meeting_title, platform)
        self.notes = MeetingNotes()
        self.classifier = MessageClassifier()
        self.is_monitoring = False
        self.last_message_timestamp = None

        # Temp file for persistence
        self.temp_dir = Path(__file__).parent / "temp"
        self.temp_dir.mkdir(exist_ok=True)
        self.state_file = self.temp_dir / f"active-meeting-{meeting_id[:8]}.json"

    async def start_monitoring(self):
        """Begin monitoring the meeting chat."""
        self.is_monitoring = True
        print(f"✅ Now monitoring '{self.context.meeting_title}' ({self.platform})")
        print(f"💡 I'll answer questions and take notes.")

        try:
            while self.is_monitoring:
                # Poll for new messages
                # Note: This requires Teams MCP tools to be extended with:
                # - teams_monitor_chat(chat_id, since_timestamp)
                # For now, this is a placeholder showing the intended flow

                # Check if meeting has ended (no activity for MEETING_END_IDLE_TIME)
                if self._should_end_meeting():
                    await self.finalize_meeting()
                    break

                # Save state periodically
                self._save_state()

                # Wait before next poll
                await asyncio.sleep(POLLING_INTERVAL)

        except KeyboardInterrupt:
            print("\n⚠️ Monitoring interrupted by user")
            await self.finalize_meeting()

    def stop_monitoring(self):
        """Stop monitoring the meeting."""
        self.is_monitoring = False

    async def process_message(self, message: Dict[str, Any]):
        """Process a new message from the meeting chat."""
        content = message.get('content', '')
        sender = message.get('from', {}).get('name', 'Unknown')
        timestamp = datetime.fromisoformat(message.get('createdDateTime', datetime.now(timezone.utc).isoformat()))

        # Add sender to participants
        self.context.add_participant(sender)

        # Add to recent messages
        self.context.add_message(message)

        # Update last message timestamp
        self.last_message_timestamp = timestamp

        # Classify and process message
        if self.classifier.is_question(content):
            await self._handle_question(content, sender)

        if self.classifier.is_decision(content):
            self.notes.add_decision(content, timestamp)

        if self.classifier.is_action_item(content):
            details = self.classifier.extract_action_details(content)
            self.notes.add_action_item(
                task=content,
                owner=details.get('owner') or sender,
                deadline=details.get('deadline')
            )

    async def _handle_question(self, question: str, asker: str):
        """Handle a question asked in the meeting chat."""
        # TODO: This would integrate with Claude API to generate response
        # For now, just log that a question was detected
        print(f"❓ Question from {asker}: {question}")

        # Placeholder for response generation
        # response = await self.generate_response(question)
        # confidence = response.get('confidence', 0)
        #
        # if confidence >= MIN_CONFIDENCE:
        #     await self.send_chat_message(response['answer'])
        #     self.notes.add_qa(question, response['answer'], asker)

    async def generate_response(self, question: str) -> Dict[str, Any]:
        """Generate AI response to a question (placeholder)."""
        # TODO: Implement Claude API integration
        # This would:
        # 1. Load company context files
        # 2. Load meeting context
        # 3. Search previous meeting notes
        # 4. Generate response using Claude
        # 5. Return response with confidence score
        return {
            "answer": "Response placeholder",
            "confidence": 0.5
        }

    async def send_chat_message(self, content: str):
        """Send a message to the meeting chat (placeholder)."""
        # TODO: Implement Teams MCP integration
        # teams_send_message(chat_id=self.meeting_id, content=content)
        print(f"💬 Agent response: {content}")

    def _should_end_meeting(self) -> bool:
        """Determine if meeting should be considered ended."""
        if self.last_message_timestamp is None:
            return False

        idle_time = (datetime.now(timezone.utc) - self.last_message_timestamp).total_seconds()
        return idle_time >= MEETING_END_IDLE_TIME

    async def finalize_meeting(self):
        """Generate final meeting notes and clean up."""
        print("\n📝 Finalizing meeting notes...")

        # Generate structured notes
        notes_content = self._generate_meeting_notes()

        # Save to drafts/
        drafts_dir = Path(__file__).parent.parent.parent / "drafts"
        drafts_dir.mkdir(exist_ok=True)

        date_str = datetime.now().strftime("%Y-%m-%d")
        title_slug = self.context.meeting_title.lower().replace(" ", "-")[:30]
        notes_file = drafts_dir / f"meeting-notes-{date_str}-{title_slug}.md"

        with open(notes_file, 'w') as f:
            f.write(notes_content)

        print(f"✅ Meeting notes saved: {notes_file}")

        # Propose Jira tickets if action items exist
        if self.notes.action_items:
            self._propose_jira_tickets()

        # Clean up temp file
        if self.state_file.exists():
            self.state_file.unlink()

        self.stop_monitoring()

    def _generate_meeting_notes(self) -> str:
        """Generate structured meeting notes in markdown format."""
        notes = [
            f"# Meeting Notes: {self.context.meeting_title}",
            "",
            f"**Date**: {datetime.now().strftime('%Y-%m-%d')}",
            f"**Time**: {self.context.start_time.strftime('%H:%M')} - {datetime.now().strftime('%H:%M')}",
            f"**Platform**: {self.platform.title()}",
            f"**Participants**: {', '.join(sorted(self.context.participants))}",
            "",
            "## Summary",
            "",
            "[Auto-generated summary would go here]",
            "",
        ]

        # Key Decisions
        if self.notes.key_decisions:
            notes.append("## Key Decisions")
            notes.append("")
            for decision in self.notes.key_decisions:
                notes.append(f"- {decision['decision']}")
            notes.append("")

        # Action Items
        if self.notes.action_items:
            notes.append("## Action Items")
            notes.append("")
            notes.append("| Item | Owner | Deadline | Status |")
            notes.append("|------|-------|----------|--------|")
            for item in self.notes.action_items:
                notes.append(f"| {item['task'][:50]} | {item['owner']} | {item['deadline'] or 'TBD'} | {item['status']} |")
            notes.append("")

        # Discussion Topics
        if self.notes.discussion_topics:
            notes.append("## Discussion Notes")
            notes.append("")
            for topic, summaries in self.notes.discussion_topics.items():
                notes.append(f"### {topic}")
                for summary in summaries:
                    notes.append(f"- {summary}")
                notes.append("")

        # Q&A Exchanges
        if self.notes.qa_exchanges:
            notes.append("## Q&A from Chat")
            notes.append("")
            for qa in self.notes.qa_exchanges:
                notes.append(f"**Q** ({qa['asker']}): {qa['question']}")
                notes.append(f"**A**: {qa['answer']}")
                notes.append("")

        notes.append("---")
        notes.append(f"*Notes generated by Live Meeting Agent*")
        notes.append(f"*Meeting ID: {self.meeting_id}*")

        return "\n".join(notes)

    def _propose_jira_tickets(self):
        """Propose Jira tickets for action items (requires user approval)."""
        print("\n📋 Proposed Jira Tickets:")
        print(f"({len(self.notes.action_items)} action items found)\n")

        for i, item in enumerate(self.notes.action_items, 1):
            print(f"{i}. **{item['task'][:60]}**")
            print(f"   - Owner: {item['owner']}")
            if item['deadline']:
                print(f"   - Deadline: {item['deadline']}")
            print()

        print("---")
        print("Would you like to create these Jira tickets?")
        print("- **Yes** - Create all tickets")
        print("- **Edit** - Modify before creating")
        print("- **No** - Skip ticket creation")
        print("\n⚠️ Awaiting your approval to create tickets...")

    def _save_state(self):
        """Save current meeting state to temp file."""
        state = {
            "context": self.context.to_dict(),
            "notes": self.notes.to_dict(),
            "last_updated": datetime.now(timezone.utc).isoformat()
        }

        with open(self.state_file, 'w') as f:
            json.dump(state, f, indent=2)

    def load_state(self):
        """Load meeting state from temp file if exists."""
        if self.state_file.exists():
            with open(self.state_file, 'r') as f:
                state = json.load(f)
            # TODO: Restore context and notes from state
            print(f"📂 Loaded previous meeting state")


# Example usage (for testing)
if __name__ == "__main__":
    async def test_agent():
        agent = LiveMeetingAgent(
            meeting_id="19:test-meeting-id",
            meeting_title="Product Planning Sync",
            platform='teams'
        )

        # Simulate some messages
        await agent.process_message({
            "content": "Let's go with the mobile-first approach",
            "from": {"name": "Alice"},
            "createdDateTime": datetime.now(timezone.utc).isoformat()
        })

        await agent.process_message({
            "content": "Bob will finalize the roadmap by March 1st",
            "from": {"name": "Charlie"},
            "createdDateTime": datetime.now(timezone.utc).isoformat()
        })

        await agent.process_message({
            "content": "What were our Q1 priorities?",
            "from": {"name": "Alice"},
            "createdDateTime": datetime.now(timezone.utc).isoformat()
        })

        # Finalize meeting
        await agent.finalize_meeting()

    # Run test
    asyncio.run(test_agent())
