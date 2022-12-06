# ddctl

A BDD-based model checker for CTL (Computational Tree Logic).

## Directly using the model checker library

You can directly use the model checker by called the `Model` class like below:
(Basically this is what the ddctl commandline tool does)


```python
from model import *

m = Model(specfile=args.specfile, ectl_only=args.ectl_only, output=args.output)

print(m.ectlrepr, end=', ')
print(m.check())

# alternatively if you want you can print true or false as well instead of the 
# colorized message
print(m.check().status)
```

## Command Line Tool - Usage

### Help

```bash
$ ./ddctl -h
```

### Model Checking

```bash
$ ./ddctl -s <specfile.json> [--ectl-only] [--output <outputfile.png>]
```

## SPECFILE

The specification file is a json file with the following structure:

The JSON file should contain the kripke structure and the CTL formula you want to see model checked.

The output will give you $K \models \varphi$ or $K \not \models \varphi$, where $K$ is the kripke structure and $\varphi$ is the CTL formula.

* No RELEASE operator yet

***Example Specfile:***

```
{
  "states" : ["a", "b", "c"],
  "init" : ["a"],
  "T" : {
    "a" : ["b", "c"],
    "b" : ["c"],
    "c" : ["a"]
  },
  "ap" : {
    "a" : ["p", "q"],
    "b" : ["q"]
  },
  "ctlf" : "(AG p) -> AF !q"
}
```

* Note: labels are atomic propositions

## Dependencies

- Graphviz (for visualization)
- PyDD - CuDD Python Binding  (for BDDs)
- PLY - Python Lex-Yacc (for parsing)


## Getting Dependencies

### Graphviz

If you don't have graphviz installed, you can install it with:

```bash
$ sudo apt-get install graphviz
```

Install python bindings:

```bash
pip3 install graphviz
```

### CuDD

The project internally uses`cudd` python bindings called `PyDD` for BDDs. The tar file for both `cudd` and `PyDD` are included in the `lib` folder. To build the project, you need to have `python3`, `cython` and `python3-dev` installed.


1. To get cython, run `pip3 install cython`
2. To get python3-dev, run `sudo apt-get install python3-dev`
   1. we need this to build the `PyDD` library (it requires the `python3-dev` headers)
3. To build Cudd,
   1. Go to the lib directory
   2. Run `tar -xvf cudd-3.1.0.tar.gz`
   3. Go to the cudd directory
   4. Run `./configure --enable-dddmp --enable-obj --enable-shared`
      1. If you want to build a static library, remove the `--enable-shared` flag.
      2. You can also change the installation directory by adding `--prefix=/path/to/install/dir` to the configure command.
   5. Run `make`
      1. If you want to verify that the library is built correctly, run `make check` (but this is optional)
   6. Run `make install`
   7. You should see that the cudd library is installed in the directory specified by the `--prefix` flag, or in `/usr/local/lib` if you didn't specify a prefix.
      1. I would recommend that you install it in `/usr` or `/usr/local` so that you don't have to add the library to your `LD_LIBRARY_PATH` environment variable.
4. To build PyDD,
   1. Go to the lib directory
   2. Run `tar -xvf PyDD-0.2.0.tar.gz`
   3. Go to the PyDD directory
   4. Run `python3 setup.py build`
   5. Run `python3 setup.py install`
   6. You can verify this by opening your python interpreter and running `import cudd`
5. Once you have these installed, running the `ddctl` command as mentioned above in the `Usage` section should work.
