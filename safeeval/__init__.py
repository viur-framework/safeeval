import ast
from typing import Any, Callable, Dict


class SafeEval:
	"""Safely evaluate an expression from an untrusted party
	"""

	@staticmethod
	def compareNode(node: ast.Compare, names: Dict[str, Any]) -> bool:
		"""
			Evaluates an 'if' expression.
			These are a bit tricky as they can have more than two operands (eg. "if 1 < 2 < 3")
		"""
		left = SafeEval.evalAst(node.left, names)
		for operation, rightNode in zip(node.ops, node.comparators):
			right = SafeEval.evalAst(rightNode, names)
			if not SafeEval.dualOpMap[type(operation)](left, right):
				return False
			left = right
		return True

	nodes: Dict[ast.AST, Callable[[ast.AST, Dict[str, Any]], Any]] = {
		ast.Compare: compareNode.__func__,
		ast.Name: lambda node, names: names[node.id],
		ast.Num: lambda node, _: node.n,
		ast.Str: lambda node, _: node.s,
		ast.Subscript: lambda node, names: SafeEval.evalAst(node.value, names)[SafeEval.evalAst(node.slice, names)],
		ast.Index: lambda node, names: SafeEval.evalAst(node.value, names),
		ast.BoolOp: lambda node, names: (all if isinstance(node.op, ast.And) else any)(
			[SafeEval.evalAst(x, names) for x in node.values]),
		ast.UnaryOp: lambda node, names: SafeEval.unaryOpMap[type(node.op)](SafeEval.evalAst(node.operand, names)),
		ast.BinOp: lambda node, names: SafeEval.dualOpMap[type(node.op)](SafeEval.evalAst(node.left, names),
		                                                                 SafeEval.evalAst(node.right, names)),
		ast.IfExp: lambda node, names: SafeEval.evalAst(node.body, names) if SafeEval.evalAst(node.test, names) else \
			SafeEval.evalAst(node.orelse, names),
	}

	unaryOpMap: Dict[ast.AST, Callable[[Any], Any]] = {
		ast.Not: lambda x: not x,
		ast.USub: lambda x: -x,
		ast.UAdd: lambda x: +x,
	}

	dualOpMap: Dict[ast.AST, Callable[[Any, Any], Any]] = {
		ast.Eq: lambda x, y: x == y,
		ast.Gt: lambda x, y: x > y,
		ast.GtE: lambda x, y: x >= y,
		ast.Lt: lambda x, y: x < y,
		ast.LtE: lambda x, y: x <= y,
		ast.In: lambda x, y: x in y,
		ast.NotIn: lambda x, y: x not in y,
		ast.Sub: lambda x, y: x - y,
		ast.Add: lambda x, y: x + y,
	}

	@staticmethod
	def evalAst(node: ast.AST, names: Dict[str, Any]) -> Any:
		return SafeEval.nodes[type(node)](node, names)

	@staticmethod
	def parse(expr: str) -> ast.AST:
		expr = expr.strip()
		assert len(expr) < 500 and len([x for x in expr if x in {"(", "[", "{"}]) < 60, \
			"Recursion depth or len exceeded"
		return ast.parse(expr).body[0].value

	@staticmethod
	def safeEval(expr: str, names: Dict[str, Any]) -> Any:
		"""
			Safely evaluate an expression.
			If you want to evaluate the expression multiple times with different variables use parse to generate
			the AST once and call evalAst for each set of variables
		"""
		return SafeEval.evalAst(SafeEval.parse(expr), names)


__all__ = [SafeEval]
