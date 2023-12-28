# clld-morphology-plugin

A plugin for modelling morphology in CLLD apps.

[![Versions](https://img.shields.io/pypi/pyversions/clld_morphology_plugin)](https://www.python.org/)
[![PyPI](https://img.shields.io/pypi/v/clld_morphology_plugin.svg)](https://pypi.org/project/clld_morphology_plugin)
[![License](https://img.shields.io/github/license/fmatter/clld-morphology-plugin)](https://www.apache.org/licenses/LICENSE-2.0)

## Models
The [models](/src/clld_morphology_plugin/models.py) largely reflect the structure of the morphological components of the [cldf-ldd](https://github.com/fmatter/cldf-ldd) collection.

The basic mechanism of segmentation is implemented such that `Wordform`s and `Stem`s have a list column `parts` containing the segmentation.
These parts are referenced via indices by `WordformPart`s, `StemPart`s, and `WordformStem`s, so these entities "know" their constituents.
X`Parts` can in turn be referenced by `Inflection`s, meaning that `InflectionalValue`s (which belong to `InflectionalCategorie`s) are associated with part of a wordform.
Wordform structure and inflectional information is rendered as follows:

<img src="https://user-images.githubusercontent.com/2378389/221690084-36690385-7f9d-4bd6-99ac-d87c1964f06b.png" width="50%" height="50%">

`Morpheme` detail view with `Morph`s, inflectional values, and wordforms/corpus tokens:

<img src="https://user-images.githubusercontent.com/2378389/221693305-6e97c3be-b0cc-455a-b435-fd9ac9ddf585.png" width="30%" height="30%">

If a `WordformPart` is not associated with a `Morph`, this is interpreted as zero marking (usually for inflection):
<img src="https://user-images.githubusercontent.com/2378389/221693358-7f8d3ffe-d008-4efe-a49c-b90c7de1e7dc.png" width="60%" height="60%">

Morphophonological change is modeled by `MorphoPhonoInstance`s connecting `MorphoPhonologicalChange`s with one or more of the following things: an `Inflection`, a `WordformPart`, or a `StemPart`:

<img src="https://user-images.githubusercontent.com/2378389/221693377-b45ae02b-45b0-4480-9b10-7b271cdb56cc.png" width="50%" height="50%">

Since `InflectionalValue`s are connected via `Inflection`s to `WordformPart`s, their exponents can be easily visualized:
<img src="https://user-images.githubusercontent.com/2378389/221693413-3d95b17c-b67b-434d-8db3-68e9ffe99a4b.png" width="50%" height="50%">

`Stems` can have a `Lexeme`, and `WordformPart`s + `Wordforms` + `InflectionalValue` + `InflectionalCategory` contain all the necessary information to automatically generate inflectional paradigms for lexemes:
<img src="https://user-images.githubusercontent.com/2378389/221693515-b0adcf48-f68a-4040-9f7e-47898bc73b38.png" width="100%" height="100%">

`Derivation`s connect `Stems` with other `Stem`s (or `Morph`s, when derived from a root) and `DerivationalProcess`es.
These derivational links can then be used to render the "derivational lineage" of a stem:

<img src="https://user-images.githubusercontent.com/2378389/221693470-9c811e78-8fef-45be-a648-fb73c6314dc7.png" width="70%" height="70%">

Detail views of stems also show all derived (directly or indirectly) stems:
<img src="https://user-images.githubusercontent.com/2378389/221693580-91e07656-3b0b-401c-b961-a5f5ca7dc1d0.png" width="70%" height="70%">

`DerivationalProcess`es know what stems they create (optionally using specific morphs):
<img src="https://user-images.githubusercontent.com/2378389/221693636-6f952768-ebda-4966-9b3b-10f5e0e8be8c.png" width="60%" height="60%">




## Markdown
Since this plugin is primarily being developed for an [interactive digital corpus-based grammar](https://github.com/fmatter/indicogram), comments on models are rendered using markdown.
However, it is up to the app developer to choose what markdown you want to use; the templates here assume that the parent mako template provides a function `markdown(request, content)`.
If you want to use the [clld-markdown-plugin](https://github.com/clld/clld-markdown-plugin/), use the following code in your top-level `.mako`:

    <%def name="markdown(request, content)">
        <%from clld_markdown_plugin import markdown%>
        ${markdown(request, content)|n}
    </%def>

to use plain markdown instead:

    <%def name="markdown(request, content)">
        <%from markdown import Markdown%>
        ${Markdown(content)|n}
    </%def>
