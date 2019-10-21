import re

from django.conf import settings
from django.shortcuts import HttpResponse, redirect
from django.utils.deprecation import MiddlewareMixin

from crm import models


# 1. 注册rbacapp
# 2. 注册当前中间件
# 3. 在配置文件中，设置：豁免的url，EXEMPT_URL = []， 和 白名单列表：WHITE_LIST = []
# 4. settings.PERMISSION_SESSION_KEY: session中的权限的 key

class AuthMiddleWare(MiddlewareMixin):

	def process_request(self, request):
		path = request.path
		print(path)
		"""1. print('白名单列表')"""
		for url in settings.WHITE_LIST:
			if re.match(url, path):
				return

		"""2. print('校验登录状态')"""
		if not request.session.get('is_login'):
			return redirect('login')
		obj = models.UserProfile.objects.filter(pk=request.session.get('user_id')).first()
		# print(obj)
		if obj:
			request.user_obj = obj
		# print('豁免列表')
		# 在 my_tags.py 使用了 current_menu 属性
		request.current_menu_id = None
		request.breadcrumb_list = [{'title': '首页', 'url': '/index/'}]

		""""3. 豁免的权限"""
		for url in settings.EXEMPT_URL:
			# print(path, '-'*8, url)
			if re.match(path, url):
				return

		"""4. 验证权限"""
		permission_dic = request.session.get(settings.PERMISSION_SESSION_KEY)
		# print('权限列表')
		# print(permissions,'*'*8)
		# print(permission_dic)
		for i in permission_dic.values():
			# print(permission_dic.values())
			# 二级菜单的匹配
			if re.match(r'{}$'.format(i.get('url')), path):
				sid = i.get('id')
				pid = i.get('pid')
				pname = i.get('pname')
				# print(sid, pid)
				# current_menu_id，当前url的对应的二级菜单的id
				if pid:
					# 当前访问子权限
					request.current_menu_id = pid
					# 路径导航
					request.breadcrumb_list.append({'title': permission_dic[pname]['title'], 'url': permission_dic[pname]['url']})
					request.breadcrumb_list.append({'title': i['title'], 'url': i['url']})
				else:
					# 当前访问父权限(二级菜单)
					request.current_menu_id = sid
					# 路径导航
					request.breadcrumb_list.append({'title': i['title'], 'url': i['url']})

				# # 自关联中外键不为空，减少菜单功能代码
				# # 菜单的功能
				# request.current_menu_id = pid

				# # 面包屑的功能，确认当前url是第几层菜单
				# if pid == sid:
				#     request.breadcrumb_list.append({'title': i['title'], 'url': i['url']})
				# else:
				#     request.breadcrumb_list.append(
				#         {'title': permission_dic[str(pid)]['title'], 'url': permission_dic[str(pid)]['url']})
				#     request.breadcrumb_list.append({'title': i['title'], 'url': i['url']})

				return

		return HttpResponse('没有访问权限，请联系管理员')
