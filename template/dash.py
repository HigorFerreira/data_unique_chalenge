import dash

class Dash(dash.Dash):
    def interpolate_index(self, **kwargs):
        return '''
            <!DOCTYPE html>
            <html>
                <head>
                    <title>DATA UNIQUE</title>
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <link rel="stylesheet" href="https://codepen.io/chriddyp/pen/bWLwgP.css">
                    {metas}
                    {css}
                </head>
                <body>
                    {app_entry}
                    {config}
                    {scripts}
                    {renderer}
                </body>
            </html>
        '''.format(
            app_entry=kwargs['app_entry'],
            config=kwargs['config'],
            scripts=kwargs['scripts'],
            renderer=kwargs['renderer'],
            metas=kwargs['metas'],
            css=kwargs['css']
            )