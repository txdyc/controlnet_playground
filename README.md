# ControlNet Playground
The supporting repository for all things controlnet. Contains tutorials:

## Living room remodeller

![](images/livingroom.gif)

Living room remodeller - a model that uses semantic segmentation and MLSD edge detection to take an input of a room and generate what it thinks your living room should look like, based on a prompt. 

Check out this post for details of what this does: https://hutsons-hacks.info/using-controlnet-models-to-remodel-my-living-room. 

To use the remodeller, copy the class from the article in Python, and then created a `main.py` file, or encapsulate in main block, as below: 

```
if __name__=='__main__':
    prompt = 'living room with navy theme'
    img_path = 'images/house.jpeg'

    mlsd_net_seg = ControlNetMLSD(
        prompt=prompt, 
        image_path=img_path
    )
    
    mlsd_net_seg.generate_mlsd_image(
        mlsd_save_path=f'images/house_mlsd_{prompt.strip().replace(" ", "")}.jpeg',
        mlsd_diff_gen_save_path=f'images/house_mlsd_gen_{prompt.strip().replace(" ", "")}.jpeg'
        )

```

## Doodle Face

![](images/MiniDoofdle.gif)

Doodle face - a model to take a profile picture and convert into your favourite animated images and some historical figures. 

See the supporting post: https://hutsons-hacks.info/creating-doodles-with-hed-detection-and-controlnet:




