from distutils.core import setup

setup(
    name='mkdocs_quiz',
    version='0.0.1',
    packages=['mkdocs_quiz',],
    license='Apache License 2.0',
    long_description=open('README.md').read(),
    url='https://github.com/skyface753/mkdocs-quiz',
    description='A mkdocs plugin that enables you to create a quiz in your markdown document.',
    author='Sebastian Jörz',
    author_email='sjoerz@skyface.de',
    install_requires=[
        "mkdocs",
    ],
    entry_points={
        'mkdocs.plugins': [
            'mkdocs_quiz = mkdocs_quiz.plugin:MkDocsQuizPlugin'
        ]
    }
)
