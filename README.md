# LaTeX Smart Quotes

The purpose of this Sublime Text Package is to make the quotes in LaTeX "smart", i.e. insert the quotes you intend to use.
It is inspired by the [typopunct-mode](http://www.emacswiki.org/emacs/typopunct.el) for Emacs.

To establish this goal it uses:

- language detection (supported languages: English, German, French)
- context detection according to the caret position


## Usage

Usually you do not have to do anything special and just use LaTeX as always.
If you type `"` or `'` this Package will try to extract the language of the document and insert the correct quotation marks.

The language detection is executed the first time you press `"` or `'` and the result will be cached.
If you want to rerun it open the command palette (`ctrl+shift+p`) and insert `LaTeX SmartQuotes: Auto Detect Buffer Language`, the result will be displayed in the status bar at the bottom.
If the detected language is incorrect or you use a multilingual document, you can change the language by executing the command `LaTeX SmartQuotes: Set Buffer Language` in the command palette. This command will provide you a list with all available languages. If the language ends with `-ucs` it will use unicode characters.

### Hints

- You can use `ctrl+l "` or `ctrl+l '` (respectively `super+l "` or `super+l '` on OSX) to insert the usual quotation marks instead of the LaTeX and language specific.
  If you want to disable the special quotes (e.g. in a lstlisting environment), you can set the buffer language to "None".

- If you use unicode characters you should have `\usepackage[utf8]{inputenc}` at the start of your document.

- The language detection checks for specific packages, hence it does not always work correctly. Nevertheless it should always work with the babel package.

- To disable the automatic language detection and define a language, which should always be used, you can define it in your user settings. For example you can add `"latex_smart_quotes_current_language": "german-ucs"` to always use german with unicode support. You might want to do this if you only use one language anyway.<br>
  **If you are a native english speaker you might want to add `"latex_smart_quotes_current_language": "english"` to your settings file.**


## Options

Options are set in the package settings file, which is as usual available in the menu `Prefences>Package Settings>LaTeXSmartQuotes>Settings - User`.

- __latex_smart_quotes_default_language__ The default language, which is used if no language has been detected
- __latex_smart_quotes_use_ucs__ enables unicode support, i.e. unicode quotations instead of ascii characters


## Demonstration

This demonstrates the context detection, i.e. the choice of opening and closing quotes.

![LaTeXSmartQuotes context detection](https://cloud.githubusercontent.com/assets/12573621/9733030/9648d91e-5628-11e5-94c9-cf55cf51bdc6.gif)

This demo shows some available quotes. The quote types are chosen automatically by the language detection of this package.

![LaTeXSmartQuotes all quotes](https://cloud.githubusercontent.com/assets/12573621/9706476/4f9f1de0-54e6-11e5-8bfe-b4625c8e6c76.gif)


## Issues

If something does not work as you expected or you want support of an additional language, then you can create a [pull request](https://github.com/r-stein/sublime-text-latex-smart-quotes/pulls) or an [issue](https://github.com/r-stein/sublime-text-latex-smart-quotes/issues) on [github](https://github.com/r-stein/sublime-text-latex-smart-quotes).
In the case you don't own a github account you can also write in email to [r-stein.github@web.de](mailto:r-stein.github@web.de).
