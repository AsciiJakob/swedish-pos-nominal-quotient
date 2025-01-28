# About


# Usage
Place your file(s) in /input. The format must be 

Run the program with:

`py main.py [MODEL(S)] [OPTIONS]`

## Arguments
### models
Available models are `kb_bert` and `flair`. To use both, specify `kb_bert,flair` or `all` as the first argument. Default: `kb_bert`.
### options
| Flag                  | Description|
|-----------------------|------------|
| `--tag-quotes`        | Count words inside quotes in the nominal quotient. |
| `--tag-parenthesis`   | Count words inside parenthesis in the nominal quotient. |
| `--tag-italics`       | Count words in italics in the nominal quotient. |
| `--tag-all`           | Count words inside quotes, parenthesis, and italics in the nominal quotient. |

If no options are specified the behaviour is equivalent to `--tag-all`

## Examples
`py main.py kb_bert,flair --tag-all`

`py main.py kb_bert --tag-italics --tag-quotes`