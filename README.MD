# About
## Description
A program for calculating various text metrics such as nominal ratio, word variation, readability, mean word length and text length for Swedish texts. Nominal ratios are the main focus, though, and calculating them is done with the help of POS-tagging using the language models [KB-BERT](https://arxiv.org/pdf/2007.01658) and [Flair](https://spraakbanken.gu.se/resurser/flair). I wrote this program for a study comparing nominal ratios to grades. It is quite specific and not very modular, but I've left some documentation regardless as it is not much work.

The texts that were used by the study are confidential, though I have supplied some example texts that I've written myself for anyone looking to test the program. If you just want to test the visualizer tool you don't have to run anything as I pushed part of the program output (when ran with the example) to the repo, just open the index.html in /Visualizer and you can look at the examples. 
## Screenshots


# Usage
## Input files 
Place your one or more .docx files in /input. The texts in the .docx files are seperated by a line containing the next text's metadata. Below is an example such a line.

```<ID123 Kp3 vt14 UTR A K SV ET _ _ D>```

if you browse `parsing.py` you can figure out what each part means. The only values actually used by the program is the id (ID123) and grade (A). The rest may have dummy values. Alternatively you could just copy and paste things from the `example.docx` file in /input. Not having unique Ids for every text may cause issues.
## Getting it to run
The program needs a sentence segmentizer before it can run. [Here is a model by Språkbanken that was used by the study and is known to work.](https://github.com/spraakbanken/sparv-models/blob/2e74bb6dec4326c775c3aa4a92a54468d98ae37a/segment/punkt-nltk-svenska.pickle)

Run the program with:

`py main.py [MODEL(S)] [OPTIONS]`

## Arguments
### models
Available models are `kb_bert` and `flair`. To use both, specify `kb_bert,flair` or `all` as the first argument. Default: `kb_bert`.
### options
| Flag                  | Description|
|-----------------------|------------|
| `--tag-quotes`        | Count words inside quotes in the nominal ratio. |
| `--tag-parenthesis`   | Count words inside parenthesis in the nominal ratio. |
| `--tag-italics`       | Count words in italics in the nominal ratio. |
| `--tag-all`           | Count words inside quotes, parenthesis, and italics in the nominal ratio. |

If no options are specified the behaviour is equivalent to `--tag-all`

## Examples
`py main.py kb_bert,flair --tag-all`

`py main.py kb_bert --tag-italics --tag-quotes`