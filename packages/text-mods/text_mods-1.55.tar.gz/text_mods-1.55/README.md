# Text Formatting Toolkit

text_mods is a Python module for formatting text strings in various ways. It includes functions for removing HTML tags and punctuation, replacing words with synonyms, applying different formatting styles such as bold, italic and colored text. In addition it performs natural language processing tasks such as entity recognition, word frequency counting and text summarization.

## Features

* Text Cleaning: Remove HTML tags, punctuation, and numbers from text.
* Text Formatting: Apply styles like bold, italic, underline, and color.
* NLP Tasks: Perform entity recognition, word frequency counting, and summarization.
* Text Transformation: Replace words with synonyms, translate text, and more.
* Sentiment Analysis: Analyze the sentiment of text.
* Customization: Extensive options for text processing tailored to specific needs.

## Requirements

Make sure you have the following requirements installed before running the code:

* Python 3.6 or higher
* NLTK library: Install NLTK using 'pip install nltk'
* NLTK WordNet database
* gensim library
* googletrans library
* spacy library
* en_core_web_sm package for Spacy

## Installation

* Install Python 3.6 or higher from the official website: [Here] (<https://www.python.org/downloads/>)
* Install the NLTK library by running ```pip install nltk``` in your terminal or command prompt.
* Download the WordNet database by running the following commands in a Python interpreter:

``` Python
import nltk
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
```

* Install gensim using ```pip install gensim```
* Install googletrans using ```pip install googletrans```
* Install spacy using ```pip install spacy```
* Download the en_core_web_sm package for Spacy by running ```python -m spacy download en_core_web_sm```
* Install the gensim, googletrans, and spacy libraries by running ```pip install gensim googletrans spacy```
* Download the en_core_web_sm package for Spacy by running ```python -m spacy download en_core_web_sm```
* Download or clone the code from the Github repository: [Github](<https://github.com/Ilija-nik1/text_mods>)

### Clone

Clone the repository using git

``` bash
git clone https://github.com/Ilija-nik1/text_mods.git
```

## Usage

Here are some examples of how to use the functions in the module

``` Python
from text_mods import remove_html_tags, make_bold, replace_with_first_synonym, make_colored

text = '<h1>Hello, world!</h1>'
text = remove_html_tags(text)
text = make_bold(text)
print(text)  # <b>Hello, world!</b>

text = 'This is a sample sentence.'
text = replace_with_first_synonym(text)
text = make_colored(text, 'red')
print(text)  # <span style="color:red">This is a sampling sentence.</span>
```

For more information on each function, please refer to the docstrings in the code.

## Contributing

If you find any bugs or have suggestions for new features, please open an issue or pull request on the Github repository.

## License

This code is licensed under the MIT License.
