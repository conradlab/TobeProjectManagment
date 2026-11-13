#!/usr/bin/env python3
"""
update-weekly-issues.py

Maintenance script to sync curriculum/weeks/ files with GitHub Issues #2-#13.

This script allows curriculum content to live in Git (for versioning and review)
while being published to GitHub Issues for interactive student use.

Features:
- Dry-run mode to preview changes
- Preserves student progress (student-added checkboxes, comments)
- Back up existing Issue bodies before replacement
- Verify content after update
- Refuse to overwrite checked-off student tasks

Usage:
    python scripts/update-weekly-issues.py --dry-run
    python scripts/update-weekly-issues.py --update
    python scripts/update-weekly-issues.py --help
"""

import os
import sys
import json
import argparse
import subprocess
import hashlib
from pathlib import Path
from datetime import datetime

# Repository configuration
REPO = "conradlab/TobeProjectManagment"
WEEKS_DIR = Path("curriculum/weeks")
BACKUP_DIR = Path(".backups/issue-backups")
ISSUES_START = 2  # Issue #2 is Week 01


class IssueUpdater:
    """Manages synchronization of curriculum files with GitHub Issues."""
    
    def __init__(self, repo, dry_run=False):
        self.repo = repo
        self.dry_run = dry_run
        self.issues_updated = []
        self.issues_failed = []
        self.issues_skipped = []
        
    def get_issue_body(self, issue_num):
        """Fetch current Issue body from GitHub."""
        try:
            result = subprocess.run(
                ["gh", "issue", "view", str(issue_num), "--json", "body", "--jq", ".body"],
                cwd=self.repo if self.repo else ".",
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                print(f"✗ Failed to fetch Issue #{issue_num}: {result.stderr}")
                return None
        except subprocess.TimeoutExpired:
            print(f"✗ Timeout fetching Issue #{issue_num}")
            return None
        except Exception as e:
            print(f"✗ Error fetching Issue #{issue_num}: {e}")
            return None
    
    def has_checked_boxes(self, body):
        """Check if Issue contains checked student tasks."""
        if not body:
            return False
        # Look for checked boxes: [x] or [X]
        return "[x]" in body.lower() or "- [x]" in body.lower()
    
    def has_student_comments(self, issue_num):
        """Check if Issue has student-added comments."""
        try:
            result = subprocess.run(
                ["gh", "issue", "view", str(issue_num), "--json", "comments", "--jq", ".comments | length"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                count = int(result.stdout.strip() or 0)
                return count > 0
            return False
        except Exception:
            return False
    
    def backup_issue(self, issue_num, body):
        """Backup existing Issue body."""
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup_file = BACKUP_DIR / f"issue-{issue_num}-{timestamp}.md"
        try:
            with open(backup_file, "w") as f:
                f.write(f"# Backup of Issue #{issue_num}\n")
                f.write(f"Timestamp: {datetime.now().isoformat()}\n\n")
                f.write(body)
            print(f"  ✓ Backed up to {backup_file}")
            return True
        except Exception as e:
            print(f"  ✗ Failed to backup Issue #{issue_num}: {e}")
            return False
    
    def update_issue(self, issue_num, new_body):
        """Update GitHub Issue with new body."""
        if self.dry_run:
            print(f"  [DRY RUN] Would update Issue #{issue_num}")
            return True
        
        try:
            result = subprocess.run(
                ["gh", "issue", "edit", str(issue_num), "--body", new_body],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                return True
            else:
                print(f"  ✗ GitHub API error: {result.stderr}")
                return False
        except Exception as e:
            print(f"  ✗ Failed to update Issue #{issue_num}: {e}")
            return False
    
    def verify_update(self, issue_num, expected_body):
        """Verify that Issue was updated correctly."""
        if self.dry_run:
            return True
        
        actual_body = self.get_issue_body(issue_num)
        if actual_body is None:
            return False
        
        # Compare hash to avoid large text comparisons
        expected_hash = hashlib.md5(expected_body.encode()).hexdigest()
        actual_hash = hashlib.md5(actual_body.encode()).hexdigest()
        
        if expected_hash == actual_hash:
            return True
        else:
            print(f"  ✗ Verification failed for Issue #{issue_num}")
            print(f"    Expected hash: {expected_hash}")
            print(f"    Actual hash: {actual_hash}")
            return False
    
    def load_curriculum_file(self, week_num):
        """Load curriculum file for a specific week."""
        week_str = f"{week_num:02d}"
        file_path = WEEKS_DIR / f"week-{week_str}.md"
        
        if not file_path.exists():
            print(f"✗ Curriculum file not found: {file_path}")
            return None
        
        try:
            with open(file_path, "r") as f:
                return f.read()
        except Exception as e:
            print(f"✗ Failed to read {file_path}: {e}")
            return None
    
    def should_update_issue(self, issue_num, current_body):
        """Determine if an Issue should be updated."""
        # Check for student progress
        if self.has_checked_boxes(current_body):
            print(f"  ⚠ Issue #{issue_num} has checked boxes (student progress)")
            print(f"    Skipping to preserve progress. Review and update manually if needed.")
            return False
        
        if self.has_student_comments(issue_num):
            print(f"  ⚠ Issue #{issue_num} has student comments")
            print(f"    Skipping to preserve feedback history.")
            return False
        
        return True
    
    def sync_all_issues(self):
        """Sync all 12 weekly curriculum files with Issues #2-#13."""
        print(f"\n{'='*60}")
        print(f"Syncing Curriculum with GitHub Issues")
        print(f"Repository: {self.repo}")
        print(f"Mode: {'DRY RUN' if self.dry_run else 'LIVE UPDATE'}")
        print(f"{'='*60}\n")
        
        for week_num in range(1, 13):
            issue_num = ISSUES_START + week_num - 1
            week_str = f"{week_num:02d}"
            
            print(f"Week {week_str} (Issue #{issue_num})...")
            
            # Load curriculum file
            new_body = self.load_curriculum_file(week_num)
            if new_body is None:
                self.issues_failed.append(issue_num)
                continue
            
            # Get current Issue body
            current_body = self.get_issue_body(issue_num)
            if current_body is None:
                self.issues_failed.append(issue_num)
                continue
            
            # Check if bodies are identical
            if current_body.strip() == new_body.strip():
                print(f"  ✓ Already up-to-date")
                self.issues_updated.append(issue_num)
                continue
            
            # Check if we should update
            if not self.should_update_issue(issue_num, current_body):
                self.issues_skipped.append(issue_num)
                continue
            
            # Backup current body
            self.backup_issue(issue_num, current_body)
            
            # Update Issue
            if self.update_issue(issue_num, new_body):
                # Verify update
                if self.verify_update(issue_num, new_body):
                    print(f"  ✓ Updated successfully")
                    self.issues_updated.append(issue_num)
                else:
                    print(f"  ✗ Verification failed")
                    self.issues_failed.append(issue_num)
            else:
                self.issues_failed.append(issue_num)
        
        self.print_summary()
    
    def print_summary(self):
        """Print operation summary."""
        print(f"\n{'='*60}")
        print(f"Summary")
        print(f"{'='*60}")
        print(f"Updated: {len(self.issues_updated)} issues")
        print(f"Skipped: {len(self.issues_skipped)} issues (student progress)")
        print(f"Failed: {len(self.issues_failed)} issues")
        
        if self.issues_updated:
            print(f"\nUpdated issues: {', '.join(f'#{n}' for n in self.issues_updated)}")
        
        if self.issues_skipped:
            print(f"\nSkipped issues: {', '.join(f'#{n}' for n in self.issues_skipped)}")
        
        if self.issues_failed:
            print(f"\nFailed issues: {', '.join(f'#{n}' for n in self.issues_failed)}")
        
        if self.dry_run:
            print(f"\n[DRY RUN] No changes were made. Run without --dry-run to apply updates.")
        
        return len(self.issues_failed) == 0


def main():
    parser = argparse.ArgumentParser(
        description="Sync curriculum/weeks/ files with GitHub Issues #2-#13",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/update-weekly-issues.py --dry-run
    Preview changes without modifying Issues
  
  python scripts/update-weekly-issues.py --update
    Apply all updates to GitHub Issues
  
  python scripts/update-weekly-issues.py --help
    Show this help message
        """
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without modifying GitHub Issues"
    )
    
    parser.add_argument(
        "--update",
        action="store_true",
        help="Apply updates to GitHub Issues"
    )
    
    parser.add_argument(
        "--repo",
        default=REPO,
        help=f"GitHub repository (default: {REPO})"
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if not args.dry_run and not args.update:
        parser.print_help()
        print("\n" + "="*60)
        print("ERROR: Please specify --dry-run or --update")
        print("="*60)
        sys.exit(1)
    
    # Check that we're in the repository root
    if not WEEKS_DIR.exists():
        print(f"ERROR: {WEEKS_DIR} not found")
        print("Please run this script from the repository root.")
        sys.exit(1)
    
    # Run synchronization
    updater = IssueUpdater(args.repo, dry_run=args.dry_run)
    success = updater.sync_all_issues()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
