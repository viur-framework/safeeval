# -*- coding: utf-8 -*-
__author__ = "Stefan Kögl <sk@mausbrand.de>"

import unittest

import safeeval


class SafeEvalTests(unittest.TestCase):
	def setUp(self) -> None:
		self.interpreter = safeeval.SafeEval()

	def tearDown(self):
		del self.interpreter
		self.interpreter = None

	def test_inOperator(self):
		ast = self.interpreter.compile('"foo" in data')
		self.assertTrue(
			self.interpreter.execute(
				ast,
				{"data": ["foo", "bar", "baz"]}),
			"in operator does not evaluates to True"
		)

	def test_stringConcatenation(self):
		ast = self.interpreter.compile('foo + " bar" + " " + "baz"')
		self.assertEqual(
			self.interpreter.execute(
				ast,
				{"foo": "foo"}
			),
			"foo bar baz",
			"in operator does not evaluates to True"
		)

	def test_stringMultiply(self):
		ast = self.interpreter.compile('"*" * 10')
		self.assertEqual(
			self.interpreter.execute(
				ast,
				{}
			),
			"**********",
			"multiply operator does not works for strings"
		)

	def test_numberMultiply(self):
		ast = self.interpreter.compile('23 * 42')
		self.assertEqual(
			self.interpreter.execute(
				ast,
				{}
			),
			966,
			"multiply operator does not works for numbers"
		)

	def test_simpleArithmeticExpression(self):
		ast = self.interpreter.compile('23 / 5 + (1337 - 42)')
		self.assertEqual(
			self.interpreter.execute(
				ast,
				{}
			),
			1299.6,
			"ArithmeticExpression does not work"
		)
