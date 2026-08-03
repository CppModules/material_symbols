#!/usr/bin/env python3
"""
从 Google Material Symbols codepoints 文件生成 C/C++ 码点宏头文件。

用法:
    python generate_icon_header.py <codepoints_file> <output_header> [--prefix <macro_prefix>]

示例:
    python generate_icon_header.py res/MaterialSymbolsOutlined.codepoints include/icon_codepoints.h
    python generate_icon_header.py res/MaterialSymbolsOutlined.codepoints include/icon_codepoints.h --prefix MY_ICON
"""

import argparse
import os
import re
import sys


def name_to_macro(name: str, prefix: str) -> str:
    """图标名转宏名: home -> MATERIAL_SYMBOLS_ICON_HOME"""
    s = name.upper().replace("-", "_")
    # 数字开头加前缀下划线
    if s and s[0].isdigit():
        s = "_" + s
    return f"{prefix}_{s}"


def main():
    parser = argparse.ArgumentParser(description="生成 Material Symbols 码点宏头文件")
    parser.add_argument("codepoints_file")
    parser.add_argument("output_header")
    parser.add_argument("--prefix", default="MATERIAL_SYMBOLS_ICON")
    args = parser.parse_args()

    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", args.prefix):
        print(f"错误: 无效的宏前缀: {args.prefix}", file=sys.stderr)
        sys.exit(1)

    codepoints_file = args.codepoints_file
    output_header = args.output_header

    if not os.path.isfile(codepoints_file):
        print(f"错误: 找不到 codepoints 文件: {codepoints_file}", file=sys.stderr)
        sys.exit(1)

    entries = []
    seen_macros = set()

    with open(codepoints_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) < 2:
                continue
            name = parts[0]
            hex_code = parts[1]
            macro = name_to_macro(name, args.prefix)

            # 去重（部分图标有别名，码点相同）
            if macro in seen_macros:
                continue
            seen_macros.add(macro)

            entries.append((macro, hex_code.upper()))

    os.makedirs(os.path.dirname(output_header) or ".", exist_ok=True)

    with open(output_header, "w", encoding="utf-8") as f:
        f.write("// 自动生成，勿手动编辑\n")
        f.write("// 由 generate_icon_header.py 从 MaterialSymbolsOutlined.codepoints 生成\n")
        f.write("#pragma once\n\n")

        # 计算对齐宽度
        max_name_len = max(len(m) for m, _ in entries) if entries else 0

        for macro, hex_code in entries:
            padding = " " * (max_name_len - len(macro) + 1)
            f.write(f"#define {macro}{padding}0x{hex_code}\n")

    print(f"已生成 {len(entries)} 个图标码点宏 -> {output_header}")


if __name__ == "__main__":
    main()
