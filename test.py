#!/usr/bin/env python

import unittest
import os
from install import parse_args, org_repo_from_url


class TestParseUrl(unittest.TestCase):
    def test_http_dot_git(self):
        self.assertEqual(org_repo_from_url("https://github.com/org/repo.git"), ("org", "repo"))
    
    def test_http(self):
        self.assertEqual(org_repo_from_url("https://github.com/org/repo"), ("org", "repo"))

    def test_ssh_dot_git(self):
        self.assertEqual(org_repo_from_url("git@github.com:org/repo.git"), ("org", "repo"))
    
    def test_ssh(self):
        self.assertEqual(org_repo_from_url("git@github.com:org/repo"), ("org", "repo"))


class TestArgs(unittest.TestCase):
    def test_full(self):
        cli = ['https://example.com/org/repo', '--ref=tagname', 'extra', 'args', '--script=Makefile']
        a, remaining, _ = parse_args(cli)
        self.assertEqual(os.path.expanduser('~/workspace/org/repo'), a.directory)
        self.assertEqual(a.ref, 'tagname')
        self.assertEqual(a.script, 'Makefile')
        self.assertEqual(remaining, ['extra', 'args'])


    def test_only_url(self):
        cli = ['https://example.com/org/repo']
        a, _, _ = parse_args(cli)
        self.assertEqual(a.source_url, cli[0])


if __name__ == '__main__':
    unittest.main()
