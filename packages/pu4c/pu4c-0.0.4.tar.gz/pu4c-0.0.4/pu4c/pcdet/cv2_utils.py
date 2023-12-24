import cv2
import numpy as np

def project_points_to_pixels(points, image_shape, transform_mat=None, lidar2cam_mat=None, intrinsics_4x4=None, dist_coeffs=None):
    """
    y = Rx 即 y(4,N) = transform_mat @ (4, N) 即 y(N,4) = (N,4) @ transform_mat.T
    处理带畸变参数的变换比较麻烦，cv2.projectPoints 可以直接从变换到像素坐标系，但丢失像素深度信息
    故多一步中间形式的相机坐标系下的点云，相机坐标系下的 z 就是像素坐标系下的深度
    """
    points_hom = np.hstack((points[:, :3], np.ones((points.shape[0], 1), dtype=np.float32))) # [N, 4]
    if transform_mat is not None:
        points_cam = (points_hom @ transform_mat.T)[:, :3]
        pixels_depth = points_cam[:, 2]
        pixels = (points_cam[:, :2].T / points_cam[:, 2]).T # (N, 2)[col, row]
    elif (lidar2cam_mat is not None) and (intrinsics_4x4 is not None) and (dist_coeffs is not None):
        points_cam = points_hom @ lidar2cam_mat.T
        pixels_depth = points_cam[:, 2]
        rotation, translation = np.eye(3), np.zeros((3, 1))
        pixels, jac = cv2.projectPoints(points_cam[:, :3].T, rotation, translation, intrinsics_4x4[:3, :3], dist_coeffs)
        pixels = pixels.squeeze(axis=1)

    # remove points outside the image
    mask = pixels_depth > 0
    mask = np.logical_and(mask, pixels[:, 0] > 0)
    mask = np.logical_and(mask, pixels[:, 0] < image_shape[1])
    mask = np.logical_and(mask, pixels[:, 1] > 0)
    mask = np.logical_and(mask, pixels[:, 1] < image_shape[0])

    return pixels, pixels_depth, mask