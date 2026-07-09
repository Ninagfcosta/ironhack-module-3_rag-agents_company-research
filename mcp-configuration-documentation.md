# MCP Configuration Documentation

## Where the configuration file is

On my Mac, the Claude Desktop config file is here:
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

I didn't get to set up Cursor for this lab — I don't have it installed, so I focused on getting Claude Desktop working properly instead.

## What I configured

### Filesystem Server

I set up the filesystem MCP server so Claude could access one specific folder on my computer:

- **Folder:** `/Users/Nina/Documents/mcp-test`
- **Command used:**
  ```
  npx -y @modelcontextprotocol/server-filesystem /Users/Nina/Documents/mcp-test
  ```
- **What it lets Claude do:** read files, write files, and list what's inside that folder — nothing outside of it.

## How I tested it

1. I opened the config file in VS Code and added the `mcpServers` block with the filesystem server info.
2. I completely quit Claude Desktop (Cmd+Q) and reopened it, since it only reads the config file on startup.
3. I started a new chat and asked: *"What MCP tools are available?"*
4. The filesystem tool showed up in the list, along with the other connectors I already had (Gmail, Google Calendar, Drive, Slack, etc).

## A problem I ran into (and how I fixed it)

When I tested the server directly in the Terminal, I got this:
```
Warning: Cannot access directory /Users/Nina/Documents/mcp-test, skipping
Error: None of the specified directories are accessible
```

At first I thought something was wrong with my config, but it turned out to be simpler than that — the `mcp-test` folder just didn't exist yet. I created it with:
```
mkdir -p ~/Documents/mcp-test
```

After that, running the same command again gave me:
```
Secure MCP Filesystem Server running on stdio
```

Which meant it was finally working.

I also checked that Node.js was installed properly first, using `node --version` (got `v24.16.0`), just to rule that out as the problem before digging further.

## What I'd tell myself next time

- Make sure the folder you're pointing to actually exists before starting the server — it won't create it for you.
- Testing the server command straight in the Terminal is a faster way to check if something's wrong than restarting the whole app over and over.
- After changing the config file, you have to fully quit and reopen the app — just closing the window isn't enough.
- Don't put real API keys directly in the file if you're going to share or commit it anywhere.
