import pandas as pd
import numpy as np
from engine import engine

# Database main schema creation
with engine.connect() as con:
    query = open('tables_creation.sql', "rt").read()
    con.execute(query)

# Sedding programs table
f = open("programs.txt")
data = pd.Series(f)
df = pd.DataFrame(data, columns=[ 'subject' ])
df.to_sql(
    name='programm',
    index=False,
    con=engine,
    if_exists='append'
)
f.close()

# Seeding courses table and assigning it to computer engineering program
f = open("courses.txt")
data = pd.Series(f)
program_id = pd.Series(np.full((len(data)), 20))
df = pd.concat([ data, program_id ], axis=1, keys=[ 'name', 'program_id' ])
df.to_sql(
    name='courses',
    index=False,
    con=engine,
    if_exists='append'
)
f.close()

# Creating a fictional student called Higor
df = pd.DataFrame(
    data=[
        [
            'Higor',
            'Ferreira Alves Santos',
            'hfas',
            '123456',
            20,
            201620033
        ]
    ],
    columns=[ 'fname', 'lname', 'login', 'pass', 'program_id', 'student_no' ]
)
df.to_sql(
    name='student',
    index=False,
    con=engine,
    if_exists='append'
)


# Seeding a fictional semestral report of grade means
df = pd.DataFrame(pd.read_json('espelho_escolar.json'))
df = df.drop(columns=[ 'course' ])
df.to_sql(
    name='semester',
    index=False,
    con=engine,
    if_exists='append'
)