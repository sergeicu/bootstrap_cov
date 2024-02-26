import sys 
import os 

import nibabel as nb 
import numpy as np 



if __name__=="__main__":
    file = sys.argv[1]

    os.path.exists(file)

    imo = nb.load(file)
    im = imo.get_fdata()
    assert im.ndim ==4 

    newimo = nb.Nifti1Image(im[:,:,:,0], affine=imo.affine, header=imo.header)
    nb.save(newimo, file.replace(".nii.gz", "_est_parameter.nii.gz"))
