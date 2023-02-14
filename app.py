from utils.inference.image_processing import crop_face
from utils.inference.video_processing import read_video, get_target, get_final_video, add_audio_from_another_video
from utils.inference.core import model_inference

from network.AEI_Net import AEI_Net
from coordinate_reg.image_infer import Handler
from insightface_func.face_detect_crop_multi import Face_detect_crop
from arcface_model.iresnet import iresnet100

import base64
import numpy as np 
import cv2
import requests

def init():
    global app
    global generation
    global netArc
    global handler
    global model

    app = Face_detect_crop(name='antelope', root='./insightface_func/models')
    app.prepare(ctx_id= 0, det_thresh=0.6, det_size=(640,640))
    generation = AEI_Net(backbone='unet', num_blocks=2, c_id=512)
    generation.cuda()
    netArc = iresnet100(fp16=False)
    netArc.cuda()
    handler = Handler('./coordinate_reg/model/2d106det', 0, ctx_id=0, det_size=640)


def inference(inputs):
    global app
    global generation
    global netArc
    global handler
    global model

    image = inputs['image']
    video = inputs['video']

    with open('img.png', 'wb') as f:
        f.write(requests.get(image).content)

    with open('video.mp4', 'wb') as i:
        i.write(requests.get(video).content)
    
    source_full = cv2.imread('img.png')
    OUT_VIDEO_NAME = "result.mp4"
    crop_size = 224

    source = crop_face(source_full, app, crop_size)[0]
    source = [source[:, :, ::-1]]

    full_frames, fps = read_video('video.mp4')
    target = get_target(full_frames, app, crop_size)

    batch_size = 40
    final_frames_list, crop_frames_list, full_frames, tfm_array_list = model_inference(full_frames,
                                                                                        source, target,
                                                                                        netArc,
                                                                                        generation,
                                                                                        app,
                                                                                        set_target = False,
                                                                                        crop_size = crop_size,
                                                                                        BS = batch_size)
    
    get_final_video(final_frames_list,
                    crop_frames_list,
                    full_frames,
                    tfm_array_list,
                    OUT_VIDEO_NAME,
                    fps,
                    handler)
    
    add_audio_from_another_video('video.mp4', OUT_VIDEO_NAME, "audio")

    with open(OUT_VIDEO_NAME, 'rb') as videofile:
        text = base64.b64encode(videofile.read())
    return {'output': text}
