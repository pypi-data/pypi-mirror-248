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
        template = f'{os.path.dirname(__file__)}/template'
        root = os.path.realpath(bundle[self.arg_dir])
        root_exists = os.path.exists(root)
        if root_exists and os.listdir(root):
            raise RuntimeError(f'{root} already exists and is not empty.')
        url = bundle[self.arg_url]
        branch = bundle[self.arg_branch]
        opt_branch = f'-b {branch}' if branch else ''
        try:
            sh(f'true'
               f' && mkdir -p {root}'
               f' && cp -RaT {template} {root}'
               f';')
            sh(f'git -C {root} init {opt_branch}')
            sh(f'true'
               f' && git -C {root} add -A'
               f' && git -C {root} commit -m "Initial commit"'
               f';')
            if url:
                sh(f'git -C {root} remote add origin {url}')
        except:
            if root_exists:
                sh(f'rm -rf {root}/* {root}/.* > /dev/null 2>&1', check=False)
            else:
                sh(f'rm -rf {root} > /dev/null 2>&1', check=False)
            raise
