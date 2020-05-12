from django.template.defaulttags import register


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def tour_key_chek(key):
    if key not in ['sum', 'count', 'abi', 'profit']:
        return True
    return False
