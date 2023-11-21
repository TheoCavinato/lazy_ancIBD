import h5py as h5py
import argparse

#------------------------------------------------------------------------------# 
# Parameters
#------------------------------------------------------------------------------# 

parser = argparse.ArgumentParser()
parser.add_argument('--h5', required=True, help="HDF5 file")
parser.add_argument('--eig_map', required=True, help="EIG recombination map")
parser.add_argument('--freq', required=False, help="Allele frequencies (optional)")
args = parser.parse_args()

#------------------------------------------------------------------------------# 
# Import HDF5 data
#------------------------------------------------------------------------------# 

p_col = "variants/AF_ALL" # The hdf5 column with der. all freqs
with h5py.File(args.h5, "r") as f:
    # Get allele frequencies 
    p = f[p_col][:] # Load the Allele Freqs from HDF5
    m = f["variants/MAP"][:] # Load the recombination map from HDFF5

print(len(m), len(p))

#------------------------------------------------------------------------------# 
# Compare to your allele frequencies
#------------------------------------------------------------------------------# 

if args.freq != "":
    freq_s = open(args.freq, 'r')
    freq_s.readline() # remove header
    for n, line in enumerate(freq_s):
        freq = float(line.split()[1])

        if not freq==p[n]:
            print("At postion", line.split()[0], "please verify that you have a duplication, otherwise their is a problem in your pipeline")
    freq_s.close()
    print("Frequencies are correct")

#------------------------------------------------------------------------------# 
# Compare to your recombination map
#------------------------------------------------------------------------------# 

map_s = open(args.eig_map)
for n, line in enumerate(map_s):
    rec, pos = line.rstrip().split()[2:4]
    assert abs(m[n]-float(rec)) < 10e-8
map_s.close()
