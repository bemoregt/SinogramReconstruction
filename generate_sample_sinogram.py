"""
Generate a sample sinogram for testing the reconstruction code
"""

import numpy as np
import imageio
import matplotlib.pyplot as plt
from skimage.data import shepp_logan_phantom
from skimage.transform import radon

def create_sample_sinogram():
    """
    Create a sample sinogram from the Shepp-Logan phantom
    """
    # Create a test phantom image
    phantom = shepp_logan_phantom()
    
    # Display the phantom
    plt.figure(figsize=(8, 8))
    plt.imshow(phantom, cmap=plt.cm.Greys_r)
    plt.title('Shepp-Logan Phantom')
    plt.colorbar()
    plt.savefig('phantom.png')
    plt.show()
    
    # Create a sinogram using the radon transform
    theta = np.linspace(0., 180., 180, endpoint=False)
    sinogram = radon(phantom, theta=theta)
    
    # Display the sinogram
    plt.figure(figsize=(10, 8))
    plt.imshow(sinogram, cmap=plt.cm.Greys_r,
               extent=(0, 180, 0, sinogram.shape[0]), aspect='auto')
    plt.title('Radon transform (Sinogram)')
    plt.xlabel('Projection angle (deg)')
    plt.ylabel('Projection position (pixels)')
    plt.colorbar()
    plt.savefig('sinogram.png')
    plt.show()
    
    # Save the sinogram as a PNG image
    sinogram_normalized = (sinogram - sinogram.min()) / (sinogram.max() - sinogram.min()) * 255
    imageio.imwrite('sinog.png', sinogram_normalized.astype(np.uint8))
    
    print("Sample sinogram created and saved as 'sinog.png'")
    print("Use this with the sinogram_reconstruction.py script")

if __name__ == "__main__":
    create_sample_sinogram()
