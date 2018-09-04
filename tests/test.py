import pytest
import pydl4j


def test_get_artifacts():
    artifacts = pydl4j.get_artifacts('datavec')
    expected = ['datavec-api', 'datavec-local', 'datavec-parent']
    for e in expected:
        assert e in artifacts


def test_get_versions():
    versions = pydl4j.get_versions('datavec', 'datavec-api')
    assert len(versions) >= 12


def test_get_latest_version():
    v = pydl4j.get_latest_version('datavec', 'datavec-api')
    assert len(v) > 0


def test_install():
    pydl4j.set_context('test')
    pydl4j.clear_context()
    pydl4j.install('datavec', 'datavec-api')
    pydl4j.install('datavec', 'datavec-local')
    assert len(pydl4j.get_jars()) == 2
    for jar in pydl4j.get_jars():
        pydl4j.uninstall(jar)
    assert len(pydl4j.get_jars()) == 0
    pydl4j.clear_context()



if __name__ == '__main__':
    pytest.main([__file__])