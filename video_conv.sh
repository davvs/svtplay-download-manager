#!/bin/bash
FILES=/Users/pontus.lundwall/Desktop/video-tests/*
OUT=/Users/pontus.lundwall/Desktop/video-tests/out
FF=/usr/local/bin/ffmpeg
for f in $FILES
do
	# plocka ut basnamnet, ingen path eller file extension
	y=${f/\/*\//} 
	name=${y/.*/}
	# max gränser, avrunda bredden generöst uppåt (nästa heltal; 853.3 -> 854)
	WIDTH=854
	HEIGHT=480
	# förenklad kompressionskvalité, värdet bör vara i området 16-40 (16 onödigt högt, ~10Mbit för 720p typ)
	QUALITY=26
	# plocka ett screenshot från 2s in (utan att skala ned först)
	$FF -y -i $f -an -ss 00:00:02 -r 1 -vframes 1 $OUT/$name.jpg 2>/dev/null
	# se efter om skalning kommer genomföras, och lägg till sharpen i så fall
	text=`$FF -i $f 2>&1 | grep 'Video: ' | cut -d \  -f 14`
	OW=${text%x*}
	OW=${OW//[^0-9]/}
	OH=${text#*x}
	OH=${OH//[^0-9]/}
	if [ "$OW" -gt "$WIDTH" ]
	then
		RESIZE=",unsharp=3:3:1.0:3:3:0.0"
	fi
	if  [ "$OH" -gt "$HEIGHT" ]
	then
		RESIZE=",unsharp=3:3:1.0:3:3:0.0"
	fi
	# plocka ut angiven frame rate för att låsa output till detta
	text=`$FF -i $f 2>&1 | grep 'Video: ' | cut -d \  -f 21`
	RATE=${text%x*}
	# transcoda vad som helst till x264/aac med filter brus, kanske storlek och kanske sharpen
	# ,transpose=2,vflip
	$FF -y -i $f -vf "mp=eq2=1.0:2:0.5,hqdn3d=1.5:1.5:6:6,scale=min(iw\,trunc(iw*min($WIDTH/iw\,$HEIGHT/ih)*0.5)*2):min(ih\,trunc(ih*min($WIDTH/iw\,$HEIGHT/ih)*0.5)*2)$RESIZE" -threads 0 -r $RATE -acodec libvo_aacenc -b:a 96k -ac 2 -ar 44100 -vcodec libx264 -crf $QUALITY -metadata:s:v:0 rotate=0 -movflags faststart -pix_fmt yuv420p $OUT/$name.mp4
	# plocka ut den resulterande genomsnitts bitraten på filen som skapades.
	# bitrate=`ffmpeg -i $OUT/$name.mp4 2>&1 | grep 'bitrate: ' | cut -d \  -f 8`k
	# transcoda till webm (vp8) och använd samma bitrate som för x264.
	# ffmpeg -y -i $f -quality good -qmin 10 -qmax 42 -vcodec libvpx -threads 4 -cpu-used 2 -b:v $bitrate -acodec libvorbis $OUT/$name.webm
done

