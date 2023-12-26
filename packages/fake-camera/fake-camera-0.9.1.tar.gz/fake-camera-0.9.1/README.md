**Code Example**:

``` python
import time
import cv2 as cv
from fake_camera import FakeCamera  # import the class

fake_cam_object = FakeCamera().add_foreground_image().add_background_image().build() # create an instance of the fake camera class
# fake_cam_object = FakeCamera().add_foreground_image().add_background_image().add_flip_to_feed().build() # add a random flip to the image
# fake_cam_object = FakeCamera().add_foreground_image().add_background_image().add_noise().build() # add noise to the image


while True:
       snapshot = fake_cam_object.get_snapshot()   #get the next fake snapshot from from the fake camera
       cv.imshow("Moving Image", snapshot)
       time.sleep(1/10)
       if cv.waitKey(1) & 0xFF == ord("q"):
           break
```
