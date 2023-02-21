from cog import BasePredictor, Path, Input

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
import torch

class Predictor(BasePredictor):
  def setup(self):
    self.app = Face_detect_crop(name='antelope', root='./insightface_func/models')
    self.app.prepare(ctx_id= 0, det_thresh=0.6, det_size=(640,640))
    
    self.generation = AEI_Net(backbone='unet', num_blocks=2, c_id=512)
    self.generation.eval()
    self.generation.load_state_dict(torch.load('weights/G_unet_2blocks.pth', map_location=torch.device('cpu')))
    self.generation = self.generation.cuda()
    self.generation = self.generation.half()
    
    self.netArc = iresnet100(fp16=False)
    self.netArc.load_state_dict(torch.load('arcface_model/backbone.pth'))
    self.netArc = self.netArc.cuda()
    self.netArc.eval()
    
    self.handler = Handler('./coordinate_reg/model/2d106det', 0, ctx_id=0, det_size=640)
    
  def predict(self,
              image: Path = Input(description = "image path"),
              video: Path = Input(description = "video path") 
  ) -> Path:
    
    print("type of image ",type(image))
    source_image = str(image)
    source_full = cv2.imread(source_image)
    OUT_VIDEO_NAME = "result.mp4"
    crop_size = 224

    source = crop_face(source_full, self.app, crop_size)[0]
    source = [source[:, :, ::-1]]
    
    full_frames, fps = read_video(video)
    target = get_target(full_frames, self.app, crop_size)

    batch_size = 40
    final_frames_list, crop_frames_list, full_frames, tfm_array_list = model_inference(full_frames,
                                                                                        source, target,
                                                                                        self.netArc,
                                                                                        self.generation,
                                                                                        self.app,
                                                                                        set_target = False,
                                                                                        crop_size = crop_size,
                                                                                        BS = batch_size)
    
    get_final_video(final_frames_list,
                    crop_frames_list,
                    full_frames,
                    tfm_array_list,
                    OUT_VIDEO_NAME,
                    fps,
                    self.handler)
    
    add_audio_from_another_video('video.mp4', OUT_VIDEO_NAME, "audio")

    with open(OUT_VIDEO_NAME, 'rb') as videofile:
        text = base64.b64encode(videofile.read()).decode('utf-8')
    return text
                   
