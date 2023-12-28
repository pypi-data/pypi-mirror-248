import fnmatch
import os
import platform

import setuptools


def get_files(path, pattern):
    """
    Recursive file search that is compatible with python3.4 and older
    """
    matches = []
    for root, _, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, pattern):
            matches.append(os.path.join(root, filename))
    return matches


target = platform.system().lower()
PLATFORMS = {"windows", "linux", "darwin", "cygwin"}
for known in PLATFORMS:
    if target.startswith(known):
        target = known

extra_compile_args = {
    "windows": ["/DANTLR4CPP_STATIC", "/Zc:__cplusplus", "/std:c++17"],
    "linux": ["-std=c++17"],
    "darwin": ["-std=c++17"],
    "cygwin": ["-std=c++17"],
}

# Define an Extension object that describes the Antlr accelerator
parser_ext = setuptools.Extension(
    # Extension name shall be at the same level as the sa_lua.py module
    name="speedy_antlr_lua_parser.sa_lua_cpp_parser",
    # Add the Antlr runtime source directory to the include search path
    include_dirs=["cpp_src/antlr4-cpp-runtime"],
    # Rather than listing each C++ file (Antlr has a lot!), discover them automatically
    sources=get_files("cpp_src", "*.cpp"),
    depends=get_files("cpp_src", "*.h"),
    extra_compile_args=extra_compile_args.get(target, []),
)

# Define a package
setuptools.setup(
    name="speedy-antlr-lua-parser",
    version="0.0.1",
    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
    install_requires=["antlr4-python3-runtime >= 4.13, < 4.14"],
    ext_modules=[parser_ext],
)
