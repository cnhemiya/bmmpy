# -*- coding: utf-8 -*-
"""
LICENSE  MulanPSL2
@author  cnhemiya@qq.com
@date    2024-11-12 19:30

@brief 图像处理，依赖 OpenCV。
"""


import numpy as np
import cv2
from typeguard import typechecked


@typechecked
def image_to_edges(image: np.ndarray, user_gray: bool = True, user_blur: bool = True,
                   ksize: int = 3, sigma: float = 1.0, canny_high: int = 50,
                   canny_low: int = 150) -> np.ndarray:
    """
    将图像转换为边缘图。
    此函数将输入的彩色或灰度图像转换为边缘检测结果图。
    可选地进行灰度化、高斯模糊处理，并使用 Canny 算法提取边缘。

    Args:
        image (np.ndarray): 输入图像，可以是彩色（3 通道）或灰度（1 通道）格式。
        user_gray (bool): 是否将输入图像转换为灰度图，默认为 True。
        user_blur (bool): 是否对图像进行高斯模糊处理，默认为 True。
        ksize (int): 高斯核大小，必须是奇数，默认为 3。
        sigma (float): 高斯核的标准差，默认为 1.0。
        canny_high (int): Canny 边缘检测的高阈值，默认为 50。
        canny_low (int): Canny 边缘检测的低阈值，默认为 150。

    Returns:
        np.ndarray: 输出的边缘图，类型为浮点型（float）。

    Raises:
        ValueError: 当输入图像不是有效的 numpy 数组或维度不符合要求时触发。
        TypeError: 当输入参数类型不正确时触发。

    Examples:
        >>> import numpy as np
        >>> img = np.random.rand(100, 100, 3)
        >>> edges = image_to_edges(img)
        >>> print(edges.shape)
        (100, 100)

    Note:
        输入图像的值应归一化至 [0, 1] 范围，若输入范围超出此区间，可能导致边缘检测不准确。
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


@typechecked
def image_to_edges_file(image_path: str, edges_path: str, user_gray: bool = True,
                        user_blur: bool = True, ksize: int = 3, sigma: float = 1.0,
                        canny_high: int = 50, canny_low: int = 150) -> None:
    """
    使用 OpenCV 获取图像的边缘图并保存到文件。

    Args:
        image_path (str): 输入的图像文件路径。
        edges_path (str): 输出的边缘图像文件路径。
        user_gray (bool, optional): 是否将图像转为灰度图。 默认为 True。
        user_blur (bool, optional): 是否对图像进行高斯模糊。 默认为 True。
        ksize (int, optional): 高斯模糊核的大小，必须是奇数。 默认为 3。
        sigma (float, optional): 高斯模糊的标准差。 默认为 1.0。
        canny_high (int, optional): Canny 边缘检测的高阈值。 默认为 50。
        canny_low (int, optional): Canny 边缘检测的低阈值。 默认为 150。

    Raises:
        ValueError: 如果无法读取图像文件或参数不合法。
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


@typechecked
def image_match(src_image: np.ndarray, match_image: np.ndarray, method: int = cv2.TM_CCOEFF_NORMED
                ) -> tuple[tuple[int, int], tuple[int, int]]:
    """
    使用 OpenCV 进行模板匹配。
    Args:
        src_image (numpy.ndarray): 源图像。
        match_image (numpy.ndarray): 要匹配的模板图像。
        method (int, optional): 模板匹配的方法。默认为 cv2.TM_CCOEFF_NORMED。
            可选方法包括：
            - 'cv.TM_CCOEFF'
            - 'cv.TM_CCOEFF_NORMED'
            - 'cv.TM_CCORR'
            - 'cv.TM_CCORR_NORMED'
            - 'cv.TM_SQDIFF'
            - 'cv.TM_SQDIFF_NORMED'
    Returns:
        tuple: 匹配结果的位置 (top_left, bottom_right)。
    Raises:
        ValueError: 当输入图像不符合要求时抛出。
        TypeError: 当参数类型不正确时抛出。
    Examples:
        >>> import cv2
        >>> import numpy as np
        >>> src = cv2.imread("source.png", 0)
        >>> template = cv2.imread("template.png", 0)
        >>> top_left, bottom_right = image_match(src, template)
    Note:
        输入图像必须是灰度图或单通道数组。
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


@typechecked
def image_match_file(src_path: str, match_path: str, method: int = cv2.TM_CCOEFF_NORMED
                     ) -> tuple[tuple[int, int], tuple[int, int]]:
    """
    使用 OpenCV 进行模板匹配。

    Args:
        src_path (str): 源图像文件路径。
        match_path (str): 要匹配的模板图像文件路径。
        method (int, optional): 模板匹配的方法。默认为 cv2.TM_CCOEFF_NORMED。
            支持的比较方法包括：
            - 'cv.TM_CCOEFF'
            - 'cv.TM_CCOEFF_NORMED'
            - 'cv.TM_CCORR'
            - 'cv.TM_CCORR_NORMED'
            - 'cv.TM_SQDIFF'
            - 'cv.TM_SQDIFF_NORMED'

    Returns:
        tuple: 匹配结果的位置 (top_left, bottom_right)，格式为 ((x, y), (x, y))。

    Raises:
        ValueError: 当图像文件无法读取时抛出异常。
        TypeError: 当输入参数类型不正确时抛出异常。

    Examples:
        >>> result = image_match_file("source.png", "template.png")
        >>> print(result)
        ((100, 200), (300, 400))

    Note:
        此函数依赖于 OpenCV 库，需确保已正确安装并导入。
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
