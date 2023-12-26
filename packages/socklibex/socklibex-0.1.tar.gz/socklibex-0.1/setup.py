from setuptools import setup, find_packages

setup(
    name='socklibex',
    version='0.1',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    description='Библиотека с информацией о программировании',
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='Egor',
    author_email='bykovsky.egor2017@yandex.ru',
    url='https://github.com/BykovskiiEgor/sockLibEx', 
    install_requires=[
        # Зависимости, если они есть
    ],
)
