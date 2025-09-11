Trong Python, style guide chuẩn được sử dụng rộng rãi là PEP 8

# 1. Cấu trúc & định dạng code

- Indentation: 4 spaces (không dùng tab).

- Line length: tối đa 79 ký tự (docstring 72 ký tự).

- Blank lines:

    - 2 dòng trống giữa các class, function top-level.

    - 1 dòng trống giữa các method trong class.

- Imports:

    - Một import trên một dòng.

    -  Thứ tự:

        1. Standard library

        2. Third-party libraries

        3. Local/project imports

    - Cách nhau 1 dòng trống.

# 2. Quy tắc đặt tên

- Variables / functions / methods: snake_case

- Classes: PascalCase

- Constants: UPPER_CASE

- Private/internal: _leading_underscore

# 3. Strings

- Dùng ' hoặc " nhất quán trong project.

- f-string thay cho % hoặc .format(): `print(f"Hello, {name}")`

# 4. Docstring & Comment

- Dùng triple quotes """ cho docstring.

- Docstring theo PEP 257.

- Comment: chỉ viết khi cần giải thích logic khó, không lặp lại code.