
import setuptools
  
with open("README.md", "r") as fh:
    description = fh.read()
  
setuptools.setup(
    name="clsquery",
    version="1.0",
    author="Kenneth Mead",
    author_email="kennethmead784@gmail.com",
    packages=["clsquery"],
    description="A package for querying Python classes",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/Xerner/python-class-query",
    license='MIT',
    python_requires='>=3.7',
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
    ],
    install_requires=[]
)
