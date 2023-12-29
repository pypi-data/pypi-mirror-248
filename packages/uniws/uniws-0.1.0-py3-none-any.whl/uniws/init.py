import shutil

from .core import *


class UniwsInit(App):
    def __init__(self) -> 'None':
        super().__init__(
            name='init',
            help='Initialize a workspace.',
        )
        self.arg_dir = Arg(
            name='DIR',
            help='Directory to use. Must be empty or not exist.',
            count='?',
            default=os.getcwd(),
        )
        self.add(self.arg_dir)
        self.arg_url = Arg(
            name='URL',
            sopt='u',
            lopt='git-url',
            help='Git repository URL to set as "origin".',
        )
        self.add(self.arg_url)
        self.arg_branch = Arg(
            name='NAME',
            sopt='b',
            lopt='git-branch',
            help='Branch name of the main branch.',
        )
        self.add(self.arg_branch)

    def __call__(self, bundle: 'Bundle') -> 'None':
        super().__call__(bundle)
        DIR_ROOT = os.path.realpath(bundle[self.arg_dir])
        DIR_BIN = f'{DIR_ROOT}/bin'
        DIR_ETC = f'{DIR_ROOT}/etc'
        DIR_LIB = f'{DIR_ROOT}/lib'
        DIR_TMP = f'{DIR_ROOT}/tmp'
        root_exists = os.path.exists(DIR_ROOT)
        if root_exists and os.listdir(DIR_ROOT):
            raise RuntimeError(f'{DIR_ROOT} already exists and is not empty.')
        try:
            # Git agnostic.
            os.makedirs(DIR_ROOT, 0o775, True)
            self._create_file(f'{DIR_ROOT}/.uniws')
            self._create_file(f'{DIR_ROOT}/README.md')
            self._create_file(
                f'{DIR_ROOT}/.bashrc',
                str(
                    f'# This file is sourced in the sh() function of uniws.\n'
                    f'# It also can be sourced manually, if needed.\n'
                    f'export UNIWS_DIR_ROOT="$(realpath "$(dirname ${{BASH_SOURCE[0]}})/..")"\n'
                    f'export UNIWS_DIR_BIN="${{UNIWS_DIR_ROOT}}/bin"\n'
                    f'export UNIWS_DIR_ETC="${{UNIWS_DIR_ROOT}}/etc"\n'
                    f'export UNIWS_DIR_LIB="${{UNIWS_DIR_ROOT}}/lib"\n'
                    f'export UNIWS_DIR_TMP="${{UNIWS_DIR_ROOT}}/tmp"\n'
                    f'export PATH="${{UNIWS_DIR_BIN}}:${{UNIWS_DIR_LIB}}:${{PATH}}"\n'
                    f'export PYTHONPATH="${{UNIWS_DIR_LIB}}:${{PYTHONPATH}}"\n'
                    f'export LD_LIBRARY_PATH="${{UNIWS_DIR_LIB}}:${{LD_LIBRARY_PATH}}"\n'
                    f'# Add custom environment and actions below.\n'
                ))
            os.mkdir(DIR_BIN, 0o775)
            os.mkdir(DIR_ETC, 0o775)
            os.mkdir(DIR_LIB, 0o775)
            os.mkdir(DIR_TMP, 0o775)
            # Git aware.
            url = bundle[self.arg_url]
            branch = bundle[self.arg_branch]
            if not (url or branch):
                return
            self._create_file(f'{DIR_ROOT}/.gitmodules')
            self._create_file(
                f'{DIR_ROOT}/.gitignore',
                str(
                    f'*\n\n'
                    f'!.gitignore\n'
                    f'!.gitmodules\n'
                    f'!.bashrc\n'
                    f'!.uniws\n'
                    f'!README*\n'
                    f'!bin\n'
                    f'!bin/**\n'
                    f'!etc\n'
                    f'!etc/**\n'
                    f'!lib\n'
                    f'!lib/**\n'
                    f'!tmp\n'
                    f'!tmp/**\n'
                ))
            self._create_file(f'{DIR_BIN}/.gitignore', '*\n\n!.gitignore\n')
            self._create_file(f'{DIR_ETC}/.gitignore')
            self._create_file(f'{DIR_LIB}/.gitignore', '*\n\n!.gitignore\n')
            self._create_file(f'{DIR_TMP}/.gitignore', '*\n\n!.gitignore\n')
            opt_branch = f'-b {branch}' if branch else ''
            sh(f'git -C {DIR_ROOT} init {opt_branch}')
            sh(f'true'
               f' && git -C {DIR_ROOT} add -A'
               f' && git -C {DIR_ROOT} commit -m "Initial commit"'
               f';')
            if url:
                sh(f'git -C {DIR_ROOT} remote add origin {url}')
                self._create_file(
                    f'{DIR_ROOT}/README.md',
                    str(
                        f'```shell\n'
                        f'git clone {url}\n'
                        f'```\n'
                    ))
        except:
            shutil.rmtree(DIR_ROOT, ignore_errors=True)
            if root_exists:
                os.mkdir(DIR_ROOT)
            raise

    def _create_file(self, path: 'str', contents: 'str' = '') -> 'None':
        with open(path, 'w') as file:
            file.write(contents)
