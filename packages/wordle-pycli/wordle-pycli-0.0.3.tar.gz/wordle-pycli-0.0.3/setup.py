# MIT License

# Copyright (c) 2023 Meesum Qazalbash

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from setuptools import find_packages, setup

setup(
    name='wordle-pycli',
    version='0.0.3',
    author='Meesum Qazalbash',
    author_email='meesumqazalbash@gmail.com',
    description='Play Wordle Anywhere, Anytime - Unleash Your Vocabulary Adventure!',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Qazalbash/wordle-pycli',
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Environment :: Console',
        'Topic :: Games/Entertainment :: Puzzle Games',
    ],
    keywords=['wordle', 'cli', 'game', 'word game', 'wordle game', 'wordle-cli'],
    python_requires='>=3.6',
    license='MIT',
    zip_safe=False,
    entry_points={
        'console_scripts': ['wordle-pycli=wordle_pycli.wordle:play_wordle'],
    },
)
