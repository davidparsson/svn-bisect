# svn-bisect
A bisect script with support for updating multiple local Subversion checkouts

# Usage
    usage: svn-bisect.py [-h] --good-revision REVISION --bad-revision REVISION
                         --test-commands COMMAND [COMMAND ...]
                         [--paths PATH [PATH ...]] [--skip-boundary-check]

    Finds the revision where the test command stops/starts working

    optional arguments:
      -h, --help            show this help message and exit
      --good-revision REVISION, -g REVISION
                            A revision where the test command succeeds
      --bad-revision REVISION, -b REVISION
                            A revision where the test command fails
      --test-commands COMMAND [COMMAND ...], -t COMMAND [COMMAND ...]
                            A command that returns exit code 0 if and only if it
                            succeeds
      --paths PATH [PATH ...], -p PATH [PATH ...]
                            One or more paths to local Subversion repositories
                            that should be updated
      --skip-boundary-check, -s
                            Don't execute the test for the provided good and bad
                            revision
