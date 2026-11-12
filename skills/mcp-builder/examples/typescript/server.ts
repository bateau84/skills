// A dependency-pinned SDK-v1 reference. No external APIs or credentials.
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import { createMcpExpressApp } from "@modelcontextprotocol/sdk/server/express.js";
import { z } from "zod";

export function createServer(): McpServer {
  const server = new McpServer({ name: "local-reference", version: "1.0.0" });
  server.registerTool("add", {
    description: "Add two finite numbers locally.",
    inputSchema: { a: z.number().finite(), b: z.number().finite() },
    annotations: { readOnlyHint: true, destructiveHint: false, idempotentHint: true, openWorldHint: false },
  }, async ({ a, b }) => {
    const sum = a + b;
    if (!Number.isFinite(sum)) {
      return { content: [{ type: "text", text: "The sum is outside the finite range." }], isError: true };
    }
    return { content: [{ type: "text", text: String(sum) }], structuredContent: { sum } };
  });
  server.registerResource("status", "reference://status", { mimeType: "text/plain" },
    async (uri) => ({ contents: [{ uri: uri.href, mimeType: "text/plain", text: "ready" }] }));
  return server;
}

async function main(): Promise<void> {
  if (process.argv.includes("--stdio")) {
    await createServer().connect(new StdioServerTransport());
    return;
  }
  if (process.argv.includes("--http")) {
    // Loopback only. Public hosting additionally needs explicit auth and origin policy.
    const app = createMcpExpressApp();
    app.post("/mcp", async (req, res) => {
      // A fresh server AND transport per stateless request, not a shared connected server.
      const server = createServer();
      const transport = new StreamableHTTPServerTransport({ sessionIdGenerator: undefined, enableJsonResponse: true });
      res.on("close", () => { void transport.close(); void server.close(); });
      try {
        await server.connect(transport);
        await transport.handleRequest(req, res, req.body);
      } catch {
        await transport.close();
        await server.close();
        if (!res.headersSent) res.status(500).json({ jsonrpc: "2.0", id: null,
          error: { code: -32603, message: "Internal server error" } });
      }
    });
    app.get("/mcp", (_req, res) => { res.sendStatus(405); });
    app.delete("/mcp", (_req, res) => { res.sendStatus(405); });
    app.listen(3000, "127.0.0.1");
    return;
  }
  // --help must terminate; it must not accidentally start the stdio transport.
  console.error("Usage: node dist/server.js --stdio | --http | --help");
  if (!process.argv.includes("--help")) process.exitCode = 2;
}
void main().catch((error: unknown) => { console.error(error); process.exitCode = 1; });
