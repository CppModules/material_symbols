# Material Symbols Outlined — Variable Font

Google Material Symbols 图标字体模块，为 LVGLEx 提供 4000+ 图标支持。

- **字体**：MaterialSymbolsOutlined-VariableFont
- **轴**：FILL (0/1) · wght (100~700) · GRAD (-25~200) · opsz (20~48)
- **许可**：Apache License 2.0
- **来源**：https://github.com/google/material-design-icons

## 目录结构

```
material_symbols/
├── res/
│   ├── MaterialSymbolsOutlined.ttf          # 完整字体 (~10MB)
│   └── MaterialSymbolsOutlined.codepoints   # 码点映射表 (name hex)
├── scripts/
│   ├── generate_icon_header.py              # 生成 icon_codepoints.h
│   └── subset_icon_font.py                  # 裁剪字体子集
└── README.md
```

## 构建流程

由 `cmake/icon_font.cmake` 编排，configure 阶段同步执行：

```
.codepoints ──→ generate_icon_header.py ──→ icon_codepoints.h  (LX_ICON_* 宏)
                                       ──→ icon_font_data.h    (embed 符号映射)

源码扫描 LX_ICON_* ──→ 码点列表 ──→ subset_icon_font.py ──→ 裁剪后 .ttf ──→ embed
```

## 脚本说明

### generate_icon_header.py

```bash
python generate_icon_header.py <codepoints_file> <output_header>
```

将 `name hex` 格式的码点文件转为 C/C++ 宏头文件：

```c
#define LX_ICON_HOME  0xE88A
```

### subset_icon_font.py

```bash
# 直接传码点
python subset_icon_font.py input.ttf output.ttf E88A E8B8

# 从文件读取
python subset_icon_font.py input.ttf output.ttf --file codepoints.txt
```

依赖 `fonttools`（`pip install fonttools brotli`），保留 Variable Font 轴信息。
