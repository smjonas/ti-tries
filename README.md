# ti-tries
Several trie implementations in Python.

## Requirements
- Python 3.10+ (might work with lower versions but untested)
- the `avltree` package for the balanced search tree trie: `pip install avltree`
- `run` to run the experiments: see https://thobl.github.io/run/

## Usage
Run `python base.py <variant=1-3> <input_file> <query_file>` from the `src` directory.
To run the experiments, navigate to the `eval` directory. Then run `python ./run_experiments.py <experiments>` where `<experiments>`
are either experiment groups `exp1`, `exp2` or `exp3` or individual experiments.
