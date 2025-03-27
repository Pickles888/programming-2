import asyncio
import base64
import tornado
import pokepy
import requests

client = pokepy.V2Client()

wallpaper_link = 'https://imgix.ranker.com/user_node_img/50065/1001282845/original/quick-ball-photo-u1?fit=crop&fm=pjpg&q=60&w=650&dpr=2'

def base64Image(data) -> str:
    return base64.b64encode(data).decode('utf-8')

def getSpriteData(pokemon) -> str: 
    sprite_data = requests.get(pokemon.sprites.front_default)
    
    return base64Image(sprite_data.content)

def capitalize(s: str)  -> str:
    if len(s) == 0:
        return ""
    
    lower = s.lower()
    
    return lower[0].upper() + lower[1:]

def mkCss() -> str: # THANK YOU CHATGPT <3
    return ' '.join([
        '''
        body, html {
            margin: 0;
            padding: 0;
            height: 100%;
            display: flex;
            justify-content: center;  /* Horizontally center the content */
            align-items: center;  /* Vertically center the content */
            background-size: 75px 75px;
            background-position: left top;
            background-image: url(\'''', wallpaper_link, '\');',
        '}',
        
        '''
        .container {
            display: flex;
            width: 80%;  /* Or whatever width you want */
            /*max-width: 1200px;  /* Optional: to limit the max size */*/
            justify-content: space-between; /* Distribute the panes with space between */
        }
        ''',
        
        '''
        .pane {
            padding: 20px;
            background-color: #f4f4f4;
            border: 1px solid #ddd;
            width: 600px;
            display: flex;
            flex: 1;
            flex-direction: column;
            overflow: auto;
        }
        ''',

        '''
        .poketitle-name {
            float: left;
            font-size: 50px;
        }
        ''',
        
        '''
        .lift-aligned {
            text-align: left;
        }
        ''',
        
        '''
        .right-aligned {
            text-align: right;
        }
        ''',
        
        '''
        .stat-column {
            flex-direction: column;
            padding-top: 5px;
            padding-bottom: 5px;
        }
        ''',
        
        '''
        .stat {
            padding: 5px;
        }
        ''',
        
        '''
        .stat-title {
            font-size: 30px;
        }
        ''',
        
        '''
        .abilities-title {
            font-size: 30px;
        }
        ''',
        
        '''
        .abilities-column {
            flex-direction: column
            padding-top: 5px;
            padding-bottom: 5px;
        }
        ''',
        
        '''
        .ability {
            padding: 5px;
        }
        ''',
        
        '''
        .root-container {
            flex-direction: column;
            align-items: center;
            display: flex;
        }
        ''',
        
        '''
        .search {
            width: 70%;
            align-items: center;
        }
        ''',
        
        '''.item {
            padding-top: 5px;
            padding-bottom: 5px;
        }''',
        
        '''
        img {
            image-rendering: pixelated;
            image-rendering: -moz-crisp-edges;
            image-rendering: crisp-edges;
        }
        '''
    ])

def div(content: str, css="") -> str:
    return '<div class="' + css + '">' + str(content) + '</div>'

def getStats(pokemon) -> str:
    return ''.join(map(lambda a: '<div class="stat">' + capitalize(a.stat.name) + ': ' + str(a.base_stat) + '</div>', pokemon.stats))

def getAbilities(pokemon) -> str:
    return ''.join(map(lambda a: '<div class="ability">' + a.ability.name + '</div>', pokemon.abilities))

def getTypes(pokemon) -> str:
    return 'Type: ' + ', '.join(map(lambda a: capitalize(a.type.name), pokemon.types))

def makePokemonPageBase(pokemon) -> list[str]:
    return [
        '<body>',
            '<div class="root-container">',
                '<form action="/" method="post">',
                    '<input type="text" id="name" name="name" required>',
                    '<input type="submit" value="Search">',
                '</form>',
                '<div class="container">',
                    '<div class="pane" style="background-color: lightblue;">',
                        '<img src="data:image/png;base64,', getSpriteData(pokemon), '" alt="', pokemon.name, '\'s sprite" width="500" height="500">',
                    '</div>',
                    '<div class="pane" style="background-color: lightgreen;">',
                        '<div class="poketitle-name">',
                            capitalize(pokemon.name) + " - " + str(pokemon.id),
                        '</div>',
                        '<div>',
                            div(getTypes(pokemon), css="item"),
                            div('Weight: ' + str(pokemon.weight), css="item"),
                            '<div>',
                                '<div class="stat-title">',
                                    'Stats',
                                '</div>',
                                '<div class="stat-column">',
                                    getStats(pokemon),
                                '</div>',
                            '</div>'
                            '<div>',
                                '<div class="abilities-title">',
                                    'Abilities',
                                '</div>',
                                '<div class="abilities-column">',
                                    getAbilities(pokemon),
                                '</div>',
                            '</div>'
                        '</div>',
                    '</div>',
                '</div>',
            '</div>',
        '</body>'
    ]

def mkHTML(htmlBase: list[str], css: str) -> str:
    return "".join(
        ["<html>"] +
        ["<head>"] +
        ["<style>"] + 
            [css] + 
        ["</style>"] +
        ["</head>"] +
            htmlBase +
        ["</html>"]
    )

# Frontend Server Stuff (driver code)

class MainHandler(tornado.web.RequestHandler):
    picked_pokemon = 'pikachu'
    
    def get(self):
        try:
            pokemon = client.get_pokemon(self.picked_pokemon)[0]
            self.write(mkHTML(makePokemonPageBase(pokemon), mkCss()))
        except Exception as e:
            self.write(f"Error: {str(e)}")

    def post(self):
        pokemon_name = self.get_argument("name")
        print('Searched: ' + pokemon_name)
        self.picked_pokemon = pokemon_name
        self.get()
 

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

async def main():
    app = make_app()
    app.listen(8888)
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
