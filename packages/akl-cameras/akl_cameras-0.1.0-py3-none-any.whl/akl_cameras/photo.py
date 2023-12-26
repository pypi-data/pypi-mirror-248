import json
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Photo:
    """Class representing the photo taken."""

    path: Path

    def exists(self) -> bool:
        """Check if the photo file exists."""
        return self.path.exists()

    def save_metadata(self, lat: float, lon: float, alt: float) -> bool:
        """Save the photo metadata in a JSON file
        in the same location as the related photo.
        """
        pasition = {"lat": lat, "lon": lon, "alt": alt}

        json_object = json.dumps(pasition, indent=4)
        name = self.path.name.replace("jpg", "json")
        path = self.path.with_name(name)

        with open(path, "w", encoding="utf-8") as outfile:
            outfile.write(json_object)
        return path.exists()

    def get_name(self) -> str:
        """Get the photo file name."""
        return self.path.name
