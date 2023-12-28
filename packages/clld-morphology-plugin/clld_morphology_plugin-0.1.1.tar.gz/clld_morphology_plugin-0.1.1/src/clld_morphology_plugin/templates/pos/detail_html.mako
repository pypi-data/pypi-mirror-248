<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%from clld_morphology_plugin import models%>
<%! active_menu_item = "pos" %>


<h3>${ctx.name.capitalize()} (Part of speech, ${ctx.id})</h3>

% if ctx.description:
    <p>${ctx.description}</p>
% endif

<div class="tabbable">
    <ul class="nav nav-tabs">
        % if ctx.wordforms:
            <li class='active'><a href="#wordforms" data-toggle="tab"> Wordforms </a></li>
        % endif
        % if ctx.lexemes:
            <li class=${'' if ctx.wordforms else 'active'}><a href="#lexemes" data-toggle="tab"> Lexemes </a></li>
        % endif
        % if ctx.morphs:
            <li class=${'' if (ctx.lexemes + ctx.wordforms) else 'active'}><a href="#morphs" data-toggle="tab"> Morphs </a></li>
        % endif
    </ul>

    <div class="tab-content" style="overflow: visible;">

        <div id="wordforms" class="tab-pane ${'active' if ctx.wordforms else ''}">
            ${request.get_datatable('wordforms', models.Wordform, pos=ctx).render()}
        </div>

        <div id="lexemes" class="tab-pane ${'' if (ctx.wordforms) else 'active'}">
            % if ctx.wordforms:
                ${request.get_datatable('lexemes',models.Lexeme, pos=ctx).render()}
            % endif
        </div>

        <div id="morphs" class="tab-pane ${'' if (ctx.wordforms + ctx.lexemes) else 'active'}">
            ${request.get_datatable('morphs',models.Morph, pos=ctx).render()}
        </div>

    </div>  
</div>

<p>${h.text2html(h.Markup(ctx.markup_description or ""))}</p>