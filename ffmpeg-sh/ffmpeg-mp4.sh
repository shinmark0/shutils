#!/bin/zsh
ffmpeg -i $1_A.mp4 -i $1_V.mp4 -acodec copy -vcodec copy $1.mp4