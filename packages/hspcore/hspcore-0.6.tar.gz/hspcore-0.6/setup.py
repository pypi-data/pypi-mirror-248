from setuptools import setup


with open("README.md", "r") as description:
    long_description = description.read()

setup(
  name = 'hspcore',
  version = '0.6',
  license='MIT',
  description = 'Hansen Solubility Parameters (HSP) core functions',
  long_description=long_description,
  long_description_content_type='text/markdown',
  author = 'Alejandro Gutierrez',
  author_email = 'a.gutierrez@g-npd.com',
  url = 'https://github.com/Gnpd/hspcore', 
  download_url = 'https://github.com/Gnpd/hspcore/archive/refs/tags/v_0.6.tar.gz',
  keywords = ['HSP', 'Solubility'],
  install_requires=["scipy"],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.11',
  ],
  python_requires='>=3.6',
)