#!/bin/zsh

ffmpeg -i $1_A.webm -i $1_V.webm -acodec copy -vcodec copy $1.webm