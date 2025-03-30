""" 
Sinogram to Image Reconstruction
Original code source: https://github.com/IanB14/Sinogram-to-Image.git 
Modified for manufacturing defect detection
"""

## Imports
import numpy as np
import imutils
from skimage.transform import rotate  ## Image rotation routine
import scipy.fftpack as fft  ## Fast Fourier Transform
import scipy.misc  ## Contains a package to save numpy arrays as .PNG
import imageio
import matplotlib.pyplot as plt

## Methods
def radon(image, steps):
    """
    Radon transform method - turns an image into a sinogram
    (Not used for reconstruction - this is how the original sinogram was generated)
    
    Args:
        image: Input image to transform
        steps: Number of angular projections
        
    Returns:
        Sinogram (2D array of projections)
    """
    projections = []  ## Accumulate projections in a list.
    dTheta = -180.0 / steps  ## Angle increment for rotations.
    
    for i in range(steps):
        projections.append(rotate(image, i*dTheta).sum(axis=0))
    
    return np.vstack(projections)  # Return the projections as a sinogram

def fft_translate(projs):
    """
    Translate the sinogram to the frequency domain using Fourier Transform
    
    Args:
        projs: Input projections (sinogram)
        
    Returns:
        1-d FFTs of projections
    """
    # Build 1-d FFTs of an array of projections, each projection 1 row of the array.
    return fft.rfft(projs, axis=1)

def ramp_filter(ffts):
    """
    Ramp filter a 2-d array of 1-d FFTs (1-d FFTs along the rows).
    
    Args:
        ffts: Input frequency domain data
        
    Returns:
        Ramp filtered frequency domain data
    """
    ramp = np.floor(np.arange(0.5, ffts.shape[1]//2 + 0.1, 0.5))
    return ffts * ramp

def inverse_fft_translate(operator):
    """
    Perform inverse FFT on frequency domain data
    
    Args:
        operator: Input frequency domain data
        
    Returns:
        Spatial domain data
    """
    return fft.irfft(operator, axis=1)

def back_project(operator):
    """
    Back-projection function to reconstruct image from projections
    
    Args:
        operator: Input projections (sinogram)
        
    Returns:
        Reconstructed image
    """
    laminogram = np.zeros((operator.shape[1], operator.shape[1]))
    dTheta = 180.0 / operator.shape[0]
    
    for i in range(operator.shape[0]):
        temp = np.tile(operator[i], (operator.shape[1], 1))
        temp = rotate(temp, dTheta*i)
        laminogram += temp
        
    return laminogram

## Main function
def main():
    """
    Main function to run the sinogram reconstruction
    """
    ## 시노그램 이미지 로딩.
    ## 출처: https://github.com/IanB14/Sinogram-to-Image/blob/master/Images/originalSinogramImage.png?raw=true
    try:
        sinogram = imageio.imread('sinog.png')
    except FileNotFoundError:
        print("Error: 'sinog.png' file not found. Please ensure the sinogram image is in the same directory.")
        return
    
    ## 원본 시노그램 표시
    plt.figure(figsize=(10, 8))
    plt.imshow(sinogram)
    plt.title("Original Sinogram")
    plt.colorbar()
    plt.show()
    
    ## 필터링 없는 백프로젝션 복원
    unfiltered_reconstruction = back_project(sinogram)
    
    plt.figure(figsize=(10, 8))
    plt.imshow(unfiltered_reconstruction)
    plt.title("Reconstruction with no filtering")
    plt.colorbar()
    plt.show()
    
    ## 시노그램의 1차원 진폭스펙트럼
    frequency_domain_sinogram = fft_translate(sinogram)
    
    plt.figure(figsize=(10, 8))
    plt.imshow(np.log(np.abs(frequency_domain_sinogram) + 1))  # Log scale for better visualization
    plt.title("Frequency Domain representation of sinogram")
    plt.colorbar()
    plt.show()
    
    ## 램프 필터링된 1차원 진폭 스펙트럼
    filtered_frequency_domain_sinogram = ramp_filter(frequency_domain_sinogram)
    
    plt.figure(figsize=(10, 8))
    plt.imshow(np.log(np.abs(filtered_frequency_domain_sinogram) + 1))  # Log scale for better visualization
    plt.title("Frequency domain projections multiplied with a ramp filter")
    plt.colorbar()
    plt.show()
    
    ## 1차원 역푸리에변환
    filtered_spatial_domain_sinogram = inverse_fft_translate(filtered_frequency_domain_sinogram)
    
    plt.figure(figsize=(10, 8))
    plt.imshow(filtered_spatial_domain_sinogram)
    plt.title("Spatial domain representation of ramp filtered sinogram")
    plt.colorbar()
    plt.show()
    
    ## 백프로젝션 복원
    reconstructed_image = back_project(filtered_spatial_domain_sinogram)
    
    plt.figure(figsize=(10, 8))
    plt.imshow(reconstructed_image)
    plt.title("Original, reconstructed image")
    plt.colorbar()
    plt.show()
    
    ## 해밍윈도우를 씌워 램프 필터링
    if reconstructed_image.shape[0] == reconstructed_image.shape[1]:
        window = np.hamming(reconstructed_image.shape[0])
        window_2d = np.outer(window, window)
        hamming = reconstructed_image * window_2d
    else:
        window = np.hamming(566)  # Original code used 566, update this if needed
        hamming = reconstructed_image * window
    
    plt.figure(figsize=(10, 8))
    plt.imshow(hamming)
    plt.title("Hamming-Windowed reconstructed image")
    plt.colorbar()
    plt.show()
    
    # Save the reconstructed images
    imageio.imwrite('reconstructed_no_filter.png', normalize_image(unfiltered_reconstruction))
    imageio.imwrite('reconstructed_with_filter.png', normalize_image(reconstructed_image))
    imageio.imwrite('reconstructed_with_hamming.png', normalize_image(hamming))
    
    print("Reconstruction complete. Images saved.")

def normalize_image(img):
    """
    Normalize image to 0-255 range for saving
    
    Args:
        img: Input image
        
    Returns:
        Normalized image
    """
    norm_img = ((img - img.min()) * 255 / (img.max() - img.min())).astype(np.uint8)
    return norm_img

if __name__ == "__main__":
    main()
