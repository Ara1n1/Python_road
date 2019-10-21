## RBAC

1.  表结构：4个model，6张表

    1.  用户表：user：用户名、密码（2个字段）
-   如果使用其他app的user表则在一个user表中使用`class Meta: abstract=True`
    2.  角色表：role：id、角色（2个字段）
    3.  权限表：permission：id、url、title、name、**menu_id**、**parent_id**、weight(**排序使用**)（6+1个字段）
    4.  菜单表：menu：id、icon、weight（3个字段）
    5.  用户和角色表
    6.  角色和权限表
2.  `init_permission`：在用户认证成功后， 构造`permission_dict`和`menu_dict`
3.  权限中间件功能(**4**)
    1.  白名单放行
    2.  登录状态检测
    3.  权限豁免
    4.  权限验证
4.  