import pytest
import mvn4py


def test_get_artifacts():
    artifacts = mvn4py.get_artifacts('datavec')
    expected = ['datavec-api', 'datavec-local', 'datavec-parent']
    for e in expected:
        assert e in artifacts


def test_get_versions():
    versions = mvn4py.get_versions('datavec', 'datavec-api')
    assert len(versions) >= 12


def test_get_latest_version():
    v = mvn4py.get_latest_version('datavec', 'datavec-api')
    assert len(v) > 0


def test_install():
    mvn4py.set_context('test')
    mvn4py.clear_context()
    mvn4py.install('datavec', 'datavec-api')
    mvn4py.install('datavec', 'datavec-local')
    assert len(mvn4py.get_jars()) == 2
    for jar in mvn4py.get_jars():
        mvn4py.uninstall(jar)
    assert len(mvn4py.get_jars()) == 0
    mvn4py.clear_context()



if __name__ == '__main__':
    pytest.main([__file__])