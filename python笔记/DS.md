1.  评判程序的优劣
    -   消耗计算机资源和执行效率
    -   计算算法执行的耗时(没有源码)
    -   时间复杂度(有实现源码)
2.  时间复杂度
    -   评判规则：量化算法执行的操作/执行步骤的数量
    -   原则：时间复杂度表达式中最有意义的项
3.  数据结构：数据的组织方式，解决的的是一组数据如何进行保存
4.  timeit计算程序的平均耗时

```python
from timeit import Timer
timer = Timer('test01', setup='from __main__ import test01')
# 执行次数,默认执行 10,000 次
sec = timer.timerit(1000)
print(sec)
```

# 数据结构

## 1. stack

1.  Stack()：构造方法
2.  push() / pop()
3.  peek()
4.  isEmpty
5.  size()

```python
class Stack(object):
    
    def __init__(self):
        self.items = []
    
    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop() if self.items else None
    
    def peek(self):
        return self.items[-1] if self.items else None
    
    def isEmpty(self):
        return self.items == []
    
    def size(self):
        return len(self.items)
```

## 2. queue

1.  Queue()
2.  enqueue(item)
3.  dequeue(item)
4.  isEmpty()
5.  size()

```python
class Queue(object):
    
    def __init__(self):
        self.items = []
    
    def enqueue(self,item):
        self.items.insert(0, item)

    def dequeue(self,item):
        return self.items.pop() if self.items else None
        
     def isEmpty(self):
        return self.items == []
    
    def size(self):
        return len(self.items)
```

-   示例：烫手的山芋

```python
queue = Queue()
kids = ['A', 'B', 'C', 'D', 'E', 'F']

for kid in kids:
    queue.enqueue(kid)

while queue.size() > 1:
    for i in range(6):
        kid = queue.dequeue()
        queue.enqueue(kid)
     queue.dequeue()
    
print('获胜者是：', queue.dequeue())
```

## 3. Double-ended Queue

-   双端队列

1.  Deque()
2.  addFront(item)
3.  addRear(item)
4.  removeFront()
5.  removeRear()
6.  isEmpty()
7.  size()

```python
class Deque(object):
    
    def __init__(self):
        self.items = []
    
    def addFront(self, item)
    	self.items.append(item)
    	
    def addRear(self, item)
    	self.items.insert(0, item)
    
    def removeFront(self):
        return self.items.pop() if self.items else None
    
    def removeRear(self):
        return self.items.pop(0) if self.items else None
    	
    def isEmpty(self):
        return self.items == []
    
    def size(self):
        return len(self.items)
```

-   示例：回文检查

```python
deque = Deque()
def isHuiWen(s):
    for ch in s:
        q.addFront(ch)

    flag = True
    for i in range(len(s) // 2):
        if deque.removeFront() != deque.removeRear():
            flag = False
            break
	return flag

print(isHuiWen('hello'))
```

## 4. Binary Tree

-   根节点（保存根结点的地址）
-   左叶子节点/右叶子节点
-   子树
-   高度

### 1. 初始化和插入

```python
# 封装一个节点对象
class Node():
    
	def __init__(self, item):
        self.item = item
        self.left = None
        self.right = None
    
class Tree():
    # 实例化出一个空的二叉树对象
	def __init__(self):
        # 如果root=None则，二叉树为空
    	self.root = None
    # 向二叉树中插入节点
    def addNode(self, item):
        node = Node(item)
        if not self.root:
            # 树为空
        	self.root = node
            return
        # 树非空
       	cur = self.root
        queue = [cur]
        # 列表判断法
        while True:
            n = queue.pop(0)
            if n.left:
                queue.append(n.left)
            else:
                n.left = node
                return
            if n.right:
                queue.append(n.right)
            else:
                n.right = node
                return
        # 自己实现
        # for i in queue:
        #     if i.left:
        #         queue.append(i.left)
        #     else:
        #         i.left = node
        #         return
        #     if i.right:
        #         queue.append(i.left)
        #     else:
        #         i.right = node
        #         return   
```

### 2. 二叉树

1.  广度遍历(逐层)
2.  深度遍历
    -   前序遍历：根--左--右：1、2、4、5、3、6、7
    -   中序遍历：左--根--右：4、2、5、1、6、3、7
    -   后序遍历：左--右--根：4、5、2、6、3、7、1

#### 1. 广度遍历

```python
# 广度遍历
def travel(self):
    if not self.root:
        print('树为空')
        return

    cur = self.root
    queue = [cur]
    while queue:
        n = queue.pop(0)
        if n.left:
            queue.append(n.left)
            if n.right:
                queue.append(n.right)
                print(n.item)
```

#### 2. 深度遍历

```python
# 前序遍历(从小到大)
def forward(self, root):
    # root是不同子树的根
    if not root:
        return
    print(root.item)
   	self.forward(root.left)
    self.forward(root.right)
    
# 中序遍历
def middle(self, root):
    # root是不同子树的根
    if not root:
        return
   	self.middle(root.left)
    print(root.item)
    self.middle(root.right)
    
# 后序遍历
def back(self, root):
    # root是不同子树的根
    if not root:
        return
   	self.back(root.left)
    self.back(root.right)
    print(root.item)
```

```python
# 测试效果
tree = Tree()
tree.addNode(1)
tree.addNode(2)
tree.addNode(3)
tree.addNode(4)
tree.addNode(5)
tree.addNode(6)
tree.addNode(7)
tree.travel()
tree.forward(tree.root)
tree.middle(tree.root)
tree.back(tree.root)
```

#### 3. 排序二叉树

-   插入节点时，一定要遵从：比根节点小的在左侧，大的节点在右侧

```python
class Node(object):
    
	def __init__(self, item):
        self.item = item
        self.left = None
        self.right = None

class SortTree(object):
    
    def __init__(self):
        self.root = None
	# 插入
    def insertNode(self, item):
        node = Node(item)
        if not self.root:
            self.root = node
            return
        
        cur = self.root
        while True:
            if item > cur.item:
                if not cur.right:
                    cur.right = node
                    break
                cur = cur.right
            else:
                if not cur.left:
                    cur.left = node
                    break
                cur = cur.left
        
	# 中序遍历
	def middle(self, root):
		# root是不同子树的根
        if not root:
            return
        self.middle(root.left)
        print(root.item)
        self.middle(root.right)
```

```python
tree = SortTree()
tree.insertNode(3)
```

# 查找和排序

## 1. 查找

### 1. 二分查找

-   有序容器

```python
li = [i for i in range(1,11)]

def bsearch(li, item):
    low = 0
    hight = len(li)-1
    find = False
    while low < high:
        mid = (low + high)//2
        if item > li[mid]:
            low = mid + 1
        elif item < li[mid]:
        	high = mid - 1
        else:
            find = True
            break
	return find        
```

## 4. 排序

### 1. 冒泡排序

-   将list中的每两个元素进行比较，最大值放置list末尾
-   将当前最大值放置目标位置

```python
alist = [12,3,4,6,8,9,23,45,76]

def bubble(alist):
    for j in range(len(alist) - 1):
        for i in range(1, len(alist) - j):
            if alist[i - 1] > alist[i]:
                alist[i - 1], alist[i] = alist[i], alist[i - 1]
    print(alist)
bubble(alist)
```

### 2. 选择排序

-   max指定list中最大值的位置

```python
def select(alist):
    for j in range(len(alist) - 1, 0, -1):
        max = 0
        for i in range(j):
            if alist[max] < alist[i+1]:
                max = i+1
        alist[max], alist[j] = alist[j], alist[max]
    print(alist)

select(alist)
```

### 3. 插入排序

-   利用 k = i，进行小小的优化
-   增量为一的Shell Sort

```python
def insert(alist):
    i = 1
    while i < len(alist):
        if alist[i - 1] < alist[i]:
            i += 1
        else:
            k = i
            while k > 1 and alist[k - 1] > alist[k]:
                alist[k - 1], alist[k] = alist[k], alist[k - 1]
                k -= 1
    print(alist)

insert(alist)
```

### 4. 希尔排序

-   Shell Sort
-   特殊的插入排序

```python
# 增量为gap的 shell sort
def shell(alist):
    gap = alist // 2
	i = gap
    while gap:
        while i < len(alist):
            if alist[i - gap] < alist[i]:
                i += gap
            else:
                k = i
                while k > gap and alist[k - gap] > alist[k]:
                    alist[k - gap], alist[k] = alist[k], alist[k - gap]
                    k -= gap
        gap //= 2
    print(alist)
```

### 5. 快速排序

```python
# base:基础
def quick_sort(alist, left, right):
    # 结束递归的条件
    if left >= right:
        return
    low = left
    high = right
    base = alist[left]
    while low < high:
        while low < high and alist[high] > base:
            high -= 1
        alist[low] = alist[high]
        while low < high and alist[low] <= base:
            low += 1
        alist[high] = alist[low]

    alist[high] = base
    quick_sort(alist, left, low - 1)
    quick_sort(alist, low + 1, right)

alist = [22, 13, 4, 6, 8, 9, 23, 45, 76]
quick_sort(alist, 0, len(alist) -1)
print(alist)
```


