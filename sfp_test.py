#!/usr/bin/python
"""Test Platform API 2.0 for optical transceivers"""

# Test Platform API 2.0 - optical media adapters

import sys
import re

try:
    from platform_test_common import *
except Exception as e:
    if __name__ == '__main__':
        print 'exception {} {}'.format(type(e), e)
        sys.exit(1)
    raise

platforms_dict = {
    'n3248te': {
        'num_ports': 52,
        'port_types': (((1, 52), 'sfp'))
    },
    's5212f': {
        'num_ports': 15,
        'port_types': (((1, 12), 'sfp'), ((13, 15), 'qsfp'))
    },
    's5224f': {
        'num_ports': 28,
        'port_types': (((1, 24), 'sfp'), ((25, 28), 'qsfp'))
    },
    's5232f': {
        'num_ports': 34,
        'port_types': (((1, 32), 'qsfp'), ((33, 34), 'sfp'))
    },
    's5248f': {
        'num_ports': 56,
        'port_types': (((1, 48), 'sfp'), ((49, 56), 'qsfp'))
    },
    's5296f': {
        'num_ports': 104,
        'port_types': (((1, 96), 'sfp'), ((97, 104), 'qsfp'))
    },
    's6000': {
        'num_ports': 32,
        'port_types': (((1, 32), 'qsfp'))
    },
    'z9100': {
        'num_ports': 34,
        'port_types': (((1, 32), 'qsfp'), ((33, 34), 'sfp'))
    },
    'z9264f': {
        'num_ports': 66,
        'port_types': (((1, 64), 'qsfp'), ((65, 66), 'sfp'))
    },
    'z9332f': {
        'num_ports': 34,
        'port_types': (((1, 32), 'qsfp56-dd'), ((33, 34), 'sfp'))
    },
    'z9432f': {
        'num_ports': 34,
        'port_types': (((1, 32), 'qsfp56-dd'), ((33, 34), 'sfp'))
    }
}

port_num_channels_dict = {'sfp': 1, 'qsfp': 4, 'qsfp56-dd': 8}

def port_num_channels(platform_dict, port):
    for x in platform_dict['port_types']:
        if port >= x[0][0] and port <= x[0][1]:
            return port_num_channels_dict[x[1]]
    assert False

def check_channels_ints(platform_dict, port, methods_results_dict, method):
    if not check_type(port, methods_results_dict, method, list):
        return False
    present_valid, present = method_result_get(methods_results_dict, 'get_presence')
    if not present_valid:
        return True
    li = methods_results_dict[method]
    result = True
    if present is True:
        n = port_num_channels(platform_dict, port)
        if len(li) != n or any([(not isinstance(x, int)) for x in li]):
            print_item_mesg(mesg_lvl_err, port, '{}() invalid'.format(method))
            print_mesg(mesg_lvl_info, 'expected list, of length {}, of ints'.format(n))
            result = False
    if present is False and len(li) != 0:
        print_item_mesg(mesg_lvl_err, errid, '{}() invalid'.format(method))
        print_mesg(mesg_lvl_info, 'expected empty list')
        result = False
    return result

def check_xcvr_info_str_na_if_absent(port, methods_results_dict, method, xcvr_info, xcvr_info_key):
    x = xcvr_info[xcvr_info_key]
    if not isinstance(x, str):
        print_item_mesg(mesg_lvl_err, port, '{}() key {} invalid value'.format(method, xcvr_info_key))
        print_mesg(mesg_lvl_info, 'expected str')
        return False
    present_valid, present = method_result_get(methods_results_dict, 'get_presence')
    if not present_valid:
        return True
    if present is True and x in ('', 'N/A'):
        print_item_mesg(mesg_lvl_err, port, '{}() key {} invalid value'.format(method, xcvr_info_key))
        print_mesg(mesg_lvl_info, 'expected not one of (\'\', \'N/A\')')
        return False
    if present is False and x != 'N/A':
        print_item_mesg(mesg_lvl_err, port, '{}() key {} invalid value'.format(method, xcvr_info_key))
        print_mesg(mesg_lvl_info, 'expected \'N/A\'')
        return False
    return True

def check_xcvr_info_int_0_if_absent(port, methods_results_dict, method, xcvr_info, xcvr_info_key):
    x = xcvr_info[xcvr_info_key]
    if not isinstance(x, int):
        print_item_mesg(mesg_lvl_err, port, '{}() key {} invalid value'.format(method, xcvr_info_key))
        print_mesg(mesg_lvl_info, 'expected integer')
        return False
    present_valid, present = method_result_get(methods_results_dict, 'get_presence')
    if not present_valid:
        return True
    if present is True and x == 0:
        print_item_mesg(mesg_lvl_err, port, '{}() key {} invalid value'.format(method, xcvr_info_key))
        print_mesg(mesg_lvl_info, 'expected non-zero integer')
        return False
    if present is False and x != 0:
        print_item_mesg(mesg_lvl_err, port, '{}() key {} invalid value'.format(method, xcvr_info_key))
        print_mesg(mesg_lvl_info, 'expected 0')
        return False
    return True

xcvr_info_keys_list = (
    ('type',                      check_xcvr_info_str_na_if_absent),
    ('hardwarerev',               check_xcvr_info_str_na_if_absent),
    ('serialnum',                 check_xcvr_info_str_na_if_absent),
    ('manufacturename',           check_xcvr_info_str_na_if_absent),
    ('modelname',                 check_xcvr_info_str_na_if_absent),
    ('Connector',                 check_xcvr_info_str_na_if_absent),
    ('encoding',                  check_xcvr_info_str_na_if_absent),
    ('ext_identifier',            check_xcvr_info_str_na_if_absent),
    ('ext_rateselect_compliance', check_xcvr_info_str_na_if_absent),
    ('cable_length',              check_xcvr_info_int_0_if_absent),
    ('nominal_bit_rate',          check_xcvr_info_int_0_if_absent),
    ('specification_compliance',  check_xcvr_info_str_na_if_absent),
    ('vendor_date',               check_xcvr_info_str_na_if_absent),
    ('vendor_oui',                check_xcvr_info_str_na_if_absent)
)

def check_xcvr_info(platform_dict, port, methods_results_dict, method):
    if not check_type(port, methods_results_dict, method, dict):
        return False
    result = True
    xcvr_info = dict(methods_results_dict['get_transceiver_info'])
    for key, func in xcvr_info_keys_list:
        if key not in xcvr_info:
            print_item_mesg(mesg_lvl_err, port, '{}() key {} missing'.format(method, key))
            result = False
            continue
        result &= func(port, methods_results_dict, method, xcvr_info, key)
        del xcvr_info[key]
    if xcvr_info:
        print_item_mesg(mesg_lvl_err, port, '{}() has extra keys {}'.format(method, xcvr_info.keys()))
        result = False
    return result

xcvr_thresholds_keys_list = (
    'temphighalarm', 'templowalarm', 'temphighwarning', 'templowwarning',
    'vcchighalarm', 'vcclowalarm', 'vcchighwarning', 'vcclowwarning',
    'rxpowerhighalarm', 'rxpowerlowalarm', 'rxpowerhighwarning',
    'rxpowerlowwarning', 'txpowerhighalarm', 'txpowerlowalarm',
    'txpowerhighwarning', 'txpowerlowwarning', 'txbiashighalarm', 'txbiaslowalarm',
    'txbiashighwarning', 'txbiaslowwarning'
)

def check_xcvr_threshold_info(platform_dict, port, methods_results_dict, method):
    if not check_type(port, methods_results_dict, method, dict):
        return False
    absent = methods_results_dict.get('get_presence') is False
    result = True
    xcvr_thresholds = dict(methods_results_dict['get_transceiver_threshold_info'])
    for key in xcvr_thresholds_keys_list:
        if key not in xcvr_thresholds:
            print_item_mesg(mesg_lvl_err, port, '{}() key {} missing'.format(method, key))
            result = False
            continue
        t = xcvr_thresholds[key]
        if not isinstance(t, float):
            print_item_mesg(mesg_lvl_err, port, '{}() key {} invalid type'.format(method, key))
            print_mesg(mesg_lvl_info, 'expected float')
            result = False
        elif absent and t != 0.0:
            print_item_mesg(mesg_lvl_err, port, '{}() key {} invalid'.format(method, key))
            print_mesg(mesg_lvl_info, 'expected 0.0')
            result = False
        del xcvr_thresholds[key]
    if xcvr_thresholds:
        print_item_mesg(mesg_lvl_err, port, '{}() extra keys {}'.format(method, xcvr_thresholds.keys()))
        result = False
    return result

def check_xcvr_bulk_status_bool(port, methods_results_dict, method, xcvr_bulk_status, xcvr_bulk_status_key):
    if not isinstance(xcvr_bulk_status[xcvr_bulk_status_key], bool):
        print_item_mesg(mesg_lvl_err, port, '{}() key {} invalid value'.format(method, xcvr_bulk_status_key))
        print_mesg(mesg_lvl_info, 'expected bool')
        return False
    return True

def check_xcvr_bulk_status_bool_false_if_absent(port, methods_results_dict, method, xcvr_bulk_status, xcvr_bulk_status_key):
    x = xcvr_bulk_status[xcvr_bulk_status_key]
    if not isinstance(x, bool):
        print_item_mesg(mesg_lvl_err, port, '{}() key {} invalid value'.format(method, xcvr_bulk_status_key))
        print_mesg(mesg_lvl_info, 'expected bool')
        return False
    if methods_results_dict.get('get_presence') is False and x:
        print_item_mesg(mesg_lvl_err, port, '{}() key {} incorrect'.format(method, xcvr_bulk_status_key))
        print_mesg(mesg_lvl_info, 'expected False when absent')
        return False
    return True

def check_xcvr_bulk_status_int(port, methods_results_dict, method, xcvr_bulk_status, xcvr_bulk_status_key):
    if not isinstance(xcvr_bulk_status[xcvr_bulk_status_key], int):
        print_item_mesg(mesg_lvl_err, port, '{}() key {} invalid value'.format(method, xcvr_bulk_status_key))
        print_mesg(mesg_lvl_info, 'expected int')
        return False
    return True

def check_xcvr_bulk_status_int_zero_if_absent(port, methods_results_dict, method, xcvr_bulk_status, xcvr_bulk_status_key):
    x = xcvr_bulk_status[xcvr_bulk_status_key]
    if not isinstance(x, int):
        print_item_mesg(mesg_lvl_err, port, '{}() key {} invalid value'.format(method, xcvr_bulk_status_key))
        print_mesg(mesg_lvl_info, 'expected int')
        return False
    if methods_results_dict.get('get_presence') is False and x != 0:
        print_item_mesg(mesg_lvl_err, port, '{}() key {} incorrect'.format(method, xcvr_bulk_status_key))
        print_mesg(mesg_lvl_info, 'expected 0 when absent')
        return False
    return True

xcvr_bulk_status_keys_list = (
    ('rx_los',              check_xcvr_bulk_status_bool_false_if_absent),
    ('tx_fault',            check_xcvr_bulk_status_bool_false_if_absent),
    ('reset_status',        check_xcvr_bulk_status_bool),
    ('lp_mode',             check_xcvr_bulk_status_bool),
    ('tx_disable',          check_xcvr_bulk_status_bool),
    ('tx_disable_channel',  check_xcvr_bulk_status_int),
    ('temperature',         check_xcvr_bulk_status_int_zero_if_absent),
    ('voltage',             check_xcvr_bulk_status_int_zero_if_absent)
)

xcvr_bulk_status_channel_keys_list = (
    ('tx{}bias',  check_xcvr_bulk_status_int_zero_if_absent),
    ('rx{}power', check_xcvr_bulk_status_int_zero_if_absent),
    ('tx{}power', check_xcvr_bulk_status_int_zero_if_absent)
)

def check_xcvr_bulk_status(platform_dict, port, methods_results_dict, method):
    if not check_type(port, methods_results_dict, method, dict):
        return False
    keys_list = list(xcvr_bulk_status_keys_list)
    if methods_results_dict.get('get_presence', None) is True:
        n = port_num_channels(platform_dict, port)
        for key_fmt, func in xcvr_bulk_status_channel_keys_list:
            j = 1
            while j <= n:
                keys_list.append((key_fmt.format(j), func))
                j += 1
    xcvr_bulk_status = dict(methods_results_dict[method])
    result = True
    for key, func in keys_list:
        if key not in xcvr_bulk_status:
            print_item_mesg(mesg_lvl_err, port, '{}() key {} missing'.format(method, key))
            result = False
            continue
        result &= func(port, methods_results_dict, method, xcvr_bulk_status, key)
        del xcvr_bulk_status[key]
    if xcvr_bulk_status:
        print_item_mesg(mesg_lvl_err, port, '{}() has extra keys {}'.format(method, xcvr_bulk_status.keys()))
        result = False
    return result

methods_list = (
    ('get_presence',                   check_bool_warn_if_false),
    ('get_name',                       check_non_empty_str_when_present),
    ('get_model',                      check_non_empty_str_when_present),
    ('get_serial',                     check_non_empty_str_when_present),
    ('get_reset_status',               check_boolean),
    ('get_rx_los',                     check_bool_false_if_absent),
    ('get_tx_fault',                   check_bool_false_if_absent),
    ('get_tx_disable',                 check_boolean),
    ('get_tx_disable_channel',         check_non_negative_int),
    ('get_power_override',             check_boolean),
    ('get_temperature',                check_positive_int_non_zero_when_present),
    ('get_voltage',                    check_positive_int_non_zero_when_present),
    ('get_tx_bias',                    check_channels_ints),
    ('get_tx_power',                   check_channels_ints),
    ('get_rx_power',                   check_channels_ints),
    ('get_status',                     check_status),
    ('get_lpmode',                     check_boolean),
    ('get_transceiver_info',           check_xcvr_info),
    ('get_transceiver_threshold_info', check_xcvr_threshold_info),
    ('get_transceiver_bulk_status',    check_xcvr_bulk_status)
)

def test_get(platform_dict, port, sfp):
    result = True
    methods_results_dict = {}
    for method, _ in methods_list:
        api_status, api_result = api_wrapper(port, sfp, method)
        if not api_status:
            result = False
            continue
        methods_results_dict[method] = api_result
    for method, func in methods_list:
        if method not in methods_results_dict:
            continue
        result &= func(platform_dict, port, methods_results_dict, method)
    return True

def check_tx_disable(port, sfp):
    result = True
    for x in (True, False):
        api_status, api_result = api_wrapper(port, sfp, 'tx_disable', x, check_type=bool)
        if not api_status:
            result = False
            continue
        if not api_result:
            print_item_mesg(mesg_lvl_err, port, 'tx_disable({}) failed'.format(x))
            result = False
            continue
        api_status, api_result = api_wrapper(port, sfp, 'get_tx_disable', check_type=bool)
        if not api_status:
            result = False
            continue
        if api_result != x:
            print_item_mesg(mesg_lvl_err, port, 'get_tx_disable() incorrect')
            print_mesg(mesg_lvl_info, 'expected {}'.format(x))
            result = False
    return result

def check_tx_disable_channel(platform_dict, port, sfp):
    n = port_num_channels(platform_dict, port)
    if n == 1:
        print_item_mesg(mesg_lvl_info, port, 'single channel, skipping tx_disable_channel()')
        return True
    api_status, api_result = api_wrapper(port, sfp, 'tx_disable_channel', n - 1, False, check_type=bool)
    if not api_status:
        return False
    if not api_result:
        print_item_mesg(mesg_lvl_err, port, 'tx_disable_channel({}, False) failed'.format(n - 1))
    result = True
    m = 0
    while m < n:
        for x in (True, False):
            api_status, api_result = api_wrapper(port, sfp, 'tx_disable_channel', m, x, check_type=bool)
            if not api_status:
                result = False
                continue
            if not api_result:
                print_item_mesg(mesg_lvl_err, port, 'tx_disable_channel({}, {}) failed'.format(m, x))
                result = False
                continue
            api_status, api_result = api_wrapper(port, sfp, 'get_tx_disable_channel', check_type=int)
            if not api_status:
                result = False
                continue
            expect = m if x else 0
            if api_result != expect:
                print_item_mesg(mesg_lvl_err, port, 'get_tx_disable_channel() incorrect')
                print_mesg(mesg_lvl_info, 'expected {}'.format(expect))
                result = False
        m += 1
    return result

def check_set_lpmode(port, sfp):
    result = True
    for x in (True, False):
        api_status, api_result = api_wrapper(port, sfp, 'set_lpmode', x, check_type=bool)
        if not api_status:
            result = False
            continue
        if not api_result:
            print_item_mesg(mesg_lvl_err, port, 'set_lpmode({}) failed'.format(x))
            result = False
            continue
        api_status, api_result = api_wrapper(port, sfp, 'get_lpmode', check_type=bool)
        if not api_status:
            result = False
            continue
        if api_result != x:
            print_item_mesg(mesg_lvl_err, port, 'get_lpmode() incorrect')
            print_mesg(mesg_lvl_info, 'expected {}'.format(x))
            result = False
    return result

def check_set_power_override(port, sfp):
    result = True
    for x in ((True, False), (True, True), (False, False)):
        api_status, api_result = api_wrapper(port, sfp, 'set_power_override', x[0], x[1], check_type=bool)
        if not api_status:
            result = False
            continue
        if not api_result:
            print_item_mesg(mesg_lvl_err, port, 'set_power_override({}, {}) failed'.format(x[0], x[1]))
            result = False
            continue
        if not x[0]:
            continue
        api_status, api_result = api_wrapper(port, sfp, 'get_power_override', check_type=bool)
        if not api_status:
            result = False
            continue
        if api_result != x[1]:
            print_item_mesg(mesg_lvl_err, port, 'get_power_override() incorrect')
            print_mesg(mesg_lvl_info, 'expected {}'.format(x[1]))
            result = False
    return result

def check_reset(platform_dict, port, sfp):
    api_status, api_result = api_wrapper(port, sfp, 'reset', check_type=bool)
    if not api_status:
        return False
    if not api_result:
        print_item_mesg(mesg_lvl_err, port, 'reset() failed')
        return False
    result = True
    api_status, api_result = api_wrapper(port, sfp, 'get_tx_disable', check_type=bool)
    if not api_status:
        result = False
    elif api_result:
        print_item_mesg(mesg_lvl_err, port, 'get_tx_disable() incorrect')
        print_mesg(mesg_lvl_info, 'expected False')
        result = False
    n = port_num_channels(platform_dict, port)
    if n > 1:
        api_status, api_result = api_wrapper(port, sfp, 'get_tx_disable_channel', check_type=int)
        if not api_status:
            result = False
        elif api_result != 0:
            print_item_mesg(mesg_lvl_err, port, 'get_tx_disable_channel() incorrect')
            print_mesg(mesg_lvl_info, 'expected 0')
            result = False
    api_status, api_result = api_wrapper(port, sfp, 'get_lpmode', check_type=bool)
    if not api_status:
        result = False
    elif api_result:
        print_item_mesg(mesg_lvl_err, port, 'get_lpmode() incorrect')
        print_mesg(mesg_lvl_info, 'expected False')
        result = False
    return result

def test_set(platform_dict, port, sfp):
    pmon_pause()
    result = check_tx_disable(port, sfp)
    result &= check_tx_disable_channel(platform_dict, port, sfp)
    result &= check_set_lpmode(port, sfp)
    result &= check_set_power_override(port, sfp)
    result &= check_reset(platform_dict, port, sfp)
    pmon_unpause()
    return result

def test(platform):
    test_name_set('sfp_test')
    test_item_set('port')
    if platform not in platforms_dict:
        print_mesg(mesg_lvl_err, 'unknown platform {}'.format(platform))
        return False
    platform_dict = platforms_dict[platform]
    chassis = chassis_get()
    if chassis is None:
        return False
    api_status, sfps_list = api_wrapper(None, chassis, 'get_all_sfps', check_type=list)
    if not api_status:
        return False
    if len(sfps_list) != platform_dict['num_ports']:
        print_mesg(mesg_lvl_err, 'get_all_sfps() retuned incorrect number of ports')
        return False        
    result, num_sfps = api_wrapper(None, chassis, 'get_num_sfps', check_type=int)
    if result and num_sfps != len(sfps_list):
        print_mesg(mesg_lvl_err, 'get_num_sfps() not consistent')
        print_mesg(mesg_lvl_info, 'len(get_all_sfps()) = {}'.format(len(sfps_list)))
        result = False
    port = 0
    for sfp in sfps_list:
        port += 1
        api_status, sfp_by_idx = api_wrapper(None, chassis, 'get_sfp', port - 1)
        if api_status:
            if sfp_by_idx is not sfp:
                print_item_mesg(mesg_lvl_err, port, 'get_sfp() not consistent')
                result = False
        else:
            result = False
        try:
            idx = sfp.index
        except Exception as e:
            print_item_mesg(mesg_lvl_err, port, 'failed to get sfp index')
            print_mesg(mesg_lvl_info, 'exception {} {}'.format(type(e), e))
            result = False
        else:
            if idx != port:
                print_item_mesg(mesg_lvl_err, port, 'sfp index incorrect')
                print_mesg(mesg_lvl_info, 'expected index {}'.format(port))
                result = False
        result &= test_get(platform_dict, port, sfp)
        result &= test_set(platform_dict, port, sfp)
    return result

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Run Platform API 2.0 test for optical media adapters')
    parser.add_argument('-q', action='store_true', help='Quiet mode, no messages printed')
    parser.add_argument('-v', action='store_true', help='Verbose mode, extra messages printed')
    parser.add_argument('platform', choices=sorted(platforms_dict.keys()), help='Platform to test')
    args = parser.parse_args()
    if args.q:
        mesg_lvl_set(mesg_lvl_none)
    if args.v:
        mesg_lvl_set(mesg_lvl_all)
    sys.exit(0 if test(args.platform) else 1)
