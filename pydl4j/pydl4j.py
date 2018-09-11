from .jarmgr import *
from .jarmgr import _MY_DIR
from .pom import *
from .docker import docker_file
import platform
import os
import warnings
import os
from subprocess import call


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
    # e.g pydl4j-1.0.0-SNAPSHOT-cpu-spark2-2.11
    context = 'pydl4j-{}-{}-spark{}-{}'.format(
        _CONFIG['dl4j_version'],
        _CONFIG['nd4j_backend'],
        _CONFIG['spark_version'],
        _CONFIG['scala_version'])
    return context


set_context(_get_context_from_config())


def create_pom_from_config():
    config = get_config()
    pom = pom_template()
    dl4j_version = config['dl4j_version']
    nd4j_backend = config['nd4j_backend']
    use_spark = config['spark']
    scala_version = config['scala_version']
    spark_version = config['spark_version']
    use_dl4j_core = config['dl4j_core']
    use_datavec = config['datavec']

    datavec_deps = datavec_dependencies() if use_datavec else ""
    pom =pom.replace('{datavec.dependencies}', datavec_deps)

    core_deps = dl4j_core_dependencies() if use_dl4j_core else ""
    pom = pom.replace('{dl4j.core.dependencies}', core_deps)

    spark_deps = spark_dependencies() if use_spark else ""
    pom = pom.replace('{spark.dependencies}', spark_deps)

    pom = pom.replace('{dl4j.version}', dl4j_version)

    if nd4j_backend == 'cpu':
        backend = "nd4j-native"
    else:
        backend = "nd4j-cuda-9.2-platform"
    pom = pom.replace('{nd4j.backend}', backend)

    if use_spark:
        pom = pom.replace('{scala.binary.version}', scala_version)
        # this naming convention seems a little off
        if "SNAPSHOT" in dl4j_version:
            dl4j_version = dl4j_version.replace("-SNAPSHOT", "")
            dl4j_spark_version = dl4j_version + "_spark_" + spark_version + "-SNAPSHOT"
        else:
            dl4j_spark_version = dl4j_version + "_spark_" + spark_version
        pom = pom.replace('{dl4j.spark.version}', dl4j_spark_version)
    
    # TODO replace if exists
    pom_xml = os.path.join(_MY_DIR, 'pom.xml')
    with open(pom_xml, 'w') as pom_file:
        pom_file.write(pom)


def docker_build():
    docker_path = os.path.join(_MY_DIR, 'Dockerfile')
    docker_string = docker_file()
    with open(docker_path, 'w') as f:
        f.write(docker_string)

    call(["sudo", "docker", "build", _MY_DIR, "-t", "pydl4j"])


def docker_run():
    create_pom_from_config()
    call(["sudo", "docker", "run", "--mount", "src=" + _MY_DIR + ",target=/app,type=bind", "pydl4j"])
    # docker will build into <context>/target, need to move to context dir
    context_dir = get_dir()
    config = get_config()
    dl4j_version = config['dl4j_version']
    jar_name = "pydl4j-{}-bin.jar".format(dl4j_version)
    base_target_dir = os.path.join(_MY_DIR, "target")
    source = os.path.join(base_target_dir, jar_name)
    target = os.path.join(context_dir, jar_name)
    # os.rename or shutil won't work in all cases, need to assume sudo role
    call(["sudo", "mv", source, target])


def install_from_docker():
    docker_build()
    docker_run()


def install_docker_jars():
    jars = get_jars()
    dl4j_version = _CONFIG['dl4j_version']
    jar_name = "pydl4j-{}-bin.jar".format(dl4j_version)
    jar = os.path.join(get_dir(), jar_name)
    if not jar in jars:
       install_from_docker()


def _nd4j_jars():
    url = 'https://deeplearning4jblob.blob.core.windows.net/jars/'
    base_name = 'nd4j-uberjar'
    version = '1.0.0-SNAPSHOT'  # uploaded uber jar version. Version installed using docker can be different.
    jar_url = url + '{}-{}-{}-{}-no_avx.jar'.format(base_name, version, get_os(), _CONFIG['nd4j_backend'])
    jar_name = '{}-{}.jar'.format(base_name, version)
    return {base_name: [jar_url, jar_name]}


def _datavec_jars():
    url = 'https://deeplearning4jblob.blob.core.windows.net/jars/'
    base_name = 'datavec-uberjar'
    version = '1.0.0-SNAPSHOT'
    spark_v = _CONFIG['spark_version']
    scala_v = _CONFIG['scala_version']
    jar_url = url + base_name + '-{}-spark{}-{}.jar'.format(version, spark_v, scala_v)
    jar_name = '{}-{}.jar'.format(base_name, version)
    return {base_name: [jar_url, jar_name]}


def _validate_jars(jars):
    installed_jars = get_jars()
    for k, v in jars.items():
        found = False
        for j in installed_jars:
            if j.startswith(k):
                found = True
                break
        if not found:
            print('pydl4j: Required jar not installed {}.'.format(v[1]))
            config = get_config()
            # TODO: do we need other checks here?
            if config['nd4j_backend'] != 'gpu' or config['dl4j_version'] != '1.0.0-SNAPSHOT':
                install_docker_jars()
            else:
                install(v[0], v[1])


def _install_jars(jars):  # Note: downloads even if already installed.
    for v in jars.values():
        install(v[0], v[1])    


def install_nd4j_jars():
    _install_jars(_nd4j_jars)


def validate_nd4j_jars():
    _validate_jars(_nd4j_jars())


def install_datavec_jars():
    _install_jars(_datavec_jars())  


def validate_datavec_jars():
    _validate_jars(_datavec_jars())


def set_jnius_config():
    try:
        import jnius_config
        jnius_config.set_classpath(os.path.join(get_dir(), '*'))
    # Further options can be set by individual projects
    except ImportError:
        warnings.warn('Pyjnius not installed.')

set_jnius_config()
