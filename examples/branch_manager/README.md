# Branch Manager MCP Server

A custom MCP server for managing context and notes across different git branches.

## Features

### 🔧 Tools (Auto-called by Claude)
- `save_branch_note` - Save notes specific to current branch
- `list_branch_notes` - View all notes for a branch
- `clear_branch_notes` - Clear notes for current branch
- `save_branch_context` - Save important context about branch work
- `compare_branches` - Compare two branches
- `list_all_branches_with_notes` - See which branches have data

### 📦 Resources (Access with @mention)
- `@current` - Current branch name
- `@context` - Saved context for current branch
- `@notes` - All notes as JSON
- `@list` - All git branches

### ⚡ Prompts (Use /command)
- `/branch_summary` - Generate comprehensive branch summary
- `/switch_branch <name>` - Prepare to switch branches with context
- `/branch_compare <name>` - Compare current branch with another

## Quick Start

### 1. Test Standalone
```bash
cd maestro_stroud
python examples/branch_manager/test_branch_manager.py
```

### 2. Use with Maestro
```bash
uv run main.py examples/branch_manager/branch_server.py
```

## Usage Examples

### Natural Language (Tools)
```
You: "Save a note that I fixed the authentication bug"
→ Claude calls save_branch_note automatically

You: "What notes do I have for feature_1 branch?"
→ Claude calls list_branch_notes with branch="feature_1"

You: "Compare feature_1 with main"
→ Claude calls compare_branches
```

### @Mentions (Resources)
```
You: "What's my @context for this branch?"
→ Shows saved context

You: "Show me @notes"
→ Returns all notes as JSON

You: "What's the @current branch?"
→ Shows current branch name
```

### /Commands (Prompts)
```
You: "/branch_summary"
→ Generates full branch summary with git diff

You: "/switch_branch feature_2"
→ Saves current context, loads target context

You: "/branch_compare main"
→ Shows detailed comparison with main branch
```

## Data Storage

Branch-specific data is stored in `.branch_data/`:
```
.branch_data/
├── main/
│   ├── notes.json
│   └── context.txt
├── feature_1/
│   ├── notes.json
│   └── context.txt
└── feature_2/
    └── notes.json
```

Add `.branch_data/` to `.gitignore` to keep it local.

## Workflow Example

```bash
# Working on feature_1
git checkout feature_1

# In Maestro chat:
> "Save context: Working on user authentication with OAuth2"
> "Save a todo note: Need to add error handling"
> "Save a decision note: Using JWT for session management"

# View everything
> "/branch_summary"

# Switch branches
> "/switch_branch feature_2"
# Claude shows you feature_2's context and asks if you're ready

git checkout feature_2

# Continue working with full context
> "What was I working on?"
# Claude shows your saved notes and context
```

## Integration with .gitignore

Add this to your `.gitignore`:
```bash
# Branch-specific context (local only)
.branch_data/
```

## Tips

1. **Save context regularly**: After making decisions or hitting blockers
2. **Use categories**: `general`, `todo`, `decision`, `issue` for organization
3. **Before switching**: Use `/switch_branch` to prepare
4. **Weekly review**: Use `list_all_branches_with_notes` to see all work
5. **Compare often**: Use `compare_branches` to track divergence

## Advanced: Multiple Developers

Each developer has their own `.branch_data/` locally. To share context:

```bash
# Export branch context
> "Show me all notes for feature_1"
# Copy output to team chat

# Or create shared docs:
> "Generate a summary of feature_1 and save to docs/feature_1.md"
```
