import os
import time
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path

from .photo import Photo


class Camera(ABC):
    """Generic class of camera containing common methods."""

    def __init__(self) -> None:
        self._time_required = 0.0  # time required to capture a photo.

    def get_required_time(self) -> float:
        """Get time required to capture a photo."""
        return self._time_required

    @abstractmethod
    def take_photo(self) -> Photo:
        """Take a photo."""

    @abstractmethod
    def determine_capture_photo_time(self) -> bool:
        """Determine time required to capture a photo."""


class Sony(Camera):
    """Class representing the Sony alpha 6000 camera."""

    def __init__(self, save_dir: Path) -> None:
        super().__init__()
        self.save_dir = save_dir

    def take_photo(self) -> Photo:
        img_name = datetime.today().strftime("%H:%M:%S") + ".jpg"
        image_path = Path.joinpath(self.save_dir, img_name)

        os.system(
            f"""
            gphoto2 --trigger-capture --wait-event-and-download=FILEADDED \
            --filename {image_path} >/dev/null 2>&1
            """
        )

        return Photo(path=image_path)

    def determine_capture_photo_time(self) -> bool:
        start_time = time.time()
        result = self.take_photo().exists()
        self._time_required = time.time() - start_time
        return result
