import math
import torch


def rotmatx(angle):
    """
    Definition to generate a rotation matrix along X axis.

    Parameters
    ----------
    angles       : list
                   Rotation angles in degrees.

    Returns
    ----------
    rotx         : ndarray
                    Rotation matrix along X axis.
    """
    angle = torch.float(angle)
    angle = torch.radians(angle)
    rotx = torch.array([
        [1.,               0.,               0.],
        [0.,  math.cos(angle), -math.sin(angle)],
        [0.,  math.sin(angle),  math.cos(angle)]
    ], dtype=torch.float)
    return rotx


def rotmaty(angle):
    """
    Definition to generate a rotation matrix along Y axis.

    Parameters
    ----------
    angles       : list
                   Rotation angles in degrees.

    Returns
    ----------
    roty         : ndarray
                   Rotation matrix along Y axis.
    """
    angle = torch.radians(angle)
    roty = torch.array([
        [math.cos(angle),  0., math.sin(angle)],
        [0.,               1.,              0.],
        [-math.sin(angle), 0., math.cos(angle)]
    ], dtype=torch.float)
    return roty


def rotmatz(angle):
    """
    Definition to generate a rotation matrix along Z axis.

    Parameters
    ----------
    angles       : list
                   Rotation angles in degrees.

    Returns
    ----------
    rotz         : ndarray
                   Rotation matrix along Z axis.
    """
    angle = torch.radians(angle)
    rotz = torch.array([
        [math.cos(angle), -math.sin(angle), 0.],
        [math.sin(angle),  math.cos(angle), 0.],
        [0.,               0., 1.]
    ], dtype=torch.float)
    return rotz


def rotate_point(point, angles=[0, 0, 0], mode='XYZ', origin=[0, 0, 0], offset=[0, 0, 0]):
    """
    Definition to rotate a given point. Note that rotation is always with respect to 0,0,0.

    Parameters
    ----------
    point        : ndarray
                   A point.
    angles       : list
                   Rotation angles in degrees. 
    mode         : str
                   Rotation mode determines ordering of the rotations at each axis. There are XYZ,YXZ,ZXY and ZYX modes.
    origin       : list
                   Reference point for a rotation.
    offset       : list
                   Shift with the given offset.

    Returns
    ----------
    result       : ndarray
                   Result of the rotation
    rotx         : ndarray
                   Rotation matrix along X axis.
    roty         : ndarray
                   Rotation matrix along Y axis.
    rotz         : ndarray
                   Rotation matrix along Z axis.
    """
    point = point - torch.tensor(origin)
    rotx = rotmatx(angles[0])
    roty = rotmaty(angles[1])
    rotz = rotmatz(angles[2])
    if mode == 'XYZ':
        result = torch.dot(rotz, torch.dot(roty, torch.dot(rotx, point)))
    elif mode == 'XZY':
        result = torch.dot(roty, torch.dot(rotz, torch.dot(rotx, point)))
    elif mode == 'YXZ':
        result = torch.dot(rotz, torch.dot(rotx, torch.dot(roty, point)))
    elif mode == 'ZXY':
        result = torch.dot(roty, torch.dot(rotx, torch.dot(rotz, point)))
    elif mode == 'ZYX':
        result = torch.dot(rotx, torch.dot(roty, torch.dot(rotz, point)))
    result += origin
    result += offset
    return result, rotx, roty, rotz


def rotate_points(points, angles=[0, 0, 0], mode='XYZ', origin=[0, 0, 0], offset=[0, 0, 0]):
    """
    Definition to rotate points.

    Parameters
    ----------
    points       : ndarray
                   Points.
    angles       : list
                   Rotation angles in degrees. 
    mode         : str
                   Rotation mode determines ordering of the rotations at each axis. There are XYZ,YXZ,ZXY and ZYX modes.
    origin       : list
                   Reference point for a rotation.
    offset       : list
                   Shift with the given offset.

    Returns
    ----------
    result       : ndarray
                   Result of the rotation   
    """
    if angles[0] == 0 and angles[1] == 0 and angles[2] == 0:
        result = torch.tensor(offset) + points
        return result
    points -= torch.tensor(origin)
    rotx = rotmatx(angles[0])
    roty = rotmaty(angles[1])
    rotz = rotmatz(angles[2])
    if mode == 'XYZ':
        result = torch.dot(rotz, torch.dot(roty, torch.dot(rotx, points.T))).T
    elif mode == 'XZY':
        result = torch.dot(roty, torch.dot(rotz, torch.dot(rotx, points.T))).T
    elif mode == 'YXZ':
        result = torch.dot(rotz, torch.dot(rotx, torch.dot(roty, points.T))).T
    elif mode == 'ZXY':
        result = torch.dot(roty, torch.dot(rotx, torch.dot(rotz, points.T))).T
    elif mode == 'ZYX':
        result = torch.dot(rotx, torch.dot(roty, torch.dot(rotz, points.T))).T
    result += torch.tensor(origin)
    result += torch.tensor(offset)
    return result


def tilt_towards(location, lookat):
    """
    Definition to tilt surface normal of a plane towards a point.

    Parameters
    ----------
    location     : list
                   Center of the plane to be tilted.
    lookat       : list
                   Tilt towards this point.

    Returns
    ----------
    angles       : list
                   Rotation angles in degrees.
    """
    dx = location[0]-lookat[0]
    dy = location[1]-lookat[1]
    dz = location[2]-lookat[2]
    dist = torch.sqrt(dx**2+dy**2+dz**2)
    phi = torch.arctan2(dy, dx)
    theta = torch.arccos(dz/dist)
    angles = [
        0,
        torch.degrees(theta).tolist(),
        torch.degrees(phi).tolist()
    ]
    return angles