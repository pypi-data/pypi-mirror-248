import base64
import typing
import tempfile
import warnings

try:
    import cv2
    import numpy as np

except ImportError as e:
    cv2 = None
    numpy = None
    warnings.warn('Package %r not found, auto preview disabled' % e.name)


class ResultMedia:
    def __repr__(self) -> str:
        return repr(vars(self))

    def __init__(self,
                 thumbnail: bytes,
                 width: typing.Optional[int] = 200,
                 height: typing.Optional[int] = 200,
                 seconds: typing.Optional[int] = 1) -> None:
        self.image = thumbnail
        self.width = width
        self.height = height
        self.seconds = seconds

    def to_base64(self):
        return base64.b64encode(self.image).decode('utf-8')


class MediaThumbnail:
    @classmethod
    def from_image(cls, image: bytes) -> ResultMedia:
        # Check if OpenCV and NumPy are available
        if cv2 is None or np is None:
            warnings.warn('OpenCV or NumPy not found, image processing disabled')
            return None

        # If image is not a NumPy array, convert it
        if not isinstance(image, np.ndarray):
            image = np.frombuffer(image, dtype=np.uint8)
            image = cv2.imdecode(image, flags=1)

        # Resize the image
        height, width = image.shape[0], image.shape[1]
        image = cv2.resize(image, (round(width / 10), round(height / 10)), interpolation=cv2.INTER_CUBIC)

        # Encode the image to PNG format
        status, buffer = cv2.imencode('.png', image)
        if status:
            return ResultMedia(bytes(buffer), width=width, height=height)

    @classmethod
    def from_video(cls, video: bytes) -> typing.Optional[ResultMedia]:
        # Check if OpenCV is available
        if cv2 is None:
            warnings.warn('OpenCV not found, video processing disabled')
            return None

        # Write video content to a temporary file
        with tempfile.NamedTemporaryFile(mode='wb+', suffix='.mp4') as file:
            file.write(video)

            # Read the video using OpenCV
            capture = cv2.VideoCapture(file.name)
            status, image = capture.read()

            # If successful, calculate video duration and create ResultMedia object
            if status:
                fps = capture.get(cv2.CAP_PROP_FPS)
                frames = capture.get(cv2.CAP_PROP_FRAME_COUNT)
                seconds = int(frames / fps) * 1000
                width = image.shape[1]
                height = image.shape[0]

                result = ResultMedia(image, width, height, seconds)
                return result