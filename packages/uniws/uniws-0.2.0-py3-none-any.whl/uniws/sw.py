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
        needs_hw: 'bool' = None,
    ) -> 'None':
        super().__init__(
            shortcut=shortcut,
            sname=sname,
            lname=lname,
            help=help,
            prolog=prolog,
            epilog=epilog,
        )
        choices = {}
        self.needs_hw = needs_hw
        self.software = {x.name: x for x in software()}
        for x in self.software.values():
            if getattr(type(x), lname) != getattr(Software, lname):
                choices[x.name] = x.help
        if choices:
            self.arg_sw = Arg(
                name='SW',
                help=f'Software to {lname}.',
                choices=choices,
            )
        else:
            self.arg_sw = Arg(
                name='SW',
                help=f'Software to {lname} (none available).',
            )
        self.lname = lname
        self.add(self.arg_sw)

    def __call__(self, bundle: 'Bundle') -> 'None':
        super().__call__(bundle)
        if not self.arg_sw.choices:
            raise RuntimeError('There is no software.')
        sw = bundle[self.arg_sw]
        if self.needs_hw:
            getattr(self.software[sw], self.lname)(hardware_unit())
        else:
            getattr(self.software[sw], self.lname)()


class UniwsSoftwareFetch(UniwsSoftwareApp):
    def __init__(self, shortcut: 'bool') -> 'None':
        super().__init__(
            shortcut=shortcut,
            sname='usf',
            lname='fetch',
            help='Fetch the software.',
            prolog=None,
            epilog=None,
            needs_hw=False,
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
            needs_hw=False,
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
            needs_hw=False,
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
            needs_hw=True,
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
            needs_hw=True,
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
            needs_hw=False,
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
            needs_hw=False,
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
            needs_hw=False,
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
            needs_hw=False,
        )

    def __call__(self, bundle: 'Bundle') -> 'None':
        super().__call__(bundle)
