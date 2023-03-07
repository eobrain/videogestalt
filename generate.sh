#IN=BigBuckBunny.mp4
IN=nightmare-castle.mp4
N=16

fullDuration=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 $IN)
fullWidth=$(ffprobe -v error -show_entries stream=width    -of default=noprint_wrappers=1:nokey=1 $IN)
fullHeight=$(ffprobe -v error -show_entries stream=height   -of default=noprint_wrappers=1:nokey=1 $IN)

segmentDuration=$(echo $fullDuration / $N | bc -l)
segmentWidth=$(echo $fullWidth / $N | bc -l)
segmentHeight=$(echo $fullHeight / $N | bc -l)

cat >x.html <<EOF
<head>
    <script src="index.js" type="module"></script>
    <link rel="stylesheet" href="x.css">
</head>

<body>
    <img id="leading" src="data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==">
EOF

for ((i = 0; i <= $N; i++)); do
  cat >>x.html <<EOF
        <video muted autoplay loop>
            <source src="${i}.mp4" type="video/mp4">
        </video>
EOF
  startOffset=$(echo $i \* $segmentDuration | bc -l)
  ffmpeg -y -ss $startOffset -t $segmentDuration -i $IN -vf scale=w=${segmentWidth}:h=${segmentHeight}:force_original_aspect_ratio=decrease:force_divisible_by=2 $i.mp4
done

cat >>x.html <<EOF
</body>

</html>
EOF

cat >x.css <<EOF
#leading {
  height: 1px;
  animation: ${segmentDuration}s linear infinite shift;
}

@keyframes shift {
  from {
    width: 0;
  }

  to {
    width: ${segmentWidth}px;
  }
}
EOF
