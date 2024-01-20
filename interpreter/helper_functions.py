def replace_value(nested_list, value_before, value_after):
    '''
    Written by GPT 3

    :param nested_list:
    :param value_before:
    :param value_after:
    :return:

    #example
    nested_list = [[1,2,3], [4,5,6], [7,8,9]]
    value_before = 8
    value_after = 10

    print(replace_value(nested_list, value_before, value_after))
    #[[1,2,3], [4,5,6], [7,10,9]]
    '''
    for sublist in nested_list:
        if isinstance(sublist, list):
            replace_value(sublist, value_before, value_after)
        else:
            if sublist == value_before:
                sublist = value_after
    return nested_list