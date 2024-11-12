# -*- coding: utf-8 -*-
"""
LICENSE  MulanPSL2
@author  cnhemiya@qq.com
@date    2024-11-12 19:30

@brief 图像处理，依赖 OpenCV。
"""


import numpy as np
import cv2


def image_to_edges(image: np.ndarray, user_gray=True, user_blur=True,
                   ksize=3, sigma=1.0, canny_high=80, canny_low=240) -> np.ndarray:
    """
    使用 OpenCV 获取图像的边缘图并返回边缘图。

    Args:
        image (numpy.ndarray): 输入的图像.
        user_gray (bool, optional): 是否将图像转为灰度图. 默认为 True.
        user_blur (bool, optional): 是否对图像进行高斯模糊. 默认为 True.
        ksize (int, optional): 高斯模糊核的大小，必须是奇数. 默认为 3.
        sigma (float, optional): 高斯模糊的标准差. 默认为 1.0.
        canny_high (int, optional): Canny 边缘检测的高阈值. 默认为 80.
        canny_low (int, optional): Canny 边缘检测的低阈值. 默认为 240.

    Returns:
        numpy.ndarray: 输出的边缘图像.
    """
    # 转为灰度图
    if user_gray:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 高斯模糊
    if user_blur:
        image = cv2.GaussianBlur(image, (ksize, ksize), sigma)

    # Canny 边缘检测
    edges = cv2.Canny(image, canny_low, canny_high)

    return edges


def image_to_edges_file(image_path: str, edges_path: str, user_gray=True, user_blur=True,
                        ksize=3, sigma=1.0, canny_high=80, canny_low=240):
    """
    使用 OpenCV 获取图像的边缘图并保存到文件。

    Args:
        image_path (str): 输入的图像文件路径。
        edges_path (str): 输出的边缘图像文件路径。
        user_gray (bool, optional): 是否将图像转为灰度图。 默认为 True。
        user_blur (bool, optional): 是否对图像进行高斯模糊。 默认为 True。
        ksize (int, optional): 高斯模糊核的大小，必须是奇数。 默认为 3。
        sigma (float, optional): 高斯模糊的标准差。 默认为 1。0。
        canny_high (int, optional): Canny 边缘检测的高阈值。 默认为 80。
        canny_low (int, optional): Canny 边缘检测的低阈值。 默认为 240。

    Raises:
        ValueError: 如果无法读取图像文件。
    """
    # 读取图像
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"无法读取图像文件: {image_path}")

    # 获取边缘图
    edges = image_to_edges(image, user_gray, user_blur,
                           ksize, sigma, canny_high, canny_low)

    # 保存边缘图
    cv2.imwrite(edges_path, edges)


def image_match(src_image: np.ndarray, match_image: np.ndarray, method=cv2.TM_CCOEFF_NORMED):
    """
    使用 OpenCV 进行模板匹配。

    Args:
        src_image (numpy.ndarray): 源图像。
        match_image (numpy.ndarray): 要匹配的模板图像。
        method (int, optional): 模板匹配的方法。默认为 cv2.TM_CCOEFF_NORMED。
            method 的6种比较方法 = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 
            'cv.TM_CCORR', 'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']

    Returns:
        tuple: 匹配结果的位置 (top_left, bottom_right)。
    """
    # 获取模板图像的宽度和高度
    h, w = match_image.shape[:2]

    # 进行模板匹配
    result = cv2.matchTemplate(src_image, match_image, method)

    # 获取匹配位置
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # 根据匹配方法确定匹配位置
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        top_left = max_loc

    bottom_right = (top_left[0] + w, top_left[1] + h)

    return top_left, bottom_right


def image_match_file(src_path: str, match_path: str, method=cv2.TM_CCOEFF_NORMED):
    """
    使用 OpenCV 进行模板匹配。

    Args:
        src_path (str): 源图像文件路径。
        match_path (str): 要匹配的模板图像文件路径。
        method (int, optional): 模板匹配的方法。默认为 cv2.TM_CCOEFF_NORMED。
            method 的6种比较方法 = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 
            'cv.TM_CCORR', 'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']

    Returns:
        tuple: 匹配结果的位置 (top_left, bottom_right)。
    """
    # 读取源图像和模板图像
    src_image = cv2.imread(src_path, cv2.IMREAD_COLOR)
    match_image = cv2.imread(match_path, cv2.IMREAD_COLOR)

    if src_image is None or match_image is None:
        raise ValueError("无法读取图像文件")

    # 获取模板图像的宽度和高度
    h, w = match_image.shape[:2]

    # 进行模板匹配
    result = cv2.matchTemplate(src_image, match_image, method)

    # 获取匹配位置
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # 根据匹配方法确定匹配位置
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        top_left = max_loc

    bottom_right = (top_left[0] + w, top_left[1] + h)

    return top_left, bottom_right
