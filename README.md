# LaTeX Smart Quotes

The purpose of this Sublime Text Package is to make the quotes in LaTeX "smart", i.e. insert the quotes you want to have.

To establish this goal it uses:

- language detection (supported languages: English, German, French)
- context detection according to the caret position


## Usage

Usually you do not have to do anything special and just use LaTeX as always.
If you type `"` or `'` this Package will try to extract the language of the document and insert the correct quotation marks.

The language detection is executed the first time you press `"` or `'` and the result is cached.
If you want to rerun it press `ctrl+p` and insert `LaTeX SmartQuotes: Auto Detect Buffer Language`, the result will be displayed in the status bar at the bottom.
If the detected language is incorrect or you use a multilingual document, you can change the language by pressing `ctrl+p` and executing the command `LaTeX SmartQuotes: Set Buffer Language`. This command will provide you a list with all available languages. If the language ends with `-ucs` it will use unicode characters.

### Hints

- If you use unicode characters you should have `\usepackage[utf8]{inputenc}` at the start of your document.

- You can use `ctrl+l "` or `ctrl+l '` to insert the usual quotation marks instead of the LaTeX and language specific.

- The language detection checks for the babel package, hence it won't work use an other package for language support

## Options

- __latex_smart_quotes_default_language__ The default language, which is used if no language has been detected
- __latex_smart_quotes_use_ucs__ enables unicode support, i.e. unicode quotations instead of ascii characters


## Demonstration

__TODO__

