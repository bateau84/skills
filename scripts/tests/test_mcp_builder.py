"""Provider-free tests of the real connection/evaluator composition.

Only third-party SDK imports and the remote model/server are substituted. The
connection adapter, serialization, model-message loop and CLI parser are real.
These tests do not claim a live MCP transport or provider call was exercised.
"""
import asyncio
import importlib.util
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "skills/mcp-builder/scripts"

def load_modules():
    names = ["mcp", "mcp.client", "mcp.client.sse", "mcp.client.stdio",
             "mcp.client.streamable_http", "anthropic"]
    stubs = {name: types.ModuleType(name) for name in names}
    stubs["mcp"].ClientSession = object
    stubs["mcp"].StdioServerParameters = lambda **kw: types.SimpleNamespace(**kw)
    stubs["mcp.client.sse"].sse_client = object
    stubs["mcp.client.stdio"].stdio_client = object
    stubs["mcp.client.streamable_http"].streamablehttp_client = object
    stubs["anthropic"].Anthropic = object
    stubs["anthropic"].AsyncAnthropic = object
    def load(name, path):
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod
    with patch.dict(sys.modules, stubs):
        con = load("mcp_builder_connections_test", SCRIPTS / "connections.py")
        with patch.dict(sys.modules, {"connections": con}):
            ev = load("mcp_builder_evaluation_test", SCRIPTS / "evaluation.py")
    return con, ev

class MCPBuilderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.connections, cls.ev = load_modules()

    def connection(self, results):
        async def call_tool(name, arguments):
            result = results[name]
            if isinstance(result, BaseException):
                raise result
            return result
        connection = self.connections.MCPConnectionStdio("unused")
        connection.session = types.SimpleNamespace(call_tool=call_tool)
        return connection

    def result(self, text="failure", error=True, structured=None):
        return types.SimpleNamespace(
            content=[types.SimpleNamespace(type="text", text=text)],
            isError=error, structuredContent=structured)

    def test_connection_preserves_result_envelope(self):
        value = self.result(structured={"retryable": False})
        actual = asyncio.run(self.connection({"read": value}).call_tool("read", {}))
        self.assertIs(actual, value)

    def test_two_calls_one_error_are_serialized_through_real_adapter(self):
        uses = [types.SimpleNamespace(type="tool_use", id="a", name="read", input={}),
                types.SimpleNamespace(type="tool_use", id="b", name="status", input={})]
        calls = []
        async def create(**kw):
            calls.append(kw)
            if len(calls) == 1:
                return types.SimpleNamespace(stop_reason="tool_use", content=uses)
            results = kw["messages"][-1]["content"]
            self.assertEqual([r["tool_use_id"] for r in results], ["a", "b"])
            self.assertEqual(results[0]["content"], "permission denied")
            self.assertTrue(results[0]["is_error"])
            self.assertEqual(results[1]["content"], "ready")
            self.assertFalse(results[1]["is_error"])
            return types.SimpleNamespace(stop_reason="end_turn", content=[types.SimpleNamespace(type="text", text="done")])
        client = types.SimpleNamespace(messages=types.SimpleNamespace(create=create))
        connection = self.connection({"read": self.result("permission denied", True, {"retryable": False}),
                                      "status": self.result("ready", False)})
        text, metrics = asyncio.run(self.ev.agent_loop(client, "test/model", "question", [], connection))
        self.assertEqual(text, "done")
        self.assertEqual(sum(v["count"] for v in metrics.values()), 2)

    def test_text_and_structured_output_are_not_duplicated(self):
        result = self.result('hello', False, {'result': 'hello'})
        self.assertEqual(self.ev._mcp_tool_response(result), ('hello', False))

    def test_structured_only_result_remains_available(self):
        result = types.SimpleNamespace(content=[], isError=False, structuredContent={"answer": 42})
        self.assertEqual(self.ev._mcp_tool_response(result), ('{"answer": 42}', False))

    def test_mixed_image_and_text_preserves_success_and_omits_bytes(self):
        result = types.SimpleNamespace(content=[
            types.SimpleNamespace(type="text", text="created"),
            types.SimpleNamespace(type="image", data="SECRET_BYTES")], isError=False)
        text, error = self.ev._mcp_tool_response(result)
        self.assertFalse(error)
        self.assertIn("created", text)
        self.assertIn("unsupported", text)
        self.assertNotIn("SECRET_BYTES", text)

    def test_model_dump_mapping_and_object_have_same_translation(self):
        mapping = {"content": [{"type": "text", "text": "denied"}],
                   "isError": True, "structuredContent": {"code": 403}}
        self.assertEqual(self.ev._mcp_tool_response(mapping),
                         self.ev._mcp_tool_response(self.result("denied", True, {"code":403})))

    def test_non_text_bytes_are_not_falsely_evaluated_as_text(self):
        result = types.SimpleNamespace(content=[types.SimpleNamespace(type="image", data="SECRET_BYTES")], isError=False)
        text, error = self.ev._mcp_tool_response(result)
        self.assertFalse(error)  # coverage limitation is not a server-side tool failure
        self.assertNotIn("SECRET_BYTES", text)
        self.assertIn("unsupported", text.lower())

    def test_cancellation_is_not_serialized_as_a_tool_error(self):
        use = types.SimpleNamespace(type="tool_use", id="a", name="read", input={})
        async def create(**kw):
            return types.SimpleNamespace(stop_reason="tool_use", content=[use])
        client = types.SimpleNamespace(messages=types.SimpleNamespace(create=create))
        with self.assertRaises(asyncio.CancelledError):
            asyncio.run(self.ev.agent_loop(client,"test/model","q",[],self.connection({"read":asyncio.CancelledError()})))

    def test_cli_repeated_values_do_not_consume_evaluation_file(self):
        args = self.ev.build_parser().parse_args([
            "-m", "test/model", "-c", "python", "-a", "server.py", "-a=--stdio",
            "-e", "TOKEN=a=b", "-e", "REGION=local", "-H", "X-A: one", "-H", "X-B: two", "eval.xml"])
        self.assertEqual(args.eval_file, Path("eval.xml"))
        self.assertEqual(args.args, ["server.py", "--stdio"])
        self.assertEqual(args.env, ["TOKEN=a=b", "REGION=local"])
        self.assertEqual(args.headers, ["X-A: one", "X-B: two"])

    def test_model_call_cancellation_reaches_inflight_request(self):
        async def scenario():
            entered, cancelled = asyncio.Event(), asyncio.Event()
            async def create(**kwargs):
                entered.set()
                try:
                    await asyncio.Event().wait()
                finally:
                    cancelled.set()
            client = types.SimpleNamespace(messages=types.SimpleNamespace(create=create))
            task = asyncio.create_task(self.ev.agent_loop(client, "test/model", "q", [], self.connection({})))
            try:
                await asyncio.wait_for(entered.wait(), 0.5)
                task.cancel()
                with self.assertRaises(asyncio.CancelledError):
                    await asyncio.wait_for(task, 0.5)
                self.assertTrue(cancelled.is_set(), "request must not remain detached in a thread")
            finally:
                if not task.done():
                    task.cancel()
                await asyncio.gather(task, return_exceptions=True)
        asyncio.run(scenario())

    def test_dash_leading_args_use_equals_form_and_space_form_is_rejected(self):
        parser = self.ev.build_parser()
        args = parser.parse_args(["-m", "test/model", "-c", "npx", "-a=-y", "-a", "pkg", "eval.xml"])
        self.assertEqual(args.args, ["-y", "pkg"])
        with patch("sys.stderr"), self.assertRaises(SystemExit):
            parser.parse_args(["-m", "test/model", "-c", "npx", "-a", "-y", "eval.xml"])
        self.assertIn("-a=--flag", parser.format_help())

    def test_env_value_whitespace_is_preserved(self):
        self.assertEqual(self.ev.parse_env_vars(["TOKEN=  a=b  ", "EMPTY="]),
                         {"TOKEN": "  a=b  ", "EMPTY": ""})

    def test_missing_model_is_not_a_retired_implicit_default(self):
        with patch("sys.stderr"), self.assertRaises(SystemExit):
            self.ev.build_parser().parse_args(["eval.xml"])

if __name__ == "__main__":
    unittest.main()
