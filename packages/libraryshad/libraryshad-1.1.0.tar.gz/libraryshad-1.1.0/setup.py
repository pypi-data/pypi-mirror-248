import os
import re
from setuptools import setup
requires = ["pycryptodome==3.16.0","websocket_client","requests","rubiran==2.0.1","Pillow==9.4.0"]
_long_description = """

## An example:
``` python
from libraryshad import Bot
import asyncio

bot = Bot(auth="Auth Account",key="Key Account")

gap = "guids"
async def main():
	data = await bot.sendMessage(gap,"mamadcodrr")
	print(data)
asyncio.run(main())
```


### How to import the shad's library

``` bash
from libraryshad import Bot
```

### How to install the library

``` bash
pip install libraryshad==1.1.1
```

### My ID in Rubika

``` bash
@professor_102
```
## And My ID Channel in Rubika

``` bash
@python_java_source 
```
"""

setup(
    name = "libraryshad",
    version = "1.1.0",
    author = "mamadcoder",
    author_email = "mamadcoder@gmail.com",
    description = ("Another example of the library making the shad's robot"),
    license = "MIT",
    keywords = ["rubika","bot","robot","library","rubikalib","rubikalib.ml","rubikalib.ir","rubika.ir","Rubika","Python","rubiran","pyrubika","shad","telebot","twine"],
    url = "https://rubika.ir/python_java_source",
    packages=['libraryshad'],
    long_description=_long_description,
    long_description_content_type = 'text/markdown',
    install_requires=requires,
    classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    "Programming Language :: Python :: Implementation :: PyPy",
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10'
    ],
)
