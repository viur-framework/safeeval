import ast
from typing import Any, Callable, Dict


class SafeEval:
	"""Safely evaluate an expression from an untrusted party
	"""

	def __init__(self, buildinCallWhitelist=[]):
		self.whitelist = buildinCallWhitelist

		self.nodes: Dict[ast.AST, Callable[[ast.AST, Dict[str, Any]], Any]] = {
			ast.Call: self.visitCallNode,
			ast.Compare: self.compareNode,
			ast.Name: lambda node, names: names[node.id],
			ast.Num: lambda node, _: node.n,
			ast.Str: lambda node, _: node.s,
			ast.Subscript: lambda node, names: self.execute(node.value, names)[self.execute(node.slice, names)],
			ast.Index: lambda node, names: self.execute(node.value, names),
			ast.BoolOp: lambda node, names: (all if isinstance(node.op, ast.And) else any)(
				[self.execute(x, names) for x in node.values]),
			ast.UnaryOp: lambda node, names: self.unaryOpMap[type(node.op)](self.execute(node.operand, names)),
			ast.BinOp: lambda node, names: self.dualOpMap[type(node.op)](self.execute(node.left, names),
			                                                             self.execute(node.right, names)),
			ast.IfExp: lambda node, names: self.execute(node.body, names) if self.execute(node.test, names) else \
				self.execute(node.orelse, names),
		}

		self.unaryOpMap: Dict[ast.AST, Callable[[Any], Any]] = {
			ast.Not: lambda x: not x,
			ast.USub: lambda x: -x,
			ast.UAdd: lambda x: +x,
		}

		self.dualOpMap: Dict[ast.AST, Callable[[Any, Any], Any]] = {
			ast.Eq: lambda x, y: x == y,
			ast.Gt: lambda x, y: x > y,
			ast.GtE: lambda x, y: x >= y,
			ast.Lt: lambda x, y: x < y,
			ast.LtE: lambda x, y: x <= y,
			ast.In: lambda x, y: x in y,
			ast.NotIn: lambda x, y: x not in y,
			ast.Sub: lambda x, y: x - y,
			ast.Add: lambda x, y: x + y,
			ast.Mult: lambda x, y: x * y,
			ast.Div: lambda x, y: x / y,
		}

	def visitCallNode(self, node: ast.Call, names: Dict[str, Any]):
		args = [self.execute(arg, names) for arg in node.args]
		if node.func.id not in self.whitelist:
			raise Exception("function not in whitelist - aborting")
		return self.whitelist[node.func.id](*args)

	def compareNode(self, node: ast.Compare, names: Dict[str, Any]) -> bool:
		"""
			Evaluates an 'if' expression.
			These are a bit tricky as they can have more than two operands (eg. "if 1 < 2 < 3")
		"""
		left = self.execute(node.left, names)
		for operation, rightNode in zip(node.ops, node.comparators):
			right = self.execute(rightNode, names)
			if not self.dualOpMap[type(operation)](left, right):
				return False
			left = right
		return True

	def execute(self, node: ast.AST, names: Dict[str, Any]) -> Any:
		return self.nodes[type(node)](node, names)

	def compile(self, expr: str) -> ast.AST:
		expr = expr.strip()
		assert len(expr) < 500 and len([x for x in expr if x in {"(", "[", "{"}]) < 60, \
			"Recursion depth or len exceeded"
		return ast.parse(expr).body[0].value

	def safeEval(self, expr: str, names: Dict[str, Any]) -> Any:
		"""
			Safely evaluate an expression.
			If you want to evaluate the expression multiple times with different variables use parse to generate
			the AST once and call execute for each set of variables
		"""
		return self.execute(self.compile(expr), names)


__all__ = ["SafeEval"]
