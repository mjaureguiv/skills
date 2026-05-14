"""
Claude Productivity Dashboard
Flask app to analyze and display AI-assisted development productivity metrics.
"""

from flask import Flask, render_template, jsonify, request
import subprocess
import os
import re
from datetime import datetime
from pathlib import Path

app = Flask(__name__)

# Get the repository root (3 levels up from this file)
REPO_ROOT = Path(__file__).parent.parent.parent


def run_git_command(cmd, cwd=None):
    """Run a git command and return output."""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            cwd=cwd or REPO_ROOT
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Error: {e}"


def get_skills_and_scenarios():
    """Get list of all skills and scenarios in the repo."""
    items = []

    # Get skills
    skills_dir = REPO_ROOT / "skills"
    if skills_dir.exists():
        for item in skills_dir.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                items.append({
                    "name": item.name,
                    "type": "skill",
                    "path": f"skills/{item.name}"
                })

    # Get scenarios
    scenarios_dir = REPO_ROOT / "scenarios"
    if scenarios_dir.exists():
        for item in scenarios_dir.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                items.append({
                    "name": item.name,
                    "type": "scenario",
                    "path": f"scenarios/{item.name}"
                })

    return sorted(items, key=lambda x: (x["type"], x["name"]))


def analyze_folder(folder_path):
    """Analyze git history for a specific folder."""

    # Get all commits for this folder
    commits_cmd = f'git log --all --format="%H|%ai|%s" -- "{folder_path}/"'
    commits_output = run_git_command(commits_cmd)

    if not commits_output or "Error" in commits_output:
        return None

    commits = []
    total_lines_added = 0
    total_lines_deleted = 0

    for line in commits_output.strip().split('\n'):
        if not line:
            continue
        parts = line.split('|')
        if len(parts) >= 3:
            commit_hash = parts[0]
            timestamp = parts[1]
            message = '|'.join(parts[2:])  # Message might contain |

            # Get line stats for this commit
            stats_cmd = f'git show {commit_hash} --numstat --format="" -- "{folder_path}/"'
            stats_output = run_git_command(stats_cmd)

            added = 0
            deleted = 0
            for stat_line in stats_output.split('\n'):
                if stat_line and '\t' in stat_line:
                    parts = stat_line.split('\t')
                    if parts[0] != '-':
                        added += int(parts[0]) if parts[0].isdigit() else 0
                    if parts[1] != '-':
                        deleted += int(parts[1]) if parts[1].isdigit() else 0

            total_lines_added += added
            total_lines_deleted += deleted

            commits.append({
                "hash": commit_hash[:7],
                "timestamp": timestamp,
                "date": timestamp.split(' ')[0],
                "time": timestamp.split(' ')[1] if ' ' in timestamp else '',
                "message": message,
                "lines_added": added,
                "lines_deleted": deleted
            })

    if not commits:
        return None

    # Calculate metrics
    commits.reverse()  # Oldest first
    first_date = datetime.strptime(commits[0]["date"], "%Y-%m-%d")
    last_date = datetime.strptime(commits[-1]["date"], "%Y-%m-%d")
    calendar_days = (last_date - first_date).days + 1

    # Count distinct work sessions (unique days with commits)
    unique_days = len(set(c["date"] for c in commits))

    # Estimate AI coding time (based on lines written, ~100 lines/hour for AI)
    ai_hours = round(total_lines_added / 100, 1)

    # Estimate human time based on ACTUAL prompting effort:
    # - Each work session = ~1 hour of prompting/reviewing
    # - Plus ~5 minutes per commit for prompt refinement
    # This reflects real PM time, not AI output time
    human_hours = round(unique_days * 1.0 + len(commits) * 0.08, 1)

    # Traditional dev estimate (~50 lines/hour)
    traditional_hours = round(total_lines_added / 50, 1)

    # Productivity multiplier (traditional time / human prompting time)
    multiplier = round(traditional_hours / human_hours, 1) if human_hours > 0 else 0

    # Count current lines in folder
    current_lines = 0
    folder_full_path = REPO_ROOT / folder_path
    if folder_full_path.exists():
        for ext in ['*.py', '*.md', '*.html', '*.js', '*.css', '*.yaml', '*.yml', '*.json']:
            for f in folder_full_path.rglob(ext):
                try:
                    current_lines += len(f.read_text().split('\n'))
                except:
                    pass

    return {
        "folder_path": folder_path,
        "commits": commits,
        "total_commits": len(commits),
        "total_lines_added": total_lines_added,
        "total_lines_deleted": total_lines_deleted,
        "current_lines": current_lines,
        "first_date": commits[0]["date"],
        "last_date": commits[-1]["date"],
        "calendar_days": calendar_days,
        "ai_hours": ai_hours,
        "human_hours": human_hours,
        "traditional_hours": traditional_hours,
        "multiplier": multiplier
    }


@app.route('/')
def index():
    """Main dashboard page."""
    items = get_skills_and_scenarios()
    return render_template('dashboard.html', items=items)


@app.route('/api/items')
def api_items():
    """API endpoint to get all skills and scenarios."""
    return jsonify(get_skills_and_scenarios())


@app.route('/api/analyze')
def api_analyze():
    """API endpoint to analyze a specific folder."""
    folder_path = request.args.get('path', '')
    if not folder_path:
        return jsonify({"error": "No path provided"}), 400

    result = analyze_folder(folder_path)
    if not result:
        return jsonify({"error": "No commits found for this folder"}), 404

    return jsonify(result)


@app.route('/api/analyze-all')
def api_analyze_all():
    """API endpoint to analyze all skills and scenarios."""
    items = get_skills_and_scenarios()
    results = []

    for item in items:
        data = analyze_folder(item["path"])
        if data:
            results.append({
                "name": item["name"],
                "type": item["type"],
                "path": item["path"],
                "human_hours": data["human_hours"],
                "ai_hours": data["ai_hours"],
                "current_lines": data["current_lines"],
                "total_commits": data["total_commits"],
                "calendar_days": data["calendar_days"],
                "multiplier": data["multiplier"],
                "first_date": data["first_date"],
                "last_date": data["last_date"],
                "traditional_hours": data["traditional_hours"]
            })
        else:
            # Item with no commits
            results.append({
                "name": item["name"],
                "type": item["type"],
                "path": item["path"],
                "human_hours": 0,
                "ai_hours": 0,
                "current_lines": 0,
                "total_commits": 0,
                "calendar_days": 0,
                "multiplier": 0,
                "first_date": "-",
                "last_date": "-",
                "traditional_hours": 0
            })

    return jsonify(results)


@app.route('/api/global-stats')
def api_global_stats():
    """API endpoint to get global repository statistics."""
    # Get unique contributors
    contributors_cmd = 'git log --all --format="%ae" | sort | uniq'
    contributors_output = run_git_command(contributors_cmd)
    contributors = [c for c in contributors_output.split('\n') if c and '@' in c]
    unique_contributors = len(set(contributors))

    # Get date range of all commits
    first_commit_cmd = 'git log --all --reverse --format="%ai" | head -1'
    last_commit_cmd = 'git log --all --format="%ai" | head -1'
    first_commit_date = run_git_command(first_commit_cmd).split(' ')[0] if run_git_command(first_commit_cmd) else '-'
    last_commit_date = run_git_command(last_commit_cmd).split(' ')[0] if run_git_command(last_commit_cmd) else '-'

    # Calculate development period
    try:
        first_dt = datetime.strptime(first_commit_date, "%Y-%m-%d")
        last_dt = datetime.strptime(last_commit_date, "%Y-%m-%d")
        dev_days = (last_dt - first_dt).days + 1
        dev_weeks = round(dev_days / 7, 1)
    except:
        dev_days = 0
        dev_weeks = 0

    # Count skills and scenarios
    items = get_skills_and_scenarios()
    skills_count = len([i for i in items if i["type"] == "skill"])
    scenarios_count = len([i for i in items if i["type"] == "scenario"])

    # Get total commits
    total_commits_cmd = 'git rev-list --all --count'
    total_commits = int(run_git_command(total_commits_cmd) or 0)

    return jsonify({
        "unique_contributors": unique_contributors,
        "first_commit_date": first_commit_date,
        "last_commit_date": last_commit_date,
        "development_days": dev_days,
        "development_weeks": dev_weeks,
        "skills_count": skills_count,
        "scenarios_count": scenarios_count,
        "total_items": skills_count + scenarios_count,
        "total_commits": total_commits
    })


if __name__ == '__main__':
    print(f"Repository root: {REPO_ROOT}")
    print(f"Starting Claude Productivity Dashboard...")
    print(f"Open http://localhost:5050 in your browser")
    app.run(debug=True, port=5050)
