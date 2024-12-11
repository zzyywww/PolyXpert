# PolyXpert
This is a sequence-based fine-tuned ESM-2 model, named PolyXpert, for predicting polyreactivity of therapeutic mAbs candidates.

you can clone this repository locally:
```
git clone https://github.com/zzyywww/PolyXpert.git 
cd PolyXpert
pip install -r requirements.txt --ignore-installed
```
Download the model
```
wget https://i.uestc.edu.cn/esm2_finetuning.zip
unzip esm2_finetuning.zip
```
**Note:** The unzipped esm2_finetuning folder must be in the same directory as the PolyXpert.py script."

Usage:

```
python PolyXpert.py [inputfile]
```
inputfile: #sequence file, 'Name' column for **sequence id**, 'VH' column for heavy chain **Fv region** ,  'VL' column for light chain **Fv region** 
The example of inputfile can be found in **./example/example_seq.txt**

Example:
```
python PolyXpert.py ./example/example_seq.txt
```
The results will be saved in **results** folder automatically, or you can modify the source code in **PolyXpert.py** to save your results more customistically.
