import os
from subprocess import call

from .jarmgr import _MY_DIR as base_dir
from .pom import create_pom_from_config

def docker_file():
    return """FROM java:openjdk-8-jdk
ENV MAVEN_VERSION 3.3.9

RUN curl -fsSL http://archive.apache.org/dist/maven/maven-3/$MAVEN_VERSION/binaries/apache-maven-$MAVEN_VERSION-bin.tar.gz | tar xzf - -C /usr/share \
  && mv /usr/share/apache-maven-$MAVEN_VERSION /usr/share/maven \
  && ln -s /usr/share/maven/bin/mvn /usr/bin/mvn

ENV MAVEN_HOME /usr/share/maven

# Copy application to container
RUN mkdir -p app
WORKDIR /app

CMD ["mvn", "package"]
"""

def docker_build():
    docker_path = os.path.join(base_dir, 'Dockerfile')
    docker_string = docker_file()
    with open(docker_path, 'w') as f:
        f.write(docker_string)

    call(["sudo", "docker", "build", base_dir, "-t", "pydl4j"])

def docker_run():
    create_pom_from_config()
    call(["sudo", "docker", "run", "--mount", "src=" + base_dir + ",target=/app,type=bind", "pydl4j"])

