

# install 
python -m venv venv 
source venv/bin/activate
pip install -r requirements.txt 

########################################
# add noise (bootstrap)
########################################

source venv/bin/activate
python bootstrap.py --nifti example.nii.gz --iterations 10 --savedir output --snr 20

# NB this is not wildbootstrap. We simply add noise to 4D image based on SNR level N times. 
# for wild bootstrap we require multiple measurements of the same data. 
# to see code for wild bootstrap example - https://github.com/sergeicu/wild_bootstrap_adc
# best explanation of wild bootstrap - https://stats.stackexchange.com/questions/408651/intuitively-how-does-the-wild-bootstrap-work

########################################
# calculate metrics for every 4D file
########################################
for f in output/example__bs[0-9][0-9][0-9][0-9].nii.gz 
do
    echo $f
    python dummy_estimate_parameters.py $f
done 

# NB we use a dummy model here - INSERT YOUR PARAMETER ESTIMATION MODEL IN THIS PYTHON CODE


########################################
# calculate CoV
########################################

# run Coefficient_of_Variation.ipynb notebook