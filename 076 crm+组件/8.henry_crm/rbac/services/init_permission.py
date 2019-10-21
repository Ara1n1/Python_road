from django.conf import settings


def init_permission(request, obj):
    request.session['user_id'] = obj.pk
    request.session['is_login'] = True
    permissions = obj.roles.exclude(permissions__url__isnull=True).values(
        # url和title用于菜单标题和链接
        'permissions__url',
        'permissions__title',
        'permissions__name',          # 权限控制到按钮级别
        # 菜单相关
        'permissions__menu__icon',
        'permissions__menu__title',
        'permissions__menu_id',       # 二级菜单关联的外键
        'permissions__menu__weight',  # 优先级，用于对一级菜单的排序
        # 二级菜单的子菜单，和面包屑
        'permissions__parent_id',
        'permissions__parent__name',
        'permissions__id',
    ).distinct()

    # 构造权限和菜单字典
    permission_dic = {}
    menu_dic = {}
    for i in permissions:
        # 构造权限信息
        permission_dic[i['permissions__name']] = {
            'url': i.get('permissions__url', None),
            'title': i.get('permissions__title', None),
            # id 和 pid 用于访问二级菜单中的子菜单时，保持二级菜单处于活跃状态
            'id': i.get('permissions__id', None),
            'pid': i.get('permissions__parent_id', None),
            'pname': i.get('permissions__parent__name', None),
        }

        # 构造菜单信息
        menu_id = i.get('permissions__menu_id', None)
        if menu_id:
            if not menu_dic.get(menu_id):
                menu_dic[menu_id] = {
                    'title': i.get('permissions__menu__title', None),
                    'icon': i.get('permissions__menu__icon', None),
                    'weight': i.get('permissions__menu__weight', None),

                    'children': [
                        {'title': i.get('permissions__title', None),
                         'url': i.get('permissions__url', None),
                         'id': i.get('permissions__id', None),
                         }]
                }
            else:
                menu_dic[menu_id]['children'].append(
                    {'title': i.get('permissions__title', None),
                     'url': i.get('permissions__url', None),
                     'id': i.get('permissions__id', None),
                     })
    # print(permissions)
    # print(permission_dic)
    # print(menu_dic)
    # 权限列表
    request.session[settings.PERMISSION_SESSION_KEY] = permission_dic
    # 菜单列表
    request.session[settings.MENU_SESSION_KEY] = menu_dic
