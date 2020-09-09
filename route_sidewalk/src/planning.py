from heapq import heappush, heappop


def cal_weight(from_x, from_y, to_x, to_y):
    """
    calculate distance

    Args:
        from_x: x coordinate
        from_y: y coordinate
        to_x: x coordinate
        to_y: y coordinate

    Returns:
        distance
    """

    # return abs(from_x - to_x) + abs(from_y - to_y)  # manhattan
    return ((from_x - to_x) ** 2 + (from_y - to_y) ** 2) ** 0.5  # euclidean dist


def find_closest_road(data, from_):
    """
    Find closest road with Breadth First Search (BFS).

    Args:
        data: array for search
        from_: [x, y] starting point for search
    """

    queue = [(from_, [tuple(from_)])]
    visited = set()
    visited.add(tuple(from_))

    while len(queue):
        # pop position & paths
        current, paths = queue.pop(0)

        if data[current[0], current[1]] != data[from_[0], from_[1]]:  # if found road then return paths
            return paths
        for (dix, diy) in [(-1, -1), (-1, 0), (0, -1), (1, 1), (1, 0), (0, 1), (1, -1), (-1, 1)]:
            to_ = (
                current[0] + dix,
                current[1] + diy
            )
            if to_ not in visited and 0 <= to_[0] < data.shape[0] and 0 <= to_[1] < data.shape[1]:
                # add to queue
                queue.append((to_, paths + [to_]))
                visited.add(to_)


def move_point_inside_road(data, from_):
    """
    Find closest road with Breadth First Search (BFS). [Modify]

    Args:
        data: array for search
        from_: [x, y] starting point for search
    """

    queue = [(from_, [tuple(from_)])]
    visited = set()
    visited.add(tuple(from_))

    while len(queue):
        # pop position & paths
        current, paths = queue.pop(0)

        if data[current[0], current[1]] == 255:  # if found road then return paths
            return paths
        for (dix, diy) in [(-1, -1), (-1, 0), (0, -1), (1, 1), (1, 0), (0, 1), (1, -1), (-1, 1)]:
            to_ = (
                current[0] + dix,
                current[1] + diy
            )
            if to_ not in visited and 0 <= to_[0] < data.shape[0] and 0 <= to_[1] < data.shape[1]:
                # add to queue
                queue.append((to_, paths + [to_]))
                visited.add(to_)


def route_condition(data, from_, to_, v):
    """
    Route with condition

    Args:
        data: array of map
        from_: (x, y) coordinate
        to_: (x, y) coordinate
        v: value

    Returns:
        list of path to target
    """

    heap = []
    heappush(heap, (0, from_[0], from_[1], [(from_[0], from_[1])]))  # (weight, x, y, path)

    visited = set()
    visited.add((from_[0], from_[1]))
    while heap:
        weight, current_x, current_y, path = heappop(heap)
        if current_x == to_[0] and current_y == to_[1]:  # if reach target
            return path
        for dix in range(-1, 2):
            for diy in range(-1, 2):
                to_x = current_x + dix
                to_y = current_y + diy
                if (to_x, to_y) not in visited and \
                        0 <= to_x < data.shape[0] and \
                        0 <= to_y < data.shape[1] and \
                        data[to_x, to_y] == v:
                    weight = cal_weight(to_x, to_y, to_[0], to_[1]) + len(path) * 1000
                    heappush(heap, (weight, to_x, to_y, path + [(to_x, to_y)]))
                    visited.add((to_x, to_y))


def route(data, from_, to_):
    """
    Route without condition

    Args:
        data: array of map
        from_: (x, y) coordinate
        to_: (x, y) coordinate

    Returns:
        list of path to target
    """
    heap = []
    heappush(heap, (0, from_[0], from_[1], [(from_[0], from_[1])]))  # (weight, x, y, path)

    visited = set()
    visited.add((from_[0], from_[1]))
    while heap:
        weight, current_x, current_y, path = heappop(heap)
        if current_x == to_[0] and current_y == to_[1]:  # if reach target
            return path
        for dix in range(-1, 2):
            for diy in range(-1, 2):
                to_x = current_x + dix
                to_y = current_y + diy
                if (to_x, to_y) not in visited and \
                        0 <= to_x < data.shape[0] and \
                        0 <= to_y < data.shape[1]:
                    weight = cal_weight(to_x, to_y, to_[0], to_[1]) + len(path) * 1000
                    heappush(heap, (weight, to_x, to_y, path + [(to_x, to_y)]))
                    visited.add((to_x, to_y))
