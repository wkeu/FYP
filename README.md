# 360 Video Derotator

## Introduction 
This repo presents a method for removing rotational motion from an omnidirectional video captured from the viewpoint of a spinning object. This agorithm can be used to recover stable footage from spherical video captured from a spinning 360 camera. 
The algorithm has been successfully tested with various styles of footage which can be viewed [here](https://www.youtube.com/playlist?list=PL9XiBq5tluqSOiY56WZ51r66WDUoJMMfZ). Below is an image example of specific frames showcasing the result of the algorithm. The left shows the video when derotated and the video on the right is the original test footage. Note in the derotated footage the horizon stays constant within the frame. 

![alt text](https://github.com/wkeu/360-video-derotator/blob/master/figures/throw_test.png)

## Package Requirements
Note that the following packages are required/recommended in order to use the directory:
- Anaconda2 4.2.0 (Python 2.7.12)
- OpenCV 2.4.13
- Numpy 
- Matplotlib
- PIL 

The algorithm was built and tested using windows 10 but it should work on either Linux or MacOS. The test footage we obtained was from using the lg 360 camera.

## How to use
1. In order to use the package first download the repo. 
2. Set up your environment with the required packages as specified above. 
3. Edit the parameter *fname="path_to_raw_video.mp4"* in the file main.py.
4. Run main.py using your python environment. The command will look something like *"python.exe C:\users\wkeu\Downloads\360-video-derotator\main.py"*
5. The resolution,length and framerate of the video will determine how long it takes to derotate your video. If using 4k video expect the deroation process to take a considerable amount of time.  
6. The algorithm will have finished running when the message *"Stabilised Video Outputted"* is displayed in your terminal. The video will be saved as "derotated_footage.avi" in you terminal current directory. 
*Note:* Depending on the rotational motion of the raw video it may be necessary to rerun the outputted video through the algorithm multiple times. See the accompanying thesis for more details on this.   

### Tuning
It is possible to experiment with the results of the video by varying the number of features point which are used to track the motion between frames. By default the parameter NUMBER_OF_POINTS is set to 50. The success of tuning this parameter will depend on both the amount of noise in your video and also the type of test footage. 

## Methodology
The methodology uses a rotationally-invariant algorithm to obtain feature points and descriptors for pairs of successive frames. This information is then abstracted into three-dimensional point clouds, from which the Kabsch algorithm can infer the rotational motion between frames. The resulting rotational matrices are used to remap each equirectangular frame to a reference frame, and thereby offset the effect of frame-to-frame camera rotations.

For more comprehensive details about the methodology please refer to the following:  
- IEEECON 2019 Publication ([link](https://researchrepository.ucd.ie/handle/10197/10985)) 
- Maters Thesis ([link](https://drive.google.com/file/d/1C_PAVe0sNiquvzk1Aolnvb1vl0BBU330/view?usp=sharing))

## Future Works
The following are items which are required to improve the quality of the repository. The small ticket items won't affect the performance of the algorithm but will make the repository more maintainable and user friendly. The big ticket items will require more work but will significantly improve the results and performance of the algorithm.  

### TODO (Small Ticket)
- [ ] Refactoring of main.py, get_xyz.py and rotate_map.py. They require modularisation to break the code up into more manageable/readable functions.
- [ ] Renaming of functions to have intuitive and consistent naming.  
- [ ] Addition of TODO: for areas which can be improved.  
- [ ] Removal of unused functions present in the code. 
- [ ] Improve functionality for outputting video in .mp4 format. 
- [ ] Add functionality for inputting raw video file directory into script via the command line. 

### TODO (Big Ticket)
- [ ] Porting to C#/C++. Specifically the image rotational functions as they are computationally heavy.
- [ ] Change software architecture to obtain rotational matrix from heavily downsampled video.
- [ ] Add scope for parallel computing to rotate multiple frames at the same time.
