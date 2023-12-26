from setuptools import setup, find_packages

setup(
    name='easymake',
    version = '0.1.0',
    packages= find_packages(),
    install_require=[],
    entry_points={
        "console_scripts":[
            "easymake_entrypoints = easymake:iseven"
        ],
    }
)
