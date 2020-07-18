import dash_core_components as dcc
import dash_html_components as html


def Row(children, flex=1, style=dict()):
    _style = { 'flex': flex }
    _style.update(style)
    return html.Div(children, className="row2", style=_style)

def RowElement(children, flex=1, style=dict()):
    _style = { 'flex': flex }
    _style.update(style)
    return html.Div(children, className="row-element2", style=_style)

def Column(children, flex=1, style=dict()):
    _style = { 'flex': flex }
    _style.update(style)
    return html.Div(children, className="column2", style=_style)

def ColumnElement(children, flex=1, style=dict()):
    _style = { 'flex': flex }
    _style.update(style)
    return html.Div(children, className="column-element2", style=_style)