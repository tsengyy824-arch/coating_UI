"""
创建 GitHub 上传包
打包所有项目文件为 ZIP 档案
"""

import zipfile
import os
from pathlib import Path

def create_package():
    """创建项目打包文件"""
    
    # 项目根目录
    project_root = Path(__file__).parent
    
    # 输出 ZIP 文件名
    output_zip = project_root.parent / "coating_UI_package.zip"
    
    # 要包含的文件和文件夹
    files_to_include = [
        'main.py',
        'requirements.txt',
        'README.md',
        'modbus_server_simulator.py',
        'MODBUS_SIMULATOR_GUIDE.md',
    ]
    
    folders_to_include = [
        'src',
        'config',
        '.github',
    ]
    
    # 要排除的文件/文件夹
    exclude_patterns = [
        '.venv',
        '__pycache__',
        '*.pyc',
        '.git',
        '.vscode',
        'create_github_package.py',
    ]
    
    print(f"开始打包项目到: {output_zip}")
    print("=" * 50)
    
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # 添加单个文件
        for file_name in files_to_include:
            file_path = project_root / file_name
            if file_path.exists():
                arcname = file_name
                zipf.write(file_path, arcname)
                print(f"✓ 添加文件: {file_name}")
            else:
                print(f"✗ 跳过 (不存在): {file_name}")
        
        # 添加文件夹
        for folder_name in folders_to_include:
            folder_path = project_root / folder_name
            if folder_path.exists() and folder_path.is_dir():
                for root, dirs, files in os.walk(folder_path):
                    # 过滤排除的文件夹
                    dirs[:] = [d for d in dirs if d not in exclude_patterns]
                    
                    for file in files:
                        # 检查是否应该排除
                        if any(file.endswith(pattern.replace('*', '')) for pattern in exclude_patterns if '*' in pattern):
                            continue
                        if file in exclude_patterns:
                            continue
                        
                        file_path = Path(root) / file
                        arcname = file_path.relative_to(project_root)
                        zipf.write(file_path, arcname)
                        print(f"✓ 添加: {arcname}")
            else:
                print(f"✗ 跳过 (不存在): {folder_name}/")
    
    print("=" * 50)
    print(f"✅ 打包完成!")
    print(f"📦 文件位置: {output_zip}")
    print(f"📏 文件大小: {output_zip.stat().st_size / 1024:.2f} KB")
    print("")
    print("接下来的步骤:")
    print("1. 打开此文件: {}".format(output_zip))
    print("2. 登入 GitHub: https://github.com/tsengyy824-arch/coating_UI")
    print("3. 点击「Add file」→「Upload files」")
    print("4. 解压 ZIP 并拖拽所有文件到浏览器")
    print("5. 填写 commit 信息: Initial commit - Robot arm control system")
    print("6. 点击「Commit changes」")


if __name__ == '__main__':
    create_package()
