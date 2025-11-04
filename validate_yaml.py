import yaml
import sys

try:
    with open('test_codemagic.yaml', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查内容
    print("=== 文件内容检查 ===")
    lines = content.split('\n')
    print(f"总行数: {len(lines)}")
    print(f"第一行: '{lines[0]}'")
    print(f"第一行字节: {[hex(ord(c)) for c in lines[0][:5]]}")
    print()
    
    # 尝试解析 YAML
    print("=== YAML 解析 ===")
    config = yaml.safe_load(content)
    print("✅ YAML 解析成功！")
    print()
    
    # 显示结构
    print("=== 配置结构 ===")
    print(yaml.dump(config, default_flow_style=False, allow_unicode=True))
    
except yaml.YAMLError as e:
    print(" YAML 错误:")
    print(f"错误类型: {type(e).__name__}")
    print(f"错误信息: {e}")
    sys.exit(1)
except Exception as e:
    print(f" 其他错误: {e}")
    sys.exit(1)
