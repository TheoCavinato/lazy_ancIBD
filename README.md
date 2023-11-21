# lazy ancIBD

You want to use GLIMPSE's genetic map and allele frequencies in ancIBD? Here you go:

## Original data
I simulated a pedigree and imputed it. All the information is Ori_data/
simulation.chr20.lowcov.0.5x.imputed.vcf.gz -> contains the imputed genoytpes with GPs + phase
chr20.b37.gmap.gz -> GMAP used by GLIMPSE for imputation

## 1. Converting GMAP to EIGENSTRAT MAP
```
VCF=Ori_data/simulation.chr20.lowcov.0.5x.imputed.vcf.gz
MAP=Ori_data/chr20.b37.gmap.gz
EIG_MAP=EIGENSTRAT_map/chr20.linear.snp

# run the conversion
python3 Scripts/genetic_map_converter.py --vcf $VCF --map $MAP --out $EIG_MAP

# validation
echo "These two next numbers should be equal:"
bcftools index -n $VCF
wc -l $EIG_MAP
```

## 2. Computing allele frequencies (optional)
Reference panel is to big to be stored on github. Just make sure the reference panel contains the same positions than the imputed vcf.
```
FREQ=Ori_data/allele_frequencies.tsv
REF=Ori_data/ref_panel.bcf
bcftools +fill-tags $REF  -Ob -- -t AF | \
bcftools query -f '%POS %AF %CHROM\n' | \
awk 'BEGIN{print "pos","af","ch"} {print $0}' | \
sed 's/ /\t/g' > $FREQ
```


## 3. Converting VCF to HDF5
```
HDF5_FORMAT=H5_converted/simulation.chr20.h5
python3 Scripts/h5_conversion.py --vcf $VCF --eig_map $EIG_MAP  --out $HDF5_FORMAT (--freq $FREQ)
```


## 4. Validation
```
python3 Scripts/validation.py --freq $FREQ --eig_map $EIG_MAP --h5 $HDF5_FORMAT (--freq $FREQ)
```
