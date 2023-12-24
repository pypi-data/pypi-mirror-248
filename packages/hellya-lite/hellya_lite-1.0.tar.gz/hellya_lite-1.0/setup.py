from setuptools import setup, find_packages


def readme():
  with open('README.md', 'r', encoding='utf-8') as f:
    return f.read()


setup(
  name='hellya_lite',
  version='1.0',
  author='soviet_workshop',
  author_email='soviet.workshop23@gmail.com',
  description='Библиотека для программирования рисунков.',
  long_description=readme(),
  long_description_content_type='text/markdown',
  packages=find_packages(),
  install_requires=[
    'requests>=2.25.1',
    'pillow>=10.1.0',
    'opencv-python>=4.8.1.78',
    'numpy>=1.26.2'],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='soviet hellya pixel workshop',
  python_requires='>=3.9',
  url = "https://github.com/Soviet-WorkShop/hellya_lite"
)