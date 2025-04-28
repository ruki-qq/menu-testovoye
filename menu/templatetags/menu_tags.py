from django import template
from ..models import MenuItem

register = template.Library()

@register.inclusion_tag('menu/menu_template.html', takes_context=True)
def draw_menu(context, menu_name):
    request = context.get('request')
    current_path = request.path if request else ''

    items = MenuItem.objects.filter(menu_name=menu_name).order_by('order')
    items_dict = {item.id: {'item': item, 'children': [], 'active': False, 'expand': False} for item in items}

    root = []
    active_item = None

    for item in items:
        node = items_dict[item.id]
        node_url = item.get_url()
        if node_url == current_path:
            node['active'] = True
            active_item = node
        if item.parent_id is None:
            root.append(node)
        else:
            parent_node = items_dict.get(item.parent_id)
            if parent_node:
                parent_node['children'].append(node)

    if active_item:
        current = active_item
        while current:
            current['expand'] = True
            parent_id = current['item'].parent_id
            current = items_dict.get(parent_id) if parent_id else None

        for child in active_item['children']:
            child['expand'] = True

    return {'nodes': root}
