from .pydl4j import *

if 'PYDL4J_HOME' in os.environ:
    _pydl4j_dir = os.environ.get('PYDL4J_HOME')
else:
    _pydl4j_base_dir = os.path.expanduser('~')
    if not os.access(_pydl4j_base_dir, os.W_OK):
        _pydl4j_base_dir = '/tmp'
    _pydl4j_dir = os.path.join(_pydl4j_base_dir, '.pydl4j')

if not os.path.exists(_pydl4j_dir):
    try:
        os.makedirs(_pydl4j_dir)
    except OSError:
        pass