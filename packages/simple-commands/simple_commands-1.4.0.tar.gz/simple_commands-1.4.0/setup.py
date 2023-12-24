from setuptools import setup, find_packages

setup(
    name="simple_commands",
    version="1.4.0",
    description="simple_commands",
    python_requires=">=3.9",
    
    packages=[
        'simple_commands',
        'simple_commands.img',
        'simple_commands.CLASS',
        'simple_commands.CLASS.time_zone',
        'simple_commands.CLASS.SQL_class',
        'simple_commands.CLASS.ProgressBar',
        'simple_commands.file',
        'simple_commands.file.savedata',
        'simple_commands.file.deletedata',      
    ],
    package_data={
        '': ['*db','*txt'],

    },
    include_package_data=True,
    install_requires=[
    'pillow',
    'numpy',
    'opencv-python',
    'tqdm',
    'pytz',
    'imagehash'
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
