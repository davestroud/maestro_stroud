# Quick Start: Multi-Branch Development with Maestro + Claude Code

🎯 **Goal**: Work efficiently across multiple branches with persistent context.

## 5-Minute Setup

### Step 1: Test the Branch Manager

```bash
cd ~/maestro_stroud

# Test the MCP server
python examples/branch_manager/test_branch_manager.py
```

You should see: `✅ All tests passed!`

### Step 2: Start Maestro with Branch Manager

```bash
# Start Maestro with the Branch Manager loaded
uv run main.py examples/branch_manager/branch_server.py
```

### Step 3: Try It Out

In the Maestro chat, try these commands:

```
# Save context for current branch
> Save context: Working on the main branch, setting up the project

# Save some notes
> Save a TODO note: Need to test the authentication flow
> Save a DECISION note: Using JWT tokens for session management

# View what you saved
> Show me my @context
> Show me my @notes

# Get a summary
> /branch_summary
```

**That's it!** You now have persistent branch context. 🎉

---

## Daily Workflow

### When Starting Work

```bash
# 1. Check which branch you're on
git branch

# 2. Start Maestro with Branch Manager
uv run main.py examples/branch_manager/branch_server.py

# 3. Load your context
> What's my @current branch?
> Show me my @context
> Show me my @notes
```

### When Working

```
# Save important decisions
> Save a DECISION note: Switched from REST to GraphQL for the API

# Save TODOs as you think of them
> Save a TODO note: Add unit tests for the new endpoint

# Save issues you encounter
> Save an ISSUE note: OAuth callback timing out on slow connections
```

### When Switching Branches

```bash
# 1. Save current state
> /branch_summary
> git commit -am "WIP: checkpoint"

# 2. Switch branch
> git checkout feature_2

# 3. Tell Claude and load context
> /switch_branch feature_2
```

### End of Day

```
> /branch_summary
> git commit -am "feat: completed OAuth flow"
```

---

## Understanding the Three Ways to Use It

### 1. Natural Language (Claude decides when to use tools)

```
You: "Remember that I decided to use PostgreSQL instead of MySQL"
→ Claude calls save_branch_note automatically

You: "What was I working on yesterday?"
→ Claude reads your context and notes

You: "Show me all my TODOs"
→ Claude calls list_branch_notes
```

### 2. @Mentions (Direct resource access)

```
You: "What's my @context?"
→ Directly fetches branch://context

You: "Show me @notes"
→ Directly fetches branch://notes

You: "What's the @current branch?"
→ Directly fetches branch://current
```

### 3. /Commands (Pre-built workflows)

```
You: "/branch_summary"
→ Runs full branch analysis workflow

You: "/switch_branch feature_2"
→ Saves current context, loads target context

You: "/branch_compare main"
→ Shows detailed diff with main branch
```

**Use whatever feels natural!** They all work together.

---

## Working on Multiple Branches

### Option A: One Branch at a Time (Simple)

```bash
# Work on feature_1
git checkout feature_1
uv run main.py examples/branch_manager/branch_server.py
# Work... commit... save context

# Switch to feature_2
git checkout feature_2
> /switch_branch feature_2
# Work... commit... save context
```

### Option B: Multiple Terminal Sessions (Power User)

```bash
# Terminal 1 - feature_1
cd ~/maestro_stroud && git checkout feature_1
uv run main.py examples/branch_manager/branch_server.py

# Terminal 2 - feature_2
cd ~/maestro_stroud && git checkout feature_2
uv run main.py examples/branch_manager/branch_server.py

# Terminal 3 - main
cd ~/maestro_stroud && git checkout main
uv run main.py examples/branch_manager/branch_server.py
```

**Benefits:**
- Complete isolation
- Easy switching (just switch terminal tabs)
- Each branch has its own Claude conversation

---

## Real-World Example

### Monday: Start new feature

```bash
git checkout -b feature_auth
uv run main.py examples/branch_manager/branch_server.py
```

```
> Save context: Building OAuth2 authentication. Starting with Google provider.
> Save a TODO note: Research best practices for storing refresh tokens
> Build me the basic OAuth flow
```

### Tuesday: Urgent bug fix

```bash
git checkout -b hotfix_payment
```

```
> /switch_branch hotfix_payment
> Save context: URGENT - Payment webhook failing in production
> Help me debug the webhook handler
> Save a DECISION note: Added retry logic with exponential backoff
```

### Wednesday: Back to feature

```bash
git checkout feature_auth
```

```
> /switch_branch feature_auth
> What was I working on?
# Claude shows: "Building OAuth2 authentication. Starting with Google provider."
# Shows your TODO about refresh tokens
> Let's continue with the refresh token handling
```

### Friday: Review week

```
> Show me list_all_branches_with_notes
> For each branch, summarize my progress this week
> Which branches are ready to merge?
```

---

## Comparison: With vs Without Branch Manager

### Without Branch Manager ❌

```
You: [Switch to feature_2]
Claude: [Lost context, doesn't know what you were working on]
You: "What was I doing on this branch?"
Claude: "I don't have context about your previous work on this branch"
You: [Have to explain everything again] 😫
```

### With Branch Manager ✅

```
You: [Switch to feature_2]
You: "/switch_branch feature_2"
Claude: "Loading context for feature_2..."
Claude: "You were working on: Building the payment integration
         Your TODOs:
         - Add error handling for failed payments
         - Test with Stripe test mode
         Your last note: Switched to Stripe instead of PayPal"
You: "Perfect, let's continue!" 😊
```

---

## Pro Tips

### 1. Save Context Early and Often

Don't wait until you're done. Save context after:
- Making an important decision
- Hitting a blocker
- Discovering something tricky
- Before taking a break

### 2. Use Descriptive Categories

```
✅ Good:
> Save a TODO note: Add unit tests for OAuth callback
> Save a DECISION note: Using JWT instead of sessions
> Save an ISSUE note: Rate limiting not working in production

❌ Less useful:
> Save a note: Need to do something with tests
> Save a note: Changed some stuff
```

### 3. Review Before Switching

Always run `/branch_summary` before switching. It helps you:
- Remember what you did
- Commit anything uncommitted
- Save important context you might forget

### 4. Compare Before Merging

Before merging to main:

```
> Compare feature_auth with main
> What conflicts might occur?
> Is feature_auth ahead or behind main?
```

### 5. Weekly Cleanup

Every Friday:

```
> Show me list_all_branches_with_notes
> Which branches can be deleted (already merged)?
> For merged branches: clear_branch_notes
```

---

## Troubleshooting

### "Claude doesn't remember what I was working on"

**Solution:** Load your context explicitly:
```
> Show me my @context
> Show me my @notes
> /branch_summary
```

### "I forgot which branch I'm on"

**Solution:**
```
> What's my @current branch?
```

Or in terminal:
```bash
git branch
```

### "I accidentally worked on the wrong branch"

**Solution:**
```bash
# Save your work
git stash

# Switch to correct branch
git checkout correct_branch

# Apply your work
git stash pop

# Update context
> I moved work from wrong_branch to correct_branch
```

### "Too many branches, lost track"

**Solution:**
```
> Show me list_all_branches_with_notes
> For each branch, show when it was last updated
> Which branches have no activity in 2 weeks?
```

---

## What You Get

### Before (Just Claude Code) ⚪

- ✅ Great at coding assistance
- ✅ Understands current files
- ❌ No branch context persistence
- ❌ Context lost when switching branches
- ❌ Have to re-explain after conversation compaction

### After (Claude Code + Maestro + Branch Manager) 🎯

- ✅ Great at coding assistance
- ✅ Understands current files
- ✅ **Branch context persists forever**
- ✅ **Smooth branch switching with context**
- ✅ **Notes survive conversation compaction**
- ✅ **Overview of all work in progress**

---

## Next Steps

1. ✅ **You just finished**: This quick start
2. 📖 **Read next**: `BRANCH_WORKFLOW_GUIDE.md` for advanced techniques
3. 🔧 **Explore**: `examples/branch_manager/README.md` for all features
4. 🎨 **Customize**: Modify `branch_server.py` to add your own tools
5. 🚀 **Build**: Create your own MCP servers (see `examples/README.md`)

---

## Summary

**3 Key Commands:**

```bash
# Start Maestro with Branch Manager
uv run main.py examples/branch_manager/branch_server.py

# When switching branches
/switch_branch <target>

# To review your work
/branch_summary
```

**3 Key Concepts:**

1. **Save context** = Your branch work persists across sessions
2. **@mentions** = Quick access to your saved data
3. **/commands** = Powerful workflows in one command

**You're all set!** Start saving context and never lose track of your branches again. 🎉

---

## Questions?

- **More examples?** → See `examples/WALKTHROUGH.md`
- **Advanced workflows?** → See `BRANCH_WORKFLOW_GUIDE.md`
- **Build your own MCP server?** → See `examples/README.md`
- **Maestro documentation?** → See `README.md`
