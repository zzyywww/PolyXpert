# PolyXpert：Sequence-Based Therapeutic Antibody Polyreactivity Prediction
A fine-tuned ESM-2 model for predicting polyreactivity of  antibody candidates using scFv sequence data.

## Key Features:
Requires only heavy/light chain Fv sequences (no structural data).
Achieves 0.9672 AUC on held-out test set.

## Development environment:
Python 3.9.16
CUDA Version: 12.2
transformers version：4.26.1
torch version：1.13.1

## data prepare Example (example_seq.txt)
Required columns in TXT file:
Name: Unique sequence identifier (string)
VH: Heavy chain Fv sequence (e.g. QVQLQESGGGVVQPGRSLRLSCAASGFTFSSYGMHWVRQAPGKGLEWVAVIWYDGSNKYYADSVKGRFTISRDNSRNTLYLQMNSLRGEDTAVYYCAKRGTGSSFYYFDYWGQGTLVTVSS)
VL: Light chain Fv sequence (e.g. EIVLTQSPSALSASVGDRVTITCRASQNIANYLNWYQQKPGKPPKLLIYVASNLPSGVPSRFSGSGSGTDFTLTISGLQPDDFATYYCQQSYTTPRTFGQGTKVDIK)

## Installation
we recommend using the conda environment zand you can clone this repository locally:
```
conda create -n polyxpert python=3.9
conda activate polyxpert
git clone https://github.com/zzyywww/PolyXpert.git 
cd PolyXpert
pip install -r requirements.txt --ignore-installed
```

## Download the model
```
wget https://i.uestc.edu.cn/PolyXpert.zip
unzip PolyXpert.zip
```
If you are using a Windows system, you can copy the link and paste it into browser to download the file directly.

**Note:** The unzipped PolyXpert folder must be in the same directory as the PolyXpert.py script."

##Usage:

```
python PolyXpert.py [inputfile]
```
inputfile: sequence file, 'Name' column for **sequence id**, 'VH' column for heavy chain **Fv region** ,  'VL' column for light chain **Fv region** 
The example of inputfile can be found in **./example/example_seq.txt**

## Example:
```
python PolyXpert.py ./example/example_seq.txt
```
The results will be saved in **results** folder automatically, or you can modify the source code in **PolyXpert.py** to save your results more customistically.
