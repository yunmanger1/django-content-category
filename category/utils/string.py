#coding: utf-8
from django.template import defaultfilters
from django.template.defaultfilters import stringfilter

# Get the old slugifier
old_slugify = defaultfilters.slugify
def translat_slugify(str):
    char_translat = {
        ("а", "А", "ә", "Ә",) : "a",
        ("б", "Б",) : "b",
        ("в", "В",) : "v",
        ("г", "Г", "ғ", "Ғ",) : "g",
        ("д", "Д",) : "d",
        ("е", "Е",) : "e",
        ("ё", "Ё",) : "e",
        ("ж", "Ж",) : "j",
        ("з", "З",) : "z",
        ("и", "И", "і", "І",) : "i",
        ("й", "Й",) : "y",
        ("к", "К", "қ", "Қ",) : "k",
        ("л", "Л",) : "l",
        ("м", "М",) : "m",
        ("н", "Н", "ң", "Ң",) : "n",
        ("о", "О", "ө", "Ө",) : "o",
        ("п", "П",) : "p",
        ("р", "Р",) : "r",
        ("с", "С",) : "s",
        ("т", "Т",) : "t",
        ("у", "У", "ү", "Ү", "ұ", "Ұ",) : "u",
        ("ф", "Ф",) : "f",
        ("х", "Х", "һ", "Һ",) : "h",
        ("ц", "Ц",) : "c",
        ("ч", "Ч",) : "ch",
        ("ш", "Ш",) : "sh",
        ("щ", "Щ",) : "sh",
        ("ъ", "Ъ",) : "",
        ("ы", "Ы",) : "i",
        ("ь", "Ь",) : "",
        ("э", "Э",) : "e",
        ("ю", "Ю",) : "yu",
        ("я", "Я",) : "ya",
    }
    for chars, trans in char_translat.items():
        for char in chars:
            str = str.replace(char.decode('utf-8'), trans)
    return old_slugify(str)

defaultfilters.slugify = translat_slugify

@stringfilter
def slugify(value):
    return translat_slugify(value)
