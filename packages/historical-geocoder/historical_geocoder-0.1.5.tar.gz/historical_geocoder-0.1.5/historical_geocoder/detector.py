import json
from .utils.detection import direction_detection_ch as direction_detector_ch


def detect_direction(data, lang):
    if lang == "ch":
        with open("./direction.json", "r", encoding="utf-8-sig") as f:
            direction_dictionary = json.load(f)
        directions = direction_dictionary["ch"]["directions"]
        direction_postfixes = direction_dictionary["ch"]["postfixes"]

        direction_with_postfixes = directions.copy()
        for direction in directions:
            for direction_postfix in direction_postfixes:
                direction_with_postfixes.append(direction + direction_postfix)

    direction_detector_ch.detect_direction(data, direction_with_postfixes, direction_postfixes)
    
    return data