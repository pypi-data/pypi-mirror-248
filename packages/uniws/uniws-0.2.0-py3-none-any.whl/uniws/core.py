import sys
import glob
import json
import os

from argapp.cli import *
from argapp.log import *
from argapp.shell import *
from argapp.shell import sh as _sh


def __pwd() -> 'str':
    return os.path.abspath(os.getenv('PWD'))


def __root() -> 'str':
    '''
    Get the first directory that contains a .uniws file.

    Returns:
     * If .uniws is found, returns an absoulte path to its directory.
     * str().
    '''
    result = __pwd()
    while result != '/':
        if os.path.exists(f'{result}/.uniws'):
            return result
        result = os.path.dirname(result)
    return str()


DIR_PWD = __pwd()
'''Current working directory (symlinks unresolved).'''
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

    def __call__(self, bundle: 'Bundle') -> 'None':
        super().__call__(bundle)
        if not DIR_ROOT:
            raise RuntimeError(
                f'No uniws workspace found in the entire path: {DIR_PWD}')


#
# Hardware.
#


class Terminal:
    '''
    This is a data class that represents a terminal associated with a Hardware
    instance. Aside from name, its properties determine which terminals will be
    available to certain commands.
    Instances of this class are added to Hardware.ttys and used by commands.
    '''

    def __init__(
        self,
        name: 'str',
        connect: 'object',
        execute: 'object',
        transfer: 'object',
    ) -> 'None':
        self.__name = name
        self.__connect = connect
        self.__execute = execute
        self.__transfer = transfer

    @property
    def name(self) -> 'str':
        '''
        A unique name used in the command line options, never None.
        '''
        return self.__name

    @property
    def connect(self) -> 'object':
        '''
        Connection support: ssh, screen, etc.
        The value can be used as an implementation detail.
        If None, Hardware.tty cannot be used.
        '''
        return self.__connect

    @property
    def execute(self) -> 'object':
        '''
        Execution support: ssh CMD, adb shell CMD, etc.
        The value can be used as an implementation detail.
        If None, Hardware.sh cannot be used.
        '''
        return self.__execute

    @property
    def transfer(self) -> 'object':
        '''
        File transfer support: scp, adb push, adb pull, etc.
        The value can be used as an implementation detail.
        If None, Hardware.push and Hardware.pull cannot be used.
        '''
        return self.__transfer


class Hardware:
    '''
    An abstract physical setup and its associated Terminals.
    Sub-classes of this class are supposed to be added in _hw.py.
    '''

    def __init__(
        self,
        name: 'str',
        terminals: 'list[Terminal]',
    ) -> 'None':
        self.__name = name
        self.__ttys = terminals
        if not self.__ttys:
            self.__ttys.append(Terminal('default', '', '', ''))

    @property
    def name(self) -> 'str':
        '''
        A unique name used in the command line options, never None.
        '''
        return self.__name

    @property
    def ttys(self) -> 'list[Terminal]':
        '''
        A list of associated terminals.
        If empty or None, a default Terminal that supports all operations
        is added implicitly.
        If there is only one Terminal in the list, the command line interface
        will be altered to not include the positional argument "TTY". Since
        there is only one Terminal, there is no need to explicitly specify it.
        '''
        return self.__ttys

    def attach(self) -> 'None':
        '''
        Attach to the hardware.
        '''
        raise NotImplementedError('TODO')

    def detach(self) -> 'None':
        '''
        Detach from the hardware.
        '''
        raise NotImplementedError('TODO')

    def on(self) -> 'None':
        '''
        Power on the hardware.
        '''
        raise NotImplementedError('TODO')

    def off(self) -> 'None':
        '''
        Power off the hardware.
        '''
        raise NotImplementedError('TODO')

    def put(self, tty: 'Terminal', src: 'str', dst: 'str') -> 'None':
        '''
        Tranfer a file from the local machine.

        Parameters:
         * tty - Terminal to use, t.transfer is not None.
         * src - source path (local machine).
         * dst - destination path (Terminal).
        '''
        raise NotImplementedError('TODO')

    def get(self, tty: 'Terminal', src: 'str', dst: 'str') -> 'None':
        '''
        Tranfer a file to the local machine.

        Parameters:
         * tty - Terminal to use, t.transfer is not None.
         * src - source path (Terminal).
         * dst - destination path (local machine).
        '''
        raise NotImplementedError('TODO')

    def connect(self, tty: 'Terminal') -> 'None':
        '''
        Connect to the shell.

        Parameters:
         * tty - Terminal to use, tty.connect is not None.
        '''
        raise NotImplementedError('TODO')

    def execute(self, tty: 'Terminal', cmd: 'str') -> 'None':
        '''
        Execute the shell command.

        Parameters:
         * tty - Terminal to use, tty.execute is not None.
        '''
        raise NotImplementedError('TODO')

    def watch(self) -> 'None':
        '''
        Watch the live stream.
        '''
        raise NotImplementedError('TODO')


def hardware_list() -> 'list[Hardware]':
    result = hardware()
    if isinstance(result, Hardware):
        return []
    return result


def hardware_unit() -> 'Hardware':
    result = hardware()
    if not isinstance(result, Hardware):
        raise RuntimeError('Not attached.')
    return result


class ArgTerminal(Arg):
    def __init__(self, choices: 'list[str]') -> 'None':
        super().__init__(
            name='TTY',
            help='A terminal to use.',
            choices=choices,
            default=next(iter(choices)),
        )

    def __call__(self, v: 'list[str]') -> 'Terminal':
        name = super().__call__(v)
        for x in hardware_unit().ttys:
            if x.name == name:
                return x


#
# Software.
#


class Software:
    '''
    Base class for any kind of software. Also represents an action.
    '''

    def __init__(
        self,
        name: 'str',
        help: 'str',
    ) -> 'None':
        self.name = name
        self.help = help

    def fetch(self) -> 'None':
        '''
        Download the sources.
        '''
        raise NotImplementedError('TODO')

    def patch(self) -> 'None':
        '''
        Patch the sources.
        '''
        raise NotImplementedError('TODO')

    def build(self) -> 'None':
        '''
        Build the binaries.
        '''
        raise NotImplementedError('TODO')

    def install(self, hw: 'Hardware') -> 'None':
        '''
        Install binaries on the hardware.

        Parameters:
         * hw - Hardware to install on.
        '''
        raise NotImplementedError('TODO')

    def test(self, hw: 'Hardware') -> 'None':
        '''
        Test the installed binaries on the hardware.

        Parameters:
         * hw - Hardware to test on.
        '''
        raise NotImplementedError('TODO')

    def deploy(self) -> 'None':
        '''
        Prepare the release.
        '''
        raise NotImplementedError('TODO')

    def reset(self) -> 'None':
        '''
        Reset the sources.
        '''
        raise NotImplementedError('TODO')

    def clean(self) -> 'None':
        '''
        Delete the binaries.
        '''
        raise NotImplementedError('TODO')

    def wipe(self) -> 'None':
        '''
        Delete the sources.
        '''
        raise NotImplementedError('TODO')

    @staticmethod
    def git_patch(name: 'str', repos: 'list[str]' = None) -> 'None':
        '''
        Reset the Git repositories and apply patches.
        Note that all revisions are preserved under tmp/{name}.json.
        The patches are searched under etc folder - simply all .patch files.
        Note that the layout is flexible:
         * etc/{name}/subrepo/my1.patch
         * etc/{name}/subrepo/my2.patch
        and
         * etc/nested_1/{name}/subrepo/my.patch
         * etc/nested_2/{name}/subrepo/my.patch
        are equivalent and will be applied in the lexicographical order.
        Any number of nested directories is allowed.

        Parameters:
         * name  - name of the workspace under tmp. It determines where the
           nested directories end.
         * repos - paths to repositories, must be relative to the workspace
           root. If None, all repositories are patched.
        '''
        revs = Software.__git_revisions(name)
        patches = Software.__git_patches(name)
        repos = repos if repos == None else patches.keys()
        for x in repos:
            if x not in patches:
                continue
            if x not in revs:
                revs[x] = Software.__git_revision(name, x)
            Software.__git_reset(name, x, revs[x])
            patch_list = ' '.join(patches[x])
            sh(f'git -C {DIR_TMP}/{name}/{x} am {patch_list}')
        Software.__git_revisions_set(name, revs)

    @staticmethod
    def git_reset(name: 'str', repos: 'list[str]' = None) -> 'None':
        '''
        Reset the Git repositories.

        Parameters:
         * name  - name of the workspace.
         * repos - paths to repositories, must be relative to the workspace
           root. If None, all repositories in tmp/{name}.json are reset.
        '''
        revs = Software.__git_revisions(name)
        repos = repos if repos == None else revs.keys()
        for x in revs.keys():
            Software.__git_reset(name, x, revs.get(x, 'HEAD'))

    @staticmethod
    def __git_patches(name: 'str') -> 'dict[str, list[str]]':
        patch_glob = f'{DIR_ETC}/**/{name}/**/*.patch'
        result: 'dict[str, list[str]]' = {}
        for x in glob.glob(patch_glob, recursive=True):
            repo = os.path.dirname(x).partition(f'/{name}/')[2]
            if not result.get(repo, None):
                result[repo] = []
            result[repo].append(x)
        for x in result:
            result[x].sort()
        return result

    @staticmethod
    def __git_revisions(name: 'str') -> 'dict[str, str]':
        revs_file = f'{DIR_TMP}/{name}.json'
        if not os.path.exists(revs_file):
            return {}
        with open(revs_file, 'r') as x:
            return json.load(x)

    @staticmethod
    def __git_reset(name: 'str', repo: 'str', rev: 'str') -> 'None':
        sh(f'git -C {DIR_TMP}/{name}/{repo} reset --hard {rev}')

    @staticmethod
    def __git_revision(name: 'str', repo: 'str') -> 'str':
        return sh(
            cmd=f'git -C {DIR_TMP}/{name}/{repo} rev-parse HEAD',
            mode=sh_mode_cap,
        ).out.strip()

    @staticmethod
    def __git_revisions_set(name: 'str', revs: 'dict[str, str]') -> 'None':
        with open(f'{DIR_TMP}/{name}.json', 'w') as x:
            json.dump(revs, x)


class SoftwareWorkspace(Software):
    '''
    A standalone workspace. It must be fetched under self.root, which is
    set to tmp/{self.name} (absolute path).
    '''

    def __init__(self, name: 'str', help: 'str') -> 'None':
        super().__init__(name, help)
        self.root = f'{DIR_TMP}/{self.name}'

    def patch(self) -> 'None':
        '''
        Calls Software.git_patch(self.name).
        '''
        Software.git_patch(self.name)

    def reset(self) -> 'None':
        '''
        Calls Software.git_reset(self.name).
        '''
        Software.git_reset(self.name)

    def purge(self) -> 'None':
        sh(f'true'
           f' && rm -f  {self.root}.json'
           f' && rm -rf {self.root}'
           f';')


class SoftwareComponent(Software):
    '''
    SoftwareComponent is a logical part of some SoftwareWorkspace. Even if
    it is a repository, SoftwareComponent.root should refer to
    SoftwareWorkspace.root.
    '''

    def __init__(self, name: 'str', help: 'str', root: 'str') -> 'None':
        super().__init__(name, help)
        self.root = root


#
# Stubs of hardware() and software().
# Available when hw or sw command is run from a regular directory.
#


def hardware() -> 'list[Hardware] | Hardware':
    return []


def software() -> 'list[Software]':
    return []


#
# User implementation of hardware() and software().
# Available when hw or sw command is run from a uniws-based workspace.
#


if DIR_ROOT:
    sys.path.insert(0, f'{DIR_ROOT}/.uniws')
    from hardware import hardware
    from software import software
