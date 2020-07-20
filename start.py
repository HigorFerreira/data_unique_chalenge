from template.dash import Dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px
from database_config.engine import engine

from modules.Layout import Row, RowElement, Column, ColumnElement, Table

programs = pd.read_sql("programm", engine)

app = Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.Img(src='assets/logo.png')
    ], className="header"),
    html.Div([
        dcc.Tabs(id="tabs", children=[
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

                    html.Div(id="grade-means-report-container"),
                    html.Div(id="courses-container"),
                    html.Div(id="extra"),

                ], id="data-analysis-container"),

                html.Div(id="test"),
            ]),
            dcc.Tab(label="Inserção", children=[
                html.Div(id="input-data-container", children=[
                    html.H3("Cadastro de Estudante:"),
                    Row([
                        Column([
                            html.H6("Curso"),
                            dcc.Dropdown(
                                "program-list-input",
                                [{'label': element[1], 'value': element[0]} for element in programs.values.tolist()],
                            )
                        ])
                    ]),
                    Row([
                        RowElement([
                            Column([
                                html.H6("Nome"),
                                dcc.Input(id="fname", placeholder="Digite o seu nome")
                            ]),
                        ], 6),
                        RowElement([
                            Column([
                                html.H6("Matrícula"),
                                dcc.Input(id="student-no", placeholder="A matrícula do estudante", type="number")
                            ]),
                        ], 3)
                    ]),
                    Row([
                        Column([
                            html.H6("Sobrenome"),
                            dcc.Input(id="lname", placeholder="Digite o seu sobrenome")
                        ]),
                    ]),
                    Row([
                        RowElement([], 9),
                        RowElement([
                            html.Button("Enviar", id="send-button")
                        ], 0, {
                            'marginTop': '10px'
                        })
                    ])
                ])
            ])
        ]),
    ], style={ 'padding': '0 8px' }),
    html.Script(id="script-injection")

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
        Output("courses-container", "children"),
        Output("extra", "children"),
    ],
    [Input("student-list", "value")],
    prevent_initial_call=True
)
def student_selected(value):

    student = pd.read_sql_query('''
        select * from semester_reports
        where student_id={}
    '''.format(value), engine)

    statistics = student.describe()

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
        html.H4("Todas as matérias feitas"),
        Table(courses),
    ])
    extra_data_layout = html.Div([
        html.H4("Statísticas"),
        html.P("Nota mais baixa: {}".format(statistics['mean']['min'])),
        html.P("Nota mais alta: {}".format(statistics['mean']['max'])),
        html.P("Média global: {}".format(
            round(statistics['mean']['mean'], 2))),
    ], style={
        'backgroundColor': '#8395a7',
        'padding': '15px 40px',
        'borderRadius': '10px',
    })
    return graph_layout, courses_layout, extra_data_layout,

# @app.callback(
#     Output("test", "children"),
#     [ Input("student-report", "loading_state") ]
# )
# def loading_graph(loading):
#     print(loading)

# Script injection isn't a good practice, use event listener in next commit instead
@app.callback(
    Output("script-injection", "children"),
    [ Input("send-button", "n_clicks") ],
    [
        State("program-list-input", "value"),
        State("student-no", "value"),
        State("fname", "value"),
        State("lname", "value"),
    ],
    prevent_initial_call=True
)
def sending_forms(clicks, program, no, name, lname):
    # print('''
    # INSERTED DATA
    # Name: {name} {lname}
    # No: {no}
    # P Code: {program}
    # '''.format(
    #     name=name,
    #     lname=lname,
    #     program=program,
    #     no=no
    # ))
    with engine.connect() as con:
        query_response = con.execute('''
            INSERT INTO student(fname, lname, program_id, student_no)
            VALUES ('{fname}', '{lname}', {program_id}, {student_no});
        '''.format(
            fname=name,
            lname=lname,
            program_id=program,
            student_no=no
        ))
        print(query_response)
    return "location.reload()"


if __name__ == '__main__':
    app.run_server(port=3001)
