import math
from io import BytesIO
from pathlib import Path
from typing import Literal

import googlemaps
import numpy as np
from PIL import Image

from geomlcv.utils.download_data import google

# Functions to download images and stitch them


def get_min_max_xy_bbox_coords(bbox_tight_coords):
    exterior_ring = bbox_tight_coords.exterior
    x_coords, y_coords = exterior_ring.xy

    x_min = min(x_coords)
    y_min = min(y_coords)
    x_max = max(x_coords)
    y_max = max(y_coords)

    return x_min, y_min, x_max, y_max


def calculate_tile_size_degrees(
    side_pixels: int, zoom_level: int, latitude_degrees: float
):
    # Reference: https://wiki.openstreetmap.org/wiki/Zoom_levels
    # Latitude to radians
    latitude_radians = math.radians(latitude_degrees)

    earth_circunf = 2 * math.pi * 6378137

    # horizontal distance in meters represented by each square tile in GMS
    gms_side_tile_meters = (earth_circunf * math.cos(latitude_radians)) / (
        2**zoom_level
    )

    # GMS tiles are 256-pixels wide, horizontal distance in meters
    # represented by one pixel is:
    gms_side_pixel_meters = gms_side_tile_meters / 256

    # Calculate size of the tile
    tile_side_meters = side_pixels * gms_side_pixel_meters
    tile_side_degrees = (tile_side_meters / 1000) / 111

    return tile_side_degrees


def generate_centroid_grid_array(
    cx: float,  # longitud degrees
    cy: float,  # latitude degrees
    n_tiles_horizontal: int,
    n_tiles_vertical: int,
    height_degrees: float,
    width_degrees: float,
    bbox_coords=None,
    n_tiles_limit=None,
):
    if bbox_coords is None:
        # Calculate coordinates of the centroids for the endpoints
        x_min = cx - (n_tiles_horizontal - 1) / 2 * width_degrees
        x_max = cx + (n_tiles_horizontal - 1) / 2 * width_degrees
        y_min = cy - (n_tiles_vertical - 1) / 2 * height_degrees
        y_max = cy + (n_tiles_vertical - 1) / 2 * height_degrees

        # Calculate x and y coordinates of each centroid
        centroids_x = list(np.arange(x_min, x_max + width_degrees / 2, width_degrees))
        centroids_y = list(np.arange(y_min, y_max + height_degrees / 2, height_degrees))

        # Draw the centroids grid
        centroid_grid = np.empty((n_tiles_horizontal, n_tiles_vertical), dtype=object)

        for i in range(n_tiles_horizontal):
            for j in range(n_tiles_vertical):
                centroid_grid[i, j] = (centroids_x[i], centroids_y[j])

    else:
        # Calculate coordinates of the centroids for the endpoints
        x_min, y_min, x_max, y_max = get_min_max_xy_bbox_coords(bbox_coords)

        # Calculate x and y coordinates of each centroid
        centroids_x = list(np.arange(x_min + width_degrees / 2, x_max, width_degrees))
        centroids_y = list(np.arange(y_min + height_degrees / 2, y_max, height_degrees))

        # Get number of horizontal and vertical tiles
        n_tiles_horizontal = len(centroids_x)
        n_tiles_vertical = len(centroids_y)

        # Set condition when no tiles were drawn
        if n_tiles_horizontal == 0 or n_tiles_vertical == 0:
            centroid_grid = np.empty((1, 1), dtype=object)
            centroid_grid[0, 0] = (cx, cy)

        elif (
            n_tiles_limit is not None
            and n_tiles_horizontal * n_tiles_vertical > n_tiles_limit
        ):
            grid_side_limit = math.floor(math.sqrt(n_tiles_limit))
            # Calculate coordinates of the centroids for the endpoints
            x_min = cx - (grid_side_limit - 1) / 2 * width_degrees
            x_max = cx + (grid_side_limit - 1) / 2 * width_degrees
            y_min = cy - (grid_side_limit - 1) / 2 * height_degrees
            y_max = cy + (grid_side_limit - 1) / 2 * height_degrees

            # Calculate x and y coordinates of each centroid
            centroids_x = list(
                np.arange(x_min, x_max + width_degrees / 2, width_degrees)
            )
            centroids_y = list(
                np.arange(y_min, y_max + height_degrees / 2, height_degrees)
            )

            # Draw the centroids grid
            centroid_grid = np.empty((grid_side_limit, grid_side_limit), dtype=object)

            for i in range(grid_side_limit):
                for j in range(grid_side_limit):
                    centroid_grid[i, j] = (centroids_x[i], centroids_y[j])

        else:
            # Draw the centroids grid
            centroid_grid = np.empty(
                (n_tiles_horizontal, n_tiles_vertical), dtype=object
            )

            for i in range(n_tiles_horizontal):
                for j in range(n_tiles_vertical):
                    centroid_grid[i, j] = (centroids_x[i], centroids_y[j])

    return centroid_grid


def crop_image(img):
    # Define coordinates of the left upper and right lower pixels of the cropped img
    box = (
        20,
        20,
        620,
        620,
    )  # (x_left_upper, y_left_upper, x_right_lower, y_right_lower)
    return img.crop(box)


def convert_image_to_bytes(img, format="JPEG"):
    # Create a BytesIO object
    image_bytes = BytesIO()
    # Save the image to the BytesIO object
    img.save(image_bytes, format=format)
    return image_bytes.getvalue()


def gms_image_data(
    lat: str,
    lon: str,
    api_key: str,
    secret: str | None = None,
    size: int = 640,
    zoom: int = 16,
    maptype: str = "satellite",
    format: str = "jpg",
):
    if secret:
        return google.gms_static_map(
            lat=lat,
            lon=lon,
            api_key=api_key,
            secret=secret,
            size=size,
            zoom=zoom,
            maptype=maptype,
            format=format,
        )

    else:
        # Initialize Google Maps Static API
        gmaps = googlemaps.Client(key=api_key)
        # Fetch
        image_data = gmaps.static_map(
            size=(size, size),
            center=(lat, lon),  # (latitude, longitud),
            zoom=zoom,
            maptype=maptype,
            format=format,
        )
        return b"".join(image_data)


## 1.2 Main function
def generate_stitched_gms_image(
    cx: float,  # longitud degrees
    cy: float,  # latitude degrees
    n_tiles_horizontal: int,
    n_tiles_vertical: int,
    zoom_level: int,
    api_key: str,
    dir_img: str,
    img_name: str,
    size: int = 640,
    bbox_coords=None,
    n_tiles_limit: int = None,
    save: bool = False,
    output_format: Literal["jpg", "bytes"] = "jpg",
    secret: str | None = None,
    maptype: str = "satellite",
):
    # --Calculate width and height of each tile in degrees
    height_pixels = 600
    width_pixels = 600
    # zoom_level = 15

    height_degrees = calculate_tile_size_degrees(height_pixels, zoom_level, cy)
    width_degrees = calculate_tile_size_degrees(width_pixels, zoom_level, 0.0)

    # --Create grid of centroids
    grid_centroids = generate_centroid_grid_array(
        cx,
        cy,
        n_tiles_horizontal,
        n_tiles_vertical,
        height_degrees,
        width_degrees,
        bbox_coords,
        n_tiles_limit,
    )

    # --Download images
    images = []
    for i, centroid_coords in enumerate(grid_centroids.flatten()):
        lat = centroid_coords[1]
        lon = centroid_coords[0]

        # Download image
        image_data = gms_image_data(
            lat=lat,
            lon=lon,
            api_key=api_key,
            secret=secret,
            size=size,
            zoom=zoom_level,
            maptype=maptype,
            format=output_format,
        )

        assert isinstance(image_data, bytes)
        image_bytes = image_data
        # Crop images to get ride of the watermark
        img_crop = crop_image(Image.open(BytesIO(image_bytes)))
        images.append(img_crop)

    # --Reconstruct image
    # Get the size of the image
    width_img, height_img = images[0].size

    # Create a new image with the size of the grid
    num_img = int(math.sqrt(len(images)))
    grid_width = num_img * width_img
    grid_height = num_img * height_img
    img_stitched = Image.new("RGB", (grid_width, grid_height))

    # Paste the images into the grid
    for i in range(num_img):
        for j in range(num_img):
            img_stitched.paste(
                images[i * num_img + j],
                (i * width_img, abs(num_img - 1 - j) * height_img),
            )  # .paste(image, (x,y))

    # --Save the stitched image
    if save:
        img_stitched.save(Path(dir_img) / f"stitched_{img_name}.jpg")

    if output_format == "bytes":
        return convert_image_to_bytes(img_stitched)
    else:
        return img_stitched
