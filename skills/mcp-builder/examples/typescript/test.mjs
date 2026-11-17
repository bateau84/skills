import { test } from 'node:test';
import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js';

test('compiled server completes the real stdio MCP handshake and preserves errors', { timeout: 20000 }, async () => {
  const client = new Client({ name: 'reference-test', version: '1.0.0' });
  const transport = new StdioClientTransport({ command: process.execPath, args: ['dist/server.js', '--stdio'], stderr: 'pipe' });
  try {
    await client.connect(transport);
    const tools = await client.listTools();
    assert.equal(tools.tools[0].name, 'add');
    const ok = await client.callTool({ name: 'add', arguments: { a: 2, b: 3 } });
    assert.equal(ok.content[0].text, '5');
    assert.equal(ok.structuredContent.sum, 5);
    const failure = await client.callTool({ name: 'add', arguments: { a: 1e308, b: 1e308 } });
    assert.equal(failure.isError, true);
    const resource = await client.readResource({ uri: 'reference://status' });
    assert.equal(resource.contents[0].text, 'ready');
  } finally { await client.close(); await transport.close(); }
});

test('--help exits instead of waiting for an MCP client', () => {
  execFileSync(process.execPath, ['dist/server.js', '--help'], { timeout: 3000, stdio: 'pipe' });
});

test('guide tool catch returns an MCP error over the real SDK transport', { timeout: 20000 }, async () => {
  const { readFileSync } = await import('node:fs');
  const { runInNewContext } = await import('node:vm');
  const { default: ts } = await import('typescript');
  const { McpServer } = await import('@modelcontextprotocol/sdk/server/mcp.js');
  const { InMemoryTransport } = await import('@modelcontextprotocol/sdk/inMemory.js');
  const { z } = await import('zod');
  const markdown = readFileSync(new URL('../../reference/node_mcp_server.md', import.meta.url), 'utf8');
  const snippet = [...markdown.matchAll(/```typescript\n([\s\S]*?)```/g)]
    .map(m => m[1]).find(code => code.includes('"example_search_users"') && code.includes('server.registerTool'));
  assert.ok(snippet, 'main user-search example must be exercised, not a hand-copied replacement');
  const client = new Client({ name: 'guide-client', version: '1.0.0' });
  const [clientTransport, serverTransport] = InMemoryTransport.createLinkedPair();
  const compiled = ts.transpileModule(snippet, { reportDiagnostics: true, compilerOptions: {
    target: ts.ScriptTarget.ES2022, module: ts.ModuleKind.CommonJS,
  } });
  const syntaxErrors = (compiled.diagnostics ?? []).filter(d => d.category === ts.DiagnosticCategory.Error);
  assert.deepEqual(syntaxErrors.map(d => ts.flattenDiagnosticMessageText(d.messageText, '\n')), [],
    'guide example must parse before exercising its runtime error path');
  const js = compiled.outputText;
  // Execute the actual schema, registration and catch from the guide. Only
  // its upstream API and pure error formatter are substituted; SDK code is real.
  const sandbox = {
    exports: {},
    require: name => {
      if (name === '@modelcontextprotocol/sdk/server/mcp.js') return { McpServer };
      if (name === 'zod') return { z };
      throw new Error(`Unexpected guide import: ${name}`);
    },
    ResponseFormat: { JSON: 'json', MARKDOWN: 'markdown' },
    makeApiRequest: async () => { throw new Error('upstream 403'); },
    handleApiError: error => `Error: ${error.message}`,
  };
  runInNewContext(js + '\nglobalThis.guideServer = server;', sandbox);
  const server = sandbox.guideServer;
  try {
    await server.connect(serverTransport);
    await client.connect(clientTransport);
    const result = await client.callTool({ name: 'example_search_users', arguments: { query: 'test' } });
    assert.equal(result.isError, true);
    assert.match(result.content[0].text, /upstream 403/);
  } finally {
    await client.close();
    await server.close();
  }
});
