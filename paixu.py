# ''' 冒泡排序
# * Reference: 
# *	http://en.wikipedia.org/wiki/Bubble_sort
# *	https://github.com/xtaci/algorithms/blob/master/include/bubble_sort.h
# *   https://zhuanlan.zhihu.com/p/37077924
# *
# * 冒泡排序说明：比较相邻的两个元素，将值大的元素交换到右边（降序则相反）
# *
# '''
# def BubbleSort(array):
#     lengths = len(array)
#     for i in range(lengths-1):
#         for j in range(lengths-1-i):
#             if array[j] > array[j+1]:
#                array[j+1], array[j] = array[j], array[j+1]

#     return array


# array = [1,3,8,5,2,10,7,16,7,4,5]
# print("Original array: ", array)
# array = BubbleSort(array)
# print("BubbleSort: ", array)
import cv2
import numpy as np
def fourier_ssim(im1, im2):
  K = 1e-5
  # imf1 = fft2(im1)
  # imf2 = fft2(im2)
  # num = 2 * np.abs(np.sum(imf1 * np.conj(imf2))) + K
  # denom = np.sum(np.square(np.abs(imf1))) + np.sum(np.square(np.abs(imf2))) + K  
  from scipy.ndimage import uniform_filter, gaussian_filter
  win_size = 7
  fargs = {'size': win_size}
  
  imf1 = cv2.dft(np.float32(im1),flags = cv2.DFT_COMPLEX_OUTPUT)
  imf2 = cv2.dft(np.float32(im2),flags = cv2.DFT_COMPLEX_OUTPUT)
  c1c2_conj = np.zeros_like(imf1)
  cv2.mulSpectrums(imf1, imf2, 0, c1c2_conj, True)
  # print(f"c1c2_conj ({c1c2_conj.dtype})= {c1c2_conj}")
  corr = uniform_filter(c1c2_conj, **fargs)
  varr = np.abs(imf1) ** 2 + np.abs(imf2) ** 2
  corr_band = uniform_filter(corr, **fargs)
  varr_band = uniform_filter(varr, **fargs)
  cssim_map = (2 * np.abs(corr_band) + K) / (varr_band + K)
  # num = 2 * np.abs(np.sum(c1c2_conj)) + K
  # denom = np.sum(np.square(np.abs(imf1))) + np.sum(np.square(np.abs(imf2))) + K
  # res = num / denom
  res = np.mean(cssim_map)
  return res