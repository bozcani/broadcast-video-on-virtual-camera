
# Broadcast Video On Virtual Camera In Linux

## Installation
1. Install v4l2loopback:
    `sudo apt-get install v4l2loopback-dkms`
2. Install the library
	```
	git clone https://github.com/bozcani/broadcast-video-on-virtual-camera
	cd broadcast-video-on-virtual-camera
	pip install -r requirement.txt
	```
## Usage
1. Create virtual camera with ID 42.
	```
	sudo modprobe -r v4l2loopback 
	sudo modprobe v4l2loopback devices=1 video_nr=42 card_label="Virtual" exclusive_caps=1 max_buffers=2
	```
2. Run streaming a video on the camera 42.
```python run_broadcast.py --input_video chickens.mp4 --device_number 42```

3. Check your camera with webcam, zoom, google-meet, or anything that show your camera. You should see chickens!

![image info](./chickens.jpg)

Video is taken from https://youtu.be/oHpetnUFQMA
