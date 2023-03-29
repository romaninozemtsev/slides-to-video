import os
import pathlib
import sys

def convert_mov_to_mp4(mov_file_path, out_video_path):
    os.system(f'ffmpeg -y -i "{mov_file_path}" -vcodec h264 -acodec aac {out_video_path}')
    return mov_file_path


def concat_videos_force_reencode(concat_file_path: str, out_video_path: str) -> str:
    os.system(f'ffmpeg -y -f concat -safe 0 -i {concat_file_path} -c:v h264 -c:a aac {out_video_path}')
    print("concatenated videos into ", out_video_path)
    return out_video_path


def create_concat_from_folder(folder_path: str, concat_file_path: str, extensions: list[str]) -> str:
    with open(concat_file_path, 'w') as f:
        for file in sorted(os.listdir(folder_path)):
            file_extension = pathlib.Path(file).suffix
            if file_extension in extensions:
                f.write(f"file '{file}'\n")
    return concat_file_path


def convert_folder_of_mov_to_single_mp4(folder_path: str, out_video: str) -> str:
    print("converting folder of mov to single mp4", folder_path, out_video)
    concat_file_path = os.path.join(folder_path, 'videos.txt')
    # we'll re-encode each file to mp4 first
    for file in sorted(os.listdir(folder_path)):
        file_extension = pathlib.Path(file).suffix
        if file_extension == '.mov':
            full_path = os.path.join(folder_path, file)
            out_file = full_path.replace('.mov', '.mp4').replace(' ', '_')
            convert_mov_to_mp4(full_path, out_file)
    create_concat_from_folder(folder_path, concat_file_path, ['.mp4'])
    concat_videos_force_reencode(concat_file_path, out_video)
    return out_video


if __name__ == '__main__':
    folder_path = 'testdata'
    out_video = 'out/combined.mp4'
    
    if len(sys.argv) > 1:
        folder_path = sys.argv[1]
    if len(sys.argv) > 2:
        out_video = sys.argv[2]

    convert_folder_of_mov_to_single_mp4(folder_path, out_video)
    print("done")