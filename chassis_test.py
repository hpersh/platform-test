#!/usr/bin/python
"""Test Platform API 2.0 for chassis"""

import sys

try:
    from platform_test_common import *
except Exception as e:
    if __name__ == '__main__':
        print 'exception {} {}'.format(type(e), e)
        sys.exit(1)
    raise

def test(mesg_lvl):
    test_name_set('chassis_test')
    chassis = chassis_get()
    if chassis is None:
        return False
    result = True
    api_status, reboot_cause = api_wrapper(None, chassis, 'get_reboot_cause')
    if api_status:
        if not (isinstance(reboot_cause, tuple) and len(reboot_cause) == 2 and all([isinstance(x, str) for x in reboot_cause])):
            print_mesg(mesg_lvl_err, 'get_reboot_cause() invalid type')
            print_mesg(mesg_lvl_info, 'expected tuple of strings, length 2')
            result = False
    else:
        result = False
    return result
        
if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Run Platform API 2.0 test for chassis')
    parser.add_argument('-q', action='store_true', help='Quiet mode, no messages printed')
    parser.add_argument('-v', action='store_true', help='Verbose mode, extra messagesprinted')
    args = parser.parse_args()
    if args.q:
        mesg_lvl_set(mesg_lvl_none)
    if args.v:
        mesg_lvl_set(mesg_lvl_all)
    sys.exit(0 if test(mesg_lvl) else 1)
