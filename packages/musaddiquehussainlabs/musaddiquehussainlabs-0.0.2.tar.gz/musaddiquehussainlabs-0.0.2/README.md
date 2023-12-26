# MusaddiqueHussainLabs NLP: State-of-the-Art Natural Language Processing & LLMs Library

MusaddiqueHussainLabs is a comprehensive Natural Language Processing (NLP) library designed to offer state-of-the-art functionality for various NLP tasks. This Python package provides a range of tools and functionalities aimed at facilitating NLP tasks, document analysis, and text preprocessing.

## Features

Currently the package is organized into three primary modules:

### 1. NLP Components

| Component Type | Description                 |
|----------------|-----------------------------|
| tokenize       | Text tokenization           |
| pos            | Part-of-Speech tagging      |
| lemma          | Word lemmatization          |
| morphology     | Study of word forms         |
| dep            | Dependency parsing          |
| ner            | Named Entity Recognition    |
| norm           | Text normalization          |

### 2. Text Preprocessing

This module equips users with an extensive set of text preprocessing tools:

| Function                      | Description                                          |
|-------------------------------|------------------------------------------------------|
| to_lower                      | Convert text to lowercase                             |
| to_upper                      | Convert text to uppercase                             |
| remove_number                 | Remove numerical characters                           |
| remove_itemized_bullet_and_numbering | Eliminate itemized/bullet-point numbering |
| remove_url                    | Remove URLs from text                                 |
| remove_punctuation            | Remove punctuation marks                              |
| remove_special_character      | Remove special characters                             |
| keep_alpha_numeric            | Keep only alphanumeric characters                     |
| remove_whitespace             | Remove excess whitespace                              |
| normalize_unicode             | Normalize Unicode characters                          |
| remove_stopword               | Eliminate common stopwords                            |
| remove_freqwords              | Remove frequently occurring words                      |
| remove_rarewords              | Remove rare words                                     |
| remove_email                  | Remove email addresses                                |
| remove_phone_number           | Remove phone numbers                                  |
| remove_ssn                    | Remove Social Security Numbers (SSN)                  |
| remove_credit_card_number     | Remove credit card numbers                            |
| remove_emoji                  | Remove emojis                                         |
| remove_emoticons              | Remove emoticons                                      |
| convert_emoticons_to_words    | Convert emoticons to words                            |
| convert_emojis_to_words       | Convert emojis to words                               |
| remove_html                   | Remove HTML tags                                      |
| chat_words_conversion         | Convert chat language to standard English              |
| expand_contraction            | Expand contractions (e.g., "can't" to "cannot")        |
| tokenize_word                 | Tokenize words                                        |
| tokenize_sentence             | Tokenize sentences                                    |
| stem_word                     | Stem words                                            |
| lemmatize_word                | Lemmatize words                                       |
| preprocess_text               | Combine multiple preprocessing steps into one function|

### 3. Document Analysis

| Functionality     | Description                                  |
|-------------------|----------------------------------------------|
| Language          | Detect document language                     |
| Linguistic Analysis    | Resolve ambiguities                          |
| Key phrases         | Retrieve relevant information from documents |
| NER               | Named Entity Recognition                     |
| Sentiment         | Analyze sentiment of text                    |
| PII Anonymization | Anonymize Personally Identifiable Information|

## Prerequisites

- Python >= 3.9
- GOOGLE_API_KEY from [Google AI Studio](https://makersuite.google.com)
- Place the API key in a `.env` file in the project root directory.

## Installation

To install `musaddiquehussainlabs`, you can use `pip`:

```bash
pip install musaddiquehussainlabs
```

## Usage

```python
from musaddiquehussainlabs.nlp_components import nlp
from musaddiquehussainlabs.text_preprocessing import preprocess_text, preprocess_operations
from musaddiquehussainlabs.document_analysis import DocumentAnalysis

data_to_process = "The employee's SSN is 859-98-0987. The employee's phone number is 555-555-5555."

# Using NLP component
result = nlp.predict(component_type="ner", input_text=data_to_process)
print(result)

# Text preprocessing
preprocessed_text = preprocess_text(data_to_process)
print(preprocessed_text)

# Custom Text preprocessing
preprocess_functions = [preprocess_operations.to_lower]
preprocessed_text = preprocess_text(data_to_process, preprocess_functions)
print(preprocessed_text)

# Document analysis
document_analysis = DocumentAnalysis()

# Option 1: full analysis
result = document_analysis.full_analysis(data_to_process)

# Option 2: Individual document analysis
result = document_analysis.pii_anonymization(data_to_process)

print(result)
```

Feel free to explore more functionalities and customize the usage based on your requirements!

For detailed usage examples and API documentation, please refer to the [documentation](link_to_your_documentation) (docs link comming soon) available.

## Upcoming Features

We're continuously working on expanding MusaddiqueHussainLabs to provide even more capabilities for NLP tasks.
Please stay tuned for these exciting enhancements!

## License

This project is licensed under the [MIT License](LICENSE).