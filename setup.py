from distutils.core import setup

import re


VERSIONFILE="catheat/__init__.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))


setup(
    name='catheat',
    version=verstr,
    packages=['catheat',],
    license='GNU GPL V3',
    description='Plot categorical heatmaps in seaborn.',
    long_description=open('README.md').read(),
    url = 'https://github.com/schlegelp/catheat',
    author='Philipp Schlegel',
    author_email = 'pms70@cam.ac.uk',
    keywords='seaborn categorical heatmap',

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',

        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],   
)
