from utils.Vector import Vector

# http://jeffreythompson.org/collision-detection/circle-rect.php


def circleRectangle(circ, rect):
    """Function to resolve collisions between circle and rectangle

    Args:
        c (ObjectCircle)
        r (ObjectRect)

    Returns:
        bool: true if objects collide
    """

    return circ.pos.distance(circRectClosestPoint(circ, rect)) <= circ.r


def circRectClosestPoint(circ, rect):
    """Find the closest point on rectangle closest to given circle

    Args:
        circ (ObjectCircle)
        rect (ObjectRectangle)

    Returns:
        Vector: point on the perimeter of the rectangle
    """
    # sides of rectangle (left, right, bottom, up)
    l = rect.pos.x
    r = rect.pos.x + rect.size.x
    b = rect.pos.y
    u = rect.pos.y + rect.size.y

    # nearest point on the perimeter of the rectangle
    # if c.x > r, r is returned, if c.x < l, l is returned, otherwise c.x
    return Vector(max(l, min(circ.pos.x, r)), max(b, min(circ.pos.y, u)))


# https://gamedev.stackexchange.com/questions/26004/how-to-detect-2d-line-on-line-collision


def lineLine(l1, l2):
    """Function that determines if two lines collide

    Args:
        l1 (tuple(Vector)): first line defined by its corner points
        l2 (tuple(Vector)): second line defined by its corner points

    Returns:
        bool: true if lines collide
    """
    a = l1[0]
    b = l1[1]
    c = l2[0]
    d = l2[1]

    den = ((b.x - a.x) * (d.y - c.y)) - ((b.y - a.y) * (d.x - c.x))
    n1 = ((a.y - c.y) * (d.x - c.x)) - ((a.x - c.x) * (d.y - c.y))
    n2 = ((a.y - c.y) * (b.x - a.x)) - ((a.x - c.x) * (b.y - a.y))

    if den == 0:
        return n1 == 0 and n2 == 0
    r = n1 / den
    s = n2 / den

    return r >= 0 and r <= 1 and s >= 0 and s <= 1


def lineRect(line, rect):
    """Function that determines whether line and a rectangle collide or not

    Args:
        line (tuple(Vector)): line defined by corner points
        rect (ObjectRect)

    Returns:
        bool: true if objects collide
    """

    # check if line collides with every side of the rectangle
    l = (Vector(rect.pos.x, rect.pos.y),
         Vector(rect.pos.x, rect.pos.y+rect.size.y))
    r = (Vector(rect.pos.x+rect.size.x, rect.pos.y),
         Vector(rect.pos.x+rect.size.x, rect.pos.y+rect.size.y))
    b = (Vector(rect.pos.x, rect.pos.y),
         Vector(rect.pos.x+rect.size.x, rect.pos.y))
    u = (Vector(rect.pos.x, rect.pos.y+rect.size.y),
         Vector(rect.pos.x+rect.size.x, rect.pos.y+rect.size.y))

    return lineLine(line, l) or lineLine(line, r) or lineLine(line, b) or lineLine(line, u)


def circleCircle(c1, c2):
    """Function that determines if two circles collide

    Args:
        c1 (ObjectCircle) 
        c2 (ObjectCircle)

    Returns:
        bool: true if circles collide
    """
    return c1.pos.distance(c2.pos) <= c1.r + c2.r
