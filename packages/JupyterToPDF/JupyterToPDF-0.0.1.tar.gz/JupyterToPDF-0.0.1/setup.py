from setuptools import setup, find_packages

setup(
    name='JupyterToPDF',
    version='0.0.1',
    author='Nayeem Islam',
    author_email='nayeem60151126@gmail.com',  # Replace with your email
    description='A simple tool to convert Jupyter notebooks to PDF',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/nomannayeem',  # Replace with the URL of your package
    packages=find_packages(),
    install_requires=[
        'pdfkit',
        # Add other dependencies here, if any
    ],
    entry_points={
        'console_scripts': [
            'JupyterToPDF=JupyterToPDF.converter:convert_notebook_to_pdf',
        ],
    },
    classifiers=[
        # Choose classifiers as appropriate
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
    python_requires='>=3.6',
)
