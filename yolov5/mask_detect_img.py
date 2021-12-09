# YOLOv5 🚀 by Ultralytics, GPL-3.0 license
"""
Run inference on images, videos, directories, streams, etc.

Usage:
    $ python path/to/detect.py --source path/to/img.jpg --weights yolov5s.pt --img 640
"""

import argparse
import os
import sys
from pathlib import Path

import cv2
import numpy as np
import torch
import torch.backends.cudnn as cudnn

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

from models.experimental import attempt_load
from utils.datasets import LoadImages, LoadStreams
from utils.general import apply_classifier, check_img_size, check_imshow, check_requirements, check_suffix, colorstr, \
    increment_path, non_max_suppression, print_args, save_one_box, scale_coords, set_logging, \
    strip_optimizer, xyxy2xywh
from utils.plots import Annotator, colors
from utils.torch_utils import load_classifier, select_device, time_sync
from utils.augmentations import letterbox

@torch.no_grad()
def run(weights=ROOT / './runs/train/exp5/weights/best.pt',  # model.pt path(s)
        source=ROOT / 'data/images',  # file/dir/URL/glob, 0 for webcam
        imgsz=[320, 320],  # inference size (pixels)
        conf_thres=0.35,  # confidence threshold
        iou_thres=0.45,  # NMS IOU threshold
        max_det=1000,  # maximum detections per image
        device='',  # cuda device, i.e. 0 or 0,1,2,3 or cpu
        save_txt=True,  # save results to *.txt
        save_conf=False,  # save confidences in --save-txt labels
        classes=None,  # filter by class: --class 0, or --class 0 2 3
        agnostic_nms=False,  # class-agnostic NMS
        augment=False,  # augmented inference
        visualize=False,  # visualize features
        line_thickness=3,  # bounding box thickness (pixels)
        hide_labels=True,  # hide labels
        hide_conf=False,  # hide confidences
        half=False,  # use FP16 half-precision inference
        ):
    txt = []

    # Initialize
    set_logging()
    device = select_device(device)
    half &= device.type != 'cpu'  # half precision only supported on CUDA

    # Load model
    w = str(weights[0] if isinstance(weights, list) else weights)
    classify, suffix, suffixes = False, Path(w).suffix.lower(), ['.pt', '.onnx', '.tflite', '.pb', '']
    check_suffix(w, suffixes)  # check weights have acceptable suffix
    pt, onnx, tflite, pb, saved_model = (suffix == x for x in suffixes)  # backend booleans

    model = torch.jit.load(w) if 'torchscript' in w else attempt_load(weights, map_location=device)
    stride = int(model.stride.max())  # model stride
    names = model.module.names if hasattr(model, 'module') else model.names  # get class names
    if half:
        model.half()  # to FP16

    if classify:  # second-stage classifier
        modelc = load_classifier(name='resnet50', n=2)  # initialize
        modelc.load_state_dict(torch.load('resnet50.pt', map_location=device)['model']).to(device).eval()

    imgsz = check_img_size(imgsz, s=stride)  # check image size

    path = None
    im0s = source
    img = letterbox(im0s, imgsz, stride=stride, auto=pt)[0]
    # Convert
    img = img.transpose((2, 0, 1))[::-1]  # HWC to CHW, BGR to RGB
    img = np.ascontiguousarray(img)

    # Run inference
    if pt and device.type != 'cpu':
        model(torch.zeros(1, 3, *imgsz).to(device).type_as(next(model.parameters())))  # run once
    dt, seen = [0.0, 0.0, 0.0], 0

    t1 = time_sync()
    if onnx:
        img = img.astype('float32')
    else:
        img = torch.from_numpy(img).to(device)
        img = img.half() if half else img.float()  # uint8 to fp16/32
    img /= 255.0  # 0 - 255 to 0.0 - 1.0
    if len(img.shape) == 3:
        img = img[None]  # expand for batch dim
    t2 = time_sync()
    dt[0] += t2 - t1

    # Inference
    pred = model(img, augment=augment, visualize=visualize)[0]
    t3 = time_sync()
    dt[1] += t3 - t2

    # NMS
    pred = non_max_suppression(pred, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)
    dt[2] += time_sync() - t3

    # Second-stage classifier (optional)
    if classify:
        pred = apply_classifier(pred, modelc, img, im0s)

    # Process predictions
    for i, det in enumerate(pred):  # per image
        seen += 1
        p, s, im0, frame = path, '', im0s.copy(), 0
        s += '%gx%g ' % img.shape[2:]  # print string
        gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
        annotator = Annotator(im0, line_width=line_thickness, example=str(names))
        if len(det):
            # Rescale boxes from img_size to im0 size
            det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()

            # Print results
            for c in det[:, -1].unique():
                n = (det[:, -1] == c).sum()  # detections per class
                s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string

            # Write results
            for *xyxy, conf, cls in reversed(det):
                if save_txt:  # Write to file
                    xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()  # normalized xywh
                    line = (cls, *xywh, conf) if save_conf else (cls, *xywh)  # label format
                txt.append(('%g ' * len(line)).rstrip() % line)

                c = int(cls)  # integer class
                label = None if hide_labels else (names[c] if hide_conf else f'{names[c]} {conf:.2f}')
                annotator.box_label(xyxy, label, color=colors(c, True))

        # Print time (inference-only)
        # print(f'{s}Done. ({t3 - t2:.3f}s)')

        # Stream results
        im0 = annotator.result()
    # Print results
    t = tuple(x / seen * 1E3 for x in dt)  # speeds per image
    # print(f'Speed: %.1fms pre-process, %.1fms inference, %.1fms NMS per image at shape {(1, 3, *imgsz)}' % t)

    return im0, txt


# def parse_opt():
#     parser = argparse.ArgumentParser()
#     parser.add_argument('--weights', nargs='+', type=str, default=ROOT / './runs/train/exp5/weights/best.pt', help='model path(s)')
#     parser.add_argument('--source', type=str, default='0', help='file/dir/URL/glob, 0 for webcam')
#     parser.add_argument('--imgsz', '--img', '--img-size', nargs='+', type=int, default=[320], help='inference size h,w')
#     parser.add_argument('--conf-thres', type=float, default=0.35, help='confidence threshold')
#     parser.add_argument('--iou-thres', type=float, default=0.45, help='NMS IoU threshold')
#     parser.add_argument('--max-det', type=int, default=1000, help='maximum detections per image')
#     parser.add_argument('--device', default='', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
#     parser.add_argument('--save-txt', default=True, help='save results to *.txt')
#     parser.add_argument('--save-conf', action='store_true', help='save confidences in --save-txt labels')
#     parser.add_argument('--classes', nargs='+', type=int, help='filter by class: --classes 0, or --classes 0 2 3')
#     parser.add_argument('--agnostic-nms', action='store_true', help='class-agnostic NMS')
#     parser.add_argument('--augment', action='store_true', help='augmented inference')
#     parser.add_argument('--visualize', action='store_true', help='visualize features')
#     parser.add_argument('--line-thickness', default=3, type=int, help='bounding box thickness (pixels)')
#     parser.add_argument('--hide-labels', default=True, action='store_true', help='hide labels')
#     parser.add_argument('--hide-conf', default=False, action='store_true', help='hide confidences')
#     parser.add_argument('--half', action='store_true', help='use FP16 half-precision inference')
#     opt = parser.parse_args()
#     opt.imgsz *= 2 if len(opt.imgsz) == 1 else 1  # expand
#     print_args(FILE.stem, opt)
#     return opt


def main_img(input_img=None):
    check_requirements(exclude=('tensorboard', 'thop'))
    img, txt = run(source=input_img)
    return img, txt
    # cv2.imshow('a',img)
    # cv2.waitKey()
    # print(txt)


# if __name__ == "__main__":
#     # opt = parse_opt()
#     # print(opt)
#     cap = cv2.VideoCapture(0)
#     while True:
#         hx, frame = cap.read()
#         img, text = main(frame)
#         cv2.imshow('a', img)
#         cv2.waitKey(1)

