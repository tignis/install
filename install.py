#!/usr/bin/env python

from __future__ import print_function

import subprocess
import sys
import os
import argparse

try:
    _input = raw_input
except NameError:
    _input = input


def org_repo_from_url(url):
    chunks = url.replace(':', '/').split('/')
    org, repo = chunks[-2], chunks[-1]
    if repo.endswith('.git'):
        repo = repo[:-4]
    return (org, repo)


def display_available_refs():
    print("Available versions (refs):")

    print("- Last 5 commits (unstable):")
    subprocess.check_call(['git', 'log', '--pretty=format:   %h %s (%cr)', '-n', '5'])

    print("- Branches:")
    subprocess.check_call(['git', 'for-each-ref', 'refs/heads', '--format=   %(objectname:short) %(refname:short)  (%(creatordate:relative))'])

    print("- Tagged releases:")
    subprocess.check_call(['git', 'for-each-ref', 'refs/tags', '--format=   %(objectname:short) %(refname:short)  (%(creatordate:relative))'])


def parse_args(args):
    p = argparse.ArgumentParser(
        prog='python -c "$(curl -sL https://raw.githubusercontent.com/tignis/install/main/install.py)"',
        epilog="Leftover arguments passed to script."
    )
    p.add_argument("source_url", help="Git repo to clone. Required.")
    p.add_argument("--directory", help="Clone to target directory, use if exists. Default: %s" % os.path.expanduser('~/workspace/$org/$repo/'), metavar="D")
    p.add_argument("--ref", help="Ref to 'git checkout'. Default: prompt")
    p.add_argument("--script", default="./install.py", help="Target script to run. Default: %(default)s", metavar="S")
    a, r = p.parse_known_args(args)
    if not a.directory:
        try:
            org, repo = org_repo_from_url(a.source_url)
            a.directory = "%s/%s/%s" % (os.path.expanduser('~/workspace'), org, repo)
        except IndexError:
            p.error("Cannot guess directory from url, specify --directory")
    return a, r, p


def main(args):
    a, remaining, parser = parse_args(args)
    print(a)
    print(remaining)

    if not os.path.exists(a.directory):
        print("Cloning %s into %s" % (a.source_url, a.directory))
        subprocess.check_call(["git", "clone", a.source_url, a.directory])
    else:
        print("Target directory", a.directory, "already exists")

    os.chdir(a.directory)

    if not a.ref:
        display_available_refs()
        a.ref = _input("Checkout ref: ")
        if not a.ref:
            parser.error("Git ref is required")

    subprocess.check_call(["git", "checkout", a.ref])

    if os.path.exists(a.script):
        print("Running installer script", [a.script] + remaining)
        subprocess.check_call([a.script] + remaining)
    else:
        parser.error("Cannot find installer script, specify --script")


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
