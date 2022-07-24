import math

import numpy as np


def angle(v1, v2):
    cosTh = np.dot(v1, v2)
    sinTh = np.cross(v1, v2)
    return np.rad2deg(np.arctan2(sinTh, cosTh))


# Given three collinear points p, q, r, the function checks if
# point q lies on line segment 'pr'
def onSegment(p, q, r):
    if ((q.x <= max(p.x, r.x)) and (q.x >= min(p.x, r.x)) and
            (q.y <= max(p.y, r.y)) and (q.y >= min(p.y, r.y))):
        return True
    return False


def orientation(p, q, r):
    # to find the orientation of an ordered triplet (p,q,r)
    # function returns the following values:
    # 0 : Collinear points
    # 1 : Clockwise points
    # 2 : Counterclockwise

    # See https://www.geeksforgeeks.org/orientation-3-ordered-points/amp/
    # for details of below formula.

    val = (float(q.y - p.y) * (r.x - q.x)) - (float(q.x - p.x) * (r.y - q.y))
    if (val > 0):

        # Clockwise orientation
        return 1
    elif (val < 0):

        # Counterclockwise orientation
        return 2
    else:

        # Collinear orientation
        return 0


# The main function that returns true if
# the line segment 'p1q1' and 'p2q2' intersect.
def doIntersect(p1, q1, p2, q2):
    # Find the 4 orientations required for
    # the general and special cases
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    # General case
    if ((o1 != o2) and (o3 != o4)):
        return True

    # Special Cases
    # Partial overlaps:
    if (o1 == 0) and onSegment(p1, p2, q1):
        print('hi')
        return True

    if (o2 == 0) and onSegment(p1, q2, q1):
        print('hi')
        return True

    if (o3 == 0) and onSegment(p2, p1, q2) and ():
        print('hi')
        return True

    if (o4 == 0) and onSegment(p2, q1, q2):
        print('hi')
        return True

    # If none of the cases
    return False


def fbl(beta, _lambda):
    print('(1/' + str(beta) + ')*(1 - ((((3 - 3*' + str(_lambda) + ' + ' + str(_lambda) + '^2)*(8 + 3 * ' + str(_lambda) + ' - ' + str(_lambda) + '^2))/(2 * ' + str(_lambda) + ' *(1 - ' + str(_lambda) + ') *(2 - ' + str(_lambda) + ')^2)) * ((' + str(beta) + ')/(e^(' + str(beta) + '-5)))))')
    print((1/beta)*(1 - ((((3 - 3*_lambda + _lambda**2)*(8 + 3 * _lambda - _lambda**2))/(2 * _lambda *(1 - _lambda) *(2 - _lambda)**2)) * ((beta)/(math.e**(beta-5))))))
