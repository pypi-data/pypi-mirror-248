from .core import *


class UniwsHardware(App):
    def __init__(self) -> 'None':
        super().__init__(
            name='hw',
            help='Hardware manipulation.',
        )
        self.add(UniwsHardwareAttach(False))
        self.add(UniwsHardwareDetach(False))
        self.add(UniwsHardwareOff(False))
        self.add(UniwsHardwareOn(False))
        self.add(UniwsHardwareShell(False))
        self.add(UniwsHardwareGet(False))
        self.add(UniwsHardwarePut(False))
        self.add(UniwsHardwareWatch(False))

    def __call__(self, bundle: 'Bundle') -> 'None':
        super().__call__(bundle)


class UniwsHardwareApp(UniwsShortcutApp):
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


class UniwsHardwareAttach(UniwsHardwareApp):
    def __init__(self, shortcut: 'bool') -> 'None':
        super().__init__(
            shortcut=shortcut,
            sname='uha',
            lname='attach',
            help='Attach to the hardware.',
            prolog=None,
            epilog=None,
        )

    def __call__(self, bundle: 'Bundle') -> 'None':
        super().__call__(bundle)


class UniwsHardwareDetach(UniwsHardwareApp):
    def __init__(self, shortcut: 'bool') -> 'None':
        super().__init__(
            shortcut=shortcut,
            sname='uhd',
            lname='detach',
            help='Detach from the hardware.',
            prolog=None,
            epilog=None,
        )

    def __call__(self, bundle: 'Bundle') -> 'None':
        super().__call__(bundle)


class UniwsHardwareOff(UniwsHardwareApp):
    def __init__(self, shortcut: 'bool') -> 'None':
        super().__init__(
            shortcut=shortcut,
            sname='uh0',
            lname='off',
            help='Power off the hardware.',
            prolog=None,
            epilog=None,
        )

    def __call__(self, bundle: 'Bundle') -> 'None':
        super().__call__(bundle)


class UniwsHardwareOn(UniwsHardwareApp):
    def __init__(self, shortcut: 'bool') -> 'None':
        super().__init__(
            shortcut=shortcut,
            sname='uh1',
            lname='on',
            help='Power on the hardware.',
            prolog=None,
            epilog=None,
        )

    def __call__(self, bundle: 'Bundle') -> 'None':
        super().__call__(bundle)


class UniwsHardwareShell(UniwsHardwareApp):
    def __init__(self, shortcut: 'bool') -> 'None':
        super().__init__(
            shortcut=shortcut,
            sname='uhs',
            lname='shell',
            help='Execute or connect to the shell.',
            prolog=None,
            epilog=None,
        )

    def __call__(self, bundle: 'Bundle') -> 'None':
        super().__call__(bundle)


class UniwsHardwareGet(UniwsHardwareApp):
    def __init__(self, shortcut: 'bool') -> 'None':
        super().__init__(
            shortcut=shortcut,
            sname='uhg',
            lname='get',
            help='Download file from the hardware.',
            prolog=None,
            epilog=None,
        )

    def __call__(self, bundle: 'Bundle') -> 'None':
        super().__call__(bundle)


class UniwsHardwarePut(UniwsHardwareApp):
    def __init__(self, shortcut: 'bool') -> 'None':
        super().__init__(
            shortcut=shortcut,
            sname='uhp',
            lname='put',
            help='Upload file to the hardware.',
            prolog=None,
            epilog=None,
        )

    def __call__(self, bundle: 'Bundle') -> 'None':
        super().__call__(bundle)


class UniwsHardwareWatch(UniwsHardwareApp):
    def __init__(self, shortcut: 'bool') -> 'None':
        super().__init__(
            shortcut=shortcut,
            sname='uhw',
            lname='watch',
            help='Watch the hardware live stream.',
            prolog=None,
            epilog=None,
        )

    def __call__(self, bundle: 'Bundle') -> 'None':
        super().__call__(bundle)
