# PYTHON_ARGCOMPLETE_OK

import sys

from .hw import *
from .init import *
from .sw import *


class UniwsMain(Main):
    def __init__(self) -> 'None':
        super().__init__(
            name='uniws',
            help='The primary application.',
        )
        self.add(UniwsInit())
        self.add(UniwsHardware())
        self.add(UniwsSoftware())


class UniwsShortcut(Main):
    def __init__(self, app_class: 'type') -> 'None':
        self.app: 'App' = app_class(True)
        super().__init__(
            name=self.app.name,
            help=self.app.help,
            prolog=self.app.prolog,
            epilog=self.app.epilog,
        )
        for x in self.app.args:
            self.add(x)

    def __call__(self, bundle: 'Bundle' = sys.argv) -> 'None':
        super().__call__(bundle)
        self.app(bundle)


#
# Entry points.
#


def uniws():
    '''
    The primary application.
    '''
    UniwsMain()()


def uha():
    '''
    Shortcut: uniws hw attach.
    '''
    UniwsShortcut(UniwsHardwareAttach)()


def uhd():
    '''
    Shortcut: uniws hw detach.
    '''
    UniwsShortcut(UniwsHardwareDetach)()


def uh0():
    '''
    Shortcut: uniws hw off.
    '''
    UniwsShortcut(UniwsHardwareOff)()


def uh1():
    '''
    Shortcut: uniws hw on.
    '''
    UniwsShortcut(UniwsHardwareOn)()


def uhs():
    '''
    Shortcut: uniws hw shell.
    '''
    UniwsShortcut(UniwsHardwareShell)()


def uhg():
    '''
    Shortcut: uniws hw get.
    '''
    UniwsShortcut(UniwsHardwareGet)()


def uhp():
    '''
    Shortcut: uniws hw put.
    '''
    UniwsShortcut(UniwsHardwarePut)()


def uhw():
    '''
    Shortcut: uniws hw watch.
    '''
    UniwsShortcut(UniwsHardwareWatch)()


def usf():
    '''
    Shortcut: uniws sw fetch.
    '''
    UniwsShortcut(UniwsSoftwareFetch)()


def usp():
    '''
    Shortcut: uniws sw patch.
    '''
    UniwsShortcut(UniwsSoftwarePatch)()


def usb():
    '''
    Shortcut: uniws sw build.
    '''
    UniwsShortcut(UniwsSoftwareBuild)()


def usi():
    '''
    Shortcut: uniws sw install.
    '''
    UniwsShortcut(UniwsSoftwareInstall)()


def ust():
    '''
    Shortcut: uniws sw test.
    '''
    UniwsShortcut(UniwsSoftwareTest)()


def usd():
    '''
    Shortcut: uniws sw deploy.
    '''
    UniwsShortcut(UniwsSoftwareDeploy)()


def usc():
    '''
    Shortcut: uniws sw clean.
    '''
    UniwsShortcut(UniwsSoftwareClean)()


def usr():
    '''
    Shortcut: uniws sw reset.
    '''
    UniwsShortcut(UniwsSoftwareReset)()


def usw():
    '''
    Shortcut: uniws sw wipe.
    '''
    UniwsShortcut(UniwsSoftwareWipe)()
