from moviepy.editor import *
from tqdm import tqdm
import sys
tqdm(disable=True, total=0)  # initialise internal lock

ipython_display("test.mp4", maxduration=70)

importedvideo = VideoFileClip("test.mp4")  #Video Imported to System
exportedvideo = importedvideo.subclip(20,40)  #Clip the Video

# Write a text overlay on the video
txt_clip = ( TextClip("Test Text",fontsize=40,color='white')
             .set_position('center')
             .set_duration(10) )

result = CompositeVideoClip([exportedvideo, txt_clip]) # Overlay text on video
result.write_videofile("test_edited.mp4",fps=25) # Final Result on the video
