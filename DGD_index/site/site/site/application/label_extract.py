from imageai.Detection import ObjectDetection
import os
from application.translator import translator


def setModel(execution_path):
    detector = ObjectDetection()
    detector.setModelTypeAsRetinaNet()
    detector.setModelPath(os.path.join(execution_path, "models/resnet50_coco_best_v2.0.1.h5"))
    detector.loadModel()
    return detector


def label_extraction(img, detector):
    # out_file = os.path.join(os.getcwd(), "imagenew.jpg")
    _, detections = detector.detectObjectsFromImage(input_image=img, input_type="array",
                                                    output_type="array",
                                                    minimum_percentage_probability=30)

    labels = []
    for eachObject in detections:
        label = translator(eachObject["name"])
        if label not in labels:
            labels.append(label)
    # return detections
    return ' '.join(labels)
