import numpy as np

def mask_points_and_boxes_outside_range(points, limit_range, bboxes_3d=None):
    point_mask = (points[:, 0] >= limit_range[0]) & (points[:, 0] <= limit_range[3]) \
           & (points[:, 1] >= limit_range[1]) & (points[:, 1] <= limit_range[4])
    box_mask = ((bboxes_3d[:, :3] >= limit_range[:3]) & (bboxes_3d[:, :3]  <= limit_range[3:6])).all(axis=-1) if bboxes_3d is not None else None

    return point_mask, box_mask

def project_points_to_pixels(points, image_shape, transform_mat):
    """
    y = Rx 即 y(4,N) = transform_mat @ (4, N) 即 y(N,4) = (N,4) @ transform_mat.T
    """
    points_hom = np.hstack((points[:, :3], np.ones((points.shape[0], 1), dtype=np.float32))) # [N, 4]
    points_cam = (points_hom @ transform_mat.T)[:, :3]
    
    pixels_depth = points_cam[:, 2]
    pixels = (points_cam[:, :2].T / points_cam[:, 2]).T # (N, 2)[col, row]

    # remove points outside the image
    mask = pixels_depth > 0
    mask = np.logical_and(mask, pixels[:, 0] > 0)
    mask = np.logical_and(mask, pixels[:, 0] < image_shape[1])
    mask = np.logical_and(mask, pixels[:, 1] > 0)
    mask = np.logical_and(mask, pixels[:, 1] < image_shape[0])

    return pixels, pixels_depth, mask

def get_oriented_bounding_box_corners(xyz, lwh, axis_angles):
    """
        轴角转旋转矩阵（暂只考虑偏航）来将其旋转为有向包围盒，计算盒子的 8 个角点，添加连线
        Locals:
            lines: (10, 2), 预定义的 14 条连线
            4-------- 6
        /|         /|
        5 -------- 3 .
        | |        | |
        . 7 -------- 1          
        |/         |/       z |/ x  
        2 -------- 0      y - 0
        Returns:
            corners: (N, 8, 3)
    """
    x, y, z = xyz
    l, w, h = lwh
    roll, pitch, yaw = axis_angles
    xdif, ydif, zdif = l/2, w/2, h/2
    offsets = np.array([
        [-xdif,  xdif, -xdif, -xdif, xdif, -xdif,  xdif,  xdif],
        [-ydif, -ydif,  ydif, -ydif, ydif,  ydif, -ydif,  ydif],
        [-zdif, -zdif, -zdif,  zdif, zdif,  zdif,  zdif, -zdif],
    ])
    R_x = np.array([
        [ 1, 0            ,  0          ],
        [ 0, np.cos(roll) , -np.sin(roll)],
        [ 0, np.sin(roll) ,  np.cos(roll)],
    ])
    R_y = np.array([
        [ np.cos(pitch),  0,  np.sin(pitch)],
        [ 0            ,  1,  0            ],
        [-np.sin(pitch),  0,  np.cos(pitch)],
    ])
    R_z = np.array([
        [ np.cos(yaw), -np.sin(yaw),  0],
        [ np.sin(yaw),  np.cos(yaw),  0],
        [ 0          ,  0          ,  1],
    ])
    R = R_x @ R_y @ R_z
    corners = (R @ offsets + np.array([[x], [y], [z]])).T
    
    return corners

def get_oriented_bounding_box_lines(head_cross_lines=True):
    lines = [
                [0, 2], [0, 3], [2, 5], [3, 5],
                [0, 1], [3, 6], [5, 4], [2, 7],
                [1, 6], [1, 7], [7, 4], [4, 6],
            ]
    if head_cross_lines:
        lines.extend([[1, 4], [6, 7]])
    return lines

def range_projection(points, fov_up=np.radians(2), fov_down=np.radians(-25), height=64, width=720):
    """
        Returns: 
        proj_range: projected range image with depth, each pixel contains the corresponding depth
        proj_vertex: each pixel contains the corresponding point (x, y, z, 1)，附加的节点信息
        proj_idx: each pixel contains the corresponding index of the point in the raw point cloud
    """
    fov = abs(fov_up) + abs(fov_down)
    depth = np.linalg.norm(points[:, :3], ord=2, axis=1) # 按行求二范数，即距离

    yaw, pitch = -np.arctan2(points[:, 1], points[:, 0]), np.arcsin(points[:, 2] / depth)
    proj_x = 0.5 * (yaw / np.pi + 1.0)            # yaw=[-pi, pi] to [0.0, 1.0]
    proj_y = 1.0 - (pitch + abs(fov_down)) / fov  # pitch=[fov_up, fov_down] to [0.0, 1.0]
    proj_x *= width     # to [0.0, W]
    proj_y *= height    # to [0.0, H]

    # 坐标取整作为像素坐标
    proj_x = np.minimum(width - 1, np.floor(proj_x))
    proj_x = np.maximum(0, proj_x).astype(np.int32)  # to [0, W-1]
    proj_y = np.minimum(height - 1, np.floor(proj_y))
    proj_y = np.maximum(0, proj_y).astype(np.int32)  # to [0, H-1]

    range_image = np.full((height, width), -1, dtype=np.float32)  # [H,W] range (-1 is no data)
    point_idx = np.full((height, width), -1, dtype=np.int32)  # [H,W] index (-1 is no data)
    range_image[proj_y, proj_x] = depth
    point_idx[proj_y, proj_x] = np.arange(depth.shape[0])

    return range_image, point_idx


def transform_matrix(rotation_mat, translation, inverse: bool = False) -> np.ndarray:
    """
    返回变换矩阵或变换矩阵的逆，直接对变换矩阵求逆可能无解报错
    """
    tm = np.eye(4)

    if inverse:
        rot_inv = rotation_mat.T
        trans = np.transpose(-np.array(translation))
        tm[:3, :3] = rot_inv
        tm[:3, 3] = rot_inv.dot(trans)
    else:
        tm[:3, :3] = rotation_mat
        tm[:3, 3] = np.transpose(np.array(translation))

    return tm