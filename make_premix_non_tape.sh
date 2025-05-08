#!/bin/bash

# 参数检查
if [ $# -lt 2 ] || [ $# -gt 3 ]; then
    echo "用法：$0 <数据集名称> <输出文件名称> [并发数，默认4]"
    exit 1
fi

dataset="$1"
output="$2"
concurrency="${3:-4}"
tmpdir=$(mktemp -d)  # 创建临时工作目录

# 验证输出目录可写性
output_dir=$(dirname "$output")
if [ ! -d "$output_dir" ] || [ ! -w "$output_dir" ]; then
    echo "错误：输出目录不可写 ($output_dir)"
    rm -rf "$tmpdir"
    exit 1
fi

# 获取数据集文件列表
echo "正在查询数据集文件列表..."
files=$(dasgoclient --query "file dataset=$dataset" 2>/dev/null)
if [ -z "$files" ]; then
    echo "错误：无法获取数据集文件列表"
    rm -rf "$tmpdir"
    exit 1
fi

total=$(echo "$files" | wc -l)
echo "总文件数：$total，并发数：$concurrency"

# 进度统计文件
progress_file="$tmpdir/progress"
echo 0 > "$progress_file"

# 处理器函数（带进度显示）
process_file() {
    local file="$1"
    # 查询存储位置
    local sites=$(dasgoclient --query "site file=$file" 2>/dev/null)
    
    # 判断存储类型
    if echo "$sites" | grep -qv "Tape"; then
        echo "$file" >> "$tmpdir/output"
    fi
    
    # 原子级更新进度
    flock -x 200
    current=$(($(cat "$progress_file") + 1))
    echo "$current" > "$progress_file"
    echo -ne "进度：$current/$total (${concurrency}并发)\r"
    flock -u 200
} 200>"$tmpdir/lock"

# 导出函数和环境变量
export -f process_file
export tmpdir progress_file

# 使用parallel实现并行处理
echo "开始并行处理..."
echo "$files" | xargs -P $concurrency -n 1 -I {} bash -c 'process_file "$@"' _ {}

# 合并结果并排序去重
echo -e "\n正在合并结果..."
sort -u "$tmpdir"/output > "$output"

# 清理临时目录
rm -rf "$tmpdir"

# 结果统计
valid_count=$(wc -l < "$output")
echo "处理完成！有效文件数：$valid_count"
echo "结果已保存到：$output"