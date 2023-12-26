# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ast_comments']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'better-ast-comments',
    'version': '1.2.1',
    'description': '',
    'long_description': '# ast-comments\n\nAn extension to the built-in `ast` module. \nFinds comments in source code and adds them to the parsed tree.\n\n## Installation\n```\npip install ast-comments\n```\n\n## Usage\n\nThere is no difference in usage between `ast` and `ast-comments`\n```\n>>> from ast_comments import *\n>>> tree = parse("hello = \'hello\' # comment to hello")\n```\nParsed tree is an instance of the original `ast.Module` object.\nThe only difference is that there is a new type of tree node: `Comment`\n```\n>>> tree\n<_ast.Module object at 0x7ffba52322e0>\n>>> tree.body\n[<ast.Assign object at 0x10a01d5b0>, <ast_comments.Comment object at 0x10a09e0a0>]\n>>> tree.body[1].value\n\'# comment to hello\'\n>>> dump(tree)\n"Module(body=[Assign(targets=[Name(id=\'hello\', ctx=Store())], value=Constant(value=\'hello\')), Comment(value=\'# comment to hello\', inline=True)], type_ignores=[])"\n```\nIf you have python3.9 or above it\'s also possible to unparse the tree object with its comments preserved.\n```\n>>> print(unparse(tree))\nhello = \'hello\'  # comment to hello\n```\n**Note**: Python `compile()` cannot be run on the tree output from parse. The included `pre_compile_fixer()` function can be used to fix the tree (stripping \ncomment nodes) if it will be necessary to compile the output.\n\nMore examples can be found in test_parse.py and test_unparse.py.\n\n## Contributing\nYou are welcome to open an issue or create a pull request\n',
    'author': 'Dmitry Makarov',
    'author_email': 'dmtern0vnik@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/zmievsa/better-ast-comments',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
