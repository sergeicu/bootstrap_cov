# NB this is not wildbootstrap. We simply add noise to 4D image based on SNR level N times. 
# to see wild bootstrap example - https://github.com/sergeicu/wild_bootstrap_adc
# best explanation of wild bootstrap - https://stats.stackexchange.com/questions/408651/intuitively-how-does-the-wild-bootstrap-work


import os
import argparse

import numpy as np
import nibabel as nb


def load_args():
    parser = argparse.ArgumentParser(description="Load arguments for processing 4D nifti files.")
    parser.add_argument("--nifti", help="4D nifti filename")
    parser.add_argument("--snr", type=float, help="SNR is required for bootstrap calculation. Please provide as dB")
    parser.add_argument("--iterations", type=int, help="Number of wild bootstrap iterations to perform. ")
    parser.add_argument("--seg", default=None, help="3D segmentation filename - bootstrap will only be computed over masked region. If not defined - bootstrap over entire region")

    parser.add_argument("--savedir", help="Save directory")
    

    args = parser.parse_args()

    return args
    

if __name__ == '__main__':
    
    
    args = load_args()
    niftipath = args.nifti
    segfilename=args.seg
    savedir=args.savedir + "/"
    iterations = args.iterations
    

    ####################################
    # load data and params 
    ####################################
    
 
    # Get params 
    nii_basename = os.path.basename(niftipath).replace(".nii.gz", "_") # assumes that files will be name as svr.nii.gz or vol.nii.gz

    # load nifti 
    assert os.path.exists(niftipath)
    imo = nb.load(niftipath)
    data = imo.get_fdata()
    assert data.ndim == 4, f"Must be a 4D file"
    x,y,z,t = data.shape
    
    # load mask 
    if segfilename is not None:
        assert os.path.exists(segfilename)
        seg = nb.load(segfilename).get_fdata()    
    else: 
        seg = np.ones((x,y,z))
        nb.save(nb.Nifti1Image(seg,header=imo.header, affine=imo.affine), "seg_generated.nii.gz")
    assert data.shape[:-1] == seg.shape
    
    seg_4D = np.tile(np.expand_dims(seg,-1), (1,1,1,t))

    ####################################
    # Add Noise 
    ####################################
    


    os.makedirs(savedir,exist_ok=True)
    
    # random swap of residuals (with permutation)
    for i in range(iterations):

        # Generate noise with the calculated noise power for the given SNR ratio
        noise = np.random.normal(0, np.sqrt(args.snr), data.shape)

        # Add noise to the original signal for the SNR ratio case
        data_n = data + noise
        
        # mask areas         
        data_n[seg_4D==0] = 0
        
        imonew_dwi = nb.Nifti1Image(data_n, affine=imo.affine,header=imo.header)
        savename = savedir + nii_basename + "_bs" + str(i).zfill(4) + ".nii.gz"
        nb.save(imonew_dwi,savename)
        
        print(f"{i}:{iterations-1}")
        
        
    print(f"Images saved to: {savedir}")
    
