#!/usr/bin/env python3
"""
Transcript Pseudonymization for Decision Logging

Replaces real names with pseudonyms locally before LLM processing,
then restores original names after processing. This ensures personal
data never leaves the local environment.

Usage:
    from pseudonymize import pseudonymize_transcript, restore_names, cleanup_temp_files

    # Clean previous session files first
    cleanup_temp_files('skills/log-decision/temp')

    # Before LLM processing
    pseudo_text, mapping = pseudonymize_transcript(transcript)

    # After LLM processing
    final_text = restore_names(llm_output, mapping)
"""

import re
import json
import glob as glob_module
from pathlib import Path
from typing import Tuple
from datetime import datetime


# Pseudonym templates
PERSON_TEMPLATE = "Person_{}"  # Person_A, Person_B, etc.
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def extract_vtt_speakers(transcript: str) -> set[str]:
    """
    Extract speaker names from MS Teams VTT format.

    VTT format example:
        <v John Smith>I think we should...
        <v Jane Doe>I agree with...
    """
    # Pattern: <v Name>
    pattern = r'<v\s+([^>]+)>'
    matches = re.findall(pattern, transcript)
    return set(matches)


def extract_common_name_patterns(transcript: str) -> set[str]:
    """
    Extract names from common transcript patterns.

    Patterns detected:
        - "Name:" at start of line (speaker labels)
        - "@Name" mentions
        - "Name said", "Name mentioned", "Name suggested"
    """
    names = set()

    # Pattern: "Name:" at start of line (common transcript format)
    # Matches "John Smith:" or "John:" at line start
    speaker_pattern = r'^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s*:'
    for match in re.finditer(speaker_pattern, transcript, re.MULTILINE):
        names.add(match.group(1))

    # Pattern: @mentions
    mention_pattern = r'@([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)'
    for match in re.finditer(mention_pattern, transcript):
        names.add(match.group(1))

    # Pattern: "Name said/mentioned/suggested/asked/noted"
    action_pattern = r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s+(?:said|mentioned|suggested|asked|noted|agreed|disagreed|proposed|recommended)\b'
    for match in re.finditer(action_pattern, transcript):
        names.add(match.group(1))

    return names


def extract_all_names(transcript: str) -> set[str]:
    """
    Extract all detected names from transcript using multiple patterns.
    """
    names = set()

    # VTT speaker tags
    names.update(extract_vtt_speakers(transcript))

    # Common patterns
    names.update(extract_common_name_patterns(transcript))

    # Filter out common false positives
    false_positives = {
        'I', 'We', 'They', 'The', 'This', 'That', 'What', 'When', 'Where',
        'Why', 'How', 'Yes', 'No', 'Option', 'Decision', 'Action', 'Item',
        'Next', 'Step', 'Meeting', 'Team', 'Project', 'Monday', 'Tuesday',
        'Wednesday', 'Thursday', 'Friday', 'January', 'February', 'March',
        'April', 'May', 'June', 'July', 'August', 'September', 'October',
        'November', 'December'
    }
    names = {n for n in names if n not in false_positives}

    return names


def create_pseudonym_mapping(names: set[str]) -> dict[str, str]:
    """
    Create a mapping from real names to pseudonyms.

    Returns:
        Dict mapping real name -> pseudonym (e.g., "John Smith" -> "Person_A")
    """
    mapping = {}
    sorted_names = sorted(names)  # Sort for consistent ordering

    for i, name in enumerate(sorted_names):
        if i < len(ALPHABET):
            pseudonym = PERSON_TEMPLATE.format(ALPHABET[i])
        else:
            # For more than 26 names, use Person_AA, Person_AB, etc.
            first = ALPHABET[i // len(ALPHABET) - 1]
            second = ALPHABET[i % len(ALPHABET)]
            pseudonym = PERSON_TEMPLATE.format(f"{first}{second}")
        mapping[name] = pseudonym

    return mapping


def pseudonymize_transcript(transcript: str) -> Tuple[str, dict]:
    """
    Replace all detected names with pseudonyms.

    Args:
        transcript: Raw transcript text

    Returns:
        Tuple of (pseudonymized_text, mapping_dict)
        mapping_dict maps real names to pseudonyms for later restoration
    """
    # Extract all names
    names = extract_all_names(transcript)

    if not names:
        return transcript, {}

    # Create pseudonym mapping
    mapping = create_pseudonym_mapping(names)

    # Create reverse mapping for replacement (pseudonym -> real name)
    # We store this format for restoration later
    reverse_mapping = {v: k for k, v in mapping.items()}

    # Replace names in transcript
    # Sort by length (longest first) to avoid partial replacements
    pseudonymized = transcript
    for name in sorted(names, key=len, reverse=True):
        pseudonym = mapping[name]
        # Replace in VTT tags
        pseudonymized = re.sub(
            rf'<v\s+{re.escape(name)}>',
            f'<v {pseudonym}>',
            pseudonymized
        )
        # Replace in speaker labels (Name:)
        pseudonymized = re.sub(
            rf'^({re.escape(name)})\s*:',
            f'{pseudonym}:',
            pseudonymized,
            flags=re.MULTILINE
        )
        # Replace @mentions
        pseudonymized = re.sub(
            rf'@{re.escape(name)}\b',
            f'@{pseudonym}',
            pseudonymized
        )
        # Replace general occurrences (word boundary)
        pseudonymized = re.sub(
            rf'\b{re.escape(name)}\b',
            pseudonym,
            pseudonymized
        )

    return pseudonymized, reverse_mapping


def restore_names(text: str, mapping: dict) -> str:
    """
    Restore original names from pseudonyms.

    Args:
        text: Text with pseudonyms (e.g., LLM output)
        mapping: Dict mapping pseudonym -> real name

    Returns:
        Text with original names restored
    """
    if not mapping:
        return text

    restored = text
    # Sort by pseudonym length (longest first) to avoid partial replacements
    for pseudonym in sorted(mapping.keys(), key=len, reverse=True):
        real_name = mapping[pseudonym]
        restored = re.sub(
            rf'\b{re.escape(pseudonym)}\b',
            real_name,
            restored
        )

    return restored


def save_mapping(mapping: dict, filepath: Path) -> None:
    """Save mapping to JSON file for persistence."""
    with open(filepath, 'w') as f:
        json.dump(mapping, f, indent=2)


def load_mapping(filepath: Path) -> dict:
    """Load mapping from JSON file."""
    with open(filepath, 'r') as f:
        return json.load(f)


def cleanup_temp_files(temp_dir: str, keep_gitkeep: bool = True) -> list[str]:
    """
    Remove all temporary files from a directory to ensure session isolation.

    Args:
        temp_dir: Path to the temp directory
        keep_gitkeep: If True, preserve .gitkeep files (default True)

    Returns:
        List of files that were removed
    """
    temp_path = Path(temp_dir)
    removed = []

    if not temp_path.exists():
        return removed

    for file in temp_path.iterdir():
        if file.is_file():
            if keep_gitkeep and file.name == '.gitkeep':
                continue
            try:
                file.unlink()
                removed.append(str(file))
            except OSError as e:
                print(f"Warning: Could not remove {file}: {e}")

    return removed


def generate_session_id() -> str:
    """Generate a unique session ID based on current timestamp."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def get_session_files(temp_dir: str, session_id: str) -> dict[str, Path]:
    """
    Get paths for session-specific files.

    Args:
        temp_dir: Path to the temp directory
        session_id: Unique session identifier

    Returns:
        Dict with paths for 'raw', 'pseudo', and 'mapping' files
    """
    temp_path = Path(temp_dir)
    return {
        'raw': temp_path / f"session_{session_id}_raw.txt",
        'pseudo': temp_path / f"session_{session_id}_pseudo.txt",
        'mapping': temp_path / f"session_{session_id}_mapping.json"
    }


# CLI interface for testing
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python pseudonymize.py <transcript_file>     - Pseudonymize and show result")
        print("  python pseudonymize.py test                  - Run test with sample data")
        print("  python pseudonymize.py cleanup <temp_dir>    - Clean temp directory")
        sys.exit(1)

    if sys.argv[1] == "cleanup":
        if len(sys.argv) < 3:
            temp_dir = "skills/log-decision/temp"
        else:
            temp_dir = sys.argv[2]
        removed = cleanup_temp_files(temp_dir)
        if removed:
            print(f"Removed {len(removed)} file(s):")
            for f in removed:
                print(f"  - {f}")
        else:
            print("No files to remove.")
        sys.exit(0)

    if sys.argv[1] == "test":
        # Test with sample VTT transcript
        sample = """WEBVTT

00:00:05.000 --> 00:00:10.000
<v John Smith>I think we should go with option A for the API design.

00:00:10.500 --> 00:00:15.000
<v Jane Doe>I agree with John. Option A gives us better flexibility.

00:00:15.500 --> 00:00:20.000
<v Michael Johnson>What about the timeline? Jane mentioned we're tight on resources.

00:00:20.500 --> 00:00:25.000
<v John Smith>Good point Michael. Let's make the decision and assign @Jane Doe as owner.
"""
        print("=== Original Transcript ===")
        print(sample)
        print()

        pseudo, mapping = pseudonymize_transcript(sample)
        print("=== Pseudonymized Transcript ===")
        print(pseudo)
        print()

        print("=== Mapping (pseudonym -> real name) ===")
        print(json.dumps(mapping, indent=2))
        print()

        # Simulate LLM output
        llm_output = """
## Deciders
Person_A, Person_B, Person_C

## Decision
Person_A proposed option A for API design. Person_B agreed.
Person_C raised concerns about timeline.

## Owner
Person_B
"""
        print("=== Simulated LLM Output ===")
        print(llm_output)
        print()

        restored = restore_names(llm_output, mapping)
        print("=== Restored Output ===")
        print(restored)

    else:
        filepath = Path(sys.argv[1])
        if not filepath.exists():
            print(f"File not found: {filepath}")
            sys.exit(1)

        # Generate session ID for this run
        session_id = generate_session_id()
        print(f"Session ID: {session_id}")
        print()

        transcript = filepath.read_text()
        pseudo, mapping = pseudonymize_transcript(transcript)

        print("=== Detected Names ===")
        for pseudonym, real_name in mapping.items():
            print(f"  {real_name} -> {pseudonym}")
        print()

        print("=== Pseudonymized Transcript ===")
        print(pseudo)

        # Save mapping with session ID
        temp_dir = filepath.parent if 'temp' in str(filepath.parent) else Path("skills/log-decision/temp")
        session_files = get_session_files(str(temp_dir), session_id)

        save_mapping(mapping, session_files['mapping'])
        print(f"\nMapping saved to: {session_files['mapping']}")
        print(f"\nIMPORTANT: Use session ID '{session_id}' to reference these files.")
