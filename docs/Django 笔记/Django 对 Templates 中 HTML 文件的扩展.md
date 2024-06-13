# Django 对 Templates 中 HTML 文件的扩展

## Django 模板标签

### 基本语法

```python
view：｛"HTML变量名" : "views变量名"｝
HTML：｛｛变量名｝｝
```

### views 变量

1. 列表

   ```html
   <p>{{ views_list }}</p>   # 取出整个列表 
   <p>{{ views_list.0 }}</p> # 取出列表的第一个元素
   ```

2. 字典

   ```html
   <p>{{ views_dict }}</p>
   <p>{{ views_dict.name }}</p>
   ```

### HTML 变量

#### 过滤器

1. 语法

   使用管道操作，过滤器的参数跟随**冒号**之后并且总是以**双引号**包含

   ```html
   {{ 变量名 | 过滤器：可选参数 }}
   ```

2. 过滤器类型

   - lower / upper

   - first：第一个元素

   - truncateword / truncatechars：截断，后面加冒号、数字表示截断数量，截断的字符串将以 **...** 结尾。

   - date : 按指定的格式字符串参数格式化 date 或者 datetime 对象

   - default：为变量提供一个默认值，如果 views 传的变量的布尔值是 false，则使用指定的默认值。

     默认值通常有：`0  0.0  False  0j  ""  []  ()  set()  {}  None`

   - length：变量长度

   - safe：Django 会自动对 views.py 传到HTML文件中的标签语法进行转义，令其语义失效。加 safe 过滤器是告诉 Django 该数据是安全的，不必对其进行转义，可以让该数据语义生效。

#### 标签

1. if / else 标签

   ```html
   {% if condition1 %}
      ... display 1
   {% elif condition2 %}
      ... display 2
   {% else %}
      ... display 3
   {% endif %}
   ```

2. for 标签

   对 list：

   ```html
   {% for i in views_list %}
   {{ i }}
   {% endfor %}
   ```
   对 dict：

   ```html
   {% for i,j in views_dict.items %}
   {{ i }}-{{ j }}
   {% endfor %}
   ```

   空语句，在循环为空的时候执行（即 in 后面的参数布尔值为 False ）。

   ```html
   {% for i in listvar %}
       ...
   {% empty %}
       ...
   {% endfor %}
   ```

3. 注释标签

   ```html
   {# 这是一个注释 #}
   ```

   