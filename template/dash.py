import dash

class Dash(dash.Dash):
    def interpolate_index(self, **kwargs):
        print(kwargs)
        return '''
            <!DOCTYPE html>
            <html>
                <head>
                    <title>DATA UNIQUE</title>
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