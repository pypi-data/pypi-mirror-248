import glob as glob
import multiprocessing
import os
from pathlib import Path
from typing import Literal

import cv2
import numpy as np
import torch
import torchvision
from ensemble_boxes import weighted_boxes_fusion
from loguru import logger
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor

from geomlcv.utils.process_images.utils import _pcahog, _svhog

PATH_BASE = Path("/home/ec2-user/geomlcv/")  # TODO: from config
PATH_WEIGHTS = Path(
    os.getenv("PATH_WEIGHTS", PATH_BASE / "docs/notebooks/.data/weights")
)
MODELS = {
    "RCNN": {
        "rgb": PATH_WEIGHTS
        / "fasterrcnn_resnet50_fpnv2_pretrained_rgb_v5_640_2023-12-12.pth",
        "svhog": PATH_WEIGHTS
        / "fasterrcnn_resnet50_fpnv2_pretrained_svhog_v3_640_2023-12-13.pth",
        "pcahog": PATH_WEIGHTS
        / "fasterrcnn_resnet50_fpnv2_pretrained_pcahog_v3_640_2023-12-14.pth",
        "classes": ["__background__", "non-pitlake-water", "pitlake"],
    },
    "YOLO": {
        "rgb": "",
        "svhog": "",
        "pcahog": "",
        "classes": ["non-pitlake-water", "pitlake"],
    },
}


def create_RCNN_model(num_classes):
    model = torchvision.models.detection.fasterrcnn_resnet50_fpn_v2(
        weights="FasterRCNN_ResNet50_FPN_V2_Weights.DEFAULT"
    )
    in_features = model.roi_heads.box_predictor.cls_score.in_features
    model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)

    return model


def fasterRCNN_inference(model, image):
    orig_image = image.copy()
    image = cv2.cvtColor(orig_image, cv2.COLOR_BGR2RGB).astype(np.float32)
    image /= 255.0
    image = np.transpose(image, (2, 0, 1)).astype(np.float32)
    if torch.cuda.is_available():
        image = torch.tensor(image, dtype=torch.float).cuda()
    else:
        image = torch.tensor(image, dtype=torch.float)
    image = torch.unsqueeze(image, 0)
    with torch.no_grad():
        outputs = model(image.to("cpu"))
    outputs = [{k: v.to("cpu") for k, v in t.items()} for t in outputs]

    return outputs


def create_YOLO_model(num_classes):
    raise


def YOLOv8_inference(model, image):
    raise


def select_model(model_name, model_path, classes):
    if model_name == "RCNN":
        model = create_RCNN_model(num_classes=len(classes))
        checkpoint = torch.load(model_path, map_location="cpu")
        model.load_state_dict(checkpoint["model_state_dict"])
        if torch.cuda.is_available():
            model.eval()
        else:
            model.to("cpu").eval()
        return model
    elif model_name == "YOLO":
        raise ("no model found")


def normalize_boxes(boxes, norm):
    for k in range(boxes.shape[0]):
        for i in range(4):
            boxes[k][i] = boxes[k][i] / norm[i]

    return boxes


def run_inference(
    img,
    model_name: Literal["RCNN", "YOLO"],
    img_transform: Literal["rgb", "svhog", "pcahog"],
    confidence_threshold=0.5,
):
    # Preprocess input image with faux-color
    if img_transform == "svhog":
        img = _svhog(img)
    elif img_transform == "pcahog":
        img = _pcahog(img)

    # Inference
    if model_name == "RCNN":
        out = fasterRCNN_inference(
            select_model(
                model_name,
                MODELS[model_name][img_transform],
                MODELS[model_name]["classes"],
            ),
            img,
        )[0]
    else:
        raise ("Model not found.")

    # Normalize
    h, w, _ = img.shape
    out["boxes_normalized"] = normalize_boxes(out["boxes"].data.numpy(), [w, h, w, h])

    # Filter results based on the confidence threshold
    scores = out["scores"].data.numpy()
    keep_indices = scores >= confidence_threshold

    out["boxes"] = out["boxes"][keep_indices]
    out["labels"] = out["labels"][keep_indices]
    out["scores"] = out["scores"][keep_indices]
    out["boxes_normalized"] = out["boxes_normalized"][keep_indices]

    return out


def _worker(img, model_name, img_transform):
    return run_inference(img, model_name=model_name, img_transform=img_transform)


def run_combined_inference(img, results_dir, image_name, detection_threshold=0.2):
    # Run inferences in parallel
    # Create a pool of processes
    with multiprocessing.Pool() as pool:
        # Map the run_inference function to multiple arguments
        results = pool.starmap(
            _worker,
            [(img, "RCNN", "rgb"), (img, "RCNN", "svhog"), (img, "RCNN", "pcahog")],
        )

    # Unpack results
    rgb_output, svhog_output, pcahog_output = results

    # TODO: cleanup with dict comprehension
    boxes_list = [
        rgb_output[0]["boxes_normalized"].data.numpy(),
        svhog_output[0]["boxes_normalized"].data.numpy(),
        pcahog_output[0]["boxes_normalized"].data.numpy(),
    ]
    scores_list = [
        rgb_output[0]["scores"].data.numpy(),
        svhog_output[0]["scores"].data.numpy(),
        pcahog_output[0]["scores"].data.numpy(),
    ]
    labels_list = [
        rgb_output[0]["labels"].data.numpy(),
        svhog_output[0]["labels"].data.numpy(),
        pcahog_output[0]["labels"].data.numpy(),
    ]

    # Hyperparameters for weighted fusion
    weights = [3, 2, 1]
    iou_thr = 0.8
    skip_box_thr = 0.0001
    detection_threshold = 0.2

    boxes, scores, labels = weighted_boxes_fusion(
        boxes_list,
        scores_list,
        labels_list,
        weights=weights,
        iou_thr=iou_thr,
        skip_box_thr=skip_box_thr,
    )

    # carry further only if there are detected boxes
    h, w, _ = img.shape
    if len(boxes) != 0:
        # filter out boxes according to `detection_threshold`
        _indices = scores >= detection_threshold
        boxes_filtered = boxes[_indices]
        scores_filtered = scores[_indices]
        labels_filtered = labels[_indices].astype(int)
        draw_boxes = boxes_filtered.copy()
        classes = MODELS["RCNN"]["classes"]

        # TODO: write these out to a file, perhaps separately prior to weighted
        # NOTE: rcnn has 3 classes, bc background.
        # TODO: this maps class int to class name

        # get all the predicited class names
        pred_classes_filtered = [classes[i] for i in labels_filtered]

        # draw the bounding boxes and write the class name on top of it
        for j, box in enumerate(draw_boxes):
            class_name = pred_classes_filtered[j]
            score_j = scores_filtered[j]
            textToDisplay = class_name + ", score=" + str(np.round(score_j, 2))

            cv2.rectangle(
                img,
                (int(box[0] * w), int(box[1] * h)),
                (int(box[2] * w), int(box[3] * h)),
                (255, 255, 255),
                4,
            )
            cv2.putText(
                img,
                textToDisplay,
                (int(box[0] * w), int((box[1] * h) - 5)),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                4,
                lineType=cv2.LINE_AA,
            )

        output_file = Path(results_dir) / f"{image_name}_wf_inference.jpg"
        cv2.imwrite(str(output_file), img)
    logger.info("run_combined_inference completed successfully")
    return
