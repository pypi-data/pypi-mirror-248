Supported OS’s - Windows 10 (64-bit), Windows 8.1 (64-bit)

[e-con opencv] (https://github.com/econsystems/opencv/tree/v1.0.4)

Replace the "cv2.cp36-win32" file to "PYTHON_INSTALLED_PATH\Lib\site-packages\cv2\” 
 with the folder downloaded from the https://github.com/econsystems/opencv/tree/v1.0.4 
pyd and dll files are found in this downloaded (v1.0.4/Binary/Opencv_4.5.5/Windows/x64) path.

Pre-requisite-
Download all the dll and pyd from the above GIT link.
1.	Python – 3.10.
2.	OpenCV – pip install opencv-python==4.5.5.62 (Need to replace the e-con OpenCV.pyd and rename to cv2.pyd, rename the general OpenCV as any other name, opencv_videoio_ffmpeg455_64.dll, opencv_world455.dll and copy eCAMFwSw.dll in the OpenCV installed path).
3.	Pretty table – pip install prettytable==3.8.0.
4.	HID – pip install hidapi==0.13.1.
5.	Numpy – pip install numpy==1.24.3.

Using Camera API
	This API is provided with a set of features that can be used to test the functionality of cameras.

get_devices
	get_devices API is used to get the connected camera names and nodes. Using the camera nodes user can open and accessing the camera.
	
Syntax- Camera_API.get_devices()

Example –
	from camera_API import Camera_API
Camera_API.get_devices()

Output-
	0: Integrated Camera
1: See3CAM_CU55
Here,
0 – refers to connected node
1 – refers to camera name.

open_camera
	open_camera API is used to open the camera using the node. Once open the camera then only user able to access the camera.

Syntax- Camera_API.open_camera(node)

Example –
	from camera_API import Camera_API
	Camera_API.open_camera(1)

Output-
	Object – It assigned the camera.
Error- 
	Error code: 101 Camera not found.

get_device_path
	get_device_path is used to getting the path of the camera, It is unique for the connected camera. Using the node user get the device path.

Syntax- Camera_API.get_device_path(node)

Example –
	from camera_API import Camera_API
	Camera_API.open_camera(1)
	Camera_API.get_device_path(1)
Output-
	\\?\usb#vid_2560&pid_c154&mi_00#6&686f1de&6&0000#{65e8773d-8f56-11d0-a3b9-00a0c9223196}\global


get_VID
	get_VID is used to getting the Vendor ID of the camera. Using the node get the vendor ID its only for e-con cameras.

Syntax- Camera_API.get_VID(node)

Example –
	from camera_API import Camera_API
Camera_API.open_camera(1)
Camera_API.get_VID (1)
Output-
	2560

get_PID
	get_PID is used to getting the product ID of the camera. Using the node get the product ID its only for e-con cameras. Product ID may vary for different camera models.

Syntax- Camera_API.get_PID(node)

Example –
	from camera_API import Camera_API
Camera_API.open_camera(1)
Camera_API.get_PID (1)
Output-
	c154

get_firmware_version
	get_firmware_version is used to getting the firmware version of the e-con camera. Using the HID commands get the firmware version of the camera.

Syntax- get_firmware_version(node)

Example –
	from camera_API import Camera_API
Camera_API.open_camera(1)
Camera_API.get_firmware_version(1)
Output-
	Firmware version : 1.11.131.2051

getting_unique_ID
	getting_unique_ID is ised to getting the serial number of the e-con camera. Using the HID commands get the unique ID of the camera.

Syntax- getting_unique_ID(node)

Example –
	from camera_API import Camera_API
Camera_API.open_camera(1)
Camera_API. getting_unique_ID(1)
Output-
	Serial Number: 09128306



get_resolution
	get_resolution is used to getting the supported resolutions, formats and FPS of the give node. Output will be the list data type it returns all the supported resolutions.

Syntax- camera_accessing_api.get_resolution(node)

Example –
	from camera_API import Camera_API
Camera_API.open_camera(1)
camera_accessing_api.get_resolution(1)
Output-
	[('UYVY', 1920, 1080, 30), ('UYVY', 1920, 1080, 15), ('UYVY', 640, 480, 60), ('UYVY', 640, 480, 45), ('UYVY', 960, 540, 58), ('UYVY', 960, 540, 30), ('UYVY', 1280, 960, 34), ('UYVY', 1280, 960, 23), ('UYVY', 1280, 720, 45), ('UYVY', 1280, 720, 30)]

getting_supported_uvc_parameter
	getting_supported_uvc_parameter is used to getting the supported UVC parameters along with the minimum, maximum, step, current values, and supported modes. Output will be the dict data type it returns all the supported UVC parameters.


Syntax- camera_accessing_api.getting_supported_uvc_parameter(node)

Example –
	from camera_API import Camera_API
Camera_API.open_camera(1)
camera_accessing_api.getting_supported_uvc_parameter(1)
Output-
	{'brightness': [1, 5, 1, 2, 2, 2, 2], 'contrast': [1, 10, 1, 3, 3, 2, 2], 'saturation': [1, 10, 1, 6, 6, 2, 2], 'gain': [1, 63, 1, 5, 5, 2, 2], 'exposure': [-10, -1, 1, -5, -5, 1, 3], 'white_balance_blue_u': [2500, 6000, 50, 4500, 4500, 1, 3], 'sharpness': [1, 10, 1, 5, 5, 2, 2], 'pan': [-180, 180, 1, 0, 0, 2, 2], 'tilt': [-180, 180, 1, 0, 0, 2, 2]}

set_resolution
	set_resolution is used to set the resolution in the camera, it requires the arguments height, width, format, and FPS of the resolution. Output will be the bool data type, it returns True/ None. 

Syntax- camera_accessing_api.set_resolution(node, height, width, Format, FPS)

Example –
	from camera_API import Camera_API
Camera_API.open_camera(1)
Camera_API.set_resolution(1,640, 480, UYVY, 60)
Output-
	True

streaming
	streaming is used to show the preview for the given duration, if you are not giving the duration it streaming continuously. Duration and show FPS are not mandatory. By default, show_FPS is disabled. Duration is represented in seconds.

Syntax-camera_accessing_api.streaming(node, duration, show_FPS)	

Example –
	from camera_API import Camera_API
Camera_API.open_camera(1)
Camera_API.streaming(1, 20, True)

Output-
	It will show the streaming for 20 seconds and show the FPS in top left corner of the preview.

uvc_var
	uvc_var is used to varying the given UVC parameter for the given minimum, maximum and step value and if user required able to save the image in the given image formats. hold is used to hold the applied value for the given hold time in seconds. 

Syntax- uvc_var(node, parameter_name, min, max, step, hold, image_save, save_format)

Example –
	from camera_API import Camera_API
Camera_API.open_camera(1)
Camera_API.streaming(1, 20, True)
Camera_API. uvc_var(1, “brightness, -15, 15, 3, 2, True, 'bmp')
Output- 
	It will be varying the brightness for given node -15 to 15 with step size of 3 and save the image “brightness_-15.bmp” and so on.
