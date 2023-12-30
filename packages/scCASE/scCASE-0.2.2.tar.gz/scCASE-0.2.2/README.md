[![PyPI](https://img.shields.io/pypi/v/sccase.svg)](https://pypi.org/project/sccase)
[![Downloads](https://pepy.tech/badge/sccase)](https://pepy.tech/project/sccase)
# Accurate and interpretable enhancement for single-cell chromatin accessibility sequencing data with scCASE
![](scCASE.png)

## Installation
scCASE is available on [PyPI](https://pypi.org/project/sccase/) and can be installed via
	
	pip install scCASE

You can also install scCASE from GitHub via
	
	git clone git://github.com/BioX-NKU/scCASE.git
	cd scCASE
	python setup.py install
	
The dependencies will be automatically installed along with scCASE. Normally, the installation time does not exceed one minute.   

## Quick Start

#### Input
* **h5ad file**:
	* AnnData object of shape `n_obs` × `n_vars`. 
* **count matrix file**:  
	* Rows correspond to peaks and columns to cells, in **txt**/**tsv** (sep=**"\t"**) or **csv** (sep=**","**) format.

#### Output
* **Enhanced scCAS data**:  The data enhanced by scCASE.
* **Optional output:**
	* **Projection matrix(W)**:  Projection matrix created by scCASE, which is the peak expression program.
	* **Cell embedding matrix(H)**:  Cell embedding created by scCASE, which is the low-dimensional representation of cells.
	* **Similarity matrix(Z)**: Similarity matrix created by scCASE, which is the cell-to-cell similarity calculated through iteration.

#### Run scCASE 
* **Run scCASE to enhance scCASE data:**
	import scCASE
	data_enhanced = scCASE.run(adata,method= "scCASE")
    
* **Use scCASER to enhance scCASE data with reference data:**
	data_enhanced = scCASE.run(data_path,ref_path,method= "scCASER")

* **Use scCASE to correct sequencing depth:**
	data_enhanced = scCASE.run(data_path,method= "Correct seq depth")
    
* **Use scCASE to correct batch effect:**
	data_enhanced = scCASE.run(data_path,method = "Correct batch effect",batchlabel = "batch")

## Tutorials and reproduction
### We provide a [tutorial](https://github.com/BioX-NKU/scCASE/blob/main/Tutorial.ipynb) for running scCASE and integrating [EpiScanpy](https://colomemaria.github.io/episcanpy_doc/)  for scCAS data analysis. (tested on Ubuntu 22.04 LTS). The expected run time for the tutorial is less than 5 minutes.

### The extension of scCASE can additionally correct sequencing depth, and we provide a [tutorial](https://github.com/BioX-NKU/scCASE/blob/main/Tutorial of correct seq depth.ipynb).

### To enhance datasets with batch effects, refer to the [tutorial](https://github.com/BioX-NKU/scCASE/blob/main/Tutorial of correct batch effect.ipynb).

### The source codes for the reproduction of results, all dependencies including version numbers, and the dataset for tutorial are publicly available at [Zenodo](https://zenodo.org/record/8382877).


## API
### Main functions of scCASE:
#### run(data_path,ref_path = None,method = "scCASE",data_format = "h5ad", data_sep=",",ref_sep=",",  K = "Auto",K_ref = "Auto", type_number_range=range(3, 15), save_result = False, output_path = "./",  batchlabel= "batch",threshold = 0.01)
Function "scCASE.run()"is the main function of scCASE.
* [data_path]:`str` or `ad.AnnData`
The path or variable name of the target scCAS data. 
* [ref_path]:`str`
The path of the reference data,file format should be "csv".
* [method]:`str`
Enhancement methods including **"scCASE"**, **"scCASER"**, **"Correct seq depth"** or **"Correct batch effect"**.
* [data_format]:`str`
The format of data and reference data, including **"count matrix"**(csv/txt/tsv) and **"h5ad"**. Default: **"h5ad"**
* [data_sep]:`str` 
The Separator of target scCAS data, only for count matrix file. Default: **","**
* [ref_sep] :str 
The Separator of reference data, only for count matrix file. Default: **","**
* [ K ] :`"Auto" or int`
The parameter K. Default: **"Auto"**
* [K_ref] :`"Auto" or int`
The parameter K_ref. Default: **"Auto"**
* [type_number_range]:`range`
The range of estimate parameter K, only for K = "Auto. Default: **range(3, 15)**
* [save_result]: `bool` 
If save the enhanced result or not .Default: **Flase**
* [output_path]:`str`
The path of the output, only for save_result is True. Default: **"./"**
* [batchlabel]:`str`
The key of the observation stored batch label, only for method="Correct batch effect".
* [threshold]:`float` 
The threshold of filtering peaks. Default: **0.01**

#### lazy(data)
Function "scCASE.lazy()" including TF-IDF, PCA, creating neighbors graph,and t-SNE/UMAP.

#### identify_specific_peaks(data_enhanced, type_ ,obs = "cell_type",peak_name = "peak")
Function "scCASE.identify_specific_peaks()" is used to identify specific peaks of given cell labels.

* [data_enhanced]:`str`
The data enhanced by scCASE.
* [obs]:`str`
The key of the observation to consider.
* [type_]:`str`
The type in adata.obs to consider.
* [peak_name]:`str` 
The key of the variables annotation which represent peak names.
