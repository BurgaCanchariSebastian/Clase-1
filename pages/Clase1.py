import dash
import dash
from dash import html, dcc

dash.register_page(__name__, path='/Inicio', name='Inicio')

layout = html.Div([
    html.H1('Sebastian Burga Canchari', style={'textAlign': 'center', 'marginBottom': '30px'}),
    html.Div([
        # Columna izquierda: Biografía
        html.Div([
            html.H2('', style={'marginBottom': '10px'}),
            dcc.Markdown('''
Soy Sebastian Burga Canchari, una persona un poco introvertida cuando tengo confianza con las personas, actualmente tengo 20 años y tengo 2 hermosos
gatos rusos azules llamados "Eddy y Crash", estos nombres nacieron de las zarigueyas de la Era del Hielo, ya que un dia mi madre, les habia puesto de
ropa unas medias rayadas y parecian las zarigueyas, por lo que decidimos ponerles esos nombres y nos pareció divertido.

Me preparé en una academia llamada "Aula 20" la cual me regaló muy buenos momentos, amistades y conocimientos. Al principio no sabia que estudiar y habia elegido la carrera de Ingenieria Industrial,
por lo que mi preparación estuvo enfocada en ello, al dar mi primer examen, no logré ingresar por 5 puntos, lo cual me bajoneó un poco, pero no me 
di por vencido y decidí volver a intentar, en el transcurso de ello, hablé con mis tutores y me recomendaron ver otras carreras, entre ellas estaba
Computación Científica, la cual me llamó mucho la atención, investigué sobre ella y me gustó mucho, por lo que decidí cambiarme a esa carrera y me becaron
con el 50% de la pensión, lo cual me motivó aún más. Finalmente, me iban muy bien en los simulacros de la academia y logré ingresar a la Universidad 
Mayor de San Marcos en Admision 2023-II y así inicié mi camino en esta nueva etapa académica.

Mis primeros ciclos no fueron los mejores la verdad pero logré superar las dificultades y ahora tengo un buen pondero académico.

Siguiendo con un poco más de mi vida, soy una persona que le gusta mucho los videojuegos y en mis tiempos libre suelo jugar varios tipos de juegos,
entre ellos los principales son Shooters y MMORPG.

Mi familia tambien es muy importante para mi, a mi madre le encanta viajar mucho y uno de sus metas era que yo lograra sacar una licencia de conducir,
ya que ella siempre tuvo la idea de que yo maneje a los lugares que a ella le gustaria viajar y así sucedió, logré sacar mi licencia de conducir A-I 
y ahora puedo manejar por la ciudad e incluso ya realicé mi primer viaje "largo" que fue a la Ciudad de Ica, unas 4 horas y tambien sucedieron varias
anécdotas en el camino.

Y esto es un poco de mi, espero que les haya gustado conocerme un poco más.
            '''),
        ], style={
            'width': '70%',
            'display': 'inline-block',
            'verticalAlign': 'top',
            'paddingRight': '60px',
            'fontSize': '20px',  
            'lineHeight': '1',
        }),

        # Columna derecha: Foto
        html.Div([
            html.Img(
                src='/assets/foto.jpg',
                alt='Foto de Sebastian',
                style={
                    'width': '320px',
                    'height': 'auto',
                    'borderRadius': '8px',
                    'boxShadow': '0 4px 16px rgba(25, 118, 210, 0.15)',
                    'margin': '0 auto',
                    'display': 'block',
                }
            ),
        ], style={'width': '35%', 'display': 'inline-block', 'verticalAlign': 'top', 'textAlign': 'center'}),
    ], style={'width': '100%', 'display': 'flex', 'justifyContent': 'center'}),
])