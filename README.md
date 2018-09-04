# mvn4py
Jar manager for pyjnius applications

---------

Mvn4py is a lightweight package manager for pyjnius based python applications. Jars can be pulled from Maven central or arbitrary url.

### Example:

```python
import mvn4py
import jnius_config

mvn4py.set_context('my_python_app_name')

# Fetch latest version of datavec.datavec-api from Maven central
mvn4py.install(group='datavec', artifact='datavec-api')

# Or fetch a specific version:
mvn4py.install(group='datavec', artifact='datavec-api', version='1.0.0-beta')


jnius_config.set_classpath(mvn4py.get_dir())
```

### Installation

```
git clone https://www.github.com/deeplearning4j/mvn4py.git
cd mvn4py
python setup.py install
```

### Full API:

#### List all artifacts in a group:
```python
mvn4py.get_artifacts(group_id)
```
##### Example:
```python
mvn4py.get_atrifacts('datavec')
```
```
['datavec-api', 'datavec-arrow', 'datavec-camel', 'datavec-cli', 'datavec-data', 'datavec-data-audio', 'datavec-data-codec', 'datavec-d
ata-image', 'datavec-data-nlp', 'datavec-dataframe', 'datavec-excel', 'datavec-geo', 'datavec-hadoop', 'datavec-jdbc', 'datavec-local',
 'datavec-nd4j-common', 'datavec-parent', 'datavec-perf', 'datavec-spark-inference-client', 'datavec-spark-inference-model', 'datavec-s
park-inference-parent', 'datavec-spark-inference-server_2.10', 'datavec-spark-inference-server_2.11', 'datavec-spark_2.10', 'datavec-sp
ark_2.11']
```

#### List all versions of an artifact:

```python
mvn4py.get_versions(group_id, artifact_id)
```

##### Example:

```python
mvn4py.get_versions('datavec', 'datavec-api')
```

```
['0.4.0', '0.5.0', '0.6.0', '0.7.0', '0.7.1', '0.7.2', '0.8.0', '0.9.0', '0.9.1', '1.0.0-alpha', '1.0.0-beta', '1.0.0-beta2']
```

#### Get latest version of an artifact:

```python
mvn4py.get_latest_version(group_id, artifact_id)
```

##### Example:

```python
mvn4py.get_latest_version('datavec', 'datavec-api')
```
```
'1.0.0-beta2'
```

#### List all installed jars

```python
mvn4py.get_jars()
```

#### Uninstall a jar

```python
# Find jar name from mvn4py.get_jars()
mvn4py.uninstall(jar_name)
```

#### Uninstall all jars:

```python
mvn4py.clear_context()
```



