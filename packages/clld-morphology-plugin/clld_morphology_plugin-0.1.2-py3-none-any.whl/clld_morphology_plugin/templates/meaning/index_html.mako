<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "meanings" %>
<%block name="title">${_('Meanings')}</%block>

<h2>${title()}</h2>
<div>
    ${ctx.render()}
</div>

