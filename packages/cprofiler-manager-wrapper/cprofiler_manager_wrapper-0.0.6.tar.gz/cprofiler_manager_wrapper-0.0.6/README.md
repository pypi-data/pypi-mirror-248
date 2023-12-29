### Install

`pip install cprofiler-manager-wrapper`

### Usage

```python
from cprofiler_manager_wrapper import Profiler


def func_to_profile():
    from time import sleep

    result = []
    for i in range(10):
        result.append(i)
    sleep(1)

    a = 10

    return 'hello world'


with Profiler(func_about_string='func', disable=False):
    func_to_profile()
```

По итогу будет создана, если ее не было, папка _prof_folder_, внутри которой будет лежат файл _<some>.prof_

Для открытия .prof файла используется **snakeviz** - `snakeviz prof_folder/<some>.prof`
