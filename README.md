# LaTeX Smart Quotes

The purpose of this Sublime Text Package is to make the quotes in LaTeX "smart", i.e. insert the quotes you want to have.

To establish this goal it uses:

- language detection (supported languages: English, German, French)
- context detection according to the caret position


## Usage

Usually you do not have to do anything special and just use LaTeX as always.
If you type `"` or `'` this Package will try to extract the language of the document and insert the correct quotation marks.

The language detection is executed the first time you press `"` or `'` and the result is cached.
If you want to rerun it press `ctrl+shift+p` and insert `LaTeX SmartQuotes: Auto Detect Buffer Language`, the result will be displayed in the status bar at the bottom.
If the detected language is incorrect or you use a multilingual document, you can change the language by pressing `ctrl+shift+p` and executing the command `LaTeX SmartQuotes: Set Buffer Language`. This command will provide you a list with all available languages. If the language ends with `-ucs` it will use unicode characters.

### Hints

- You can use `ctrl+l "` or `ctrl+l '` to insert the usual quotation marks instead of the LaTeX and language specific.
  If you want to disable the special quotes (e.g. in a lstlisting environment), you can set the buffer language to "None".

- If you use unicode characters you should have `\usepackage[utf8]{inputenc}` at the start of your document.

- The language detection checks for the babel package, hence it won't work if you use an other package for language support.

- To disable the automatic language detection and define a language, which should always be used, you can define it in your user settings. For example you can add `"latex_smart_quotes_current_language": "german-ucs"` to always use german with unicode support. You might want to do this if you only use one language anyway.<br>
  **If you are a native english speaker you might want to add `"latex_smart_quotes_current_language": "english"` to your settings file.**


## Options

- __latex_smart_quotes_default_language__ The default language, which is used if no language has been detected
- __latex_smart_quotes_use_ucs__ enables unicode support, i.e. unicode quotations instead of ascii characters


## Demonstration

This demonstrates the context detection, i.e. the choice of opening and closing quotes.

![LaTeXSmartQuotes context detection](https://cloud.githubusercontent.com/assets/12573621/9733030/9648d91e-5628-11e5-94c9-cf55cf51bdc6.gif)

This demo shows some available quotes. The quote types are chosen automatically by the language detection of this package.

![LaTeXSmartQuotes all quotes](https://cloud.githubusercontent.com/assets/12573621/9706476/4f9f1de0-54e6-11e5-8bfe-b4625c8e6c76.gif)
