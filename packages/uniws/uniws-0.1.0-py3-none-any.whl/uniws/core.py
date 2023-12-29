import os

from argapp.cli import *
from argapp.log import *
from argapp.shell import *
from argapp.shell import sh as _sh


def __root() -> 'str':
    '''
    Get the first directory that contains a .uniws file.

    Returns:
     * If .uniws is found, returns an absoulte path to its directory.
     * str().
    '''
    result = os.path.abspath(os.getenv('PWD'))
    while result != '/':
        if os.path.exists(f'{result}/.uniws'):
            return result
        result = os.path.dirname(result)
    return str()


DIR_ROOT = __root()
'''The root is the first directory that contains a .uniws file.'''
DIR_BIN = f'{DIR_ROOT}/bin'
'''{DIR_ROOT}/bin - executable files, added to PATH.'''
DIR_ETC = f'{DIR_ROOT}/etc'
'''{DIR_ROOT}/etc - persistent files.'''
DIR_LIB = f'{DIR_ROOT}/lib'
'''{DIR_ROOT}/lib - source and binary files, added to PATH, PYTHONPATH and LD_LIBRARY_PATH.'''
DIR_TMP = f'{DIR_ROOT}/tmp'
'''{DIR_ROOT}/tmp - software workspaces and temporary files.'''


def sh(
    cmd: 'str',
    check: 'bool' = True,
    mode: 'object' = sh_mode_sub,
) -> 'ShellResult':
    '''
    Execute a command using /bin/bash.
    This is a wrapper around argapp.shell.sh(): additionally sources
    {DIR_ROOT}/.bashrc, if it exists.

    Parameters:
     * cmd   - command to execute.
     * check - whether to raise ShellError if cmd fails.
     * mode  - determines how to handle the output of cmd.
               Must be set to one of sh_mode_* values.

    Raises:
     * ShellError, if check is True and cmd failed.

    Return:
     * ShellResult.
    '''
    bashrc = f'{DIR_ROOT}/.bashrc'
    if os.path.exists(bashrc):
        cmd = f'source {bashrc};\n{cmd}'
    else:
        PATH = f'export PATH="{DIR_BIN}:{DIR_LIB}:${{PATH}}"'
        PYTHONPATH = f'export PYTHONPATH="{DIR_LIB}:${{PYTHONPATH}}"'
        LD_LIBRARY_PATH = f'export LD_LIBRARY_PATH="{DIR_LIB}:${{LD_LIBRARY_PATH}}"'
        cmd = f'{PATH};{PYTHONPATH};{LD_LIBRARY_PATH};{cmd}'
    _sh(cmd, check, mode)


class UniwsShortcutApp(App):
    def __init__(
        self,
        shortcut: 'bool',
        sname: 'str' = None,
        lname: 'str' = None,
        help: 'str' = None,
        prolog: 'str' = None,
        epilog: 'str' = None,
    ) -> 'None':
        super().__init__(
            name=sname if shortcut else lname,
            help=help,
            prolog=prolog,
            epilog=epilog,
        )
