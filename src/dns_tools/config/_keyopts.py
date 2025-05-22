# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
 Initialize for dns-tool
 All controls are command line arguments.
"""
# pylint: disable=too-many-instance-attributes,too-few-public-methods


class KeyOpts:
    """
    Options for ksk or zsk keys
    """
    def __init__(self, ktype: str):
        self.ktype: str = ktype
        self.gen_curr: bool = False
        self.gen_next: bool = False
        self.roll_1: bool = False
        self.roll_2: bool = False
        self.sign_curr: bool = False
        self.sign_next: bool = False
        self.algo: str = 'ED25519'

        if ktype not in ('ksk', 'zsk'):
            raise ValueError(f'Key type error: {ktype} must be ksk or zsk')

    def set_opt(self, key: str, val: bool | str):
        """
        Set corresponding option for self.ktype

            ksk_xxx, zsk_ksk => xxx
            gen_ksk_xxx, gen_zsk_xxx => gen_xxx
        """
        txt = self.ktype + '_'
        new_key = key.replace(txt, '')
        setattr(self, new_key, val)

    def check_options(self) -> tuple[bool, str]:
        """
        Check options

        Returns:
            tuple[success: bool, msg: str]
            success is True if all ok.
            If not ok then error message is returned
        """
        #
        # roll phase 1 and 2 are mutually exclusive - either but not both
        #
        full_msg = ''
        success = True
        if self.roll_1 and self.roll_2:
            ktype = self.ktype
            full_msg = f'Error: {ktype}_roll must be phase 1 or 2 not both'
            success = False
            # return (False, msg)

        (okay, msg) = self._algo_check()
        if not okay:
            success = False
            full_msg += '\n' + msg
        return (success, msg)

    def do_sign(self) -> bool:
        """
        return true if sign_curr or sign_next is true
         """
        if self.sign_curr or self.sign_next:
            return True
        return False

    def _algo_check(self) -> tuple[bool, str]:
        """
        Check algo is supported.

        Returns:
            (okay: bool, message: str)
        """
        if not self.algo:
            return (False, 'Missing algo')

        supported = ['ECDSAP256SHA256', 'ECDSAP384SHA384',
                     'ED25519', 'ED448']

        if self.algo.upper() not in supported:
            msg = f'Error : Unsupported key algorithm {self.algo}'
            msg += f'      : Must be {supported}'
            return (False, msg)
        return (True, '')


class KeyOptions:
    """
    KSK / ZSK Key Options
    """
    def __init__(self):
        self.ksk: KeyOpts = KeyOpts('ksk')
        self.zsk: KeyOpts = KeyOpts('zsk')

        self.serial_bump: bool = False
        self.sign: bool = False
        self.print_keys: bool = False
        self.do_keys: bool = False

    def check(self) -> tuple[bool, str]:
        """
        Valid option check.
        """
        full_msg = ''
        success = True
        (good, msg) = self.ksk.check_options()
        if not good:
            success = False
            full_msg = 'ksk: ' + msg + '\n'

        (good, msg) = self.zsk.check_options()
        if not good:
            success = False
            full_msg = 'zsk: ' + msg + '\n'

        if not success:
            return (False, full_msg)
        return (True, '')

    def implied_options(self):
        """
        Some requests require additional actions.
        """
        if self.ksk.roll_1:
            self.ksk.gen_next = True
            self.ksk.sign_curr = True
            self.ksk.sign_next = True

            self.zsk.sign_curr = True

            self.serial_bump = True
            self.sign = True

        if self.ksk.roll_2:
            self.ksk.sign_curr = True
            self.zsk.sign_curr = True

            self.serial_bump = True
            self.sign = True

        if self.zsk.roll_1:
            self.zsk.gen_next = True
            self.zsk.sign_curr = True
            self.zsk.sign_next = True

            self.ksk.sign_curr = True

            self.serial_bump = True
            self.sign = True

        if self.zsk.roll_2:
            self.ksk.sign_curr = True
            self.zsk.sign_curr = True

            self.serial_bump = True
            self.sign = True

        if self.serial_bump:
            self.sign = True    # keep consistent, change zone must re-sign

        if self.sign:
            self.ksk.sign_curr = True
            self.zsk.sign_curr = True

        if self.ksk.do_sign():
            self.sign = True

        if self.zsk.do_sign():
            self.sign = True

        if self.zsk.gen_curr or self.zsk.gen_next:
            self.do_keys = True

        if self.ksk.gen_curr or self.ksk.gen_next:
            self.do_keys = True

        if self.zsk.sign_curr or self.zsk.sign_next:
            self.sign = True

        if self.ksk.sign_curr or self.ksk.sign_next:
            self.sign = True

    def do_sign(self):
        """ return true if sign_curr or sign_next is true """
        if self.ksk.sign_curr or self.ksk.sign_next:
            return True
        if self.zsk.sign_curr or self.zsk.sign_next:
            return True
        return False
