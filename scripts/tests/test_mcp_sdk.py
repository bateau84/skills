"""Exercise real SDK types and HTTP serialization without provider calls.

The model HTTP service is the fake boundary; connection/result adapters and
installed SDK serialization are real. CI requires these optional dependencies.
"""
import asyncio
import importlib
import importlib.util
import json
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

HAS_SDK = all(importlib.util.find_spec(x) for x in ("mcp", "anthropic"))
if os.environ.get("SKILLS_REQUIRE_MCP_SDK_TESTS") == "1" and not HAS_SDK:
    raise RuntimeError("SDK checks required but optional MCP test dependencies are absent")


@unittest.skipUnless(HAS_SDK, "optional SDK dependencies; required in reference-check CI")
class RealSDKChecks(unittest.IsolatedAsyncioTestCase):
    def load_adapters(self):
        root = Path(__file__).resolve().parents[2] / "skills/mcp-builder/scripts"
        def load(name, path):
            spec = importlib.util.spec_from_file_location(name, path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
        connections = load("sdk_test_connections", root / "connections.py")
        with patch.dict(sys.modules, {"connections": connections}):
            ev = load("sdk_test_evaluation", root / "evaluation.py")
        return connections, ev

    def http_backend(self):
        from anthropic import DefaultAsyncHttpxClient
        # Do not alias globally: MCP may use httpx while Anthropic uses httpx2.
        names = {base.__module__.split(".")[0] for base in DefaultAsyncHttpxClient.__mro__}
        names &= {"httpx", "httpx2"}
        self.assertEqual(len(names), 1, "unsupported SDK HTTP implementation")
        return importlib.import_module(names.pop())

    async def test_real_sdk_results_serialize_as_matching_tool_results(self):
        from anthropic import AsyncAnthropic, DefaultAsyncHttpxClient
        from mcp.types import CallToolResult, TextContent, ImageContent
        backend = self.http_backend()
        connections, ev = self.load_adapters()
        class Session:
            async def call_tool(self, name, arguments):
                if name == "structured":
                    return CallToolResult(content=[], structuredContent={"answer": 42})
                blocks = [TextContent(type="text", text=name)]
                if name == "mixed":
                    blocks.append(ImageContent(type="image", data="c2VjcmV0", mimeType="image/png"))
                return CallToolResult(content=blocks, isError=name == "denied",
                                      structuredContent={"result": name})
        connection = connections.MCPConnectionStdio("unused")
        connection.session = Session()
        requests = []
        async def handle(request):
            data = json.loads(request.content)
            requests.append(data)
            if len(requests) == 1:
                content = [{"type": "tool_use", "id": f"call_{i}", "name": name, "input": {}}
                           for i, name in enumerate(("denied", "ready", "mixed", "structured"))]
                stop = "tool_use"
            else:
                results = data["messages"][-1]["content"]
                self.assertEqual([r["tool_use_id"] for r in results], [f"call_{i}" for i in range(4)])
                self.assertEqual([r["is_error"] for r in results], [True, False, False, False])
                self.assertEqual(results[0]["content"], "denied")
                self.assertEqual(results[1]["content"], "ready")
                self.assertIn("mixed", results[2]["content"])
                self.assertIn("unsupported", results[2]["content"])
                self.assertNotIn("c2VjcmV0", results[2]["content"])
                self.assertEqual(json.loads(results[3]["content"]), {"answer": 42})
                content, stop = [{"type": "text", "text": "finished"}], "end_turn"
            return backend.Response(200, json={"id": "msg_test", "type": "message", "role": "assistant",
                "model": "test-model", "content": content, "stop_reason": stop, "stop_sequence": None,
                "usage": {"input_tokens": 1, "output_tokens": 1}})
        async with AsyncAnthropic(api_key="non-secret-test-only", max_retries=0,
                http_client=DefaultAsyncHttpxClient(transport=backend.MockTransport(handle), trust_env=False)) as client:
            answer, metrics = await ev.agent_loop(client, "test-model", "q", [], connection)
        self.assertEqual(answer, "finished")
        self.assertEqual(len(requests), 2)
        self.assertEqual(sum(x["count"] for x in metrics.values()), 4)

    async def test_cancellation_stops_awaiting_the_real_sdk_transport(self):
        from anthropic import AsyncAnthropic, DefaultAsyncHttpxClient
        backend = self.http_backend()
        connections, ev = self.load_adapters()
        entered, released = asyncio.Event(), asyncio.Event()
        async def slow(request):
            entered.set()
            try:
                await asyncio.sleep(60)
            finally:
                released.set()
        async with AsyncAnthropic(api_key="non-secret-test-only", max_retries=0,
                http_client=DefaultAsyncHttpxClient(transport=backend.MockTransport(slow), trust_env=False)) as client:
            task = asyncio.create_task(ev.agent_loop(client, "test-model", "q", [],
                                                     connections.MCPConnectionStdio("unused")))
            try:
                await asyncio.wait_for(entered.wait(), 2)
                task.cancel()
                with self.assertRaises(asyncio.CancelledError):
                    await asyncio.wait_for(task, 1)
                self.assertTrue(released.is_set(), "HTTP await must unwind on cancellation")
            finally:
                if not task.done():
                    task.cancel()
                await asyncio.gather(task, return_exceptions=True)

    async def test_run_evaluation_closes_the_client_on_cancellation(self):
        connections, ev = self.load_adapters()
        entered, closed = asyncio.Event(), asyncio.Event()
        class Client:
            async def __aenter__(self): return self
            async def __aexit__(self, *args): closed.set()
        class Connection:
            async def list_tools(self): return []
        async def blocked(*args):
            entered.set()
            await asyncio.Event().wait()
        with patch.object(ev, "AsyncAnthropic", return_value=Client()), \
             patch.object(ev, "parse_evaluation_file", return_value=[{"question": "q", "answer": "a"}]), \
             patch.object(ev, "evaluate_single_task", side_effect=blocked):
            task = asyncio.create_task(ev.run_evaluation(Path("unused.xml"), Connection(), "test-model"))
            await asyncio.wait_for(entered.wait(), 1)
            task.cancel()
            with self.assertRaises(asyncio.CancelledError):
                await task
        self.assertTrue(closed.is_set())

    def test_v1_context_api_signatures_and_transport_are_supported(self):
        import inspect
        from mcp.server.fastmcp import Context, FastMCP
        from mcp.shared.context import RequestContext
        from mcp.client.streamable_http import streamablehttp_client
        self.assertTrue(callable(streamablehttp_client))
        for name in ("info", "error", "debug", "elicit", "report_progress"):
            self.assertTrue(callable(getattr(Context, name)))
        progress = inspect.signature(Context.report_progress).parameters
        for name in ("progress", "total", "message"):
            self.assertIn(name, progress)
        self.assertIn("schema", inspect.signature(Context.elicit).parameters)
        self.assertIn("streamable-http", str(inspect.signature(FastMCP.run)))
        # A real SDK request context must expose the exact field used in the guide.
        ctx = RequestContext(request_id="test", meta=None, session=None, lifespan_context={"db": "sentinel"})
        self.assertEqual(ctx.lifespan_context["db"], "sentinel")
        guide = (Path(__file__).resolve().parents[2] / "skills/mcp-builder/reference/python_mcp_server.md").read_text()
        self.assertIn('ctx.request_context.lifespan_context["db"]', guide)
        self.assertNotIn("lifespan_state", guide)


if __name__ == "__main__":
    unittest.main()
