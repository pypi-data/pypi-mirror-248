from setuptools import setup, find_packages

read_md = lambda f: open(f, 'r').read()

setup(
    name='auto_find_date_pdf',
    version='0.2.22',
    description='A simple lib to find dates from any txt/ pdf/ docx/ rtf source. For documentation see',
    long_description=read_md('README.md'),
    long_description_content_type="text/markdown; charset=UTF-8",
    author='Your Name',

    author_email='open@marvsai.com',
    packages=find_packages(exclude=['test_fast*']),
    py_modules=['text_search', 'main'],
    install_requires=[
        'python-docx',
        'pypdf',
        'pytz',
        'striprtf',
        'Pillow'
    ],
    entry_points='''
        [console_scripts]
        your_script_name=main:main
    '''
)
