import sys
import os
import subprocess
import importlib.util

def check_and_install_dependencies():
    """检查并自动安装所需的依赖包"""
    required_packages = {
        'pycryptodome': 'pycryptodome',
        'cryptography': 'cryptography',
        'wmi': 'WMI',
        'pyarmor': 'pyarmor'
    }

    # 国内镜像源列表
    mirrors = [
        'https://pypi.tuna.tsinghua.edu.cn/simple/',
        'https://mirrors.aliyun.com/pypi/simple/',
        'https://pypi.douban.com/simple/',
        'https://pypi.mirrors.ustc.edu.cn/simple/',
        None  # 官方源
    ]

    missing_packages = []

    # 检查哪些包缺失
    for import_name, package_name in required_packages.items():
        try:
            if import_name == 'pycryptodome':
                # pycryptodome 导入时使用 Crypto
                __import__('Crypto')
            else:
                __import__(import_name)
            print(f"[LG_Lock] ✓ {package_name} 已安装")
        except ImportError:
            missing_packages.append(package_name)
            print(f"[LG_Lock] ✗ {package_name} 未安装")

    # 安装缺失的包
    for package in missing_packages:
        print(f"[LG_Lock] 正在安装 {package}...")
        installed = False

        for mirror in mirrors:
            try:
                cmd = [sys.executable, '-m', 'pip', 'install', package]
                if mirror:
                    cmd.extend(['-i', mirror])
                    print(f"[LG_Lock] 尝试使用镜像: {mirror}")
                else:
                    print(f"[LG_Lock] 尝试使用官方源")

                result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

                if result.returncode == 0:
                    print(f"[LG_Lock] ✓ {package} 安装成功")
                    installed = True
                    break
                else:
                    print(f"[LG_Lock] ✗ 安装失败: {result.stderr.strip()}")

            except subprocess.TimeoutExpired:
                print(f"[LG_Lock] ✗ 安装超时")
            except Exception as e:
                print(f"[LG_Lock] ✗ 安装出错: {str(e)}")

        if not installed:
            print(f"[LG_Lock] ⚠️  警告: {package} 安装失败，可能影响功能使用")

# 在导入模块前检查并安装依赖
print("[LG_Lock] 检查依赖包...")
check_and_install_dependencies()

major, minor = sys.version_info.major, sys.version_info.minor
current_version = f"{major}.{minor}"
current_dir = os.path.dirname(__file__)
lib_dir = os.path.join(current_dir, "lib")
folders_to_try = [
    f"py{current_version}",
    "py3.13", "py3.12", "py3.11", "py3.10",
]

lib_path = None
for folder in folders_to_try:
    path = os.path.join(lib_dir, folder)
    if os.path.exists(path):
        lib_path = path
        print(f"[LG_Lock] 使用库文件夹: lib/{folder} (Python {current_version})")
        break

if lib_path is None:
    raise ImportError(f"无法找到适合Python {current_version}的库文件夹")

sys.path.insert(0, lib_path)
py_files = [f for f in os.listdir(lib_path) if f.endswith('.py') and f != '__init__.py' and os.path.isfile(os.path.join(lib_path, f))]
if not py_files:
    raise ImportError(f"在 {lib_path} 下找不到可用的py文件")
module_name = os.path.splitext(py_files[0])[0]
print(f"[LG_Lock] 正在导入模块: {module_name} (从文件: {py_files[0]})")

import importlib
a = importlib.import_module(module_name)
print(f"[LG_Lock] 成功导入模块: {module_name}")

NODE_CLASS_MAPPINGS = getattr(a, 'NODE_CLASS_MAPPINGS', {})
NODE_DISPLAY_NAME_MAPPINGS = getattr(a, 'NODE_DISPLAY_NAME_MAPPINGS', {})
WEB_DIRECTORY = getattr(a, 'WEB_DIRECTORY', None)
