# Flexible and comprehensive software app for design of synthetic DNA sequences without unwanted patterns

## Pre-Requisite

Please execute the following command within your working environment:

```
pip3.9 install -r requirements.txt
```

## Execute Terminal Program

To execute the elimination tool from the Terminal, please use the following command:

```
python3.9 ./BioSynth.py -s <seq_file_path> -p <pattern_file_path> -c <codon_usage_table>
```

For example:

```
python3.9 ./BioSynth.py -s ./files/one_coding/s_file_one_coding.txt -p ./files/one_coding/p_file_one_coding.txt -c ./files/one_coding/codon_usage.txt
```

## Execute GUI Program

To execute the elimination tool GUI, please use the following command:

```
python3.9 ./BioSynth.py -g
```
