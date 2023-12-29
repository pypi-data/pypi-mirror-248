from setuptools import setup, find_packages

setup(
    name='basextools',
    version='0.0.20',
    packages=find_packages(),
    package_data={
        'pt_core_news_md':['basex/models/pt_core_news_md/*']
    },
    install_requires=[
        'numpy~=1.24.3',
        'pandas~=2.0.2',
        'scipy~=1.10.1',
        'matplotlib~=3.7.1',
        'matplotlib_venn~=0.11.9',
        'sentence-transformers~=2.2.2',
        'scikit-learn~=1.3.1',
        'plotly~=5.15.0',
        'seaborn~=0.12.2',
        'spacy==3.7.2',
        'Unidecode==1.3.7',
        'nltk==3.8.1',
        'regex==2023.10.3'
    ],
    author='pin-people',
    author_email='rodrigo.toledo@pinpeople.com.br',
    description='Tools for EX Analysis',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    extras_require={
        "dev":[
            "pytest>=3.7"
        ],
    },
    classifiers=[]
)
