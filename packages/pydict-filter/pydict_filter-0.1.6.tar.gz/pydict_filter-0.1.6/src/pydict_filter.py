#!/usr/bin/python3

DOT_REPLACEMENT = "(64026441-ba8a-4fa2-a46e-1ac743191dab)"

def deny_filter(filtering_dict, filter_list, current_path=""):
    """
    This function using a filter_list for removing dictionary keys recursively.

    Attributes:
    filtering_dict (dict): Some dictionary that might have a complex structure.
    current_path (str): The path in the dictionary structure that checks in the current call (for first call empty string).
    filter_list (list): Consists of filtering strings.
    If you need to remove a field in the nested dictionary then the filter string would look like this:
        top_dictionary_field.middle_dictionary_field.field_to_remove.
    If you need to remove all fields in a dictionary or nested dictionary you can use the symbol *:
        top_dictionary_field.middle_dictionary_field.*
    """

    return _generic_filter(filtering_dict=filtering_dict, current_path=current_path, filter_list=filter_list, allow_mode=False)


def allow_filter(filtering_dict, filter_list, current_path=""):
    """
        This function using a filter_list for allow dictionary keys recursively. If keys are not in this list,
        they will be deleted.

        Attributes:
        filtering_dict (dict): Some dictionary that might have a complex structure.
        current_path (str): The path in the dictionary structure that checks in the current call (for first call empty string).
        filter_list (list): Consists of filtering strings.
        If you need to allow a field in the nested dictionary then the filter string would look like this:
            top_dictionary_field.middle_dictionary_field.field_to_remove.
        If you need to allow all fields in a dictionary or nested dictionary you can use the symbol *:
            top_dictionary_field.middle_dictionary_field.*
    """

    return _generic_filter(filtering_dict=filtering_dict, current_path=current_path, filter_list=filter_list, allow_mode=True)


def check_path(check_path, filter_list):
    if check_path.replace(DOT_REPLACEMENT, "(.)") in filter_list:
        return True
    split_path = check_path.split(".")
    for filter_item in filter_list:
        safe_filter_item = filter_item.replace("(.)", DOT_REPLACEMENT)
        split_item = safe_filter_item.split(".")
        if len(split_item) == len(split_path):
            formated_path = ".".join(["*" if item == "*" else split_path[idx] for idx, item in enumerate(split_item)])
            if formated_path == safe_filter_item:
                return True
    return False


def _generic_filter(filtering_dict, filter_list, current_path="", allow_mode=False):
    delete_list = []
    for key in filtering_dict.keys():
        safe_key = key.replace(".", DOT_REPLACEMENT)
        safe_path = f"{current_path}.{safe_key}" if current_path != "" else safe_key

        if allow_mode and not check_path(safe_path, filter_list):
            delete_list.append(key)
        elif not allow_mode and check_path(safe_path, filter_list):
            delete_list.append(key)

        elif issubclass(type(filtering_dict[key]), dict) and filtering_dict[key] != {}:
            _generic_filter(filtering_dict=filtering_dict[key], current_path=safe_path, filter_list=filter_list, allow_mode=allow_mode)

        elif issubclass(type(filtering_dict[key]), list):
            if issubclass(type(next(iter(filtering_dict[key] or []), None)), dict):
                for item in filtering_dict[key]:
                    _generic_filter(filtering_dict=item, current_path=safe_path, filter_list=filter_list, allow_mode=allow_mode)

    for key in delete_list:
        filtering_dict.pop(key)
    return filtering_dict


def none_values_filter(filtering_dict, filter_list, current_path="", recursive=True, is_reversed=False):
    """
            This function using a filter_list for allow or deny dictionary's None keys recursively or not. If keys are not in this list
            and is_reversed=True, they will be deleted but if is_reversed=False, fields in filter_list will be deleted.

            Attributes:
            filtering_dict (dict): Some dictionary that might have a complex structure.
            current_path (str): The path in the dictionary structure that checks in the current call (for first call empty string).
            filter_list (list): Consists of filtering strings.
            recursive (boolean): If this param is set as True, all dictionary fields will be checked recursively otherwise only top level.
            is_reversed (boolean): If this param is set as False, filtering string in filter_list will deny None fields otherwise allow.

            If you need to check a field in the nested dictionary then the filter string would look like this:
                top_dictionary_field.middle_dictionary_field.field_to_remove.
            If you need to check all fields in a dictionary or nested dictionary you can use the symbol *:
                top_dictionary_field.middle_dictionary_field.*
        """

    delete_list = []
    for key in filtering_dict.keys():
        safe_key = key.replace(".", DOT_REPLACEMENT)
        safe_path = f"{current_path}.{safe_key}" if current_path != "" else safe_key

        if not is_reversed and check_path(safe_path, filter_list) and filtering_dict[key] is None:
            delete_list.append(key)
        elif is_reversed and not check_path(safe_path, filter_list) and filtering_dict[key] is None:
            delete_list.append(key)

        elif issubclass(type(filtering_dict[key]), dict) and filtering_dict[key] != {} and recursive:
            none_values_filter(filtering_dict=filtering_dict[key], current_path=safe_path, filter_list=filter_list, recursive=True, is_reversed=is_reversed)
        elif issubclass(type(filtering_dict[key]), list) and recursive:
            if issubclass(type(next(iter(filtering_dict[key] or []), None)), dict):
                for item in filtering_dict[key]:
                    none_values_filter(filtering_dict=item, current_path=safe_path, filter_list=filter_list, recursive=True, is_reversed=is_reversed)

    for key in delete_list:
        filtering_dict.pop(key)
    return filtering_dict
