import pytest
from pydl4j import *


def test_get_artifacts():
    artifacts = get_artifacts('datavec')
    expected = ['datavec-api', 'datavec-local', 'datavec-parent']
    for e in expected:
        assert e in artifacts


def test_get_versions():
    versions = get_versions('datavec', 'datavec-api')
    assert len(versions) >= 12


def test_get_latest_version():
    v = get_latest_version('datavec', 'datavec-api')
    assert len(v) > 0


def test_install():
    set_context('test')
    clear_context()
    mvn_install('datavec', 'datavec-api')
    mvn_install('datavec', 'datavec-local')
    assert len(get_jars()) == 2
    for jar in get_jars():
        uninstall(jar)
    assert len(get_jars()) == 0
    clear_context()



if __name__ == '__main__':
    pytest.main([__file__])