#!/usr/bin/env python
import os
from distutils.core import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


# Compile the list of packages available, because distutils doesn't have
# an easy way to do this.
packages, data_files = [], []
root_dir = os.path.dirname(__file__)
if root_dir:
    os.chdir(root_dir)

folder_name = 'category'
for dirpath, dirnames, filenames in os.walk(folder_name):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'): del dirnames[i]
    if '__init__.py' in filenames:
        pkg = dirpath.replace(os.path.sep, '.')
        if os.path.altsep:
            pkg = pkg.replace(os.path.altsep, '.')
        packages.append(pkg)
    elif filenames:
        prefix = dirpath[len(folder_name) + 1:] # Strip "registration/" or "registration\"
        for f in filenames:
            data_files.append(os.path.join(prefix, f))

print packages, data_files

setup(name = 'django-content-category',
    version = '1.0.4',
    description = 'This django application gives category functionality. Can be used by other applications.',
    author = 'German Ilyin',
    author_email = 'germanilyin@gmail.com',
    url = 'https://github.com/yunmanger1/django-content-category/',
    license = 'WTFPL',
    long_description = read('README'),
    package_dir = {folder_name: folder_name},
    packages = packages,
    package_data = {folder_name: data_files},
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "Environment :: Plugins",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: Freeware",
        "Programming Language :: Python :: 2.6",
    ],
)
