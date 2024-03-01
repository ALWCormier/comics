from django import template

register = template.Library()


@register.filter(name="comics_in_series")
def comics_in_series(series_list, series):
    return series_list[series]


@register.filter(name="cover")
def cover(obj):
    return obj["cover"]


@register.filter(name="obj_name")
def obj_name(obj):
    return obj["name"]


@register.filter(name="number")
def number(obj):
    return obj["number"]


@register.filter(name="add_id")
def add_id(base, addon):
    return f"{base}_{str(addon)}"


@register.filter(name="obj_id")
def obj_id(obj):
    return obj["id"]


@register.filter(name="modal_target")
def modal_target(obj):
    return f"modal{obj[id]}"


@register.filter(name="variant_list")
def variant_list(obj):
    vlist = obj["variants"]

    return vlist


@register.filter(name="variant_name")
def variant_list(obj):
    return obj["name"]


@register.filter(name="variant_data")
def variant_list(obj):
    return [obj["name"], obj["image"]]


@register.filter(name="issue_formbundle")
def issue_formbundle(obj, series_data):
    return {"name": series_data[0], "number": obj["number"], "series_cgid": series_data[1], "issue_cgid": obj["id"],
            "cover": obj["cover"]}
