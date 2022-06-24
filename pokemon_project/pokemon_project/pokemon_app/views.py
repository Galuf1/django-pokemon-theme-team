import random
from django.shortcuts import render
from django.http import HttpResponse
import requests
import pprint



pp = pprint.PrettyPrinter(indent=2, depth=4)

# Create your views here.
def index(request):
    # we get this call to get the amount of pokemon available to randomize
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon-species/?limit=0")
    limit = response.json()['count']
    random_num = random.randrange(0, limit, 1)
    # we get the first random pokemon, assign the teams type and store the first sprite 
    id = request.GET.get("id") or random_num
    first_pokemon = requests.get(f'https://pokeapi.co/api/v2/pokemon/{id}')
    pokeType = first_pokemon.json()['types'][0]['type']['url']
    image = first_pokemon.json()['sprites']['front_default']
    # with the type we request a list of all the pokemons with that type to randomize
    team = requests.get(pokeType)
    team_list = {0:image}
    for i in range(1,6):
        random_team_number = random.randrange(0,len(team.json()['pokemon']))
        if random_team_number < limit:
            random_team_url = team.json()['pokemon'][random_team_number]['pokemon']['url']
        else:
            pass
        get_team_sprites = requests.get(random_team_url)
        team_list[i] = get_team_sprites.json()['sprites']['front_default']
    # print(team_list)
    # print(type(team_list))
    return render(request, "pokemon_app/index.html", {'team_list':team_list})


    

    