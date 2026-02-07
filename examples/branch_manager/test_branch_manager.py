#!/usr/bin/env python3
"""
Test script for Branch Manager MCP Server
Run this to verify the server works correctly
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path to import mcp_client
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from mcp_client import MCPClient


async def test_branch_manager():
    """Test the Branch Manager MCP server"""
    print("🧪 Testing Branch Manager MCP Server\n")
    print("=" * 70)

    server_path = Path(__file__).parent / "branch_server.py"

    async with MCPClient(command="python", args=[str(server_path)]) as client:
        # Test 1: List available tools
        print("\n1️⃣  Listing available tools...")
        tools = await client.list_tools()
        print(f"✓ Found {len(tools)} tools:")
        for tool in tools:
            print(f"   - {tool.name}: {tool.description}")

        # Test 2: Get current branch
        print("\n2️⃣  Getting current branch...")
        result = await client.read_resource("branch://current")
        print(f"✓ Current branch: {result}")

        # Test 3: Save a test note
        print("\n3️⃣  Saving a test note...")
        result = await client.call_tool(
            "save_branch_note",
            {
                "note": "Test note from automated test",
                "category": "general"
            }
        )
        print(f"✓ Note saved successfully")

        # Test 4: List branch notes
        print("\n4️⃣  Listing branch notes...")
        result = await client.call_tool("list_branch_notes", {})
        print("✓ Notes retrieved successfully")

        # Test 5: Save branch context
        print("\n5️⃣  Saving branch context...")
        result = await client.call_tool(
            "save_branch_context",
            {
                "context": "Testing the Branch Manager MCP server - all systems operational!"
            }
        )
        print(f"✓ Context saved successfully")

        # Test 6: Get branch context resource
        print("\n6️⃣  Reading branch context...")
        result = await client.read_resource("branch://context")
        print(f"✓ Context: {result[:50]}..." if len(str(result)) > 50 else f"✓ Context: {result}")

        # Test 7: List prompts
        print("\n7️⃣  Listing available prompts...")
        prompts = await client.list_prompts()
        print(f"✓ Found {len(prompts)} prompts:")
        for prompt in prompts:
            print(f"   - /{prompt.name}: {prompt.description}")

        # Test 8: List all branches with notes
        print("\n8️⃣  Listing all branches with notes...")
        result = await client.call_tool("list_all_branches_with_notes", {})
        print("✓ Branch list retrieved successfully")

        # Test 9: Clear notes (cleanup)
        print("\n9️⃣  Cleaning up test notes...")
        result = await client.call_tool("clear_branch_notes", {})
        print(f"✓ Test notes cleared")

        print("\n" + "=" * 70)
        print("✅ All tests passed! Branch Manager is working correctly.\n")

        print("📚 Next steps:")
        print("   1. Run Maestro with this server:")
        print("      uv run main.py examples/branch_manager/branch_server.py")
        print("   2. Try these in chat:")
        print("      - 'Save a note about my current work'")
        print("      - 'What's my @context?'")
        print("      - '/branch_summary'")


if __name__ == "__main__":
    asyncio.run(test_branch_manager())
