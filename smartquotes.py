import re

import sublime
import sublime_plugin

from .getTeXRoot import get_tex_root

quotes = {
    "english": {
        "single": {
            "start": "`",
            "end": "'"
        },
        "double": {
            "start": "``",
            "end": "''"
        }
    },
    "english-ucs": {
        "single": {
            "start": "\u2018",
            "end": "\u2019"
        },
        "double": {
            "start": "\u201C",
            "end": "\u201D"
        }
    },
    "german": {
        "single": {
            "start": "\glq ",
            "end": "\grq"
        },
        # TODO this requires babel
        "double": {
            "start": "\"`",
            "end": "\"'"
        }
    },
    "german-ucs": {
        "single": {
            "start": "\u201A",
            "end": "\u2018"
        },
        "double": {
            "start": "\u201E",
            "end": "\u201C"
        }
    },
    "german-chevron-ucs": {
        "single": {
            "start": "\u203A",
            "end": "\u2039"
        },
        "double": {
            "start": "\u00BB",
            "end": "\u00AB"
        }
    },
    "french": {
        "single": {
            "start": "\\flq ",
            "end": "\\frq"
        },
        "double": {
            "start": "\\flqq ",
            "end": "\\frqq"
        }
    },
    "french-babel": {
        "single": {
            "start": "\u2039",
            "end": "\u203A"
        },
        "double": {
            "start": "\\og ",
            "end": " \\fg{}"
        }
    }
    "french-ucs": {
        "single": {
            "start": "\u2039",
            "end": "\u203A"
        },
        "double": {
            "start": "\u00AB",
            "end": "\u00BB"
        }
    },
    "None": {
        "single": {
            "start": "'",
            "end": "'"
        },
        "double": {
            "start": "\"",
            "end": "\""
        }
    }
}

OPTIONS_DEFAULT_LANG = "latex_smart_quotes_default_language"
OPTIONS_CURRENT_LANG = "latex_smart_quotes_current_language"
OPTIONS_UCS = "latex_smart_quotes_use_ucs"
OPTIONS_WORD_SEPARATORS = "latex_smart_quotes_insert_word_separators"


class LanguageDetection:
    def package_settings(self):
        return sublime.load_settings('LaTeXSmartQuotes.sublime-settings')

    def get_current_language(self):
        # check if the language has already been saved in the options
        return self.view.settings().get(OPTIONS_CURRENT_LANG, None)

    def add_word_seperators(self, language):
        word_separators = self.view.settings().get("word_separators")
        quote_signs = "".join(
            quote_sign
            for quote_type in quotes[language].values()
            for quote_sign in quote_type.values()
            if (len(quote_sign) == 1 and
                quote_sign not in word_separators)
        )
        if not quote_signs:
            return
        new_word_separators = word_separators + quote_signs
        self.view.settings().set("word_separators", new_word_separators)

    def set_current_language(self, language):
        self.view.settings().set(OPTIONS_CURRENT_LANG, language)
        if (language.endswith("-ucs") and
                self.package_settings().get(OPTIONS_WORD_SEPARATORS)):
            self.add_word_seperators(language)

    def get_default_language(self):
        ucs_settings = self.package_settings().get(OPTIONS_UCS, False)
        fallback_lang = "english-ucs" if ucs_settings else "english"
        return self.package_settings().get(OPTIONS_DEFAULT_LANG, fallback_lang)

    def _auto_detect_language_from_file(self, file_name):
        # open the file in binary mode and try to convert it later to avoid
        # decoding errors, we are only interested in lines
        # without special chars anyway
        tex_file = open(file_name, 'rb')

        ucs_string = ''
        is_root = ucs_found = False
        lang = None

        for bline in tex_file:
            try:
                line = bline.decode("UTF-8")
            except UnicodeDecodeError:
                continue
            is_root = is_root or line.find("documentclass") > -1
            ucsr = re.search(
                r"\\((use)|(Require))package\[utf(8)|(16)\]"
                r"\{inputenc\}",
                line)
            if ucsr and self.package_settings().get(OPTIONS_UCS, True):
                ucs_string = '-ucs'
            langr = re.search(
                r"\\((use)|(Require))package"
                r"(\[(\w+,\s*)*(?P<lang>\w*)\])?"
                r"\{babel\}",
                line)
            if langr:
                lang = langr.group("lang")
            elif re.search(
                    r"\\((use)|(Require))package\{([^\}]*,\s*)?"
                    r"n?german"
                    r"(\s*,[^\}]*)?\}",
                    line):
                lang = "german"

            # early break conditions to improve performance
            if re.search(r"\\begin\{document\}", line):
                is_root = True
                break
            ucs_found = ucs_found or bool(ucsr)
            if lang is not None and ucs_found:
                break

        tex_file.close()

        if lang is None and is_root:
            # if its the root document, but no language specified
            # it is most likely english!
            return "english" + ucs_string
        elif lang is None:
            return

        if re.match(r"n?german", lang):
            lang = "german"
        elif re.match(r"(frenchb?)|(francais)|(acadian)|(canadien)", lang):
            lang = "french"

        return lang + ucs_string

    def auto_detect_language(self):
        sublime.status_message("Detecting Language...")

        file_name = self.view.file_name()
        if file_name is None:
            lang = self.get_default_language()
            message = "Save the file to enable language detection." +\
                " Set to default: '%s'" % lang
            sublime.status_message(message)
            return lang

        # the language is set in the the TeX root,
        # if the root is defined try to get the language from the root
        # else assume the current file is the root
        root = get_tex_root(self.view)
        if root:
            file_name = root
        lang = self._auto_detect_language_from_file(file_name)

        # combine the results
        if not lang:
            lang = self.get_default_language()
            message = "Could not detect language. Set to default: '%s'" % lang
            sublime.status_message(message)
        # check if the detected language is valid
        elif lang not in quotes:
            # language with(out) ucs might be supported
            newlang = ""
            if lang.replace("-ucs", "") in quotes:
                newlang = lang.replace("-ucs", "")
            elif lang + "-ucs" in quotes:
                newlang = lang + "-ucs"
            default_lang = newlang if newlang else self.get_default_language()
            message = "Language not supported: '%s' Set to fallback: '%s'" % \
                (lang, default_lang)
            sublime.status_message(message)
            lang = default_lang
        else:
            message = "Language detected: '%s'" % lang
            sublime.status_message(message)
        # print("LSQ: " + message)

        # change the current set language
        self.set_current_language(lang)
        return lang


class LsqAutoDetectBufferLangCommand(sublime_plugin.TextCommand,
                                     LanguageDetection):
    def run(self, edit):
        self.auto_detect_language()


class LsqSetBufferLangCommand(sublime_plugin.TextCommand, LanguageDetection):
    def run(self, edit):
        languages = list(quotes.keys())

        # change the sorting, such that None is the last entry
        def sortkey(lang):
            return lang.upper() if lang.islower else lang.lower()
        self.supported_languages = sorted(languages, key=sortkey)

        def example_string(language):
            return ("{single[start]}single{single[end]}  -  "
                    "{double[start]}double{double[end]}"
                    .format(**quotes[language]))

        panel_entries = [[lang, example_string(lang)]
                         for lang in self.supported_languages]
        window = self.view.window()
        window.show_quick_panel(panel_entries, self.result)

    def result(self, value):
        if value != -1:
            language = self.supported_languages[value]
            self.set_current_language(language)


class InsertQuotesCommand(sublime_plugin.TextCommand, LanguageDetection):
    def extract_language(self):
        # check if the language is already set
        lang = self.get_current_language()
        if lang:
            return lang
        else:
            return self.auto_detect_language()

    def run(self, edit, quote_type=None, which_quote=None, language=None):
        if not quote_type:
            quote_type = "double"
        if not which_quote:
            which_quote = "both"
        if not language:
            language = self.extract_language()

        quote = quotes[language][quote_type]

        if which_quote == "open":
            for sel in self.view.sel():
                self.view.insert(edit, sel.begin(), quote["start"])

        elif which_quote == "close":
            for sel in self.view.sel():
                self.view.insert(edit, sel.end(), quote["end"])

        elif which_quote == "both":
            for sel in self.view.sel():
                self.view.insert(edit, sel.begin(), quote["start"])
            sels = []  # restore the sels, after the insertion
            for sel in self.view.sel():
                sels.append(sel)
                self.view.insert(edit, sel.end(), quote["end"])
            self.view.sel().clear()
            for sel in sels:
                self.view.sel().add(sel)
