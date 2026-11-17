"""Small structural guards for version-bound examples and repaired references.

These are documentation consistency checks, not model-performance evidence.
Runtime tool behavior is exercised separately by the real SDK suites.
"""
import ast
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKILLS = ROOT / "skills"


class ReferenceDocsTests(unittest.TestCase):
    def test_mcp_v1_references_do_not_select_v2_readmes(self):
        bad = []
        for path in (SKILLS / "mcp-builder").rglob("*.md"):
            if re.search(r"modelcontextprotocol/(?:python|typescript)-sdk/(?:blob/)?main/README\.md", path.read_text()):
                bad.append(str(path.relative_to(ROOT)))
        self.assertEqual(bad, [], "the bundled examples target SDK v1")

    def test_python_lifespan_example_accesses_v1_request_context(self):
        guide = (SKILLS / "mcp-builder/reference/python_mcp_server.md").read_text()
        snippet = next(s for s in re.findall(r"```python\n(.*?)```", guide, re.S)
                       if "def app_lifespan" in s)
        attrs = {node.attr for node in ast.walk(ast.parse(snippet)) if isinstance(node, ast.Attribute)}
        self.assertIn("lifespan_context", attrs)
        self.assertNotIn("lifespan_state", attrs)

    def test_known_dead_sibling_references_are_gone(self):
        bad = [str(p.relative_to(ROOT)) for p in SKILLS.rglob("*.md")
               if "promql-cli" in p.read_text()]
        self.assertEqual(bad, [])
        self.assertTrue((SKILLS / "promql/SKILL.md").is_file())

    def test_cobra_filterdirs_is_a_directive_not_a_function(self):
        guide = (SKILLS / "golang-spf13-cobra/references/completions.md").read_text()
        self.assertNotIn("ShellCompDirectiveFilterDirs(", guide)

    def test_workspace_example_initializes_the_modules_it_shows(self):
        guide = (SKILLS / "golang-project-layout/references/workspaces.md").read_text()
        command = re.search(r"^go work init (.+)$", guide, re.M).group(1)
        entries = re.search(r"use \(\n(.*?)\n\)", guide, re.S).group(1).split()
        self.assertEqual(set(command.split()), set(entries))
