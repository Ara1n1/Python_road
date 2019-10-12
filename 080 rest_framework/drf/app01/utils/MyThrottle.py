"""访问频率限制"""

# """继承BaseThrottle"""
# class MyThrottle(BaseThrottle):
#     VISIT_HIS = {}
#
#     def __init__(self):
#         self.history = None
#
#     def allow_request(self, request, view):
#         atime = time.time()
#         # remote_addr = request.META.get('REMOTE_ADDR')
#         remote_addr = self.get_ident(request)
#         print(remote_addr)
#         self.history = self.VISIT_HIS.get(remote_addr)
#
#         if not self.history:
#             self.VISIT_HIS[remote_addr] = [atime, ]
#             return True
#
#         while self.history and self.history[-1] < atime - 10:
#             self.history.pop()
#         if len(self.history) < 3:
#             self.history.insert(0, atime)
#             return True
#
#     def wait(self):
#         return 10 - time.time() + self.history[-1]


"""继承SimpleRateThrottle"""
from rest_framework.throttling import SimpleRateThrottle


class MyThrottle(SimpleRateThrottle):
    scope = 'any string'

    def get_cache_key(self, request, view):
        return self.get_ident(request)
