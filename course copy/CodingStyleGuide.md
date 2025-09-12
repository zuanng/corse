Trong Python, coding style guide chuẩn được sử dụng rộng rãi là PEP 8

# 1. Cấu trúc & định dạng code

- Thụt lề bằng 4 spaces (không dùng tab)

- Mỗi dòng tối đa 79 ký tự

- cách dòng:

    - 2 dòng trống giữa các class, function top-level.

    - 1 dòng trống giữa các method trong class.

- Imports theo thứ tự:

    - Một import trên một dòng.

    -  Thứ tự:

        1. Standard library

        2. Third-party libraries

        3. Local/project imports

    - Cách nhau 1 dòng trống.

# 2. Quy tắc đặt tên

- Variables / functions / methods: `snake_case`

- Classes: `PascalCase`

- Constants: `UPPER_CASE`

- Private/internal: `_leading_underscore`

# 3. Strings

- Dùng ' hoặc " nhất quán trong project

- f-string thay cho % hoặc .format(): 

`print(f"Hello, {name}")`

# 4. Docstring & Comment

- Dùng triple quotes `"""` cho docstring.

- Docstring theo PEP 257.

- Comment: chỉ viết khi cần giải thích logic khó, không lặp lại code.

# 5. Git commit convention 

Dùng conventional commits:t

- feat: thêm chức năng mới

- fix: sửa bug

- refactor: tối ưu code, không làm thay đổi chức năng

- docs: thay đổi tài liệu (README, comment, wiki, …)

- test: thêm/sửa test

- chore: thay đổi lặt vặt (config, build script, dependency, …)

- style: thay đổi code style (formatting, dấu chấm phẩy, indent…), không ảnh hưởng logic

- perf: cải thiện hiệu năng

- ci: thay đổi liên quan CI/CD (pipeline, GitHub Actions, GitLab CI, …)

- build: thay đổi hệ thống build hoặc dependency (npm, pip, docker, …)

- revert: hoàn tác (revert) commit trước đó

# 1 số quy tắc khác

- Type Hint: Luôn dùng type hint cho hàm/method.

```python
def greet(name: str, age: int) -> str:
    return f"{name} is {age} years old" 
```

- Code layout: Spaces quanh toán tử và Không thêm space sau ( hoặc trước ):

```a = (b * c) + d```

- Error Handling: Ưu tiên try/except cụ thể, tránh except Exception.

```python
    user = get_user(id)
except ValueError:
    return Non
```