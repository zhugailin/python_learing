import cv2
import matplotlib
import matplotlib.pyplot as plt
from skimage.metrics import structural_similarity as ssim
import numpy as np
import pyrtools as pt
from scipy.fft import fft2, ifft2
from PIL import Image
from ssim import SSIM

import time
from scipy import signal


def preprocess(im, eq=False, int=False):
  eps = 1e-5
  # imf = fft2(im)
  # mag = np.abs(imf)
  imf = cv2.dft(np.float32(im),flags = cv2.DFT_COMPLEX_OUTPUT)
  mag = np.sqrt(np.square(imf[:, :, 0]) + np.square(imf[:, :, 1]))
  # imp = np.log(mag + eps)
  imp = 20 * np.log10(mag + eps) # convert to dB scale
  imp = cv2.equalizeHist(imp.astype(np.uint8)) if eq else imp
  imp = imp.astype(np.uint8) if int else imp
  return imp

def visualize(im):
  fig, axes = plt.subplots(1,2,sharex=True,sharey=True)
  imp = preprocess(im)
  im = axes[0].imshow(im, cmap="gray")
  plt.colorbar(im, ax=axes[0])
  im = axes[1].imshow(imp, cmap="gray")
  plt.colorbar(im, ax=axes[1])
  plt.show()
def dotprod(im1, im2):
  im1 = im1 / im1.sum()
  im2 = im2 / im2.sum()
  return (im1 * im2).sum()

def mae(im1, im2):
  res = np.abs(im1 - im2).mean()
  return res

def phase_corr(im1, im2):
  img1_fs = fft2(im1)
  img2_fs = fft2(im2)
  cross_power_spectrum = (img1_fs * img2_fs.conj()) / np.abs(img1_fs * img2_fs.conj())
  r = np.abs(np.fft.ifft2(cross_power_spectrum))
  return r[0, 0]

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
  c1c2_conj = np.zeros_like(imf1)  #想实现构造一个矩阵c1c2_conj，其维度与矩阵imf1一致，并为其初始化为全0；这个函数方便的构造了新矩阵
  cv2.mulSpectrums(imf1, imf2, 0, c1c2_conj, True) #两个傅立叶频谱的每个元素的乘法，输出数组和输入数组有相同的类型和大小。 
  # print(f"c1c2_conj ({c1c2_conj.dtype})= {c1c2_conj}")
  corr = uniform_filter(c1c2_conj, **fargs) #均值滤波
  varr = np.abs(imf1) ** 2 + np.abs(imf2) ** 2
  corr_band = uniform_filter(corr, **fargs)
  varr_band = uniform_filter(varr, **fargs)
  cssim_map = (2 * np.abs(corr_band) + K) / (varr_band + K)
  # num = 2 * np.abs(np.sum(c1c2_conj)) + K
  # denom = np.sum(np.square(np.abs(imf1))) + np.sum(np.square(np.abs(imf2))) + K
  # res = num / denom
  res = np.mean(cssim_map)
  return res

def gkern(height=7, width=7, std=3, scale=True):
    """Returns a 2D Gaussian kernel array."""
    gkernh = signal.gaussian(height, std=std).reshape(height, 1)
    gkernv = signal.gaussian(width, std=std).reshape(width, 1)
    gkern2d = np.outer(gkernh, gkernv)
    gkern2d = gkern2d / np.sum(gkern2d) * gkern2d.size if scale else gkern2d
    return gkern2d

def cw_ssim_index(im1, im2, height='auto', order=4):
  assert im1.shape == im2.shape, "im1.shape == im2.shape"
  K = 1e-5
  from scipy.ndimage import uniform_filter, gaussian_filter
  win_size = 7
  fargs = {'size': win_size}
  nrow, ncol = im1.shape
  pyr1 = pt.pyramids.SteerablePyramidFreq(im1, height=height, order=order, is_complex=True)
  pyr2 = pt.pyramids.SteerablePyramidFreq(im2, height=height, order=order, is_complex=True)
  level = pyr1.num_scales
  nori = pyr1.num_orientations 
  ssims = []
  
  def ssim_(band1, band2):
    corr = np.abs(band1 * band2.conj())
    varr = np.abs(band1) ** 2 + np.abs(band2) ** 2
    corr_band = uniform_filter(corr, **fargs)
    varr_band = uniform_filter(varr, **fargs)
    cssim_map = (2 * corr_band + K) / (varr_band + K)
    gauss_kern = gkern(height=corr.shape[0], width=corr.shape[1], std=np.max(corr.shape) / 4)
    cssim_map = cssim_map * gauss_kern
    res = np.mean(cssim_map)
    return res

  for i in range(level):
    for j in range(nori):
      band1 = pyr1.pyr_coeffs[(i, j)]
      band2 = pyr2.pyr_coeffs[(i, j)]
      ssims.append(ssim_(band1, band2))

  res = np.mean(ssims)
  return res

def compare(im1, im2):
  s = ssim(im1, im2, multichannel=False)
  ds = ssim(im1.astype(np.float32) * 2, im2.astype(np.float32) * 2, multichannel=False)
  dp=dotprod(im1, im2)
  m=mae(im1, im2)
  pc=phase_corr(im1, im2)

  sp=ssim(preprocess(im1), preprocess(im2), multichannel=False)
  dpp=dotprod(preprocess(im1), preprocess(im2))
  mp=mae(preprocess(im1), preprocess(im2))
  pcp=phase_corr(preprocess(im1), preprocess(im2))

  im1_im = Image.fromarray(im1)
  im2_im = Image.fromarray(im2)
  # cw_ssim = SSIM(im1_im).cw_ssim_value(im2_im)
  cw_ssim = cw_ssim_index(im1, im2)
  f_ssim = fourier_ssim(im1, im2)
  print(f"SSIM between im1 and im2 is {s}")
  print(f"double SSIM between im1 and im2 is {ds}")
  print(f"dotprod between im1 and im2 is {dp}")
  print(f"MAE between im1 and im2 is {m}")
  print(f"phase corr between im1 and im2 is {pc}")
  print(f"with preprocess:")
  print(f"SSIM between im1 and im2 w/ preprocess is {sp}")
  print(f"dotprod w/ preprocess between im1 and im2 is {dpp}")
  print(f"MAE w/ preprocess between im1 and im2 is {mp}")
  print(f"phase corr w/ preprocess between im1 and im2 is {pcp}")
  score = (s + sp + pc) / 3
  print(f"ensemble (s, sp, pc) similarity is {score}")
  score = (s + sp + pc + pcp) / 4
  print(f"ensemble (s, sp, pc, pcp) similarity is {score}")
  print(f"CW-SSIM between im1 and im2 is {cw_ssim}")
  print(f"Fourier-SSIM between im1 and im2 is {f_ssim}")
  
im = cv2.imread('/data/home/zgl/Github/python_learing/000.jpg', cv2.IMREAD_GRAYSCALE)
im0 = cv2.imread('/data/home/zgl/Github/python_learing/001.jpg', cv2.IMREAD_GRAYSCALE)
compare(im, im0)