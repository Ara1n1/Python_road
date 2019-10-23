```python
def iterator(x):
    print(f'iter{x:03d}start')
    res = []
    for _ in range(0, x, 2):
        res.append((_ ** 2) // 3)
        yield res
    print(f'iter{x:03d}finish')


def main():
    print('start')
    _iter = iterator(6)
    for _ in _iter:
        print(_)
        print('end')
main()

# start
# iter006start
# [0]
# end
# [0, 1]
# end
# [0, 1, 5]
# end
# iter006finish
```

```python
def cor():
    data_list = []
    while True:
        print('go', end='')
        x = yield
        print(x)
        if x is None:
            break
        data_list.append(x)
    ret = sum(data_list) / len(data_list)

    print('average', ret)
    return ret


def main():
    print('call cor()')
    func = cor()
    print('next(func)')
    next(func)
    try:
        for x in range(3):
            print('->', x)
            func.send(x)
        func.send(None)

    except StopIteration as exp:
        print('func return', exp.value)

main()
# call cor()
# next(func)
# go-> 0
# 0
# go-> 1
# 1
# go-> 2
# 2
# goNone
# average 1.0
# func return 1.0
```

```python
def check_func():
    print('call check_func')
    return true

def check_before_fun(func):
    print('call decorator')
    
    def func_wrapper(f):
        
        def call_func(*args, **kwargs):
            is_ok = func()
            if is_ok:
                print('checked')
                return f(*args, **kwargs)
            else:
                print('check failed')
                raise ImportError('check failed')
		return call_func
    return func_wrapper

@check_before_run(check_func)
def a_foo(name):
    print('call a_foo ->', name)

print('call a_foo start')
a_foo('abc')
print('call a_foo end')
```



