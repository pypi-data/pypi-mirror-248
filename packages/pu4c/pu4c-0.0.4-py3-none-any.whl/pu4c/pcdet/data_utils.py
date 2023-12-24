from . import config
from .common_utils import transform_matrix
from ..common.common_utils import limit_period
import pickle
import numpy as np
from pyquaternion import Quaternion


def decode_kitti_infos(pkl, valid_classes, num_features=4, **kwargs):
    with open(pkl, 'rb') as f:
        infos = pickle.load(f)
    split = "training" if ("train" in pkl or "val" in pkl) else "testing"
    vis_infos = []
    for info in infos:
        frame_id = info['point_cloud']['lidar_idx']
        cloudpath = f"{split}/velodyne/{frame_id}.bin"
        lidar_info = {
            'frame_id': frame_id,
            'filepath': cloudpath,
            'num_features': num_features,
        }
        
        imagepath = f"{split}/image_2/{info['image']['image_idx']}.png"
        lidar2pixel_mat = info['calib']['P2'] @ info['calib']['R0_rect'] @ info['calib']['Tr_velo_to_cam']
        image_info = {
            'image_2': {
                'filepath': imagepath,
                'l2p_mat': lidar2pixel_mat,
            },
        }

        if 'annos' in info:
            annos = {}
            gt_boxes_lidar = []
            for i, name in enumerate(info['annos']['name']):
                if name in valid_classes:
                    gt_boxes_lidar.append(info['annos']['gt_boxes_lidar'][i])
            annos['gt_boxes_lidar'] = np.array(gt_boxes_lidar)

            mask = np.array([name in valid_classes for name in info['annos']['name']], dtype=bool)
            for k, v in info['annos'].items():
                if k in ['name', 'num_points_in_gt', 'difficulty', 'occluded', 'truncated']:
                    annos[k] = v[mask]
        vis_infos.append({'lidar': lidar_info, 'image': image_info, 'annos': annos})

    return vis_infos
def decode_nuscenes_infos(pkl, valid_classes, num_features=5, add_ext_info=False):
    with open(pkl, 'rb') as f:
        infos = pickle.load(f)

    vis_infos = []
    for info in infos:
        lidar_info = {
            'frame_id': info['token'],
            'filepath': info['lidar_path'],
            'num_features': num_features,
        }

        image_info = {}
        e2l_mat = info['ref_from_car']
        g2e_lidar_mat = info['car_from_global']
        l2e_mat = transform_matrix(e2l_mat[:3, :3], e2l_mat[:3, 3], inverse=True)
        e2g_lidar_mat = transform_matrix(g2e_lidar_mat[:3, :3], g2e_lidar_mat[:3, 3], inverse=True)
        for key, cam in info['cams'].items():
            intrinsics_4x4 = np.eye(4)
            intrinsics_4x4[:3, :3] = cam['camera_intrinsics']
            c2e_mat_inv = transform_matrix(Quaternion(cam['sensor2ego_rotation']).rotation_matrix, np.array(cam['sensor2ego_translation']), inverse=True)
            e2g_cam_mat_inv = transform_matrix(Quaternion(cam['ego2global_rotation']).rotation_matrix, np.array(cam['ego2global_translation']), inverse=True)

            lidar2pixel_mat = intrinsics_4x4 @ c2e_mat_inv @ e2g_cam_mat_inv @ e2g_lidar_mat @ l2e_mat

            image_info[key] = {
                'filepath': cam['data_path'],
                'l2p_mat': lidar2pixel_mat,
            }

        annos = {
            'name': info['gt_names'],
            'gt_boxes_lidar': info['gt_boxes'][:, :7],
            'num_points_in_gt': info['num_lidar_pts'],
        }
        vis_infos.append({'lidar': lidar_info, 'image': image_info, 'annos': annos})
        
    if add_ext_info:
        from nuscenes.nuscenes import NuScenes
        version = "v1.0-trainval"
        nusc = NuScenes(version=version, dataroot=config.nus_root, verbose=True)
        # 添加场景描述信息用于可视化时，过滤样本
        for info in vis_infos:
            sample_token = info['lidar']['frame_id']
            sample = nusc.get('sample', sample_token)
            scene = nusc.get('scene', sample['scene_token'])
            info['lidar']['desc'] = scene['description'].lower()

    return vis_infos
def decode_waymo_infos(fname, valid_classes, num_features=6, add_ext_info=False):
    with open(fname, 'rb') as f:
        infos = pickle.load(f)

    map_cam_name2id = {'CAM_FRONT': 0, 'CAM_FRONT_LEFT': 1, 'CAM_FRONT_RIGHT': 2, 'CAM_SIDE_LEFT': 3, 'CAM_SIDE_RIGHT': 4}
    map_label2name = {v: k for k, v in infos['metainfo']['categories'].items()}
    spilt = "training" if ("train" in fname or "val" in fname) else "testing"
    vis_infos = []
    for info in infos['data_list']:
        cloudpath = f"{spilt}/velodyne/{info['lidar_points']['lidar_path']}"
        lidar_info = {
            'frame_id': info['sample_idx'],
            'filepath': cloudpath,
            'num_features': num_features,
        }
        
        image_info = {}
        for key, cam in info['images'].items():
            img_ix = f"image_{map_cam_name2id[key]}"
            imagepath = f"{spilt}/{img_ix}/{cam['img_path']}"

            lidar2pixel_mat = np.array(cam['lidar2img'])
            image_info[key] = {
                'filepath': imagepath,
                'l2p_mat': lidar2pixel_mat,
            }
        
        names, boxes, num_pts = [], [], []
        for instance in info['instances']:
            name = map_label2name[instance['bbox_label_3d']]
            if name in valid_classes:
                # 3D 框需要计算，参考 WaymoDataset.parse_ann_info/CameraInstance3DBoxes.convert_to
                # camera_name = map_cam_id2name[int(instance['camera_id'])] # 用每个相机自己的矩阵反而是错了
                # lidar2cam = np.array(info['images'][camera_name]['lidar2cam'])
                lidar2cam = np.array(info['images']['CAM_FRONT']['lidar2cam'])
                cam2lidar = np.linalg.inv(lidar2cam)

                # box 转坐标系还挺麻烦
                gt_boxes_cam = instance['bbox_3d']
                xyz_ext = np.ones(4)
                xyz_ext[:3] = gt_boxes_cam[:3]
                xyz_ext = xyz_ext @ cam2lidar.T
                # % 这里注意相机坐标系转雷达坐标系，坐标轴要变
                xyz_size = np.array([gt_boxes_cam[3], gt_boxes_cam[5], gt_boxes_cam[4]])
                # 将角度映射 [-pi, pi] 区间内
                yaw = limit_period(-gt_boxes_cam[6] - np.pi / 2, period=np.pi * 2)

                # mmdet3d 中似乎有 bug，没对 z 纠正导致框高度上有偏移
                xyz_ext[2] = xyz_ext[2] + (xyz_size[2] / 2)
                
                names.append(name)
                boxes.append(np.concatenate([xyz_ext[:3], xyz_size, yaw[..., np.newaxis]]))
                num_pts.append(instance['num_lidar_pts'])
                # difficultys.append(instance['difficulty'])
        annos = {
            'name': np.array(names),
            'gt_boxes_lidar': np.array(boxes),
            'num_points_in_gt': np.array(num_pts),
        }
        vis_infos.append({'lidar': lidar_info, 'image': image_info, 'annos': annos})
    
    if add_ext_info:
        import os
        from . import config

        waymo_ext_info_pkl = config.waymo_ext_info_pkls[0] if 'train' in fname else config.waymo_ext_info_pkls[1]
        if os.path.exists(waymo_ext_info_pkl):
            print(f"file exist: {waymo_ext_info_pkl}")
            with open(waymo_ext_info_pkl, 'rb') as f:
                all_ext_infos = pickle.load(f)
        else:
            from waymo_open_dataset import dataset_pb2
            import tensorflow as tf
            from tqdm import tqdm
            from glob import glob
            key = 'training' if 'train' in fname else 'validation'
            load_dir = f"{config.waymo_raw_root}/{key}"
            tfrecord_pathnames = sorted(glob(os.path.join(load_dir, '*.tfrecord')))
            
            def get_ext_info_sigle(sequence_file):
                dataset = tf.data.TFRecordDataset(str(sequence_file), compression_type='')
                ext_infos = []
                for data in dataset:
                    frame = dataset_pb2.Frame()
                    frame.ParseFromString(bytearray(data.numpy()))
                    time_of_day = frame.context.stats.time_of_day.lower()
                    weather = frame.context.stats.weather.lower()
                    location = frame.context.stats.location.lower()
                    ext_info = {
                        'desc': f"{time_of_day} {weather} {location}"
                    }
                    ext_infos.append(ext_info)
                return ext_infos
            
            num_workers=8
            import concurrent.futures as futures
            with futures.ThreadPoolExecutor(num_workers) as executor:
                ext_infos_list = list(tqdm(executor.map(get_ext_info_sigle, tfrecord_pathnames), total=len(tfrecord_pathnames)))

            all_ext_infos = [ext_info for ext_info_seq in ext_infos_list for ext_info in ext_info_seq]
            with open(waymo_ext_info_pkl, 'wb') as f:
                pickle.dump(all_ext_infos, f)

        assert (len(all_ext_infos) == len(vis_infos))
        for i in range(len(all_ext_infos)):
            vis_infos[i]['lidar']['desc'] = all_ext_infos[i]['desc']
        

    return vis_infos
