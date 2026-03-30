#!/usr/bin/env python3
"""
从完整 Material Symbols ttf 裁剪出仅包含指定码点的子集字体。
保留 Variable Font 轴信息（FILL/wght/GRAD/opsz）。

用法:
    python subset_icon_font.py <input_ttf> <output_ttf> <codepoints...>

示例:
    python subset_icon_font.py res/MaterialSymbolsOutlined.ttf out/icon_subset.ttf E88A E8B8 E8B6

也支持从文件读取码点列表:
    python subset_icon_font.py res/MaterialSymbolsOutlined.ttf out/icon_subset.ttf --file codepoints.txt
"""

import sys
import os


def main():
    if len(sys.argv) < 4:
        print(f"用法: {sys.argv[0]} <input_ttf> <output_ttf> [--file <file>] | <codepoints...>",
              file=sys.stderr)
        sys.exit(1)

    input_ttf = sys.argv[1]
    output_ttf = sys.argv[2]

    if not os.path.isfile(input_ttf):
        print(f"错误: 找不到输入字体: {input_ttf}", file=sys.stderr)
        sys.exit(1)

    # 解析码点列表
    codepoints = []
    if sys.argv[3] == "--file":
        if len(sys.argv) < 5:
            print("错误: --file 需要指定文件路径", file=sys.stderr)
            sys.exit(1)
        with open(sys.argv[4], "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    codepoints.append(int(line, 16))
    else:
        for arg in sys.argv[3:]:
            codepoints.append(int(arg, 16))

    if not codepoints:
        print("错误: 无码点输入", file=sys.stderr)
        sys.exit(1)

    try:
        from fontTools.subset import Subsetter, Options
        from fontTools.ttLib import TTFont
    except ImportError:
        print("错误: 需要安装 fonttools: pip install fonttools brotli", file=sys.stderr)
        sys.exit(1)

    # 配置: 保留 Variable Font 轴
    options = Options()
    options.layout_features = ["*"]
    options.name_IDs = ["*"]
    options.notdef_outline = True
    options.recalc_average_width = True
    options.drop_tables = []

    font = TTFont(input_ttf)
    subsetter = Subsetter(options=options)

    # 转为 Unicode 字符集
    unicodes = set(codepoints)
    subsetter.populate(unicodes=unicodes)
    subsetter.subset(font)

    os.makedirs(os.path.dirname(output_ttf) or ".", exist_ok=True)
    font.save(output_ttf)

    input_size = os.path.getsize(input_ttf)
    output_size = os.path.getsize(output_ttf)
    print(f"裁剪完成: {len(codepoints)} 个码点")
    print(f"  输入: {input_ttf} ({input_size:,} bytes)")
    print(f"  输出: {output_ttf} ({output_size:,} bytes)")
    print(f"  压缩比: {output_size / input_size * 100:.1f}%")


if __name__ == "__main__":
    main()
