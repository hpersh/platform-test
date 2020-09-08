#!/usr/bin/python
"""Test Platform API 2.0 for PSUs"""

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
        'names': ['PSU1', 'PSU2'],
        'skus': (
            {'model': 'DPS-240AB-13 A.S', 'serial': 'CN0DHYD0DED00.*$', 'mfr_id': 'DELTA', 'type': 'AC', 'capacity': 0},
        ),
        'set_methods': ('set_status_led')            
    },

    's5212f': {
        'names': ['PSU1', 'PSU2'],
        'skus': (
            {'model': '0VK93CX01', 'serial': 'CN0VK93CCES00.*$', 'mfr_id': 'DELL', 'type': 'AC', 'capacity': 0},
        ),
        'set_methods': ('set_status_led')            
    },

    's5224f': {
        'names': ['PSU1', 'PSU2'],
        'skus': (
            {'model': '02RPHXA00', 'serial': 'CNDED00.*$', 'mfr_id': 'CHECK_THIS', 'type': 'AC', 'capacity': 0},
        ),
        'set_methods': ('set_status_led')            
    },

    's5232f': {
        'names': ['PSU1', 'PSU2'],
        'skus': (
            {'model': '0HXWNFA00', 'serial': 'CNDED00.*$', 'mfr_id': 'DELL', 'type': 'AC', 'capacity': 0},
        ),
        'set_methods': ('set_status_led')            
    },

    's5248f': {
        'names': ['PSU1', 'PSU2'],
        'skus': (
            {'model': '02RPHXA00', 'serial': 'CNDED00.*$', 'mfr_id': 'DELL', 'type': 'AC', 'capacity': 0},
        ),
        'set_methods': ('set_status_led')            
    },

    's5296f': {
        'names': ['PSU1', 'PSU2'],
        'skus': (
            {'model': '0J6J4KA00', 'serial': 'CNDED00.*$', 'mfr_id': 'DELL', 'type': 'AC', 'capacity': 0},
        ),
        'set_methods': ('set_status_led')            
    },

    's6000': {
        'names': ['PSU1', 'PSU2'],
        'skus': (
            {'model': 'CHECK_THIS', 'serial': 'CHECK_THIS', 'mfr_id': 'CHECK_THIS', 'type': 'AC', 'capacity': 0},
        ),
        'set_methods': ('set_status_led')            
    },

    'z9100': {
        'names': ['PSU1', 'PSU2'],
        'skus': (
            {'model': 'CHECK_THIS', 'serial': 'CHECK_THIS', 'mfr_id': 'CHECK_THIS', 'type': 'AC', 'capacity': 0},
        ),
        'set_methods': ('set_status_led')            
    },

    'z9264f': {
        'names': ['PSU1', 'PSU2'],
        'skus': (
            {'model': '095HR5A03', 'serial': 'CNDED00.*$', 'mfr_id': 'DELL', 'type': 'AC', 'capacity': 0},
        ),
        'set_methods': ('set_status_led')            
    },

    'z9332f': {
        'names': ['PSU1', 'PSU2'],
        'skus': (
            {'model': 'TDPS1500AB6D', 'serial': 'GGCT1928.*$', 'mfr_id': 'DELTA-THAILAND', 'type': 'AC', 'capacity': 0},
        ),
        'set_methods': ('set_status_led')            
    },

    'z9432f': {
        'names': ['PSU1', 'PSU2'],
        'skus': (
            {'model': 'CHECK_THIS', 'serial': 'CHECK_THIS', 'mfr_id': 'CHECK_THIS', 'type': 'AC', 'capacity': 0},
        ),
        'set_methods': ('set_status_led')            
    }    
}

def check_name(platform_dict, errid, methods_results_dict, method):
    if not check_type(errid, methods_results_dict, method, str):
        return False
    if methods_results_dict[method] not in platform_dict['names']:
        print_item_mesg(mesg_lvl_err, errid, '{}() unknown or duplicated'.format(method))
        return False
    return True

def check_positive_int_zero_if_absent_or_no_pwr(platform_dict, errid, methods_results_dict, method):
    if not check_type(errid, methods_results_dict, method, int):
        return False
    present_valid, present = method_result_get(methods_results_dict, 'get_presence')
    pwrgood_valid, pwrgood = method_result_get(methods_results_dict, 'get_powergood_status')
    if not present_valid or not pwrgood_valid:
        return True
    i = methods_results_dict[method]
    if present is True and pwrgood is True:
        if  i <= 0:
            print_item_mesg(mesg_lvl_err, errid, '{}() invalid'.format(method))
            print_mesg(mesg_lvl_info, 'expected integer > 0')
            return False
    elif i != 0:
        print_item_mesg(mesg_lvl_err, errid, '{}() invalid'.format(method))
        print_mesg(mesg_lvl_info, 'expected 0')
        return False
    return True

def check_psu_type(platform_dict, errid, methods_results_dict, method):
    return check_str_in_list(platform_dict, errid, methods_results_dict, method, ('AC', 'DC'))

def check_sku(skus_list, errid, methods_results_dict, method):
    if methods_results_dict.get('get_presence') is not True:
        print_item_mesg(mesg_lvl_info, errid, 'not present, skipping SKU check')
        return True
    for sku in skus_list:
        if (methods_results_dict.get('get_model') == sku['model']
            and re.match(sku['serial'], methods_results_dict.get('get_serial')) is not None
            and methods_results_dict.get('get_mfr_id') == sku['mfr_id']
            ):
            print_item_mesg(mesg_lvl_info, errid, 'matches SKU model {} serial {} mfr_id {}'.format(sku['model'], sku['serial'], sku['mfr_id']))
            status, val = method_result_get(methods_results_dict, 'get_type')
            if status and val != sku['type']:
                print_item_mesg(mesg_lvl_err, errid, 'type incorrect for SKU')
                print_mesg(mesg_lvl_info, 'expected {}'.format(sku['type']))
                return False
            status, val = method_result_get(methods_results_dict, 'get_capacity')
            if status and val != sku['capacity']:
                print_item_mesg(mesg_lvl_err, errid, 'capacity incorrect for SKU')
                print_mesg(mesg_lvl_info, 'expected {}'.format(sku['capacity']))
                return False
            return True
    print_item_mesg(mesg_lvl_err, errid, 'unknown SKU')
    return False

methods_list = (
    ('get_name',             check_name),
    ('get_presence',         check_bool_warn_if_false),
    ('get_model',            check_non_empty_str_na_if_absent),
    ('get_serial',           check_non_empty_str_na_if_absent),
    ('get_status',           check_status),
    ('get_voltage',          check_positive_int_zero_if_absent_or_no_pwr),
    ('get_current',          check_positive_int_zero_if_absent_or_no_pwr),
    ('get_input_voltage',    check_positive_int_zero_if_absent_or_no_pwr),
    ('get_input_current',    check_positive_int_zero_if_absent_or_no_pwr),
    ('get_power',            check_positive_int_zero_if_absent_or_no_pwr),
    ('get_powergood_status', check_bool_false_if_absent),
    ('get_mfr_id',           check_non_empty_str_na_if_absent),
    ('get_status_led',       check_status_led),
    ('get_type',             check_psu_type),
    ('get_capacity',         check_positive_int_zero_if_absent_or_no_pwr)
)

def test(platform):
    test_name_set('psu_test')
    test_item_set('psu')
    if platform not in platforms_dict:
        print_mesg(mesg_lvl_err, 'unknown platform {}'.format(platform))
        return False
    platform_dict = dict(platforms_dict[platform])
    chassis = chassis_get()
    if chassis is None:
        return False
    api_status, psus_list = api_wrapper(None, chassis, 'get_all_psus', check_type=list)
    if not api_status:
        return False
    result, num_psus = api_wrapper(None, chassis, 'get_num_psus', check_type=int)
    if result and num_psus != len(psus_list):
        print_mesg(mesg_lvl_err, 'get_num_psus() not consistent')
        print_mesg(mesg_lvl_info, 'len(get_all_psus()) = {}'.format(len(psus_list)))
        result = False
    idx = -1
    for psu in psus_list:
        idx += 1
        api_status, psu_by_idx = api_wrapper(None, chassis, 'get_psu', idx)
        if api_status:
            if psu_by_idx is not psu:
                print_mesg(mesg_lvl_err, 'get_psu({}) not consistent'.format(idx))
                result = False
        else:
            result = False
        methods_results_dict = {}
        errid = psu
        name = None
        for method, _ in methods_list:
            api_status, api_result = api_wrapper(errid, psu, method)
            if not api_status:
                result = False
                continue
            methods_results_dict[method] = api_result
            if method == 'get_name' and api_status:
                name = api_result
                errid = api_result
        for method, func in methods_list:
            if method not in methods_results_dict:
                continue
            result &= func(platform_dict, errid, methods_results_dict, method)
        result &= check_sku(platform_dict['skus'], errid, methods_results_dict, method)
        if name in platform_dict['names']:
            platform_dict['names'].remove(name)
    if platform_dict['names']:
        print_mesg(mesg_lvl_err, 'missing psus {}'.format(platform_dict['names']))
        result = False
    return result

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Run Platform API 2.0 test for psus')
    parser.add_argument('-q', action='store_true', help='Quiet mode, no messages printed')
    parser.add_argument('-v', action='store_true', help='Verbose mode, extra messages printed')
    parser.add_argument('platform', choices=sorted(platforms_dict.keys()), help='Platform to test')
    args = parser.parse_args()
    if args.q:
        mesg_lvl_set(mesg_lvl_none)
    if args.v:
        mesg_lvl_set(mesg_lvl_all)
    sys.exit(0 if test(args.platform) else 1)
