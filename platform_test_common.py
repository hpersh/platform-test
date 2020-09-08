"""Common functions for Platfrom API 2.0 testing"""

import sys
import os

import sonic_platform

mesg_lvl_none = 0
mesg_lvl_err  = 1
mesg_lvl_warn = 2
mesg_lvl_info = 3
mesg_lvl_all  = mesg_lvl_info
mesg_lvls_map = ('', 'error', 'warning', 'info')

test_name = None
test_item = None
mesg_lvl = mesg_lvl_warn

def test_name_set(nm):
    global test_name
    test_name = nm

def test_item_set(item):
    global test_item
    test_item = item

def mesg_lvl_set(lvl):
    global mesg_lvl
    mesg_lvl = lvl
    
def print_mesg(lvl, mesg):
    if lvl <= mesg_lvl:
        print '{} {:7}: {}'.format(test_name, mesg_lvls_map[lvl], mesg)

def print_item_mesg(lvl, itemid, mesg):
    print_mesg(lvl, mesg if itemid is None else '{} {!r}: {}'.format(test_item, itemid, mesg))

def chassis_get():
    try:
        result = sonic_platform.chassis.Chassis()
    except Exception as e:
        print_mesg(mesg_lvl_err, 'failed to instantiate chassis')
        print_mesg(mesg_lvl_info, 'exception {} {}'.format(type(e), e))
        return None
    return result

def api_wrapper(errid, inst, method, *args, **kwargs):
    if kwargs.get('check_not_implemented', False):
        try:
            result = getattr(inst, method)(*args)
        except NotImplementedError:
            return True
        except Exception as e:
            print_item_mesg(mesg_lvl_err, errid, '{}{} failed with unexpected exception'.format(method, args))
            print_mesg(mesg_lvl_info, 'exception {} {}'.format(type(e), e))
        else:
            print_item_mesg(mesg_lvl_err, errid, '{}{} raised no exception'.format(method, args))
        return False
    try:
        result = getattr(inst, method)(*args)
    except Exception as e:
        print_item_mesg(mesg_lvl_err, errid, '{}{} failed'.format(method, args))
        print_mesg(mesg_lvl_info, 'exception {} {}'.format(type(e), e))
        return False, None
    print_item_mesg(mesg_lvl_info, errid, '{}{} => {!r}'.format(method, args, result))
    if 'check_type' in kwargs and not isinstance(result, kwargs['check_type']):
        print_item_mesg(mesg_lvl_err, errid, '{}{} returned invalid type'.format(method, args))
        print_mesg(mesg_lvl_info, 'expected {}'.format(kwargs['check_type']))
        return False, result
    return True, result

def method_result_get(methods_results_dict, method):
    if method not in methods_results_dict:
        return False, None
    return True, methods_results_dict[method]

def check_type(errid, methods_results_dict, method, type_):
    if isinstance(methods_results_dict[method], type_):
        return True
    print_item_mesg(mesg_lvl_err, errid, '{}() invalid type'.format(method))
    print_mesg(mesg_lvl_info, 'expected {}'.format(type_))
    return False

def check_boolean(platform_dict, errid, methods_results_dict, method):
    return check_type(errid, methods_results_dict, method, bool)

def check_bool_warn_if_false(platform_dict, errid, methods_results_dict, method):
    if not check_type(errid, methods_results_dict, method, bool):
        return False
    if not methods_results_dict[method]:
        print_item_mesg(mesg_lvl_warn, errid, '{}() is False'.format(method))
    return True

def check_bool_false_if_absent(platform_dict, errid, methods_results_dict, method):
    if not check_type(errid, methods_results_dict, method, bool):
        return False
    if methods_results_dict.get('get_presence') is False and methods_results_dict[method]:
        print_item_mesg(mesg_lvl_err, errid, '{}() returned True when absent'.format(method))
        return False
    return True

def check_status(platform_dict, errid, methods_results_dict, method):
    if not check_type(errid, methods_results_dict, method, bool):
        return False
    status = methods_results_dict[method]
    present_valid, present = method_result_get(methods_results_dict, 'get_presence')
    if not present_valid:
        return True
    if present is True and not status:
        print_item_mesg(mesg_lvl_warn, errid, '{}() is False'.format(method))
    if present is False and status:
        print_item_mesg(mesg_lvl_err, errid, '{}() incorrect'.format(method))
        print_mesg(mesg_lvl_info, 'expected False when absent')
        return False
    return True

def check_non_empty_str(platform_dict, errid, methods_results_dict, method):
    if not check_type(errid, methods_results_dict, method, str):
        return False
    if methods_results_dict[method] == '':
        print_item_mesg(mesg_lvl_err, errid, '{}() invalid'.format(method))
        print_mesg(mesg_lvl_info, 'expected non-empty string')
        return False
    return True

def check_non_empty_str_when_present(platform_dict, errid, methods_results_dict, method):
    if not check_type(errid, methods_results_dict, method, str):
        return False
    present_valid, present = method_result_get(methods_results_dict, 'get_presence')
    if not present_valid:
        return True
    s = methods_results_dict[method]
    if present is True and s == '':
        print_item_mesg(mesg_lvl_err, errid, '{}() invalid'.format(method))
        print_mesg(mesg_lvl_info, 'expected non-empty string')
        return False
    if present is False and s != '':
        print_item_mesg(mesg_lvl_err, errid, '{}() invalid'.format(method))
        print_mesg(mesg_lvl_info, 'expected empty string')
        return False
    return True

def check_non_empty_str_na_if_absent(platform_dict, errid, methods_results_dict, method):
    if not check_type(errid, methods_results_dict, method, str):
        return False
    s = methods_results_dict[method]
    present_valid, present = method_result_get(methods_results_dict, 'get_presence')
    if not present_valid:
        return True
    if present is True and s in ('', 'NA'):
        print_item_mesg(mesg_lvl_err, errid, '{}() incorrect'.format(method))
        print_mesg(mesg_lvl_info, 'expected str not one of (\'\', \'NA\') when present')
        return False
    if present is False and s != 'NA':
        print_item_mesg(mesg_lvl_err, errid, '{}() incorrect'.format(method))
        print_mesg(mesg_lvl_info, 'expected \'NA\' when absent')
        return False
    return True

def check_positive_int(platform_dict, errid, methods_results_dict, method):
    if not check_type(errid, methods_results_dict, method, int):
        return False
    if methods_results_dict[method] <= 0:
        print_item_mesg(mesg_lvl_err, errid, '{}() invalid'.format(method))
        print_mesg(mesg_lvl_info, 'expected integer > 0')
        return False
    return True

def check_non_negative_int(platform_dict, errid, methods_results_dict, method):
    if not check_type(errid, methods_results_dict, method, int):
        return False
    if methods_results_dict[method] < 0:
        print_item_mesg(mesg_lvl_err, errid, '{}() invalid'.format(method))
        print_mesg(mesg_lvl_info, 'expected integer >= 0')
        return False
    return True

def check_positive_int_non_zero_when_present(platform_dict, errid, methods_results_dict, method):
    if not check_type(errid, methods_results_dict, method, int):
        return False
    x = methods_results_dict[method]
    present_valid, present = method_result_get(methods_results_dict, 'get_presence')
    if not present_valid:
        return True
    if present is True and x <= 0:
        print_item_mesg(mesg_lvl_err, errid, '{}() incorrect'.format(method))
        print_mesg(mesg_lvl_info, 'expected > 0 when present')
        return False
    if present is False and x != 0:
        print_item_mesg(mesg_lvl_err, errid, '{}() incorrect'.format(method))
        print_mesg(mesg_lvl_info, 'expected 0 when absent')
        return False
    return True

def check_str_in_list(platform_dict, errid, methods_results_dict, method, expected):
    if not check_type(errid, methods_results_dict, method, str):
        print_item_mesg(mesg_lvl_err, errid, '{}() invalid'.format(method))
        print_mesg(mesg_lvl_info, 'expected str')
        return False
    if methods_results_dict[method] not in expected:
        print_item_mesg(mesg_lvl_err, errid, '{}() invalid'.format(method))
        print_mesg(mesg_lvl_info, 'expected one of {}'.format(expected))
        return False
    return True

def check_status_led(platform_dict, errid, methods_results_dict, method):
    return check_str_in_list(platform_dict, errid, methods_results_dict, method, ('green', 'amber', 'red', 'off'))

def pmon_pause():
    os.system('docker pause pmon >/dev/null 2>&1')

def pmon_unpause():
    os.system('docker unpause pmon >/dev/null 2>&1')
