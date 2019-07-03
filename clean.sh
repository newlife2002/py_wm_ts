#bin/sh
find . | grep ts$ | xargs rm -f
find . | grep txt$ | xargs rm -f
find . | grep m3u8$ | xargs rm -f
find . | grep -v mp4$ | xargs rmdir
