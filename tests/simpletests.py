# -*- coding: utf-8 -*-
__author__ = "Stefan Kögl <sk@mausbrand.de>"

import sys
import logging
import unittest
from unittest import TestCase

import safeeval

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


class SafeEvalTests(TestCase):
	def setUp(self) -> None:
		self.interpreter = safeeval.SafeEval({"str": str, "int": int, "lstrip": str.rstrip})

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

	def test_stringCall(self):
		ast = self.interpreter.compile('str(23)')
		self.assertEqual(
			self.interpreter.execute(
				ast,
				{}
			),
			"23",
			"str() call failed"
		)

	def test_notAllowedCallable(self):
		with self.assertRaises(NameError) as err:
			ast = self.interpreter.compile('foo("23")')
			self.interpreter.execute(ast, {})

	def test_FmtSelectionMultiple(self):
		testData = {
			"event_header_asset": [
				{'dest': {'asset_type': 'field'}},
				{'dest': {'asset_type': 'field'}},
				{'dest': {'asset_type': 'machine'}}
			]
		}
		expression = "'${event_header_asset.dest.name): $(event_header_asset.dest.lat), $(event_header_asset.dest.lng)' if event_header_asset['dest']['asset_type'] != 'field' else '$(event_header_asset.dest.name): $(event_header_asset.dest.field_coords)'"
		ast = self.interpreter.compile('str(23)')
		self.interpreter.execute(ast, testData)


if __name__ == '__main__':
	unittest.main(verbosity=4)
