# Requiremets from pip

> click==8.0.4
> decorator==4.1.2
> importlib-metadata==4.8.3
> ipython==5.5.0
> ipython_genutils==0.2.0
> numpy==1.19.5
> pandas==1.1.5
> pexpect==4.2.1
> pickleshare==0.7.4
> prompt-toolkit==1.0.15
> Pygments==2.2.0
> pysam==0.20.0
> python-dateutil==2.8.2
> pytz==2022.6
> simplegeneric==0.8.1
> six==1.11.0
> traitlets==4.3.2
> typing_extensions==4.1.1
> wcwidth==0.1.7
> zipp==3.6.0

# Специальные пакеты
> Samtools 1.16.1  Sep 02, 2022
> HTSlib 1.16 Aug 18, 2022
> BCFtools 1.16 Aug 18, 2022


# bash для получения FP_SNPs_10k_GB38_twoAllelsFormat.txt

```console

awk 'BEGIN {FS=OFS="\t"; print "CHROM#", "POS", "ID", "Allele1", "Allele2"}
NR>1 {
if($2 != 23)
print "chr"$2, $4, "rs"$1, $5, $6}' FP_SNPs.txt > FP_SNPs_10k_GB38_twoAllelsFormat.txt

'''
