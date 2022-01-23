W_CLIPPING_PLANE = 0.0001


def clip_to_plane(vertices, component, component_factor):
    clipped_polygon = []
    previous_vertex = vertices[-1]
    previous_component = previous_vertex[0][component] * component_factor
    previous_inside = previous_component <= previous_vertex[1]
    
    for current_vertex in vertices:
        current_component = current_vertex[0][component] * component_factor
        current_inside = current_component <= current_vertex[1]

        if current_inside ^ previous_inside:
            differ = (previous_vertex[1] - previous_component)
            t = (differ / (differ - (current_vertex[1] - current_component)))

            intersection = previous_vertex[0] + t * (current_vertex[0] - previous_vertex[0])
            w = previous_vertex[1] + t * (current_vertex[1] - previous_vertex[1])
            clipped_polygon.append((intersection, w))

        if current_inside:
            clipped_polygon.append(current_vertex)

        previous_vertex = current_vertex
        previous_component = current_component
        previous_inside = current_inside
    return clipped_polygon

def is_inside_frustum(vec):
    w = abs(vec[1])
    vec3 = vec[0]
    return abs(vec3.x) <= w and abs(vec3.y) <= w and abs(vec3.z) <= w

def clip_polygon(vertices, axis):
    if not vertices:
        return

    inside_frustum = [is_inside_frustum(vertex) for vertex in vertices]
    if all(inside_frustum):
        return vertices
    polygon = clip_to_plane(vertices, axis, 1)
    if polygon and axis not in [2] : # don't clip to far plane
        return clip_to_plane(polygon, axis, -1)
    return polygon
