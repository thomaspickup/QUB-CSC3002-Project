from distutils.core import setup
import py2exe

setup(console=['main.pyw'],
      data_files=[r'mlcore\Model_Creation_Script.R', r'mlcore\Product_Script.R'])
