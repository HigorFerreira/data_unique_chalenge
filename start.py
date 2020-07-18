import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
from database_config.engine import engine

from modules.Layout import Row, RowElement, Column, ColumnElement, Table

programs = pd.read_sql("programm", engine)

app = dash.Dash(__name__,
                meta_tags=[
                    {
                        'name': 'viewport',
                        'content': 'width=device-width, initial-scale=1.0'
                    }
                ],
                external_stylesheets=[
                    'https://codepen.io/chriddyp/pen/bWLwgP.css']
                )

app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label="Análise", children=[
            html.Div([
                html.Div([
                    Column([
                        ColumnElement([
                            html.H4("Cursos")
                        ]),
                        ColumnElement([
                            RowElement([
                                dcc.Dropdown(
                                    "program-list",
                                    [{'label': element[1], 'value': element[0]}
                                     for element in programs.values.tolist()],
                                    value=20
                                )
                            ]),
                        ])
                    ],),
                ], id="program-list-container"),

                html.Div([
                    Column([
                        ColumnElement([
                            html.H4("Alunos Matriculados")
                        ]),
                        ColumnElement([
                            dcc.Dropdown("student-list",
                                         placeholder="Selecione o estudante")
                        ])
                    ]),
                ], id="students-list-container"),

                html.Div([

                ], id="grade-means-report-container"),

                html.Div(id="courses-container"),

            ], id="data-analysis-container"),

            html.Div(id="test"),
        ]),
        dcc.Tab(label="Inserção", children=[
            html.H1("hello")
        ])
    ])

], id="main-container")


@app.callback(
    Output("student-list", "options"),
    [Input("program-list", "value")]
)
def program_selected(program_id):
    students = pd.read_sql_query('''
        select * from students_program
        where program_id={}
    '''.format(program_id), engine)

    students = students.drop(columns=["subject", "program_id"])

    return [
        {
            'label': '{} {}'.format(students.iloc[i]['fname'], students.iloc[i]['lname']),
            'value': students.iloc[i]['id']
        } for i in range(0, len(students))
    ]


@app.callback(
    [
        Output("grade-means-report-container", "children"),
        Output("courses-container", "children")
    ],
    [Input("student-list", "value")],
    prevent_initial_call=True
)
def student_selected(value):

    student = pd.read_sql_query('''
        select * from semester_reports
        where student_id={}
    '''.format(value), engine)

    courses = student.drop(columns=[
                           "id", "student_id", "course_id", "first_name", "last_name", "subject", "mean"])
    courses = courses.rename(columns={
        'course': 'Matéria', 'semester_no': 'Semestre', 'year': 'Ano'
    })
    student = student.drop(columns=["id", "student_id", "course_id"])

    fig = px.line(student, x=range(0, len(student)), y="mean",
                  title="Variação de notas do histórico escolar - {}".format(
                      student.iloc[0]['first_name']),
                  labels={'mean': 'Médias', 'x': 'Matérias feitas'}
                  )

    # The use of dcc.Graph in the main layout causes an unrecognezed error
    # on CSS grid layout. Keeping this in mind, i'll return the entire Graph
    # from here
    graph_layout = dcc.Graph("student-report", True, figure=fig)
    courses_layout = html.Div([
        html.H6("Todas as matérias feitas"),
        Table(courses),
    ])
    return graph_layout, courses_layout

# @app.callback(
#     Output("test", "children"),
#     [ Input("student-report", "loading_state") ]
# )
# def loading_graph(loading):
#     print(loading)


if __name__ == '__main__':
    app.run_server()
