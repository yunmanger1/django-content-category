from django.utils.safestring import mark_safe

def build_attrs_string(attrs):
    box = []
    for key, value in attrs.items():
        box.append(u"{0}=\"{1}\"".format(key, value))
    return mark_safe(" ".join(box))
