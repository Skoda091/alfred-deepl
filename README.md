DeepL translation worklflow for Alfred
-----------------

Utilize DeepL api translator.

![](/demo/deepl-workflow-demo.gif "")

Download
--------

Get DeepL for Alfred from [GitHub](https://github.com/Skoda091/alfred-deepl/releases).

Usage
-----

* `dlset` — Set target language fot DeepL.com translation.

**Supported languages:**

| Code | Language  | Icon                     |
| ---- | --------- | ------------------------ |
| DE   | German    |![](/lang_icons/de.png "")|
| EN   | English   |![](/lang_icons/en.png "")|
| FR   | French    |![](/lang_icons/fr.png "")|
| ES   | Spanish   |![](/lang_icons/es.png "")|
| IT   | Italian   |![](/lang_icons/it.png "")|
| NL   | Dutch     |![](/lang_icons/nl.png "")|
| PL   | Polish    |![](/lang_icons/pl.png "")|

* `dl <text>` — Search DeepL.com for `<text>` translation.

* `<lang> <text>` — Search DeepL.com for `<text>` translation into `<lang>`.

Disclaimer
-----

This is not an official package. It is 100% open source and non-commercial. The API of DeepL.com is free as well, but this [might](https://www.heise.de/newsticker/meldung/Maschinelles-Uebersetzen-Deutsches-Start-up-DeepL-will-230-Sprachkombinationen-unterstuetzen-3836533.html) change in the future.

DeepL is a product from DeepL GmbH. More info: deepl.com/publisher.html

To do
-----------------

* [x] Initial release
* [x] Errors handling
* [x] Updates handling
* [x] Multiple target languages support
* [ ] Simultaneous translation into multiple languages

Licensing, thanks
-----------------

This workflow is released under the [MIT License](https://opensource.org/licenses/MIT).

It is based on:
* [Alfred-Workflow](https://github.com/deanishe/alfred-workflow) [[MIT License](https://opensource.org/licenses/MIT)]
* [DeepL-Console-Translator](https://github.com/pinae/DeepL-Console-Translator.git) [[GNU License](https://www.gnu.org/licenses/gpl-3.0.en.html)]


[alfred]: https://www.alfredapp.com/
[mit]: http://opensource.org/licenses/MIT
[alfred-workflow]: http://www.deanishe.net/alfred-workflow/
