#!/usr/bin/python
"""Test Platform API 2.0 for system EEPROM"""

import sys
import re

try:
    from platform_test_common import *
except Exception as e:
    if __name__ == '__main__':
        print 'exception {} {} '.format(type(e), e)
        sys.exit(1)
    raise

eeprom_keys = ('0x21', '0x22', '0x23', '0x24', '0x25', '0x26', '0x27', '0x28', '0x29',
               '0x2A', '0x2B', '0x2C', '0x2D', '0x2E', '0x2F', '0xFD', '0xFE'
               )

eeprom_keys_value_optional = ('0xFD')

eeprom_value_regexps = {
    '0x24': '([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$',
    '0x25': '[0-9]{2}/[0-9]{2}/[0-9]{4} [0-9]{2}:[0-9]{2}:[0-9]{2}$',
    '0x26': '[0-9]+$',
    '0x27': '[AX][0-9]{2}$',
    '0x29': '[0-9]+\\.[0-9]+\\.[0-9]+\\.[0-9]+-[0-9]+$',
    '0x2E': '[0-9]+\\.[0-9]+\\.[0-9]+\\.[0-9]+-[0-9]+$',
    '0xFE': '0x[0-9A-F]+$'
    }

platforms_dict = {
    'n3248te': {
        'eeprom_values': {
            '0x21': 'N3248TE-ON',
            '0x22': '0KRFFY',
            '0x28': 'x86_64-dellemc_n3248te_c3338-r0',
            '0x2A': '256',
            '0x2B': 'DNT00',
            '0x2C': 'TW',
            '0x2D': 'Dell EMC',
            '0x2F': 'BSXFXC2'
        },
        'eeprom_value_regexps': {
            '0x23':  'TW0KRFFYDNT00.*$'
        }
    },

    's5212f': {
        'eeprom_values': {
            '0x21': 'S5212F-ON',
            '0x22': '0VK93C',
            '0x28': 'X86_64-dellemc_s5212f_c3538-r0',
            '0x2A': '128',
            '0x2B': 'CES00',
            '0x2C': 'CN',
            '0x2D': 'Dell EMC',
            '0x2F': '70410Q2'
        },
        'eeprom_value_regexps': {
            '0x23': 'CN0VK93CCES00.*$'
        }
    },

    's5224f': {
        'eeprom_values': {
            '0x21': 'S5224F-ON',
            '0x22': '0Y1XFF',
            '0x28': 'x86_64-dellemc_s5224f_c3538-r0',
            '0x2A': '128',
            '0x2B': 'CES00',
            '0x2C': 'CN',
            '0x2D': 'Dell EMC',
            '0x2F': '6N410Q2'
        },
        'eeprom_value_regexps': {
            '0x23': 'CN0Y1XFFCES00.*$'
        }        
    },

    's5232f': {
        'eeprom_values': {
            '0x21': 'S5232F-ON',
            '0x22': '0RC7V6',
            '0x28': 'x86_64-dellemc_s5232f_c3538-r0',
            '0x2A': '384',
            '0x2B': 'CES00',
            '0x2C': 'CN',
            '0x2D': 'Dell EMC',
            '0x2F': 'GQZQG02'
        },
        'eeprom_value_regexps': {
            '0x23': 'CN0RC7V6CES00.*$'
        }        
    },

    's5248f': {
        'eeprom_values': {
            '0x21': 'S5248F-ON',
            '0x22': '01XR4W',
            '0x28': 'x86_64-dellemc_s5248f_c2538-r0',
            '0x2A': '256',
            '0x2B': '77931',
            '0x2C': 'CN',
            '0x2D': 'DELL EMC',
            '0x2F': 'GCPQG02'
        },
        'eeprom_value_regexps': {
            '0x23': 'CN046MRJCES00.*$'
        }
    },

    's5296f': {
        'eeprom_values': {
            '0x21': 'S5296F-ON',
            '0x22': '099K11',
            '0x28': 'X86_64-dellemc_s5296f_c3538-r0',
            '0x2A': '384',
            '0x2B': 'CES00',
            '0x2C': 'CN',
            '0x2D': 'Dell',
            '0x2F': '7XJ00Q2'
        },
        'eeprom_value_regexps': {
            '0x23': 'CN099K11CES00.*$$'
        }        
    },

    's6000': {
        'eeprom_values': {
            '0x21': 'S6000-ON',
            '0x22': '08YWFG',
            '0x28': 'x86_64-dell_s6000_s1220-r0',
            '0x2A': '129',
            '0x2B': 'CHECK THIS',
            '0x2C': 'CHECK THIS',
            '0x2D': 'DELL',
            '0x2F': 'GXY8VS1'
        },
        'eeprom_value_regexps': {
            '0x23': 'CHECK THIS'
        }        
    },

    'z9100': {
        'eeprom_values': {
            '0x21': 'Z9100-ON',
            '0x22': '03GT5N',
            '0x28': 'x86_64-dell_z9100_c2538-r0',
            '0x2A': '384',
            '0x2B': '77931',
            '0x2C': 'CN',
            '0x2D': 'DELL',
            '0x2F': '2BZRG02'
        },
        'eeprom_value_regexps': {
            '0x23': 'CN03GT5N77931.*$'
        }        
    },

    'z9264f': {
        'eeprom_values': {
            '0x21': 'Z9264F-ON',
            '0x22': '0Z9364',
            '0x28': 'x86_64-dellemc_z9264f_c3538-r0',
            '0x2A': '640',
            '0x2B': 'DND00',
            '0x2C': 'TW',
            '0x2D': 'Dell EMC',
            '0x2F': '9ND1XC2'
        },
        'eeprom_value_regexps': {
            '0x23': 'TW0Z9364DNT00.*$'
        }        
    },

    'z9332f': {
        'eeprom_values': {
            '0x21': 'Z9332F-ON',
            '0x22': '0J5HDG',
            '0x28': 'x86_64-dellemc_z9332f_d1508-r0',
            '0x2A': '384',
            '0x2B': 'CET00',
            '0x2C': 'TH',
            '0x2D': 'Dell EMC',
            '0x2F': 'A00'
        },
        'eeprom_value_regexps': {
            '0x23': 'TH0J5HDGCET00.*$'
        }        
    },

    'z9432f': {
        'eeprom_values': {
            '0x21': 'Z9432F-ON',
            '0x22': '0GM6WJ',
            '0x28': 'x86_64-dellemc_z9432f_c3538-r0',
            '0x2A': '640',
            '0x2B': 'DNT00',
            '0x2C': 'TW',
            '0x2D': 'Dell EMC',
            '0x2F': '4168PK2'
        },
        'eeprom_value_regexps': {
            '0x23': 'TW0GM6WJDNT00.*$'
        }        
    }
}

def check_eeprom_value(platform_dict, eeprom_key, eeprom_value):
    if not isinstance(eeprom_value, str):
        print_mesg(mesg_lvl_err, 'eeprom key {} incorrect type'.format(eeprom_key))
        print_mesg(mesg_lvl_info, 'expected str')
        return False
    if eeprom_key in platform_dict['eeprom_values']:
        expected = platform_dict['eeprom_values'][eeprom_key]
        if eeprom_value != expected:
            print_mesg(mesg_lvl_err, 'eeprom key {} incorrect value'.format(eeprom_key))
            print_mesg(mesg_lvl_info, 'expected {}'.format(expected))
            return False
        return True
    r = None
    if eeprom_key in eeprom_value_regexps:
        r = eeprom_value_regexps[eeprom_key]
    if eeprom_key in platform_dict['eeprom_value_regexps']:
        r = platform_dict['eeprom_value_regexps'][eeprom_key]
    if r is not None:
        if re.match(r, eeprom_value) is None:
            print_mesg(mesg_lvl_err, 'eeprom key {} badly-formed value'.format(eeprom_key))
            return False
        return True
    if eeprom_key in eeprom_keys_value_optional:
        return True
    if eeprom_value == '':
        print_mesg(mesg_lvl_err, 'eeprom key {} value is empty'.format(eeprom_key))
        return False
    return True

def check_method_against_key(platform_dict, methods_results_dict, method, key):
    print_mesg(mesg_lvl_info, 'checking method {} against eeprom key {}'.format(method, key))
    return check_eeprom_value(platform_dict, key, methods_results_dict[method])

def check_name(platform_dict, methods_results_dict, method):
    return check_method_against_key(platform_dict, methods_results_dict, method, '0x21')

def check_model(platform_dict, methods_results_dict, method):
    return check_method_against_key(platform_dict, methods_results_dict, method, '0x22')

def check_serial(platform_dict, methods_results_dict, method):
    return check_method_against_key(platform_dict, methods_results_dict, method, '0x2F')

def check_bool_true(platform_dict, methods_results_dict, method):
    if methods_results_dict[method] is not True:
        print_mesg(mesg_lvl_err, '{}() incorrect'.format(method))
        print_mesg(mesg_lvl_info, 'expected True')
        return False
    return True

def check_base_mac(platform_dict, methods_results_dict, method):
    return check_method_against_key(platform_dict, methods_results_dict, method, '0x24')

def check_serial_num(platform_dict, methods_results_dict, method):
    return check_method_against_key(platform_dict, methods_results_dict, method, '0x23')

def check_system_eeprom_info(platform_dict, methods_results_dict, method):
    system_eeprom_info = methods_results_dict[method]
    result = True
    for k in eeprom_keys:
        if k not in system_eeprom_info:
            print_mesg(mesg_lvl_err, 'EEPROM key {} missing'.format(k))
            result = False
            continue
        result &= check_eeprom_value(platform_dict, k, system_eeprom_info[k])
        del system_eeprom_info[k]
    if system_eeprom_info:
        print_mesg(mesg_lvl_err, 'unexpected EEPROM keys {}'.format(system_eeprom_info.keys()))
        result = False
    return result

methods_list = (
    ('get_name',               check_name),
    ('get_presence',           check_bool_true),
    ('get_model',              check_model),
    ('get_serial',             check_serial),
    ('get_status',             check_bool_true),
    ('get_base_mac',           check_base_mac),
    ('get_serial_number',      check_serial_num),
    ('get_system_eeprom_info', check_system_eeprom_info)
)

def test(platform):
    test_name_set('eeprom_test')
    if platform not in platforms_dict:
        print_mesg(mesg_lvl_err, 'unknown platform {}'.format(platform))
        return False
    platform_dict = platforms_dict[platform]
    chassis = chassis_get()
    if chassis is None:
        return False
    result = True
    methods_results_dict = {}
    for method, _ in methods_list:
        api_status, api_result = api_wrapper(None, chassis, method)
        if not api_status:
            result = False
            continue
        methods_results_dict[method] = api_result
    for method, func in methods_list:
        if method not in methods_results_dict:
            continue
        result &= func(platform_dict, methods_results_dict, method)
    return result

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Run Platform API 2.0 test for system EEPROM')
    parser.add_argument('-q', action='store_true', help='Quiet mode, no messages printed')
    parser.add_argument('-v', action='store_true', help='Verbose mode, extra messages printed')
    parser.add_argument('platform', choices=sorted(platforms_dict.keys()), help='Platform to test')
    args = parser.parse_args()
    if args.q:
        mesg_lvl_set(mesg_lvl_none)
    if args.v:
        mesg_lvl_set(mesg_lvl_all)
    sys.exit(0 if test(args.platform) else 1)
