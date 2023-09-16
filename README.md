#   csv intersection
Intersection of csv files by a key column. And filelist of some folder name

Where column is a string with the file name. 

Result saved to new csv file. 

### help

```
usage:   [-h] [-V] [--work WORK] --input1 INPUT1 --input2 INPUT2 [--output OUTPUT] [--input1_key_idx INPUT1_KEY_IDX] [--verbose]

options:
  -h, --help            show this help message and exit
  -V, --version         show version of app
  --work WORK           Directory for work. Is prefix for all other directories that is not absolute, default ''
  --input1 INPUT1       Path to input1 csv file (main)
  --input2 INPUT2       Path to directory to folder with files (reference)
  --output OUTPUT       Path for output file, default 'output.csv'
  --input1_key_idx INPUT1_KEY_IDX
                        Key index for input1, default 2
  --verbose             verbose output

```



### result 

```
2023-09-16 23:10:12,826  input1 first 5 keys in list: ['2407', '2408', '2409', '2417', '2418']
2023-09-16 23:10:12,826  input2 first 5 keys in list: ['2407', '2408', '2409', '2409']
2023-09-16 23:10:12,826  input1_records=9, input2_records=4, output_records=3
2023-09-16 23:10:12,827  Output data is saved to a file: 'tests\output.csv'
```