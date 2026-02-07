# Multi-Branch Development Workflow with Claude Code + Maestro

This guide shows you how to effectively manage multiple branches with Claude Code, using Maestro's Branch Manager to maintain context.

## Table of Contents
1. [Understanding Session Isolation](#understanding-session-isolation)
2. [Branch Switching Workflow](#branch-switching-workflow)
3. [Best Practices](#best-practices)
4. [Advanced Techniques](#advanced-techniques)
5. [Troubleshooting](#troubleshooting)

---

## Understanding Session Isolation

### How Claude Code Handles Branches

Claude Code maintains context based on:
- **Current working directory** - Changes when you switch branches
- **Conversation history** - Each chat session is separate
- **File state** - What files exist and their contents

**Key Insight**: Claude Code doesn't automatically know you switched branches. You need to:
1. Start a new conversation after switching, OR
2. Explicitly tell Claude you switched branches

### Your Current Setup

```
Your branches:
├── main (current)
├── feature_1
├── feature_2
├── feature_3
├── feature_4
├── feature_5
└── feature_6
```

---

## Branch Switching Workflow

### Option 1: One Branch at a Time (Recommended for Beginners)

This is the simplest approach:

```bash
# ===== Working on feature_1 =====
git checkout feature_1

# Start Claude Code (or use existing session)
# In the chat:
> "I'm working on feature_1. Save context: Implementing user authentication"
> "Save a note: Still need to add OAuth2 integration"

# Do your work...
# Talk to Claude, make changes, test...

# Before switching:
> "/branch_summary"
# Review what you did, make sure everything is committed

# ===== Switch to feature_2 =====
git checkout feature_2

# IMPORTANT: Tell Claude you switched
> "I just switched to feature_2. Use /switch_branch to load context"

# Or start a fresh conversation:
# Exit Claude Code (Ctrl+D or /exit) and restart

# Now work on feature_2...
```

### Option 2: Multiple Terminal Sessions (Recommended for Active Development)

Work on multiple branches simultaneously:

```bash
# Terminal 1 - main branch
cd ~/maestro_stroud
git checkout main
claude code

# Terminal 2 - feature_1
cd ~/maestro_stroud
git checkout feature_1
claude code

# Terminal 3 - feature_2
cd ~/maestro_stroud
git checkout feature_2
claude code
```

**Pros:**
- Complete isolation - each branch has its own Claude session
- Easy to switch between branches (just switch terminal tabs)
- No confusion about what branch you're on

**Cons:**
- Uses more memory (multiple Claude processes)
- Need to switch terminal tabs

### Option 3: Branch Workspaces (Advanced)

Create separate VS Code workspaces for each branch:

```bash
# Create workspace files
cat > feature_1.code-workspace << 'EOF'
{
  "folders": [
    {
      "path": ".",
      "name": "feature_1"
    }
  ],
  "settings": {
    "git.defaultBranchName": "feature_1"
  }
}
EOF

# Repeat for other branches
```

Then open each workspace in separate VS Code windows.

---

## Best Practices

### 1. Save Context Before Switching

**Always do this before switching branches:**

```bash
# In Maestro chat:
> "Save my current context: <brief description of what you're working on>"
> "List any open TODOs and save as notes"
> "/branch_summary"  # Review everything
```

### 2. Load Context After Switching

**First thing after switching branches:**

```bash
git checkout feature_2

# In Maestro chat:
> "/switch_branch feature_2"
# Or:
> "I switched to feature_2. Show me my notes and context"
```

### 3. Use Descriptive Branch Context

When saving context, include:
- **Purpose**: What is this branch for?
- **Status**: How far along are you?
- **Blockers**: Any issues or dependencies?
- **Next steps**: What needs to happen next?

**Example:**
```
> "Save context: feature_1 - User Authentication
   - Purpose: Add OAuth2 authentication to the app
   - Status: 70% complete, core auth flow working
   - Blockers: Need to test with Google OAuth provider
   - Next: Add refresh token handling and error states"
```

### 4. Tag Your Notes

Use categories to organize notes:

```bash
> "Save a TODO note: Add unit tests for auth flow"
> "Save a DECISION note: Using JWT for session tokens instead of cookies"
> "Save an ISSUE note: OAuth callback URL not working in production"
```

### 5. Regular Context Reviews

Weekly or after major milestones:

```bash
> "Show me list_all_branches_with_notes"
> "For each branch, give me a status summary"
> "Which branches are ready to merge?"
```

### 6. Clean Branch Switching Protocol

**The 3-Step Protocol:**

```bash
# STEP 1: Save current state
> "/branch_summary"  # Review what you did
> git add -A
> git commit -m "WIP: <description>"  # Work in progress commit

# STEP 2: Switch branch
> git checkout <target-branch>

# STEP 3: Load new context
> "I switched to <target-branch>. Show me my @context and @notes"
```

---

## Advanced Techniques

### Technique 1: Branch Comparison Before Merging

Before merging feature branches:

```bash
> "Compare feature_1 with main"
> "What conflicts might occur?"
> "Show me the key differences"
> "/branch_compare main"
```

### Technique 2: Context Inheritance

When creating a new branch from an existing one:

```bash
git checkout feature_1
git checkout -b feature_1_subfeature

> "I created a new branch feature_1_subfeature from feature_1"
> "Copy the context from feature_1 and add: Working on OAuth refresh token handling"
```

### Technique 3: Cross-Branch Reference

Reference work from other branches:

```bash
# On feature_2
> "Show me the notes from feature_1"
> "Did I solve the OAuth issue in feature_1? Check those notes"
```

### Technique 4: Branch Cleanup Workflow

When done with a branch:

```bash
# After merging to main
git checkout main
git branch -d feature_1

# In Maestro:
> "Archive or clear notes for feature_1 since it's merged"
> "Clear branch notes for feature_1"
```

### Technique 5: Daily Standup Report

Generate a quick status report:

```bash
> "For each branch with notes, show me:
   - Branch name
   - Last context saved
   - Open TODOs
   - Blockers
   Format as a standup report"
```

---

## Troubleshooting

### Problem: Claude Doesn't Know I Switched Branches

**Solution**: Explicitly tell Claude:
```bash
> "I switched from feature_1 to feature_2"
> "What's my @current branch?" (should show feature_2)
> "/switch_branch feature_2"
```

### Problem: Lost Context After Conversation Compaction

**Solution**: Use the Branch Manager to persist context:
```bash
# Before context gets too long:
> "/branch_summary"
> "Save the key points from this conversation as branch context"
```

### Problem: Confused Which Branch I'm On

**Solution**: Always check:
```bash
> "What's my @current branch?"
> "Show me @context"
git branch  # In terminal
```

### Problem: Accidentally Worked on Wrong Branch

**Solution**: Use git to move work:
```bash
# Save your work
git stash

# Switch to correct branch
git checkout correct_branch
git stash pop

# Update context
> "I accidentally worked on wrong branch, moved work here"
```

### Problem: Too Many Branches, Lost Track

**Solution**: Use the overview tool:
```bash
> "Show me list_all_branches_with_notes"
> "For each branch, show status and last activity"
> "Which branches haven't been touched in over a week?"
```

---

## Quick Reference Card

### Essential Commands

```bash
# Before switching branches
/branch_summary

# After switching branches
/switch_branch <target>

# Check current state
What's my @current branch?
Show me @context
Show me @notes

# Save important info
Save context: <description>
Save a TODO note: <task>
Save a DECISION note: <decision>

# Compare branches
Compare <branch1> with <branch2>
/branch_compare <branch>

# Overview
list_all_branches_with_notes
```

### Git + Maestro Workflow Cheatsheet

```bash
# Starting work on new branch
git checkout -b feature_X
> "Save context: <what I'm building>"

# During work
> "Save a note: <important thing>"
git add <files>
git commit -m "<message>"

# Before switching
> "/branch_summary"
git commit -am "WIP: checkpoint"

# Switch
git checkout feature_Y
> "/switch_branch feature_Y"

# After work is done
git checkout main
git merge feature_X
> "Clear branch notes for feature_X"
git branch -d feature_X
```

---

## Example Real-World Workflow

Here's a complete example of working on multiple features:

```bash
# ===== MONDAY: Start feature_1 =====
git checkout -b feature_1
> "Save context: Building OAuth2 authentication system. Starting with Google provider."

# Work for a few hours...
> "Save a TODO note: Need to add error handling for failed OAuth"
> "Save a DECISION note: Using JWT tokens stored in httpOnly cookies"

# End of day
> "/branch_summary"
git commit -am "feat: add OAuth2 Google login flow"

# ===== TUESDAY: Urgent bug on feature_2 =====
git checkout -b feature_2
> "Save context: URGENT: Fix production bug in payment processing"

# Fix the bug
> "Save an ISSUE note: Payment webhook wasn't retrying on failure"
git commit -am "fix: add retry logic to payment webhook"

# Back to feature_1
git checkout feature_1
> "/switch_branch feature_1"
> "What was I working on?"
# Continue working...

# ===== FRIDAY: Review all work =====
> "Show me list_all_branches_with_notes"
> "For each branch, give me a summary of what I did this week"
> "Which branches are ready to merge?"

# Merge completed work
git checkout main
git merge feature_2  # Bug fix done
> "Clear branch notes for feature_2"
git branch -d feature_2

# feature_1 continues...
```

---

## Summary

**Key Takeaways:**

1. ✅ **Always save context before switching branches**
2. ✅ **Always load context after switching branches**
3. ✅ **Use categories for notes** (TODO, DECISION, ISSUE)
4. ✅ **Review regularly** with `/branch_summary`
5. ✅ **Consider multiple terminal sessions** for active branches
6. ✅ **Clean up** branch notes after merging

**The Branch Manager gives you:**
- 📝 Persistent context across conversations
- 🔄 Smooth branch switching
- 📊 Overview of all work in progress
- 🎯 Focus on one branch at a time

**Remember:** Maestro + Branch Manager = Context that survives branch switches and conversation compaction!
