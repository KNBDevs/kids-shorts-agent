#!/usr/bin/env bash
# Montaje final: frames 720x1280 -> 1080x1920 9:16, audio normalizado a -14 LUFS (YouTube).
set -euo pipefail
cd "$(dirname "$0")"
FR=${FR:-frames}
OUT=${OUT:-pilot_short.mp4}
ffmpeg -y -loglevel error -framerate 24 -start_number 0 -i "$FR/f%04d.png" -i soundtrack.wav \
  -filter_complex "[0:v]scale=1080:1920:flags=lanczos,unsharp=5:5:0.5,format=yuv420p[v];\
[1:a]loudnorm=I=-14:TP=-1.5:LRA=9,aresample=48000[a]" \
  -map "[v]" -map "[a]" -c:v libx264 -preset slow -crf 17 -profile:v high -pix_fmt yuv420p \
  -c:a aac -b:a 192k -movflags +faststart -t 20 "$OUT"
echo "OK -> $OUT"
