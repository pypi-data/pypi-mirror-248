#!/usr/bin/env python3
from setuptools import setup, Extension
import platform
import os
import subprocess


def get_command_output(command):
    return subprocess.check_output(command, shell=True).decode("utf-8").strip()


def find_c_sources(path):
    sources = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".c"):
                sources.append(os.path.join(root, file))
    return sources


def find_include_headers(path):
    headers = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".h"):
                headers.append(os.path.join(root, file))
    return headers


def find_include_dirs():
    includes = [
        "/usr/local/include",
        "/usr/local/include/freerdp2",
        "/usr/local/include/winpr2",
        "/usr/include/freerdp2",
        "/usr/include/winpr2",
    ]
    if platform.system() == "Darwin":
        freerdp2_prefix = get_command_output("brew --prefix freerdp")
        includes.append(os.path.join(freerdp2_prefix, "include", "freerdp2"))
        includes.append(os.path.join(freerdp2_prefix, "include", "winpr2"))
    return includes


def find_library_dirs():
    libraries = ["/usr/local/lib", "/usr/lib", ]
    if platform.system() == "Darwin":
        freerdp2_prefix = get_command_output("brew --prefix freerdp")
        libraries.append(os.path.join(freerdp2_prefix, "lib"))
    elif platform.system() == "Linux":
        libraries.append("/usr/lib/x86_64-linux-gnu")
        libraries.append("/usr/lib64")
    return libraries


target_os = platform.system()
package_root = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(package_root, "src")
c_sources = [os.path.relpath(item, package_root) for item in find_c_sources(src)]
c_headers = [os.path.relpath(item, package_root) for item in find_include_headers(src)]
include_dirs = find_include_dirs()
library_dirs = find_library_dirs()
module = Extension("pyfreerdp",
                   sources=c_sources,
                   depends=c_headers,
                   libraries=['freerdp2'],
                   define_macros=[("TARGET_OS_WATCH", target_os),
                                  ("TARGET_OS_IPHONE", '0'), ],
                   include_dirs=include_dirs,
                   library_dirs=library_dirs, )

setup(
    name="pyfreerdp",
    author="Eric",
    url="https://github.com/LeeEirc",
    author_email="xplzv@126.com",
    version="0.0.2",
    python_requires=">=3.10",
    description="Python wrapper for FreeRDP",
    ext_modules=[module, ],
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: CPython"
    ]
)
