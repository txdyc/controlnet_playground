# Futures
from __future__ import unicode_literals
from __future__ import print_function
# Owned
__project__ = 'Doodle Face'
__author__ = "Gary Hutson"
__copyright__ = "Copyright 2023, Hutsons-hacks.info"
__credits__ = ["Gary Hutson"]
__license__ = "MPL 2.0"
__version__ = "0.1.0"
__maintainer__ = "Gary Hutson"
__email__ = "hutsons-hacks@outlook.com"
__status__ = "Dev"

# Imports
from PIL import Image
from diffusers import StableDiffusionControlNetPipeline, ControlNetModel, UniPCMultistepScheduler
import torch
from controlnet_aux import HEDdetector

class ScribbleControlNet:
    def __init__(self, image_path, 
                 hed_detector="lllyasviel/ControlNet",
                 pt_controlnet="fusing/stable-diffusion-v1-5-controlnet-scribble", 
                 pt_stablediffusion="runwayml/stable-diffusion-v1-5"):
        self.image_path = image_path
        # Set pretrained HED detector 
        self.hed = HEDdetector.from_pretrained(hed_detector)
        # Set control net and diffusion model
        self.controlnet = ControlNetModel.from_pretrained(
            pt_controlnet, 
            torch_dtype=torch.float16
        )
        self.pipe = StableDiffusionControlNetPipeline.from_pretrained(
            pt_stablediffusion, 
            controlnet = self.controlnet,
            torch_dtype=torch.float16
        )
        # Optimize the pipe
        self.pipe.scheduler = UniPCMultistepScheduler.from_config(self.pipe.scheduler.config)
        self.pipe.enable_xformers_memory_efficient_attention()
        self.pipe.enable_model_cpu_offload()
        # Load image
        assert isinstance(self.image_path, str), 'The path to the image needs to be a string (str) data type'
        self.image = Image.open(self.image_path)
        self.image = self.hed(self.image, scribble=True)

    def generate_scribble(self, prompt, save_path=None, num_inf_steps=20):
        # Create the instance variables
        self.prompt = prompt
        self.save_path = save_path
        self.num_steps = num_inf_steps

        image = self.pipe(self.prompt, 
                          self.image, 
                          num_inference_steps=self.num_steps).images[0]
        
        if save_path is not None:
            image.save(f'{save_path}.png')

        return image
    
    def __str__(self):
        return f'Image loaded from {self.image_path}'


if __name__=='__main__':
    # Create header print before running code
    prompt = "a smart looking businessman"
    print('-' * 80)
    print(f'Script created by {__author__}\nProject: {__project__}')
    print(f'Based on prompt: {prompt}')
    print('-' * 80)

    
    doodle = ScribbleControlNet(
        'images/man.jpeg'
    )
    print(doodle)
    image_gen = doodle.generate_scribble(prompt, 
                                           num_inf_steps=50,
                                           save_path=f'images/{prompt.strip().replace(" ", "")}')
    
  