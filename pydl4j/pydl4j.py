from .jarmgr import *
from .jarmgr import _MY_DIR
import platform
import os
import warnings


def get_os():
    osname = platform.system()
    os_map = {
        'Windows': 'windows',
        'Linux': 'linux',
        'Darwin': 'mac'
    }
    if osname not in os_map:
        raise ValueError('{} platform is not supported.'.format(osname))
    return os_map[osname]


_CONFIG_FILE = os.path.join(_MY_DIR, 'config.json')



# Default config
_CONFIG = {
    'dl4j_version': '1.0.0-SNAPSHOT',
    'dl4j_core': True,
    'datavec': True,
    'spark': True,
    'spark_version': '2',
    'scala_version': '2.11',
    'nd4j_backend': 'cpu'
}


def _write_config():
    with open(_CONFIG_FILE, 'w') as f:
        json.dump(_CONFIG, f)    

if os.path.isfile(_CONFIG_FILE):
    with open(_CONFIG_FILE, 'r') as f:
        _CONFIG = json.load(f)
else:
    _write_config()


def set_config(config):
    _CONFIG.update(config)
    _write_config()


def get_config():
    return _CONFIG


def validate_config(config=None):
    if config is None:
        config = _CONFIG
    valid_options = {
        'spark_version': ['1', '2'],
        'scala_version': ['2.10', '2.11'],
        'nd4j_backend': ['cpu', 'gpu']
    }
    for k, vs in valid_options.items():
        v = config.get(k)
        if v is None:
            raise KeyError('Key not found in config : {}.'.format(k))
        if v not in vs:
            raise ValueError('Invalid value {} for key {} in config. Valid values are: {}.'.format(v, k, vs))

    # spark 2 does not work with scala 2.10
    if config['spark_version'] == '2' and config['scala_version'] == '2.10':
        raise ValueError('Scala 2.10 does not work with spark 2. Set scala_version to 2.11 in pydl4j config. ')


def _get_context_from_config():
    # e.g pydl4j-cpu-spark2-2.11
    context = 'pydl4j-{}-{}-spark{}-{}'.format(
        _CONFIG['dl4j_version'],
        _CONFIG['nd4j_backend'],
        _CONFIG['spark_version'],
        _CONFIG['scala_version'])
    return context


set_context(_get_context_from_config())


def _jumpy_jars():
    url = 'https://github.com/deeplearning4j/pydl4j_jars/releases/download/v0.1-alpha/'
    base_name = 'nd4j-uberjar-1.0.0-SNAPSHOT'
    jar_url = url + base_name + '-' + _CONFIG['nd4j_backend'] + '.jar'
    jar_name = base_name + '.jar'
    return {jar_name: jar_url}


def _pydatavec_jars():
    url = 'https://github.com/deeplearning4j/pydl4j_jars/releases/download/v0.1-alpha/'
    base_name = 'datavec-uberjar-1.0.0-SNAPSHOT'
    spark_v = _CONFIG['spark_version']
    scala_v = _CONFIG['scala_version']
    jar_url = url + base_name + '-spark{}-{}.jar'.format(spark_v, scala_v)
    jar_name = base_name + '.jar'
    return {jar_name: jar_url}


def install_jumpy_jars():  # Note: downloads even if already installed.
    for k, v in _jumpy_jars().items():
        install(v, k)

def validate_jumpy_jars():
    installed_jars = get_jars()
    for k, v in _jumpy_jars().items():
        if k not in installed_jars:
            print('pydl4j: Required jar not installed {}.'.format(k))
            install(v, k)


def install_pydatavec_jars():  # Note: downloads even if already installed.
    for k, v in _pydatavec_jars().items():
        install(v, k)   

def validate_pydatavec_jars():
    installed_jars = get_jars()
    for k, v in _pydatavec_jars().items():
        if k not in installed_jars:
            print('pydl4j: Required jar not installed {}.'.format(k))
            install(v, k)


def set_jnius_config():
    try:
        import jnius_config
        jnius_config.set_classpath(os.path.join(get_dir(), '*'))
    # Further options can be set by individual projects
    except ImportError:
        warnings.warn('Pyjnius not installed.')

set_jnius_config()
