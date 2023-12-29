from .core import *


class UniwsSoftware(App):
    def __init__(self) -> 'None':
        super().__init__(
            name='sw',
            help='Software manipulation.',
        )
        self.add(UniwsSoftwareFetch(False))
        self.add(UniwsSoftwarePatch(False))
        self.add(UniwsSoftwareBuild(False))
        self.add(UniwsSoftwareInstall(False))
        self.add(UniwsSoftwareTest(False))
        self.add(UniwsSoftwareDeploy(False))
        self.add(UniwsSoftwareClean(False))
        self.add(UniwsSoftwareReset(False))
        self.add(UniwsSoftwareWipe(False))

    def __call__(self, bundle: 'Bundle') -> 'None':
        super().__call__(bundle)


class UniwsSoftwareApp(UniwsShortcutApp):
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
            shortcut=shortcut,
            sname=sname,
            lname=lname,
            help=help,
            prolog=prolog,
            epilog=epilog,
        )

    def __call__(self, bundle: 'Bundle') -> 'None':
        super().__call__(bundle)


class UniwsSoftwareFetch(UniwsSoftwareApp):
    def __init__(self, shortcut: 'bool') -> 'None':
        super().__init__(
            shortcut=shortcut,
            sname='usf',
            lname='fetch',
            help='Fetch the software.',
            prolog=None,
            epilog=None,
        )

    def __call__(self, bundle: 'Bundle') -> 'None':
        super().__call__(bundle)


class UniwsSoftwarePatch(UniwsSoftwareApp):
    def __init__(self, shortcut: 'bool') -> 'None':
        super().__init__(
            shortcut=shortcut,
            sname='usp',
            lname='patch',
            help='Patch the software.',
            prolog=None,
            epilog=None,
        )

    def __call__(self, bundle: 'Bundle') -> 'None':
        super().__call__(bundle)


class UniwsSoftwareBuild(UniwsSoftwareApp):
    def __init__(self, shortcut: 'bool') -> 'None':
        super().__init__(
            shortcut=shortcut,
            sname='usb',
            lname='build',
            help='Build the software.',
            prolog=None,
            epilog=None,
        )

    def __call__(self, bundle: 'Bundle') -> 'None':
        super().__call__(bundle)


class UniwsSoftwareInstall(UniwsSoftwareApp):
    def __init__(self, shortcut: 'bool') -> 'None':
        super().__init__(
            shortcut=shortcut,
            sname='usi',
            lname='install',
            help='Install the software.',
            prolog=None,
            epilog=None,
        )

    def __call__(self, bundle: 'Bundle') -> 'None':
        super().__call__(bundle)


class UniwsSoftwareTest(UniwsSoftwareApp):
    def __init__(self, shortcut: 'bool') -> 'None':
        super().__init__(
            shortcut=shortcut,
            sname='ust',
            lname='test',
            help='Test the software.',
            prolog=None,
            epilog=None,
        )

    def __call__(self, bundle: 'Bundle') -> 'None':
        super().__call__(bundle)


class UniwsSoftwareDeploy(UniwsSoftwareApp):
    def __init__(self, shortcut: 'bool') -> 'None':
        super().__init__(
            shortcut=shortcut,
            sname='usd',
            lname='deploy',
            help='Deploy the software.',
            prolog=None,
            epilog=None,
        )

    def __call__(self, bundle: 'Bundle') -> 'None':
        super().__call__(bundle)


class UniwsSoftwareClean(UniwsSoftwareApp):
    def __init__(self, shortcut: 'bool') -> 'None':
        super().__init__(
            shortcut=shortcut,
            sname='usf',
            lname='clean',
            help='Clean the software.',
            prolog=None,
            epilog=None,
        )

    def __call__(self, bundle: 'Bundle') -> 'None':
        super().__call__(bundle)


class UniwsSoftwareReset(UniwsSoftwareApp):
    def __init__(self, shortcut: 'bool') -> 'None':
        super().__init__(
            shortcut=shortcut,
            sname='usf',
            lname='reset',
            help='Reset the software.',
            prolog=None,
            epilog=None,
        )

    def __call__(self, bundle: 'Bundle') -> 'None':
        super().__call__(bundle)


class UniwsSoftwareWipe(UniwsSoftwareApp):
    def __init__(self, shortcut: 'bool') -> 'None':
        super().__init__(
            shortcut=shortcut,
            sname='usf',
            lname='wipe',
            help='Wipe the software.',
            prolog=None,
            epilog=None,
        )

    def __call__(self, bundle: 'Bundle') -> 'None':
        super().__call__(bundle)
