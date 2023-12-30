from distutils.core import setup

setup(
  name = 'sentibank', 
  packages = ['sentibank'],   
  version = '0.0.1.13',      
  license='CC BY-NC-SA 4.0',        
  description = 'Unifying sentiment lexicons and dictionaries into an accessible open python package',   
  author = 'Nick S.H Oh',                   
  author_email = 'nick.sh.oh@socialscience.ai',      
  url = 'https://github.com/socius-org/sentibank',  
  download_url = 'https://github.com/socius-org/sentibank/archive/refs/tags/0.0.1.13.tar.gz', 
  keywords = ['AI', 'Social Science', 'Sentiment Analysis'],   # Keywords that define your package best
  install_requires=[
          'spacy == 3.7.2',
          'spacymoji == 3.1.0',
          'rich == 13.4.2'
      ],
  extras_require ={
    'utils': ['spacy[en_core_web_sm]'], 
  }, 
  include_package_data=True
)
