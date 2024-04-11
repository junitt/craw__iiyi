import cv2
import numpy as np

# threshold_red = 20  # 红色通道阈值


class detector:
    def __init__(self):
        self.image2=cv2.imread("./src/chart.png")
        self.threshold_blue = 55  # 蓝色通道阈值
        self.threshold_green = 30  # 绿色通道阈值
    def erode_img(self,img):
        kernel = np.ones((3, 3), np.uint8) 
        eroded_image = cv2.erode(img, kernel)
        return eroded_image
    def detect(self,img_rt):
        image1_resize = cv2.imread(img_rt)
        if image1_resize is None :
            return 
        image2 = self.image2#滑块
        image2_resize=image2

        _, binary_blue = cv2.threshold(image1_resize[:, :, 0], self.threshold_blue, 255, cv2.THRESH_BINARY)
        denoised_image1=self.erode_img(binary_blue)
        # 边缘检测
        edges = cv2.Canny(denoised_image1, threshold1=500, threshold2=900)
        _, binary_green = cv2.threshold(image2_resize[:, :, 1], 200, 255, cv2.THRESH_BINARY)
        gray_image2 = cv2.cvtColor(image2_resize, cv2.COLOR_BGR2GRAY)
        denoised_image2 = cv2.equalizeHist(gray_image2)
        # print(denoised_image2)
        denoised_image2 = cv2.GaussianBlur(denoised_image2, (3, 3), 0)
        edges2 = cv2.Canny(denoised_image2, threshold1=100, threshold2=200)

        # 进行形状匹配
        result = cv2.matchTemplate(binary_blue, binary_green, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        top_left2 = max_loc
        bottom_right2 = (top_left2[0] + edges2.shape[1], top_left2[1] + edges2.shape[0])
        # cv2.rectangle(image1_resize, top_left2, bottom_right2, (0, 0, 255), 2)
        # cv2.imshow("good",image1_resize)
        # cv2.waitKey(0)
        return (top_left2[0]+bottom_right2[0])/2,image1_resize.shape[1],edges2.shape[1]
    
    def get_distance(self,img_rt):
        dis,big_x,small_x=self.detect(img_rt)
        return (dis-small_x/2)