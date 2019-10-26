# SpellCor

SpellCor is a spell correction tools coded fully with PYTHON.

We implement this program inspired by JamSpell which writen in C++ and could used with python by swig. 
Jamspell is effective due to C++ benefits. However, it's not convenient for developers or anyone who 
wants to add some features to it. Considering the prevalence of python in NLP area, We implement a python
version spell correction program works like Jamspell, we call it SpellCor.

Compare with Jamspell, SpellCor is more flexible for Python developer:
* Fully python code, include a python version n-gram language model .
* You can easily use your own language model like NN models by writing some pieces of code.
* Support to filter candidate words by the dictionary pointed by yourself.

We also evaluate both SpellCor and Jamspell on 2W+ sentences contain spell errors, below is the detail.
SpellCor's performance is a little bad, but that maybe because we use a basic n-gram language model and the performance
can be improved if you use NN language model.
 
<img src="./img/compare.jpg"></img>

***

### Requires

> python 3.x

### Basic Usage

#### Installation

```shell
pip install spellcor
```


#### load language model

You can download basic language model [here](https://pan.baidu.com/s/1zfIdfTJvEn2x1CtFTmfD2Q)

```python
import spellcor

checker = spellcor.SpellChecker()

# show all language model we supported
checker.show_show_lang_models()

> ["BaseLanguageModel"] #  the default one

# load language model
model_name = "BaseLanguageModel"
model_path = "./tmp/nglm.bin"
checker.load_lang_model("BaseLanguageModel","./tmp/nglm.bin")
> Loading...
> Load Success!

```
#### sentence correction

```python
checker.fix_sentence("here are some Questino , I am pyspell checkre ")

>  here are some Question , I am spell checker
```

#### fix by position

```python
checker.fix_pos(["here","are", "some", "Questino"], 3)
> ['Question', 'Questino']

```


