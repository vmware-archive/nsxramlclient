from setuptools import setup
import io

def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

long_description = read('README.rst')

setup(
    name='nsxramlclient',
    version='1.0.3',
    packages=['nsxramlclient'],
    url='http://github.com/vmware/nsxramlclient',
    license='MIT',
    author='yfauser',
    author_email='yfauser@yahoo.de',
    description='A "pseudo dynamic" client for the VMware NSX for vSphere API that uses a RAML file describing the API '
                'as an Input to generate the API calls',
    long_description=long_description,
    classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Libraries',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 2.7'],
    install_requires=['pyraml-parser>=0.1.3', 'lxml', 'requests>=2.7.0', 'tabulate']
)
