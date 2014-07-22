#!/usr/bin/python

import sys
import os
import argparse
import subprocess

def update(paths, revision):
    command = ["svn", "up", "-r", str(revision)]
    command.extend(paths)
    with open(os.devnull, 'w') as dev_null:
        subprocess.call(command, stdout=dev_null, stderr=dev_null)

def is_command_successful(command):
    with open(os.devnull, 'w') as dev_null:
        return 0 == subprocess.call(command, shell=True, stdout=dev_null, stderr=dev_null)

def is_command_successful_for(paths, revision, command):
    print "Updating to revision %d..." % revision
    update(paths, revision)
    print "Testing revision %d..." % revision
    success = is_command_successful(command)
    if success:
        print "Revision %d is GOOD" % revision
    else:
        print "Revision %d is BAD" % revision
    print


def bisect(good_revision, bad_revision, paths, command):
    revision_to_test = min(good_revision, bad_revision) + (abs(good_revision - bad_revision) / 2)

    if revision_to_test in (good_revision, bad_revision):
        print "Good revision: %d" % good_revision
        print "Bad revision: %d" % bad_revision
        return

    if is_command_successful_for(paths, revision_to_test, command):
        good_revision = revision_to_test
    else:
        bad_revision = revision_to_test

    bisect(good_revision, bad_revision, paths, command)


def are_boundaries_correct(good_revision, bad_revision, paths, command):
    if not is_command_successful_for(paths, good_revision, command):
        print "ERROR: Test FAILS for provided good revision %d!" % good_revision
        return False

    if is_command_successful_for(paths, bad_revision, command):
        print "ERROR: Test SUCCEEDS for provided bad revision %d!" % bad_revision
        return False

    return True



def main():
    parser = argparse.ArgumentParser(description="Finds the revision where the test command stops/starts working")

    try:
        parser.add_argument("--good-revision", "-g", type=int, required=True, help="A revision where the test command succeeds", metavar="REVISION")
        parser.add_argument("--bad-revision", "-b", type=int, required=True, help="A revision where the test command fails", metavar="REVISION")
        parser.add_argument("--test-commands", "-t", default=[], nargs="+", required=True, help="A command that returns exit code 0 if and only if it succeeds", metavar="COMMAND")
        parser.add_argument("--paths", "-p", default=['.'], nargs="+", help="One or more paths to local Subversion repositories that should be updated", metavar="PATH")
        parser.add_argument("--skip-boundary-check", "-s", default=False, action="store_true", help="Don't execute the test for the provided good and bad revision")

        options = parser.parse_args()

        if not options.skip_boundary_check and \
           not are_boundaries_correct(options.good_revision, options.bad_revision,
                options.paths, options.test_commands):
            return 1
        bisect(options.good_revision, options.bad_revision,
                options.paths, options.test_commands)
        return 0
    except ValueError:
        parser.print_help()
        return 1

if __name__ == '__main__':
    sys.exit(main())
