from . import config

def create_vis_infos(dataset="kitti"):
    """
    生成用于可视化的数据接口
    """
    from .data_utils import decode_kitti_infos, decode_nuscenes_infos, decode_waymo_infos
    import pickle
    default_param_dict = {
        "kitti": [decode_kitti_infos, config.kitti_info_pkls, config.kitti_vis_info_pkls, config.kitti_classes[:3]],
        "nus":   [decode_nuscenes_infos, config.nus_info_pkls, config.nus_vis_info_pkls, config.nus_classes[:4]],
        "waymo": [decode_waymo_infos, config.waymo_info_pkls, config.waymo_vis_info_pkls, config.waymo_kitti_classes[:3]],
    }
    decoder, src_pkls, dst_pkls, valid_classes = default_param_dict[dataset]
    for src_pkl, dst_pkl in zip(src_pkls, dst_pkls):
        info_dict = decoder(src_pkl, valid_classes=valid_classes,
                            add_ext_info=True if dataset in ['nus', 'waymo'] else False
                            )
        print(dst_pkl)
        with open(dst_pkl, 'wb') as f:
            pickle.dump(info_dict, f)
def playdataset(root=config.kitti_root, 
                pkl=config.kitti_vis_info_pkls[0], 
                valid_classes=config.kitti_classes[:3],
                start=0, step=10,
                color=None, point_size=1,
                help=False,
                ):
    """
    visualize dataset split，A/D switch one frame ; W/S switch ${step} frame; esc to exit
    """
    if help:
        print(
            "pu4c.pcdet.app.playdataset(root=config.nus_root, pkl=config.nus_vis_info_pkls[1], valid_classes=config.nus_classes[:3])\n"
            "pu4c.pcdet.app.playdataset(root=config.waymo_root, pkl=config.waymo_vis_info_pkls[1], valid_classes=config.waymo_kitti_classes[:3])\n"
            "pu4c.pcdet.app.playdataset(root=config.pandaset_root, pkl=config.pandaset_info_pkls[1], valid_classes=config.pandaset_classes[:3])\n"
        )
        return
    from .open3d_utils import playcloud
    import pickle
    import numpy as np
    with open(pkl, 'rb') as f:
        infos = pickle.load(f)

    point_clouds, bboxes_3d = [], []
    map_cls_name2id = {cls:i for i, cls in enumerate(valid_classes)}
    for info in infos:
        info['lidar']['filepath'] = f"{root}/{info['lidar']['filepath']}"
        point_clouds.append(info['lidar'])

        if 'annos' in info:
            mask = np.array([name in valid_classes for name in info['annos']['name']], dtype=bool)
            info['annos']['name'] = info['annos']['name'][mask]
            label = [map_cls_name2id[name] for name in info['annos']['name']]
            bboxes_3d_frame = info['annos']['gt_boxes_lidar'][mask]
            bboxes_3d.append({'label': label, 'bboxes_3d': bboxes_3d_frame})
        else:
            bboxes_3d.append(None)

    print(f"visualize {pkl}, total {len(infos)} frames")
    playcloud(point_clouds, bboxes_3d=bboxes_3d, start=start, step=step,
              color=color, point_size=point_size,
              )


def cloud_viewer_from_dir(root, pattern="*",
                          num_features=4, start=0, step=10, 
                          color=None, point_size=1,
                          ):
    """
    Visualize point clouds in a directory
    """
    from .open3d_utils import playcloud
    from glob import glob
    files = sorted(glob(f'{root}/{pattern}'))

    point_clouds = []
    for filepath in files:
        point_clouds.append({
            'filepath': filepath,
            'num_features': num_features,
        })
    
    playcloud(point_clouds, start=start, step=step, 
              color=color, point_size=point_size,
              )
def cloud_viewer(filepath=None, num_features=4,
                 points=None,
                 point_size=1, transmat=None, color=None,
                 bboxes_3d=None, with_label=False,
                 help=False):
    """
    快速查看单帧点云，支持 pcd/bin/npy/pkl
    """
    if help:
        print(
            "pu4c.pcdet.app.cloud_viewer(filepath, num_features=4, point_size=1)\n"
            "pu4c.pcdet.app.cloud_viewer(points, bboxes_3d=bboxes_3d, point_size=1)\n"
        )
        return
    import open3d as o3d
    from .open3d_utils import read_points, create_add_3d_boxes
    import numpy as np

    vis = o3d.visualization.Visualizer()
    vis.create_window()
    vis.get_render_option().point_size = point_size
    vis.get_render_option().background_color = np.zeros(3)

    axis_pcd = o3d.geometry.TriangleMesh.create_coordinate_frame(size=1.0, origin=[0, 0, 0])
    vis.add_geometry(axis_pcd)

    if filepath is not None:
        points = read_points(filepath, num_features=num_features, transmat=transmat)
    elif points is None:
        raise ValueError(f"filepath and points cannot both be None")
    cloud = o3d.geometry.PointCloud()
    cloud.points = o3d.utility.Vector3dVector(points[:, :3])
    if color is not None: cloud.paint_uniform_color(color)
    vis.add_geometry(cloud)

    if bboxes_3d is not None:
        create_add_3d_boxes(bboxes_3d, vis=vis, with_label=with_label)

    vis.run()
    vis.destroy_window()
