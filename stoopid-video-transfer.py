import argparse
import os
import subprocess

import neural_style_transfer as st

FILE_NAME_NUM_DIGITS: int = 6

if __name__ == "__main__":
    fps = 24
    frame_extension = '.jpg'
    default_resource_dir = os.path.join(os.path.dirname(__file__), 'data')
    content_images_dir = os.path.join(default_resource_dir, 'frames')
    style_images_dir = os.path.join(default_resource_dir, 'style-images')
    output_img_dir = os.path.join(default_resource_dir, 'output-images')

    video_path = frames_path = os.path.join(default_resource_dir, 'video')
    frames_path = os.path.join(default_resource_dir, 'frames')
    frame_name_format = rf'%0{FILE_NAME_NUM_DIGITS}d{frame_extension}'
    out_frame_pattern = os.path.join(frames_path, frame_name_format)
    os.makedirs(frames_path, exist_ok=True)
    ffmpeg = 'ffmpeg'

    #split frames
    if len(os.listdir(frames_path)) == 0:
        subprocess.call(
            [ffmpeg, '-i', video_path, '-r', str(fps), '-start_number', '0', '-qscale:v', '2', out_frame_pattern, '-c:a', 'copy'])
    else:
        print('Skip splitting video into frames and audio, already done.')
    #stylize frames
    first_frame = 0
    current_frame= first_frame
    while current_frame < len(os.listdir(frames_path)):
        #
        # fixed args - don't change these unless you have a good reason
        #

        img_format = (format(current_frame, '06d'), '.jpg')  # saves images in the format: %04d.jpg

        #
        # modifiable args - feel free to play with these (only small subset is exposed by design to avoid cluttering)
        # sorted so that the ones on the top are more likely to be changed than the ones on the bottom
        #
        img_name = format(current_frame, '06d') + '.jpg'
        parser = argparse.ArgumentParser()
        parser.add_argument("--content_img_name", type=str, help="content image name", default=img_name)
        parser.add_argument("--style_img_name", type=str, help="style image name", default='nebulosa.jpg')
        parser.add_argument("--height", type=int, help="height of content and style images", default=1000)

        parser.add_argument("--content_weight", type=float, help="weight factor for content loss", default=1e9)
        parser.add_argument("--style_weight", type=float, help="weight factor for style loss", default=3e5)
        parser.add_argument("--tv_weight", type=float, help="weight factor for total variation loss", default=1e0)

        parser.add_argument("--optimizer", type=str, choices=['lbfgs', 'adam'], default='lbfgs')
        parser.add_argument("--model", type=str, choices=['vgg16', 'vgg19'], default='vgg19')
        parser.add_argument("--init_method", type=str, choices=['random', 'content', 'style'], default='random')
        parser.add_argument("--saving_freq", type=int,
                            help="saving frequency for intermediate images (-1 means only final)", default=-1)
        args = parser.parse_args()

        # some values of weights that worked for figures.jpg, vg_starry_night.jpg (starting point for finding good images)
        # once you understand what each one does it gets really easy -> also see README.md

        # lbfgs, content init -> (cw, sw, tv) = (1e5, 3e4, 1e0)
        # lbfgs, style   init -> (cw, sw, tv) = (1e5, 1e1, 1e-1)
        # lbfgs, random  init -> (cw, sw, tv) = (1e5, 1e3, 1e0)

        # adam, content init -> (cw, sw, tv, lr) = (1e5, 1e5, 1e-1, 1e1)
        # adam, style   init -> (cw, sw, tv, lr) = (1e5, 1e2, 1e-1, 1e1)
        # adam, random  init -> (cw, sw, tv, lr) = (1e5, 1e2, 1e-1, 1e1)

        # just wrapping settings into a dictionary
        optimization_config = dict()
        for arg in vars(args):
            optimization_config[arg] = getattr(args, arg)
        optimization_config['content_images_dir'] = content_images_dir
        optimization_config['style_images_dir'] = style_images_dir
        optimization_config['output_img_dir'] = output_img_dir
        optimization_config['img_format'] = img_format

        # original NST (Neural Style Transfer) algorithm (Gatys et al.)
        print('frame:' + format(current_frame, '06d'))
        results_path = st.neural_style_transfer(optimization_config)
        current_frame = current_frame + 1