from typing import Callable

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


class ArgSrc(Arg):
    def __init__(self) -> 'None':
        super().__init__(
            name='SRC',
            help='Source path.',
        )


class ArgDst(Arg):
    def __init__(self) -> 'None':
        super().__init__(
            name='DST',
            help='Destination path.',
        )


class UniwsHardwareApp(UniwsShortcutApp):
    def __init__(
        self,
        shortcut: 'bool',
        sname: 'str' = None,
        lname: 'str' = None,
        help: 'str' = None,
        prolog: 'str' = None,
        epilog: 'str' = None,
        tselector: 'Callable[[Terminal], bool]' = None,
    ) -> 'None':
        super().__init__(
            shortcut=shortcut,
            sname=sname,
            lname=lname,
            help=help,
            prolog=prolog,
            epilog=epilog,
        )
        try:
            self.hw = hardware_unit()
        except RuntimeError as e:
            self.hw = None
            self.error = e
            return
        # Setup tty argument, if necessary.
        self.tty = None
        self.arg_tty = None
        if not tselector:
            return
        if len(self.hw.ttys) > 1:
            choices = [x.name for x in self.hw.ttys if tselector(x)]
            if choices:
                self.arg_tty = ArgTerminal(choices)
                self.add(self.arg_tty)
        elif len(self.hw.ttys) == 1:
            self.tty = self.hw.ttys[0]

    def __call__(self, bundle: 'Bundle') -> 'None':
        super().__call__(bundle)
        if not self.hw:
            raise self.error
        if self.arg_tty:
            self.tty = bundle[self.arg_tty]


class UniwsHardwareAttach(UniwsHardwareApp):
    def __init__(self, shortcut: 'bool') -> 'None':
        try:
            hw = hardware_unit()
            help = f'Re-attach to {hw.name}.'
        except:
            hw = hardware_list()
            help = 'Attach to the hardware.'
        super().__init__(
            shortcut=shortcut,
            sname='uha',
            lname='attach',
            help=help,
            prolog=None,
            epilog=None,
            tselector=None,
        )
        self.hw = hw
        if isinstance(self.hw, Hardware):
            return
        if len(self.hw) == 1:
            self.hw = self.hw[0]
            return
        if self.hw:
            self.arg_hw = Arg(
                name='HW',
                help='A hardware to attach to.',
                choices=[x.name for x in self.hw],
            )
        else:
            self.error = RuntimeError('There is no hardware available.')
            self.arg_hw = Arg(
                name='HW',
                help='A hardware to attach to (none available).',
            )
        self.add(self.arg_hw)

    def __call__(self, bundle: 'Bundle') -> 'None':
        super().__call__(bundle)
        # Re-attach to the current Hardware.
        if isinstance(self.hw, Hardware):
            self.hw.attach()
            return
        # Attach to the available Hardware.
        name = bundle[self.arg_hw]
        for x in self.hw:
            if x.name == name:
                x.attach()
                return


class UniwsHardwareDetach(UniwsHardwareApp):
    def __init__(self, shortcut: 'bool') -> 'None':
        super().__init__(
            shortcut=shortcut,
            sname='uhd',
            lname='detach',
            help='Detach from the hardware.',
            prolog=None,
            epilog=None,
            tselector=None,
        )

    def __call__(self, bundle: 'Bundle') -> 'None':
        super().__call__(bundle)
        self.hw.detach()


class UniwsHardwareOff(UniwsHardwareApp):
    def __init__(self, shortcut: 'bool') -> 'None':
        super().__init__(
            shortcut=shortcut,
            sname='uh0',
            lname='off',
            help='Power off the hardware.',
            prolog=None,
            epilog=None,
            tselector=None,
        )

    def __call__(self, bundle: 'Bundle') -> 'None':
        super().__call__(bundle)
        self.hw.off()


class UniwsHardwareOn(UniwsHardwareApp):
    def __init__(self, shortcut: 'bool') -> 'None':
        super().__init__(
            shortcut=shortcut,
            sname='uh1',
            lname='on',
            help='Power on the hardware.',
            prolog=None,
            epilog=None,
            tselector=None,
        )

    def __call__(self, bundle: 'Bundle') -> 'None':
        super().__call__(bundle)
        self.hw.on()


class UniwsHardwareShell(UniwsHardwareApp):
    def __init__(self, shortcut: 'bool') -> 'None':
        super().__init__(
            shortcut=shortcut,
            sname='uhs',
            lname='shell',
            help='Execute or connect to the shell.',
            prolog=None,
            epilog=None,
            tselector=lambda x: ((x.connect != None) or (x.execute != None)),
        )
        self.arg_cmd = Arg(
            name='CMD',
            help='A command to run.',
            count='*',
        )
        self.add(self.arg_cmd)

    def __call__(self, bundle: 'Bundle') -> 'None':
        super().__call__(bundle)
        cmd = ' '.join(bundle[self.arg_cmd])
        if cmd:
            if self.tty.execute:
                self.hw.execute(self.tty, cmd)
                return
            raise RuntimeError(
                f'The terminal {self.tty.name} does not support execution.')
        else:
            if self.tty.connect:
                self.hw.connect(self.tty)
                return
            raise RuntimeError(
                f'The terminal {self.tty.name} does not support connection.')


class UniwsHardwareGet(UniwsHardwareApp):
    def __init__(self, shortcut: 'bool') -> 'None':
        super().__init__(
            shortcut=shortcut,
            sname='uhg',
            lname='get',
            help='Download file from the hardware.',
            prolog=None,
            epilog=None,
            tselector=lambda x: x.transfer != None,
        )
        self.arg_src = ArgSrc()
        self.add(self.arg_src)
        self.arg_dst = ArgDst()
        self.add(self.arg_dst)

    def __call__(self, bundle: 'Bundle') -> 'None':
        super().__call__(bundle)
        self.hw.get(
            self.tty,
            bundle[self.arg_src],
            bundle[self.arg_dst],
        )


class UniwsHardwarePut(UniwsHardwareApp):
    def __init__(self, shortcut: 'bool') -> 'None':
        super().__init__(
            shortcut=shortcut,
            sname='uhp',
            lname='put',
            help='Upload file to the hardware.',
            prolog=None,
            epilog=None,
            tselector=lambda x: x.transfer != None,
        )
        self.arg_src = ArgSrc()
        self.add(self.arg_src)
        self.arg_dst = ArgDst()
        self.add(self.arg_dst)

    def __call__(self, bundle: 'Bundle') -> 'None':
        super().__call__(bundle)
        self.hw.put(
            self.tty,
            bundle[self.arg_src],
            bundle[self.arg_dst],
        )


class UniwsHardwareWatch(UniwsHardwareApp):
    def __init__(self, shortcut: 'bool') -> 'None':
        super().__init__(
            shortcut=shortcut,
            sname='uhw',
            lname='watch',
            help='Watch the hardware live stream.',
            prolog=None,
            epilog=None,
            tselector=None,
        )

    def __call__(self, bundle: 'Bundle') -> 'None':
        super().__call__(bundle)
        self.hw.watch()
