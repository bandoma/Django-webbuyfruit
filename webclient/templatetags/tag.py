from django import template
register=template.Library()
@register.filter(name="nhan")
def nhan(a,b):
    return a*b

@register.filter(name="don")
def don(array,index):
    return array[index]
