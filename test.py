#!/usr/bin/env python

import unittest
import os
from install import parse_args


class TestArgs(unittest.TestCase):
    def test_full(self):
        cli = ['https://example.com/org/repo', '--directory=D', '--ref=tagname', 'extra', 'args', '--script=Makefile']
        a, remaining, _ = parse_args(cli)
        self.assertEqual('D', a.directory)
        self.assertEqual(a.ref, 'tagname')
        self.assertEqual(a.script, 'Makefile')
        self.assertEqual(remaining, ['extra', 'args'])


    def test_only_url(self):
        cli = ['https://example.com/org/repo']
        a, _, _ = parse_args(cli)
        self.assertEqual(a.source_url, cli[0])


if __name__ == '__main__':
    unittest.main()
