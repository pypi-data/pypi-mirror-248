from setuptools import setup
description = """
It is a library designed to be easy to use. We understand how difficult some things can be, so we strive to make it as user-friendly as possible.
Developed by: Bom
Contact Information:
   - Facebook: [Bom's Facebook Profile](https://www.facebook.com/profile.php?id=100083115933854)
   - Age of Developer: 14 years old

If you have any questions about using it, feel free to message me on Facebook. If I don't respond immediately, I'm probably still studying!
"""
setup(
    name="simple-commands",
    version="1.4.1",
    description=description,
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
