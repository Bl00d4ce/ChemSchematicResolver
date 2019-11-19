# ChemSchematicResolver
**ChemSchematicResolver** is a toolkit for the automatic resolution of chemical schematic diagrams and their labels.

## Features

- Extraction of generic R-Group structures
- Automatic detection and download of schematic chemical diagrams from scientific articles
- HTML and XML document format support from RSC and Elsevier
- High-throughput capabilities
- Direct extraction from image files
- PNG, GIF, JPEG, TIFF image format support

## Installation

### Option 1 - Installation via Conda

**NOTE: this installation method will only work upon release, when the conda package is uploaded to anaconda cloud**

We recommend the installation of ChemSchematicResolver through [conda](https://docs.conda.io/en/latest).

 First, install [Miniconda](https://docs.conda.io/en/latest/miniconda.html), which contains a complete Python distribution alongside the conda package manager.

Next, go to the command line terminal and create a working environment by typing

    conda create --name <my_env> python=3.6
    
Once this is created, enter this environment with the command

    conda activate <my_env>

and install ChemSchematicResolver by typing

    conda install -c edbeard chemschematicresolver
    
This command installs ChemSchematicResolver and all it's dependencies from the author's channel.
This includes [pyosra](https://github.com/edbeard/pyosra), the Python wrapper for the OSRA toolkit, and [ChemDataExtracor-CSR](https://github.com/edbeard/chemdataextractor-csr), the bespoke version of ChemDataExtractor containing diagram parsers.

*This method of installation is currently supported on linux machines only*

**NOTE: this installation method will only work upon release, when the conda package is uploaded to anaconda cloud**

### Option 2 - Installation from source

We strongly recommend installation via conda whenever possible as all the dependencies are automatically handled.
 
If this cannot be done, users are invited to compile the code from source. This is easiest to do through [conda build](https://docs.conda.io/projects/conda-build/en/latest/), by building and installing using the recipes [here](www.github.com/edbeard/conda-recipes). 

*This requires the user to set up a conda environment as described previously.*

Specifically, the required dependencies are:

1. **Pyosra**: [[recipe](https://github.com/edbeard/conda-recipes/recipe/pyosra), [source code](https://github.com/edbeard/pyosra)]

2. **ChemDataExtracor-CSR**: [[recipe](https://github.com/edbeard/conda-recipes/recipe/ChemDataExtrator-CSR), [source code](https://github.com/edbeard/chemdataextractor-csr)]

3. **ChemSchematicResolver**: [[recipe](https://github.com/edbeard/conda-recipes/recipe/ChemSchematicResolver), [source code](https://github.com/edbeard/ChemSchematicResolver)]

For local builds, clone each recipe and adjust the `source: path` variable in `<path/to/recipe/meta.yaml>` to the directory containing the source code. Then run 

    conda build .
    
to create a compressed tarball file, which contains the instructions for installing the code *(Please not that this can take up to 30 minutes to build)*.
 
Move all compressed tarballs to a single directory, enter the directory and run:

    conda index .

This changes the directory to a format emulating a conda channel. To install all code and dependencies, then simply run

    conda install -c <path/to/tarballs> chemschematicresolver
    
And you should have everything installed!

*NOTE: Before release all URLS (github source and recipes) will not work - all code must be obtained from the author)*


# Getting Started

This section gives a introduction on how to get started with ChemSchematicResolver. This assumes you already have
ChemSchematicResolver and all dependencies installed.

## Extract Image
It's simplest to run ChemSchematicResolver on an image file.

Open a python terminal and import the library with: 

    >>> import chemschematicresolver as csr
    
Then run:

    >>> result = csr.extract_image('<path/to/image/file>')
    
to perform the extraction. 

This runs ChemSchematicResolver on the image and returns a list of tuples to `output`. Each tuple consists of a SMILES string and a list of label candidates, where each tuple identifies a unique structure. For example:

    >>> print(result)
    [(['1a'], 'C1CCCCC1'), (['1b'], 'CC1CCCCC1')]

## Extract Document

To automatically extract the structures and labels of diagrams from a HTML or XML article, use the `extract_document` method instead:
 
    >>> result = csr.extract_document('<path/to/document/file>')
    
If the user has permissions to access the full article, this function will download all relevant images locally to a directory called *csr*, and extract from them automatically. The *csr* directory with then be deleted.

The tool currently supports HTML documents from the [Royal Society of Chemistry](https://www.rsc.org/) and [Springer](https://www.springer.com), as well as XML files obtained using the [Elsevier Developers Portal](https://dev.elsevier.com/index.html) .

ChemSchematicResolver will return the complete chemical records from the document extracted with [ChemDataExtractor](www.chemdataextractor.org), enriched with extracted structure and raw label. For example:

    >>> print(result)
    {'labels': ['1a'], 'roles': ['compound'], 'melting_points': [{'value': '5', 'units': '°C'}], 'diagram': { 'smiles': 'C1CCCCC1', 'label': '1a' } }

Alternatively, if you just want the structures and labels extracted from the images without the ChemDataExtractor output, run:

    >>> result = csr.extract_document('<path/to/document/file>', extract_all=False)
    
which, for the above example, will return:

    >>> print(output)
    [(['1a'], 'C1CCCCC1')]