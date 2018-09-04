from .downloader import download as download_file
import requests
import os


def mkdir(x):
	if not os.path.isdir(x):
		os.mkdir(x)


_CONTEXT_NAME = None
_CONTEXT_DIR = None
_USER_PATH = os.path.expanduser('~')


_cache = {}
def _read(url):
    text = _cache.get(url)
    if text is None:
        text = requests.get(url).text
        if not text:
            raise Exception('Empty response. Check connectivity.')
        _cache[url] = text
    return text


def _parse_contents(text):
    contents = text.split('<pre id="contents">')[1]
    contents = contents.split('</pre>')[0]
    contents = contents.split('<a href="')
    _ = contents.pop(0)
    link_to_parent = contents.pop(0)
    contents = list(map(lambda x: x.split('"')[0], contents))
    contents = [c[:-1] for c in contents if c[-1] == '/']  # removes meta data files
    return contents


def check(f):
    def wrapper(*args, **kwargs):
        if _CONTEXT_NAME is None:
            raise Exception('Context not set! Set context using mvn4py.set_context()')
        mkdir(_CONTEXT_DIR)
        return f(*args, **kwargs)
    return wrapper    


def set_context(name):
    global _CONTEXT_NAME
    global _CONTEXT_DIR
    _CONTEXT_NAME = name
    _CONTEXT_DIR = os.path.join(_USER_PATH, '.' + name)
    mkdir(_CONTEXT_DIR)


def get_artifacts(group):
    url = ('https://search.maven.org/remotecontent?filepath=' +
          'org/{}/'.format(group))
    response = _read(url)
    return _parse_contents(response)


def get_versions(group, artifact):
    url = ('https://search.maven.org/remotecontent?filepath=' +
          'org/{}/{}/'.format(group, artifact))
    response = _read(url)
    return _parse_contents(response)


def get_latest_version(group, artifact):
    return get_versions(group, artifact)[-1]


def get_jar_url(group, artifact, version=None):
    if version is None:
        version = get_versions(group, artifact)[-1]
    url = ('http://search.maven.org/remotecontent?filepath=' + 
          'org/{}/{}/{}/{}-{}.jar'.format(group, artifact, version,
                                          artifact, version))
    return url


@check
def context():
    return _CONTEXT_NAME


@check
def get_dir():
    return _CONTEXT_DIR


@check
def install_url(url):
    jar_name = os.path.basename(url)
    jar_path = os.path.join(_CONTEXT_DIR, jar_name)    
    download_file(url, jar_path)


@check
def install(group, artifact, version=None):
    if version is None:
        version = get_latest_version(group, artifact)
        print('Version not specified for org.{}.{}.'
              'Installing latest version: {}.'.format(group, artifact, version))
    url = get_jar_url(group, artifact, version)
    sha1_url = url + '.sha1'
    jar_name = os.path.basename(url)
    jar_path = os.path.join(_CONTEXT_DIR, jar_name)
    sha1_path_temp = jar_path + '.sha1.tmp'
    sha1_path = jar_path + '.sha1'
    if os.path.isfile(sha1_path):
        os.remove(sha1_path)
    if os.path.isfile(sha1_path_temp):
        os.remove(sha1_path_temp)
    download_file(sha1_url, sha1_path)
    os.rename(sha1_path, jar_path + '.sha1')
    download_file(url, jar_path)


@check
def uninstall(artifact, version=None):
    files = os.listdir(_CONTEXT_DIR)
    if version is not None:
        artifact += '-' + version
    if not artifact.endswith('.jar'):
        artifact += '.jar'
    found = False
    for f in files:
        if f == artifact:
            os.remove(os.path.join(_CONTEXT_DIR, f))
            found = True
    if not found:
        raise Exception('No matching jars found : {}. '
                        'Use mvn4py.get_jars() to see available jars.'.format(artifact))


@check
def get_jars():
    return [x for x in os.listdir(_CONTEXT_DIR) if x.endswith('.jar')]


@check
def clear_context():
    for j in get_jars():
        uninstall(j)
    try:
        os.remove(_CONTEXT_DIR)
    except:
        pass
