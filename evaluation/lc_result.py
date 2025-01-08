'''
Copyright © 2025, Sun Yat-sen University, Guangzhou, Guangdong, 510275, All Rights Reserved
Author: Ronghai He
Date: 2024-12-26 20:31:33
LastEditors: RonghaiHe hrhkjys@qq.com
LastEditTime: 2025-01-08 12:20:32
FilePath: /src/kimera_multi/evaluation/lc_result.py
Version: 1.3.0
Description: To log the loop closure result with groundtruth pose and visualize them

'''
import pandas as pd
from scipy.spatial.transform import Rotation as R
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
import time
import argparse
import os
import csv

# Create colormap for distances
norm = Normalize(vmin=0, vmax=50)  # Normalize distances from 0 to 20 meters
cmap = plt.cm.RdYlBu  # Red-Yellow-Blue colormap

ID2ROBOT = [
    'acl_jackal',
    'acl_jackal2',
    'sparkal1',
    'sparkal2',
    'hathor',
    'thoth',
    'apis',
    'sobek'
]

DATE2DATASET = {'1207': 'campus_tunnels_12_07',
                '1014': 'campus_outdoor_10_14',
                '1208': 'campus_hybrid_12_08'}


def read_groundtruth_tum(file_path):
    # Read the ground truth poses from TUM file
    groundtruth_data = pd.read_csv(file_path, sep=' ', header=None)
    groundtruth_data.columns = ['timestamp',
                                'tx', 'ty', 'tz', 'qx', 'qy', 'qz', 'qw']
    return groundtruth_data


def find_closest_pose(timestamp, groundtruth_data, tolerance=0.01):
    # Find the closest pose within the given tolerance
    closest_pose = None
    min_diff = float('inf')
    for _, row in groundtruth_data.iterrows():
        diff = abs(row['timestamp'] - timestamp)
        if diff < min_diff and diff <= tolerance:
            min_diff = diff
            closest_pose = row[1:].values
    return closest_pose


def calculate_relative_pose(pose1, pose2):
    # Extract quaternion and translation from poses
    q1 = pose1[3:]
    t1 = pose1[:3]
    q2 = pose2[3:]
    t2 = pose2[:3]

    # Convert quaternions to rotation matrices
    R1 = R.from_quat(q1).as_matrix()
    R2 = R.from_quat(q2).as_matrix()

    # Calculate relative rotation
    R_rel = R2 @ R1.T

    # Convert relative rotation matrix back to quaternion
    q_rel = R.from_matrix(R_rel).as_quat()

    # Calculate relative translation (2 local coordinate frame)
    t_rel = t2 - t1

    # Calculate distance
    distance = np.linalg.norm(t_rel)

    # Calculate rotation angle
    rotation = R.from_quat(q_rel)
    angle = rotation.magnitude()

    return q_rel, t_rel, distance, angle


def parse_args():
    parser = argparse.ArgumentParser(
        description='Process loop closure results')
    parser.add_argument('--date', type=str, default='1207',
                        choices=list(DATE2DATASET.keys()),
                        help='Date of the dataset (e.g., 1207, 1014, 1208)')
    parser.add_argument('--basic_path', type=str,
                        default='/media/sysu/Data/multi_robot_datasets/kimera_multi_datasets',
                        help='Base path to the multi-robot datasets')
    parser.add_argument('--num_robots', type=int, default=6,
                        help='Number of robots in the dataset, often 6 or 8')
    return parser.parse_args()


def parse_csv_files(loop_closure_file, lcd_status_file, lcd_result_file):
    # Read loop closures
    inter_lc = []
    with open(loop_closure_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['robot1'] != row['robot2']:  # Only keep inter-robot loop closures
                inter_lc.append({
                    'robot1': int(row['robot1']),
                    'pose1': int(row['pose1']),
                    'robot2': int(row['robot2']),
                    'pose2': int(row['pose2']),
                    'qx': float(row['qx']),
                    'qy': float(row['qy']),
                    'qz': float(row['qz']),
                    'qw': float(row['qw']),
                    'tx': float(row['tx']),
                    'ty': float(row['ty']),
                    'tz': float(row['tz']),
                    'norm_bow_score': float(row['norm_bow_score']),
                    'mono_inliers': int(row['mono_inliers']),
                    'stereo_inliers': int(row['stereo_inliers']),
                    'stamp_ns': int(row['stamp_ns'])
                })

    # Read LCD status and filter for LOOP_DETECTED
    intra_lc = []
    intra_lc_rejected_part = []
    with open(lcd_status_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['lcd_status'] == 'LOOP_DETECTED':
                intra_lc.append({
                    'pose2': int(row['query_id']),
                    'pose1': int(row['match_id']),
                    'mono_inliers': int(row['mono_inliers']),
                    'stereo_inliers': int(row['stereo_inliers']),
                })
            elif row['lcd_status'] == 'FAILED_TEMPORAL_CONSTRAINT' or \
                    row['lcd_status'] == 'FAILED_GEOM_VERIFICATION' or \
                    row['lcd_status'] == 'FAILED_POSE_RECOVERY':
                intra_lc_rejected_part.append({
                    'pose2': int(row['query_id']),
                    'pose1': int(row['match_id']),
                    'lcd_status': row['lcd_status'],
                    'mono_inliers': int(row['mono_inliers']),
                    'stereo_inliers': int(row['stereo_inliers']),
                })

    # Read LCD results
    with open(lcd_result_file, 'r') as f:
        reader = csv.DictReader(f)
        count = 0
        for row in reader:
            if row['isLoop'] == '1':
                assert (intra_lc[count]['pose2'] == int(row['queryKfId']))
                assert (intra_lc[count]['pose1'] == int(row['matchKfId']))

                intra_lc[count]['timestamp2'] = int(row['timestamp_query'])
                intra_lc[count]['timestamp1'] = int(row['timestamp_match'])
                intra_lc[count]['tx'] = float(row['x'])
                intra_lc[count]['ty'] = float(row['y'])
                intra_lc[count]['tz'] = float(row['z'])
                intra_lc[count]['qx'] = float(row['qx'])
                intra_lc[count]['qy'] = float(row['qy'])
                intra_lc[count]['qz'] = float(row['qz'])
                intra_lc[count]['qw'] = float(row['qw'])

                count += 1

                # Write intra-robot loops to new file
    output_dir = os.path.dirname(loop_closure_file)
    robot_name = os.path.basename(os.path.dirname(output_dir))
    intra_output = os.path.join(
        output_dir, f'intra_robot_lc_results_{robot_name}.csv')

    # with open(intra_output, 'w') as f:
    #     writer = csv.DictWriter(f, fieldnames=intra_robot_loops[0].keys())
    #     writer.writeheader()
    #     writer.writerows(intra_robot_loops)

    return inter_lc, intra_lc, intra_lc_rejected_part


def main(args):
    start_time = time.time()
    fig, ax = plt.subplots(figsize=(10, 8))

    if args.date not in DATE2DATASET:
        print('Invalid date: {}'.format(args.date))
        return

    dataset_name = DATE2DATASET[args.date]

    # Check if exists the file for dateoutput_file
    if not os.path.exists(f'{args.date}'):
        os.makedirs(f'{args.date}')
    else:
        # remove files in that directory
        for filename in os.listdir(f'{args.date}'):
            file_path = os.path.join(f'{args.date}', filename)
            if os.path.isfile(file_path):
                os.remove(file_path)

    # Construct paths inside main function
    loop_closure_file_prefix = f'{args.basic_path}/{dataset_name}/log_data_{args.date[:2]}_{args.date[2:]}'
    keyframes_files_prefix = f'{args.basic_path}/{dataset_name}/log_data_{args.date[:2]}_{args.date[2:]}/'
    groundtruth_files_prefix = f'{args.basic_path}/Kimera-Multi-Public-Data/ground_truth/{args.date}/'
    inter_output_file = f'./{args.date}/inter_lc_results_{args.date}_'
    intra_output_file = f'./{args.date}/intra_lc_results_{args.date}_'
    intra_rejected_part_output_file = f'./{args.date}/intra_lc_rejected_part_{args.date}_'

    # Read the loop closure data
    loop_closure_files = [f"{loop_closure_file_prefix}/{ID2ROBOT[i]}/distributed/loop_closures.csv"
                          for i in range(args.num_robots)]
    lcd_status_files = [f"{loop_closure_file_prefix}/{ID2ROBOT[i]}/single/output_lcd_status.csv"
                        for i in range(args.num_robots)]
    lcd_result_files = [f"{loop_closure_file_prefix}/{ID2ROBOT[i]}/single/output_lcd_result.csv"
                        for i in range(args.num_robots)]

    # Process each robot's data
    inter_lc_data = {}
    intra_lc_data = {}
    inter_lc_rejected_part_data = {}
    for i in range(args.num_robots):
        inter_lc_results, intra_lc_results, intra_lc_rejected_part_results = parse_csv_files(
            loop_closure_files[i], lcd_status_files[i], lcd_result_files[i])
        inter_lc_data[i] = pd.DataFrame(inter_lc_results)
        intra_lc_data[i] = pd.DataFrame(intra_lc_results)
        inter_lc_rejected_part_data[i] = pd.DataFrame(
            intra_lc_rejected_part_results)

    # Read the ground truth data for all robots
    groundtruth_files = [
        f"{groundtruth_files_prefix}modified_{ID2ROBOT[i]}_gt_odom.tum" for i in range(args.num_robots)
    ]
    groundtruth_data = {i: read_groundtruth_tum(
        file) for i, file in enumerate(groundtruth_files)}

    # Read the keyframes data for all robots, use keyframe's ID mapping timestamp
    keyframes_files = [
        f"{keyframes_files_prefix}{ID2ROBOT[i]}/distributed/kimera_distributed_keyframes.csv" for i in range(args.num_robots)
    ]
    keyframes_data = {i: pd.read_csv(
        file) for i, file in enumerate(keyframes_files)}

    # Create a dictionary to store the keyframe timestamps by ID for each robot
    keyframes_dict = {
        i: {row['keyframe_id']: row['keyframe_stamp_ns'] /
            1e9 for _, row in keyframes_data[i].iterrows()}
        for i in range(args.num_robots)
    }

    earliest_timestamp = [keyframes_dict[i].get(
        0) for i in range(args.num_robots)]

    line_collection = []
    for i in range(args.num_robots):
        with open(intra_rejected_part_output_file + ID2ROBOT[i] + '.csv', 'w') as f:
            # Write the CSV header
            f.write("Loop Closure Number,Relative Time 1,Relative Time 2,"
                    "Distance,Rotation Angle (radians),"
                    "mono_inliers,stereo_inliers,"  # Added new fields
                    "Estimated Distance,Estimated Angle(Radian),"
                    "Timestamp 1,Timestamp 2,"
                    "GT_Pose1_X,GT_Pose1_Y,GT_Pose1_Z,"  # Ground truth positions
                    "GT_Pose2_X,GT_Pose2_Y,GT_Pose2_Z,"
                    "Est_Pose1_X,Est_Pose1_Y,Est_Pose1_Z,"  # Estimated positions
                    "Est_Pose2_X,Est_Pose2_Y,Est_Pose2_Z,"
                    "Relative Rotation Quaternion, Relative Translation Vector,"
                    "Estimated Relative Rotation,Estimated Relative Translation\n")

            for index, row in inter_lc_rejected_part_data[i].iterrows():
                keyframe_id1 = row['pose1']
                keyframe_id2 = row['pose2']

                timestamp1 = keyframes_dict[i].get(keyframe_id1)
                timestamp2 = keyframes_dict[i].get(keyframe_id2)

                if timestamp1 is not None and timestamp2 is not None:
                    est_pose1 = keyframes_data[i].loc[keyframes_data[i]['keyframe_id'] == keyframe_id1][[
                        'tx', 'ty', 'tz', 'qx', 'qy', 'qz', 'qw']].values[0]
                    est_pose2 = keyframes_data[i].loc[keyframes_data[i]['keyframe_id'] == keyframe_id2][[
                        'tx', 'ty', 'tz', 'qx', 'qy', 'qz', 'qw']].values[0]

                    estimated_relative_R, estimated_relative_t, estimated_distance, estimated_angle = calculate_relative_pose(
                        est_pose1, est_pose2)

                    relative_time1 = timestamp1 - \
                        earliest_timestamp[i]
                    relative_time2 = timestamp2 - \
                        earliest_timestamp[i]

                    gt_pose1 = find_closest_pose(
                        timestamp1, groundtruth_data[i], tolerance=0.1)
                    gt_pose2 = find_closest_pose(
                        timestamp2, groundtruth_data[i], tolerance=0.1)

                    if gt_pose1 is not None and gt_pose2 is not None:

                        # Calculate the relative pose, distance, and rotation angle
                        q_rel, t_rel, distance, angle = calculate_relative_pose(
                            gt_pose1, gt_pose2)

                        f.write(
                            f"{index},{relative_time1},{relative_time2},"
                            f"{distance},{angle},"
                            f"{row['mono_inliers']},{row['stereo_inliers']},"
                            f"{estimated_distance},{estimated_angle},"
                            f"{timestamp1},{timestamp2},"
                            # GT pose
                            f"{gt_pose1[0]},{gt_pose1[1]},{gt_pose1[2]},"
                            f"{gt_pose2[0]},{gt_pose2[1]},{gt_pose2[2]},"
                            # Estimated pose
                            f"{est_pose1[0]},{est_pose1[1]},{est_pose1[2]},"
                            f"{est_pose2[0]},{est_pose2[1]},{est_pose2[2]},"
                            f"{q_rel},{t_rel},{estimated_relative_R},{estimated_relative_t}\n")
                    else:
                        f.write(
                            f"{index},{relative_time1},{relative_time2},"
                            f"No GT data,,"
                            f"{row['mono_inliers']},{row['stereo_inliers']},"
                            f"{estimated_distance},{estimated_angle},"
                            f"{timestamp1},{timestamp2},,,,,,,"
                            # Estimated pose
                            f"{est_pose1[0]},{est_pose1[1]},{est_pose1[2]},"
                            f"{est_pose2[0]},{est_pose2[1]},{est_pose2[2]},"
                            f",,{estimated_relative_R},{estimated_relative_t}\n")
                else:
                    f.write(
                        f"{index},,,No keyframe data,,\n")

        with open(intra_output_file + ID2ROBOT[i] + '.csv', 'w') as f:
            # Write the CSV header
            f.write("Loop Closure Number,Relative Time 1,Relative Time 2,"
                    "Distance,Rotation Angle (radiansinter_csv_filename),"
                    "mono_inliers,stereo_inliers,"  # Added new fields
                    "Estimated Distance,Estimated Angle(Radian),"
                    "Timestamp 1,Timestamp 2,"
                    "GT_Pose1_X,GT_Pose1_Y,GT_Pose1_Z,"  # Ground truth positions
                    "GT_Pose2_X,GT_Pose2_Y,GT_Pose2_Z,"
                    "Est_Pose1_X,Est_Pose1_Y,Est_Pose1_Z,"  # Estimated positions
                    "Est_Pose2_X,Est_Pose2_Y,Est_Pose2_Z,"
                    "Relative Rotation Quaternion,Relative Translation Vector,"
                    "Estimated Relative Rotation,Estimated Relative Translation\n")

            # f.write("Loop Closure Number,Robot 1,Relative Time 1,Robot 2,Relative Time 2,Distance,Rotation Angle (radians),Estimated Distance, Estimated Angle(Radian),Timestamp 1,Timestamp 2,Relative Rotation Quaternion,Relative Translation Vector,Estimated Relative Rotation, Estimated Relative Translation\n")

            # Iterate through intra-loop closure data to calculate relative poses
            for index, row in intra_lc_data[i].iterrows():
                keyframe_id1 = row['pose1']
                keyframe_id2 = row['pose2']

                timestamp1 = row['timestamp1'] / 1e9
                timestamp2 = row['timestamp2'] / 1e9

                estimated_relative_R = np.array(
                    [row['qw'], row['qx'], row['qy'], row['qz']])
                estimated_relative_t = np.array(
                    [row['tx'], row['ty'], row['tz']])
                estimated_distance = np.linalg.norm(estimated_relative_t)
                estimated_angle = R.from_quat(estimated_relative_R).magnitude()

                if timestamp1 is not None and timestamp2 is not None:
                    gt_pose1 = find_closest_pose(
                        timestamp1, groundtruth_data[i], tolerance=0.1)
                    gt_pose2 = find_closest_pose(
                        timestamp2, groundtruth_data[i], tolerance=0.1)

                    if gt_pose1 is not None and gt_pose2 is not None:
                        relative_time1 = timestamp1 - \
                            earliest_timestamp[i]
                        relative_time2 = timestamp2 - \
                            earliest_timestamp[i]

                        est_pose1 = keyframes_data[i].loc[keyframes_data[i]['keyframe_id'] == keyframe_id1][[
                            'tx', 'ty', 'tz']].values[0]
                        est_pose2 = keyframes_data[i].loc[keyframes_data[i]['keyframe_id'] == keyframe_id2][[
                            'tx', 'ty', 'tz']].values[0]

                        # Calculate the relative pose, distance, and rotation angle
                        q_rel, t_rel, distance, angle = calculate_relative_pose(
                            gt_pose1, gt_pose2)

                        color = cmap(norm(distance))
                        line = ax.plot([gt_pose1[0], gt_pose2[0]], [
                            gt_pose1[1], gt_pose2[1]], '-.', color=color, alpha=0.6, linewidth=1.0)
                        line_collection.append(line[0])

                        # Add distance value in the middle of the line
                        if distance >= 50:
                            mid_point = (gt_pose1 + gt_pose2) / 2
                            ax.text(mid_point[0], mid_point[1],
                                    f"{distance:.2f}",
                                    color=color,
                                    fontsize=8)

                        # Add points for corresponding poses
                        ax.scatter(gt_pose1[0], gt_pose1[1], color=color, marker='o',
                                   s=20, zorder=5, edgecolor='black', linewidth=0.5)
                        ax.scatter(gt_pose2[0], gt_pose2[1], color=color, marker='s',
                                   s=20, zorder=5, edgecolor='black', linewidth=0.5)

                        f.write(
                            f"{index},{relative_time1},{relative_time2},"
                            f"{distance},{angle},"
                            # Added new fields
                            f"{row['mono_inliers']},{row['stereo_inliers']},"
                            f"{estimated_distance},{estimated_angle},"
                            f"{timestamp1},{timestamp2},"
                            # GT pose
                            f"{gt_pose1[0]},{gt_pose1[1]},{gt_pose1[2]},"
                            f"{gt_pose2[0]},{gt_pose2[1]},{gt_pose2[2]},"
                            # Est pose
                            f"{est_pose1[0]},{est_pose1[1]},{est_pose1[2]},"
                            f"{est_pose2[0]},{est_pose2[1]},{est_pose2[2]},"
                            f"{q_rel},{t_rel},{estimated_relative_R},{estimated_relative_t}\n")
                    else:
                        f.write(
                            f"{index},{relative_time1},{relative_time2},No GT data,,"
                            # Added new fieldsinter_csv_filename
                            f"{row['mono_inliers']},{row['stereo_inliers']},"
                            f"{estimated_distance},{estimated_angle},"
                            f"{timestamp1},{timestamp2},,,,,,,"
                            f"{est_pose1[0]},{est_pose1[1]},{est_pose1[2]},"
                            f"{est_pose2[0]},{est_pose2[1]},{est_pose2[2]},"
                            f",,{estimated_relative_R},{estimated_relative_t}\n")
                else:
                    f.write(
                        f"{index},,,No keyframe data,,{estimated_distance},{estimated_angle},{timestamp1},{timestamp2}\n")

        with open(inter_output_file + ID2ROBOT[i] + '.csv', 'w') as f:
            # Write the CSV header
            f.write("Loop Closure Number,Robot 1,Relative Time 1,Robot 2,Relative Time 2,"
                    "Distance,Rotation Angle (Radian),"
                    "norm_bow_score,mono_inliers,stereo_inliers,"  # Added new fields
                    "Estimated Distance,Estimated Angle(Radian),"
                    "Timestamp 1,Timestamp 2,"
                    "GT_Pose1_X,GT_Pose1_Y,GT_Pose1_Z,"  # Ground truth positions
                    "GT_Pose2_X,GT_Pose2_Y,GT_Pose2_Z,"
                    "Est_Pose1_X,Est_Pose1_Y,Est_Pose1_Z,"  # Estimated positions
                    "Est_Pose2_X,Est_Pose2_Y,Est_Pose2_Z,"
                    "Relative Rotation Quaternion,Relative Translation Vector,"
                    "Estimated Relative Rotation,Estimated Relative Translation\n")

            # f.write("Loop Closure Number,Robot 1,Relative Time 1,Robot 2,Relative Time 2,Distance,Rotation Angle (radians),Estimated Distance, Estimated Angle(Radian),Timestamp 1,Timestamp 2,Relative Rotation Quaternion,Relative Translation Vector,Estimated Relative Rotation, Estimated Relative Translation\n")

            # Iterate through loop closure data to calculate relative poses
            for index, row in inter_lc_data[i].iterrows():
                robot1 = row['robot1']
                robot2 = row['robot2']
                keyframe_id1 = row['pose1']
                keyframe_id2 = row['pose2']

                timestamp1 = keyframes_dict[robot1].get(keyframe_id1)
                timestamp2 = keyframes_dict[robot2].get(keyframe_id2)

                estimated_relative_R = np.array(
                    [row['qw'], row['qx'], row['qy'], row['qz']])
                estimated_relative_t = row[8:11].values
                estimated_distance = np.linalg.norm(estimated_relative_t)
                estimated_angle = R.from_quat(estimated_relative_R).magnitude()

                if timestamp1 is not None and timestamp2 is not None:
                    est_pose1 = keyframes_data[robot1].loc[keyframes_data[robot1]['keyframe_id'] == keyframe_id1][[
                        'tx', 'ty', 'tz']].values[0]
                    est_pose2 = keyframes_data[robot2].loc[keyframes_data[robot2]['keyframe_id'] == keyframe_id2][[
                        'tx', 'ty', 'tz']].values[0]

                    gt_pose1 = find_closest_pose(
                        timestamp1, groundtruth_data[robot1], tolerance=0.1)
                    gt_pose2 = find_closest_pose(
                        timestamp2, groundtruth_data[robot2], tolerance=0.1)

                    if gt_pose1 is not None and gt_pose2 is not None:
                        relative_time1 = timestamp1 - \
                            earliest_timestamp[int(robot1)]
                        relative_time2 = timestamp2 - \
                            earliest_timestamp[int(robot2)]

                        # Calculate the relative pose, distance, and rotation angle
                        q_rel, t_rel, distance, angle = calculate_relative_pose(
                            gt_pose1, gt_pose2)

                        color = cmap(norm(distance))
                        line = ax.plot([gt_pose1[0], gt_pose2[0]], [
                            gt_pose1[1], gt_pose2[1]], '--', color=color, alpha=0.6, linewidth=1.0)
                        line_collection.append(line[0])

                        # Add distance value in the middle of the line
                        if distance >= 50:
                            mid_point = (gt_pose1 + gt_pose2) / 2
                            ax.text(mid_point[0], mid_point[1],
                                    f"{distance:.2f}",
                                    color=color,
                                    fontsize=8)

                        # Add points for corresponding poses
                        ax.scatter(gt_pose1[0], gt_pose1[1], color=color, marker='o',
                                   s=20, zorder=5, edgecolor='black', linewidth=0.5)
                        ax.scatter(gt_pose2[0], gt_pose2[1], color=color, marker='s',
                                   s=20, zorder=5, edgecolor='black', linewidth=0.5)

                        f.write(
                            f"{index},{ID2ROBOT[int(robot1)]},{relative_time1},"
                            f"{ID2ROBOT[int(robot2)]},{relative_time2},"
                            f"{distance},{angle},"
                            # Added new fields
                            f"{row['norm_bow_score']},{row['mono_inliers']},{row['stereo_inliers']},"
                            f"{estimated_distance},{estimated_angle},"
                            f"{timestamp1},{timestamp2},"
                            # GT pose
                            f"{gt_pose1[0]},{gt_pose1[1]},{gt_pose1[2]},"
                            f"{gt_pose2[0]},{gt_pose2[1]},{gt_pose2[2]},"
                            # Est pose
                            f"{est_pose1[0]},{est_pose1[1]},{est_pose1[2]},"
                            f"{est_pose2[0]},{est_pose2[1]},{est_pose2[2]},"
                            f"{q_rel},{t_rel},{estimated_relative_R},{estimated_relative_t}\n")
                    else:
                        f.write(
                            f"{index},{ID2ROBOT[int(robot1)]},,{ID2ROBOT[int(robot2)]},,No GT data,,"
                            f"{row['norm_bow_score']},{row['mono_inliers']},{row['stereo_inliers']},"
                            f"{estimated_distance},{estimated_angle},"
                            f"{timestamp1},{timestamp2},,,,,,,"
                            # Estimated pose
                            f"{est_pose1[0]},{est_pose1[1]},{est_pose1[2]},"
                            f"{est_pose2[0]},{est_pose2[1]},{est_pose2[2]},"
                            f",,{estimated_relative_R},{estimated_relative_t}\n")
                else:
                    f.write(
                        f"{index},{ID2ROBOT[int(robot1)]},,{ID2ROBOT[int(robot2)]},,No keyframe data,,{estimated_distance},{estimated_angle},{timestamp1},{timestamp2}\n")

        trajectory = groundtruth_data[i][['tx', 'ty', 'tz']].values
        ax.plot(trajectory[:, 0], trajectory[:, 1],
                label=ID2ROBOT[i], linewidth=1.5)

    # Add grid and labels
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.set_xlabel('X Position (m)', fontsize=12)
    ax.set_ylabel('Y Position (m)', fontsize=12)
    ax.set_title('Multi-Robot Trajectories and Loop Closures', fontsize=14)

    # Add colorbar
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax)
    cbar.set_label('Loop Closure Distance (m)', fontsize=10)

    plt.legend()
    plt.savefig(f'lc_results_{args.date}.jpg', dpi=300, bbox_inches='tight')

    print(f"Total time: {time.time() - start_time}")

    plt.show()


if __name__ == "__main__":
    args = parse_args()
    main(args)
