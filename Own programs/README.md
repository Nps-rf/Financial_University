<img src="https://cdn0.iconfinder.com/data/icons/azure-illustrations/1000/support___question_faq_list_frequently_asked_questions_question_mark_information_info-512.png" align="right" width="404px"/>  

# FrucWrapper 

### Languages and Tools
[<img align="left" width="30px" src="https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/python/python.png"/>][Python]
[<img align="left" width="40px" src="https://etu.ru/assets/cache/images/ru/povyshenie-kvalifikacii/programmy%20povysheniya%20kvalifikacii/1280x800-cplusplus.947.png"/>][C++]
[<img align="left" width="25px" src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/32/OpenCV_Logo_with_text_svg_version.svg/1200px-OpenCV_Logo_with_text_svg_version.svg.png"/>][OpenCV]
[<img align="left" width="33px" src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Breezeicons-apps-48-cmake.svg/1200px-Breezeicons-apps-48-cmake.svg.png"/>][Cmake]

<br />

### Build
### If you use [OpenCV](https://github.com/opencv/opencv)
* `git clone https://github.com/opencv/opencv`
  * `mkdir build`
  * `cd build`
  * `cmake ..`
  * `cmake --build`

#### Then
  * `mkdir build`
  * `cd build`

#### ⚠ **Commands for [OpenCV](https://github.com/opencv/opencv)** ⚠
* `cmake .. -DOPENCV_BUILD=ON -DOpenCV_DIR='opencv_build folder'`
* `else: cmake ..`
* `cmake --build`

### Info

#### Beginning

**There is a wrapper manager that is responsible for creating and deleting objects from memory.**
* `wrapper = FrucWrapperManager()`

**There are 3 main algorithms:**
1) **Do motion estimation**
   1) **First you need to create settings** ⚒
      1) `settings = MotionSettings(frame_width, frame_height, color_space)`
      2) `motion_estimation_unstance = wrapper.create_motion_estimator(settings)`
      3) `motion_vectors = motion_estimation_instance(Image_1, Image_2, motion_vectors from previos estimation = Optional`
2) **Block erosion ❌**
3) **TDRS algorithm which includes in do motion estimation (In one direction)**

#### Visualize vectors
* `vectors_on_image = visualize_vector_field(motion_vectors, rgbl_resized4x)`
* `cv2.imwrite(os.path.join(output_directory, "meerkat_0_1_do_me.png"), vectors_on_image)`

#### UnitTests
* `python unittests/test.py`


[OpenCV]: https://github.com/opencv/opencv
[Cmake]: https://cmake.org/
[Python]: https://www.python.org/
[C++]: https://docs.microsoft.com/en-us/cpp/cpp/?view=msvc-160
