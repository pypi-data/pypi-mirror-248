import io
from io import BytesIO
from pathlib import Path

import boto3
import cv2
import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
import s3fs
from loguru import logger
from PIL import Image

s3 = boto3.client("s3")


def list_objects_in_folder(bucket_name, folder_path):
    # List objects in the specified folder
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=folder_path)

    # Print the object keys
    print(f"Objects in the folder '{folder_path}':")
    for obj in response.get("Contents", []):
        print(obj["Key"])


def display_s3_image(bucket_name, object_key):
    # Download the image from S3
    response = s3.get_object(Bucket=bucket_name, Key=object_key)
    image_data = response["Body"].read()

    # Open and display the image using Pillow (PIL)
    return Image.open(BytesIO(image_data))


def get_s3_image(
    img_name,
    bucket_name="geoml-aquarry",
    path="output/gms/16dec2023/tang",
    save_path=None,
):
    # Get the file object from S3
    object_key = f"{path}/{img_name}.jpg"
    try:
        file_object = s3.get_object(Bucket=bucket_name, Key=object_key)
        file_stream = io.BytesIO(file_object["Body"].read())
        img_np_array = np.asarray(bytearray(file_stream.read()), dtype=np.uint8)
        img = cv2.imdecode(img_np_array, cv2.IMREAD_COLOR)

        # Optionally save to disk
        if save_path:
            local_file_path = f"{save_path}/{img_name}.jpg"
            with open(local_file_path, "wb") as file:
                file.write(file_stream.getvalue())

        return img
    except Exception as e:
        logger.debug(
            "Error accessing object_key: {}, bucket_name: {}. Exception: {}",
            object_key,
            bucket_name,
            e,
        )
        return None


def write_to_parquet(data, objectid, path_output_file):
    path_output_file = str(path_output_file)
    # Prepare data for each column
    labels = [data["labels"][i].item() for i in range(len(data["labels"]))]
    scores = [data["scores"][i].item() for i in range(len(data["scores"]))]
    boxes_normalized = [data["boxes_normalized"][i] for i in range(len(data["boxes_normalized"]))]
    objectid_arr = [str(objectid)] * len(data["labels"])
    try:
        # Create a PyArrow Table
        table = pa.Table.from_arrays(
            [
                pa.array(objectid_arr, pa.string()),
                pa.array(labels, pa.int64()),
                pa.array(scores, pa.float64()),
                pa.array(boxes_normalized, pa.list_(pa.float64())),
            ],
        names=["objectid", "label", "score", "boxes_normalized"])

        # If starts with `s3://` write to S3, else to disk
        if path_output_file.startswith("s3://"):
            # Use S3FileSystem to handle S3 paths
            fs = s3fs.S3FileSystem()
            with fs.open(path_output_file, "wb") as f:
                pq.write_table(table, f)
        # Write the table to a Parquet file
        pq.write_table(table, path_output_file)
        logger.debug("Successfully wrote to: {}", path_output_file)
    except Exception as e:
        logger.error("Failed to write to: {} with {}", path_output_file, e)
        raise e


def structure_s3_key(model_name, dataset_name, img_transform, filename, s3base):
    return "s3://" + str(
        Path(s3base)
        / f"dataset={dataset_name}"
        / f"model={model_name}"
        / f"color={img_transform}"
        / f"{filename}.parquet"
    )
