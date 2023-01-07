import argparse
import logging

import cv2
import pyvirtualcam


def run_broadcast(stream_video_path: str, device_number: int) -> None:
    """Starts broadcasting of input video on a virtual device.

    Args:
        stream_video_path: Path to the input video to be streamed
        device_number: Virtual device number that will be created
    """

    # Open the video
    cap = cv2.VideoCapture(stream_video_path)

    # Check if camera opened successfully
    if cap.isOpened() is False:
        logging.error(f"Error opening video stream or file: {stream_video_path}")
        exit()

    # Width, height, and fps of the video
    WIDTH = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    HEIGHT = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    FPS = int(cap.get(cv2.CAP_PROP_FPS))

    # Virtual device created by v4l2loopback
    # It should be different than existing devices
    # Check existing devices 'ls /dev/video*'
    device = f"/dev/video{device_number}"

    try:
        # Create virtual camera
        cam = pyvirtualcam.Camera(width=WIDTH, height=HEIGHT, fps=FPS, device=device)
    except RuntimeError as e:
        # Print error message and possible solution
        logging.error(e.args[0])
        logging.error("Try running this on terminal:")
        logging.error(
            "$ sudo modprobe -r v4l2loopback && "
            f"sudo modprobe v4l2loopback devices=1 video_nr={device_number} card_label='Virtual' exclusive_caps=1 max_buffers=2"
        )
        exit()

    # Start streaming
    logging.info(f"Using virtual camera: {cam.device}")
    logging.info(f"Press CTRL+C to stop streaming: {cam.device}")
    while cap.isOpened():
        ret, frame = cap.read()
        if ret == True:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            cam.send(frame)
            cam.sleep_until_next_frame()


if __name__ == "__main__":

    # Set logger level to debug to print all messages.
    logging.getLogger().setLevel(logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input_video", help="Path to the input video to be streamed", type=str
    )
    parser.add_argument(
        "--device_number",
        help="Virtual device number that will be created",
        type=int,
        default=42,
    )

    args = parser.parse_args()

    run_broadcast(stream_video_path=args.input_video, device_number=args.device_number)
