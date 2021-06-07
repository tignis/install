#!/usr/bin/env python

from __future__ import print_function

import subprocess
import sys
import os
import argparse
import tempfile
import shutil

try:
    _input = raw_input
except NameError:
    _input = input


def display_available_refs():
    print("Available versions (refs):")

    print("- Last 5 commits (unstable):")
    subprocess.check_call(['git', 'log', '--pretty=format:   %h %s (%cr)', '-n', '5'])

    print("- Local Branches:")
    subprocess.check_call(['git', 'for-each-ref', 'refs/heads', '--sort=creatordate', '--format=   %(objectname:short) %(refname:short)  (%(creatordate:relative))'])

    print("- Remote Branches:")
    subprocess.check_call(['git', 'for-each-ref', 'refs/remotes', '--sort=creatordate', '--format=   %(objectname:short) %(refname:short)  (%(creatordate:relative))'])

    print("- Tagged releases:")
    subprocess.check_call(['git', 'for-each-ref', 'refs/tags', '--sort=creatordate', '--format=   %(objectname:short) %(refname:short)  (%(creatordate:relative))'])


def parse_args(args):
    p = argparse.ArgumentParser(
        prog='python -c "$(curl -sL https://raw.githubusercontent.com/tignis/install/main/install.py)"',
        epilog="Leftover arguments passed to script."
    )
    p.add_argument("source_url", help="Git repo to clone. Required.")
    p.add_argument("--directory", help="Clone to target directory, use existing clone if exists. Default: inside %s" % tempfile.gettempdir(), metavar="D")
    p.add_argument("--ref", help="Ref to 'git checkout'. Default: prompt")
    p.add_argument("--script", default="./install.py", help="Target script to run. Default: %(default)s", metavar="S")
    a, r = p.parse_known_args(args)

    return a, r, p


def main(args):
    a, remaining, parser = parse_args(args)

    use_temporary_directory = a.directory is None
    created_temp_directory = False
    if use_temporary_directory:
        try:
            a.directory = tempfile.mkdtemp(prefix="git-clone-install")
            created_temp_directory = True
            return run(a, remaining, parser)
        finally:
            if created_temp_directory:
                shutil.rmtree(a.directory)
    else:
        return run(a, remaining, parser)


def run(a, remaining, parser):

    if (not os.path.exists(a.directory)) or (not os.listdir(a.directory)):
        print("Cloning %s into %s" % (a.source_url, a.directory))
        subprocess.check_call(["git", "clone", a.source_url, a.directory])
    else:
        print("Target directory %s already exists, assuming it's a git repository" % a.directory)

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
