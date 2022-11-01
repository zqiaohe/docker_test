FROM ubuntu:18.04

MAINTAINER Bayarma Zanaeva <zanaevab@gmail.com>

ARG samtools_version=1.16.1
ARG htslib_version=1.16
ARG bcftools_version=1.16


RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.7 \
    python3-pip \
    ipython3 \
    python3-numpy 

RUN apt-get install -y libhdf5-dev libatlas-base-dev

RUN apt-get update && apt-get -y upgrade && \
	apt-get install -y build-essential wget \
		libncurses5-dev zlib1g-dev libbz2-dev liblzma-dev libcurl3-dev && \
	apt-get clean && apt-get purge && \
	rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


RUN pip3 install pandas
RUN pip3 install --upgrade setuptools pip wheel


WORKDIR /SOFT

# HTSlib 1.16 Aug 18, 2022

RUN wget https://github.com/samtools/htslib/releases/download/${htslib_version}/htslib-${htslib_version}.tar.bz2 && \
	tar jxf htslib-${htslib_version}.tar.bz2 && \
	rm htslib-${htslib_version}.tar.bz2 && \
	cd htslib-${htslib_version} && \
	./configure --prefix $(pwd) && \
	make

#Samtools 1.16.1  Sep 02, 2022

RUN wget https://github.com/samtools/samtools/releases/download/${samtools_version}/samtools-${samtools_version}.tar.bz2 && \
	tar jxf samtools-${samtools_version}.tar.bz2 && \
	rm samtools-${samtools_version}.tar.bz2 && \
	cd samtools-${samtools_version} && \
	./configure --prefix $(pwd) && \
	make

RUN pip3 install click



RUN export HTSLIB_LIBRARY_DIR=/usr/local/lib
RUN export HTSLIB_INCLUDE_DIR=/usr/local/include
RUN pip3 install pysam


# BCFtools 1.16 Aug 18, 2022
RUN wget https://github.com/samtools/bcftools/releases/download/${bcftools_version}/bcftools-${bcftools_version}.tar.bz2 && \
	tar jxf bcftools-${bcftools_version}.tar.bz2 && \
	rm bcftools-${bcftools_version}.tar.bz2 && \
	cd bcftools-${bcftools_version} && \
	./configure --prefix $(pwd) && \
	make


COPY script.py /SOFT/script.py
COPY FP_SNPs.txt /SOFT/FP_SNPs.txt
COPY chrs /SOFT/chrs

ENV LC_ALL=C.UTF-8
ENV export LANG=C.UTF-8


