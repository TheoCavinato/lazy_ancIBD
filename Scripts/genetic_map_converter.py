import gzip as gz
import sys
import argparse
from pysam import VariantFile

""" We need to linearly convert the genetic map to get the h5 file """

def linear_conversion(X, A_1, A_2, B_1, B_2):
    return ((X-A_1)/(A_2-A_1))*(B_2-B_1)+B_1

#------------------------------------------------------------------------------# 
# Parameters
#------------------------------------------------------------------------------# 
parser = argparse.ArgumentParser()
parser.add_argument('--vcf', required=True, help="VCF so that I can match the positions between the files")
parser.add_argument('--map', required=True, help="GMAP from GLIMPSE")
parser.add_argument('--out', required=True, help="Output directory to the EIG format GMAP")
args = parser.parse_args()

#------------------------------------------------------------------------------#
# Import recombination map
#------------------------------------------------------------------------------#
gmap_s = gz.open(args.map, 'rt')
gmap_s.readline() #remove header

bp_list, cM_list = [], []
for line in gmap_s:
    bp, chr, cM = line.rstrip().split()
    bp_list.append(int(bp))
    cM_list.append(float(cM))
gmap_s.close()

# add positions that are not present in the map but present in the vcf
vcf_s = VariantFile(args.vcf, "r")
vcf_s.subset_samples([])
for rec in vcf_s:
    if rec.pos < bp_list[0]:
        bp_list.insert(0, rec.pos)
        cM_list.insert(0, 0.0)
    if rec.pos > bp_list[-1]:
        bp_list.append(rec.pos)
        cM_list.append(cM_list[-1])
vcf_s.close()

#------------------------------------------------------------------------------#
# Import recombination mpa
#------------------------------------------------------------------------------#

vcf_s = VariantFile(args.vcf, "r")
vcf_s.subset_samples([])
itr_gmap = 0
search_first_pos = True

vcf_bp = []
out_s = open(args.out, 'w')
for rec in vcf_s:
    # check that vcf positions are encompassed by the recombination map
    assert not (rec.pos < bp_list[itr_gmap] and itr_gmap==0)
    assert itr_gmap!=len(bp_list)-1

    while rec.pos > bp_list[itr_gmap+1]: itr_gmap+=1

    cM_converted = linear_conversion(rec.pos, bp_list[itr_gmap], bp_list[itr_gmap+1], cM_list[itr_gmap], cM_list[itr_gmap+1])/100
    new_line = ' '.join(map(str,[rec.id, rec.chrom, cM_converted, rec.pos, rec.ref, rec.alts[0]]))
    out_s.write(new_line)
    out_s.write('\n')

vcf_s.close()
out_s.close()
