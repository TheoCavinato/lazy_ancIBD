from ancIBD.IO.prepare_h5 import vcf_to_1240K_hdf
import argparse


#------------------------------------------------------------------------------# 
# Parameters
#------------------------------------------------------------------------------# 

parser= argparse.ArgumentParser()
parser.add_argument('--vcf', required=True, help="GLIMPSE ouptut")
parser.add_argument('--eig_map', required=True, help="EIG format recombination map", default="")
parser.add_argument('--freq', required=False, help="Allele frequencies (optional)")
parser.add_argument('--chrom', required=True, help="Chromosome", type=int)
parser.add_argument('--out', required=True, help="Output file")
args=parser.parse_args()

#------------------------------------------------------------------------------# 
# 
#------------------------------------------------------------------------------# 

vcf_to_1240K_hdf(in_vcf_path = args.vcf,
                path_vcf = "",
                path_h5 = args.out,
                marker_path = "",
                map_path = args.eig_map,
                af_path = args.freq,
                col_sample_af = "", 
                buffer_size=20000, chunk_width=8, chunk_length=20000,
                ch=args.chrom)
