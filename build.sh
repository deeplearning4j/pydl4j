#!/bin/bash
mkdir -p $HOME/.pdl4j
cp pom.xml $HOME/.pdl4j
sudo docker build . -t pydl4j
sudo docker run --mount src="$HOME/.pydl4j",target=/app,type=bind pydl4j
# this will put uberjars into ~/.pydl4j/target