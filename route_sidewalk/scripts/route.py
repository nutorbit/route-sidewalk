import cv2

from absl import app, flags
from collections import OrderedDict

from route_sidewalk.src.scraping import get_all_image
from route_sidewalk.src.preprocess import process_bg, process_target, plot_line_with_path
from route_sidewalk.src.planning import move_point_inside_road, route_condition, find_closest_road, route


FLAGS = flags.FLAGS
flags.DEFINE_float("zoom", 20, "level of zoom")
flags.DEFINE_float("lat1", None, "start latitude")
flags.DEFINE_float("lat2", None, "target latitude")
flags.DEFINE_float("lng1", None, "start longitude")
flags.DEFINE_float("lng2", None, "target longitude")
flags.mark_flag_as_required("lat1")
flags.mark_flag_as_required("lat2")
flags.mark_flag_as_required("lng1")
flags.mark_flag_as_required("lng1")


def main(_):
    req = {
        "zoom": FLAGS.zoom,
        "lat1": FLAGS.lat1,
        "long1": FLAGS.lng1,
        "lat2": FLAGS.lat2,
        "long2": FLAGS.lng2
    }

    # save necessary image
    get_all_image(req)

    # process image
    img_map, road_thresh = process_bg("./data/background-route.png")
    contours = process_target("./data/target-route.png")

    # start/stop point
    s = move_point_inside_road(road_thresh, contours[0])[-1]
    e = move_point_inside_road(road_thresh, contours[1])[-1]

    # route
    paths = route_condition(road_thresh, s, e, 255)

    addition = []
    for i in range(1, len(paths)):
        from_ = paths[i - 1]
        to_ = paths[i]
        p = route_condition(road_thresh, from_, to_, 255)
        p = list(map(lambda x: find_closest_road(road_thresh, x)[-1], p))
        addition.extend(p)
    addition = list(OrderedDict.fromkeys(addition))

    no_cross_road = 0
    for i in range(1, len(addition)):
        from_ = addition[i - 1]
        to_ = addition[i]
        p1 = route_condition(road_thresh, from_, to_, 0)
        p2 = route(road_thresh, from_, to_)  # cross road
        if not p1:
            p1 = p2
            no_cross_road += 1
        if len(p2) < len(p1) - 100:
            no_cross_road += 1

    # save image
    final = plot_line_with_path(img_map, paths, return_array=True)
    cv2.imwrite('./data/result-path-routing.png', final)

    print(f"Number of cross-road: {no_cross_road}")


if __name__ == "__main__":
    app.run(main)
