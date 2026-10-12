"""Dependency-free safety helpers used by tool implementations."""

import ast
import operator
from pathlib import Path


_BINARY_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}
_UNARY_OPERATORS = {ast.UAdd: operator.pos, ast.USub: operator.neg}


def evaluate_arithmetic(expression: str):
    """Evaluate arithmetic only; names, calls and attribute access are rejected."""
    if len(expression) > 200:
        raise ValueError("表达式过长")
    tree = ast.parse(expression, mode="eval")

    def visit(node):
        if isinstance(node, ast.Expression):
            return visit(node.body)
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in _BINARY_OPERATORS:
            left, right = visit(node.left), visit(node.right)
            if isinstance(node.op, ast.Pow) and abs(right) > 100:
                raise ValueError("指数过大")
            return _BINARY_OPERATORS[type(node.op)](left, right)
        if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY_OPERATORS:
            return _UNARY_OPERATORS[type(node.op)](visit(node.operand))
        raise ValueError("仅支持数字和基本算术运算")

    return visit(tree)


def safe_child_path(root: Path, filename: str) -> Path:
    """Resolve a file below root and reject absolute paths or traversal."""
    candidate = (root / filename).resolve()
    resolved_root = root.resolve()
    if candidate == resolved_root or resolved_root not in candidate.parents:
        raise ValueError(f"文件必须位于 {root.name} 目录内")
    return candidate
