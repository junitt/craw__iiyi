import cv2
import numpy as np
threshold_blue = 55  # 蓝色通道阈值
threshold_green = 30  # 绿色通道阈值
threshold_red = 20  # 红色通道阈值

def erode_img(img):
    kernel = np.ones((3, 3), np.uint8) 
    eroded_image = cv2.erode(img, kernel)
    return eroded_image

def img_proc(id):#66223
    image1 = cv2.imread(f".\\src\\ver_img\\{id}.png")
    if image1 is None :
        return 
    image1_resize=image1
    # image1_resize = cv2.resize(image1, (340, 212))
    image2 = cv2.imread("./src/chart.png")#滑块
    image2_resize=image2
    # image2_resize = cv2.resize(image2, (68, 68))

    # 处理图像，保留大部分白色
    # ret, thresholded_image = cv2.threshold(image1_resize, 20, 255, cv2.THRESH_BINARY)
    _, binary_blue = cv2.threshold(image1_resize[:, :, 0], threshold_blue, 255, cv2.THRESH_BINARY)
    _, binary_green = cv2.threshold(image1_resize[:, :, 1], threshold_green, 255, cv2.THRESH_BINARY)
    _, binary_red = cv2.threshold(image1_resize[:, :, 2], threshold_red, 255, cv2.THRESH_BINARY)
    # cv2.imshow('raw image',image1_resize)
    # cv2.imshow('blue image',binary_blue)
    # cv2.imshow('red image',binary_red)
    # cv2.imshow('green image',binary_green)
    # cv2.waitKey(0)
    # gray_image1 = cv2.cvtColor(thresholded_image, cv2.COLOR_BGR2GRAY)
    denoised_image1=erode_img(binary_blue)
    # denoised_image1 = cv2.equalizeHist(binary_blue)
    # 边缘检测
    edges = cv2.Canny(denoised_image1, threshold1=500, threshold2=900)
    _, binary_green = cv2.threshold(image2_resize[:, :, 1], 200, 255, cv2.THRESH_BINARY)
    # cv2.imshow("denoised_image2", binary_green)
    # cv2.imshow('blue image',binary_blue)
    # cv2.waitKey(0)
    # 滑块图片
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

    # 在输入图像上绘制矩形标记
    cv2.rectangle(image1_resize, top_left2, bottom_right2, (0, 0, 255), 2)
    # cv2.imshow("denoised_image2", denoised_image2)
    # cv2.imshow("edges2", edges2)
    # cv2.imshow("denoised_image1", denoised_image1)
    # cv2.imshow("edges", edges)
    # cv2.imshow('Target Image', image1_resize)
    # cv2.waitKey(0)
    cv2.imwrite(f".\\src\\output\\{id}.png", image1_resize)
# img_proc(66171)
for i in range(66000,66100,1):
    img_proc(i)
