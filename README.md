I made some changes to original Brandon Withrow's [Waveshare-version TV build](https://withrow.io/simpsons-tv-build-guide-waveshare).

## Hardware changes

Used the newer RPi Zero 2W. This was mostly a drop-in replacement.

I attempted to use a 64-bit version Debian Bookworm, but couldn't properly get
it to work. The screen worked using the newer Waveshare screen overlay setup,
but it took control of the GPIO pins needed for the audio circuit. So I
continued to use the 32-bit Buster OS.

I also glued in the screen upside down, since the bezel was better covered by
the 3d printed housing that way. To invert the screen, set `display_rotate=3` in `/boot/config.txt`

## Videos on FAT partition

It's much easier to manage the videos when they are on a separate FAT partition
on the SD Card. Rather than copying over the network or mounting another thumb
drive, the card can be plugged in to a normal computer and files can be copied
to a mounted partition.

After initially flashing Raspbian (and editing `config.txt`, etc) but before first boot, which will auto-resize partition to take up all the remaining free space, create a new fat32 partition at the END of the free space. But still leaving enough room for the original linux partition to grow. I left 10GB. This was done using Gparted on a separate linux machine.

Later, once the RPpi is up and you are logged in, you can manually resize the
ext4 partition, via something like:

```
# Resize the ext4 / partition
sudo parted
> print
> resizepart 2 8G
> <ctrl-D>

# Extend the ext4 filesystem to fill up the partitioned space.
df -h
blkid
sudo resize2fs /dev/mmcblk0p2
df -h
```

Finally, auto-mount the videos data partition at `/video`
`sudo mkdir /video`

Then add the following line to `/etc/fstab`
```
  /dev/mmcblk0p3 /video vfat defaults 0 2
```

## MPV Video player

Because I was originally experimenting 64-bit Bookwork, I couldn't use omxplayer
since it was no longer provided with that distribution. Instead I found MPV to
be a great replacement, and ended up using it for my touch screen scripting as
well.

`sudo apt install mpv`

## Touchscreen player control

The Waveshare 2.8" screen has capacitive touch that wasn't used in the original
build. I added a simple `touch.py` job to listen to screen events and send a
handful of commands to the video player. Be sure to add a corresponding systemd
service.

You can:
- Touch left side of screen - seek back 30 seconds
- Touch middle of screen - play / pause
- Touch right side of screen - seek forward 30 seconds
- Swipe from left to right - next video
- Swipe from right to left - previous video
