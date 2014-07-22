import sys
import os
import argparse
import subprocess

def update(modules, revision):
    command = ["svn", "up", "-r", str(revision)]
    command.extend(modules)
    with open(os.devnull, 'w') as dev_null:
        subprocess.call(command, stdout=dev_null, stderr=dev_null)

def is_command_successful(command):
    with open(os.devnull, 'w') as dev_null:
        return 0 == subprocess.call(command, shell=True, stdout=dev_null, stderr=dev_null)

def is_command_successful_for(modules, revision, command):
    print "Updating to revision %d..." % revision
    update(modules, revision)
    print "Testing revision %d..." % revision
    success = is_command_successful(command)
    if success:
        print "Revision %d is GOOD" % revision
    else:
        print "Revision %d is BAD" % revision
    print




def bisect(good_revision, bad_revision, modules, command):
    revision_to_test = min(good_revision, bad_revision) + (abs(good_revision - bad_revision) / 2)

    if revision_to_test in (good_revision, bad_revision):
        print "Good revision: %d" % good_revision
        print "Bad revision: %d" % bad_revision
        return

    if is_command_successful_for(modules, revision_to_test, command):
        good_revision = revision_to_test
    else:
        bad_revision = revision_to_test

    bisect(good_revision, bad_revision, modules, command)


def are_boundaries_correct(good_revision, bad_revision, modules, command):
    if not is_command_successful_for(modules, good_revision, command):
        print "ERROR: Test fails for good revision: %d!" % good_revision
        return False

    if is_command_successful_for(modules, bad_revision, command):
        print "ERROR: Test succeeds for bad revision: %d!" % bad_revision
        return False

    return True



def main():
    parser = argparse.ArgumentParser(description="Shows first bad revision")

    try:
        parser.add_argument("-g", "--good-revision", type=int, required=True)
        parser.add_argument("-b", "--bad-revision", type=int, required=True)
        parser.add_argument("-m", "--modules", default=['.'], nargs="+")
        parser.add_argument("-t", "--test-commands", default=[], nargs="+", required=True)
        parser.add_argument("-s", "--skip-boundary-check", default=False, action='store_true')

        options = parser.parse_args()

        if not options.skip_boundary_check and \
           not are_boundaries_correct(options.good_revision, options.bad_revision,
                options.modules, options.test_commands):
            return 1
        bisect(options.good_revision, options.bad_revision,
                options.modules, options.test_commands)
        return 0
    except ValueError:
        parser.print_help()
        return 1

if __name__ == '__main__':
    sys.exit(main())
