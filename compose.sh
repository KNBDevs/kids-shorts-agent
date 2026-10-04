set -euo pipefail
cd "$(dirname "$0")"
FR=${FR:-frames}; OUT=${OUT:-out.mp4}; MAX_BYTES=${MAX_BYTES:-4800000}; DUR=20
ABR=128
VBR=$(( (MAX_BYTES * 8 / DUR / 1000) * 92 / 100 - ABR ))
ffmpeg -y -loglevel error -i soundtrack.wav -af loudnorm=I=-14:TP=-1.5:LRA=9,aresample=48000 -c:a aac -b:a ${ABR}k a.m4a
VF="scale=1080:1920:flags=lanczos,unsharp=5:5:0.4,format=yuv420p"
for p in 1 2; do
  ffmpeg -y -loglevel error -framerate 24 -start_number 0 -i "$FR/f%04d.png" -vf "$VF" \
    -c:v libx264 -preset slow -b:v ${VBR}k -maxrate $((VBR * 2))k -bufsize $((VBR * 2))k \
    -profile:v high -pass $p -passlogfile x264 -an -f mp4 $([ $p = 1 ] && echo /dev/null || echo v.mp4)
done
ffmpeg -y -loglevel error -i v.mp4 -i a.m4a -c copy -movflags +faststart -t $DUR "$OUT"
SIZE=$(stat -c %s "$OUT"); echo "OK $OUT ${SIZE}B (video ${VBR}k)"
[ "$SIZE" -le "$MAX_BYTES" ]
