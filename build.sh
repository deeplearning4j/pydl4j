#!/bin/bash
cp pom.xml $HOME/.pydl4j
sudo docker build . -t pydl4j
sudo docker run --mount src="$HOME/.pydl4j",target=/app,type=bind pydl4j