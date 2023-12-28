import sys

import editor

# FIXME/2023-12-27: Repair test/code for Windows, which currently fails on CI:
#
#    tests\test_editor.py:7: in test_editor
#        cont = editor.edit(contents="ABC!", use_tty="use_tty" in sys.argv)
#    src\editor\__init__.py:111: in edit
#        with open(filename, mode="wb") as f:
#    E   PermissionError: [Errno 13] Permission denied:
#           'C:\\Users\\RUNNER~1\\AppData\\Local\\Temp\\tmpm64zy48i'


def test_editor(capfd):
    cont = editor.edit(contents="ABC!", use_tty="use_tty" in sys.argv)
    sys.stdout.write(cont.decode())
    out, err = capfd.readouterr()
    # I see two Warnings locally, and too many Warnings on GHA CI.
    # - Though it might be my local EDITOR setting vs. CI's.
    assert (
        err
        == (
            "Vim: Warning: Output is not to a terminal\n"
            "Vim: Warning: Input is not from a terminal\n"
        )
        or err == "Too many errors from stdin\n"
    )
