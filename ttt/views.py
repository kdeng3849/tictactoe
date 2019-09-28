from datetime import date, datetime
import json, random

# from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.core import serializers
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .forms import AddUserForm, LoginForm
from .models import Game

# Create your views here.
@csrf_exempt
def index(request):

    # if request.method == "POST":
    #     if request.POST.get('username') not in ['', None]:
    #         username, email = [request.POST.get('username'), request.POST.get('email')]
    #         # name = request.POST.get('name')
    #         context = {
    #             "username": username,
    #             "email": email,
    #         }
    #         print(context)
    #         return render(request, 'ttt/index.html', context)

    #     # username, email = [request.POST.get('username'), request.POST.get('email')]
        
    form = AddUserForm()
    form2 = LoginForm()

    context = {
        "form": form,
        "form2": form2,
    }

    # if request.session.get('username'):
    #     context['username'] = request.session.get('username')
    
    return render(request, 'ttt/index.html', context)

@csrf_exempt
def play(request):

    data = json.loads(request.body.decode('utf-8'))
    grid = data['grid']

    def check_winner(grid):
        winner = ' '

        # all the winning combinations (horizontal, vertical, diagonal; top, mid, bottom; left, mid, right)
        ht = grid[0] + grid[1] + grid[2]
        hm = grid[3] + grid[4] + grid[5]
        hb = grid[6] + grid[7] + grid[8]

        vl = grid[0] + grid[3] + grid[6]
        vm = grid[1] + grid[4] + grid[7]
        vr = grid[2] + grid[5] + grid[8]
        
        dl = grid[0] + grid[4] + grid[8]
        dr = grid[2] + grid[4] + grid[6]

        winning_combos = [ht, hm, hb, vl, vm, vr, dl, dr]

        if 'XXX' in winning_combos:
            winner = 'X'
        elif 'OOO' in winning_combos:
            winner = 'O'

        return winner

    def fill_empty(grid, x, y, z):
        for i in range(x, y, z):
            if grid[i] == ' ':
                grid[i] = 'O'

    def make_move(grid):
        if ' ' not in grid:
            return

        ht = grid[0] + grid[1] + grid[2]
        hm = grid[3] + grid[4] + grid[5]
        hb = grid[6] + grid[7] + grid[8]

        vl = grid[0] + grid[3] + grid[6]
        vm = grid[1] + grid[4] + grid[7]
        vr = grid[2] + grid[5] + grid[8]
        
        dl = grid[0] + grid[4] + grid[8]
        dr = grid[2] + grid[4] + grid[6]

        action_combos = [' XX', 'X X', 'XX ', ' OO', 'O O', 'OO ']
        if ht in action_combos:
            fill_empty(grid, 0, 3, 1)
        elif hm in action_combos:
            fill_empty(grid, 3, 6, 1)
        elif hb in action_combos:
            fill_empty(grid, 6, 9, 1)
        elif vl in action_combos:
            fill_empty(grid, 0, 7, 3)
        elif vm in action_combos:
            fill_empty(grid, 1, 8, 3)
        elif vr in action_combos:
            fill_empty(grid, 2, 9, 3)
        elif dl in action_combos:
            fill_empty(grid, 0, 9, 4)
        elif dr in action_combos:
            fill_empty(grid, 2, 7, 2)
        else:
            i, j = [random.randint(0, 8), 0]
            print(i)
            while grid[i] != ' ' and j < 9:
                i = random.randint(0, 8)
                print(i)
                j += 1
            grid[i] = 'O'

    winner = check_winner(grid)
    
    if winner == ' ':
        make_move(grid)
        winner = check_winner(grid)

    # if there is a winner, or no more empty spaces (tie)
    if winner != ' ' or ' ' not in grid:
        start_time = datetime.now().strftime("%m%d%y%H%M%S")
        grid_str = str(grid)
        # grid_str = json.dumps(grid)
        # print(grid)
        # print(grid_str)
        game = Game(id=start_time, user=request.user, grid=grid_str, winner=winner)
        game.save()

    return JsonResponse({"grid": grid, "winner": winner})

@csrf_exempt
def add_user(request):

    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        form = AddUserForm(data)

        if form.is_valid():
            username, password, email = [form.cleaned_data.get('username'), form.cleaned_data.get('password'), form.cleaned_data.get('email')]
            # print(username, password, email)

            # check if user already exists
            if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
                # messages.warning(request, f'Account already exists for {username}.')
                # return render(request, 'ttt/index.html', { 'form': form })
                context = {
                    "status": "ERROR",
                }
                # print(context)
                return JsonResponse(context)

            # create user
            user = User.objects.create_user(username=username, password=password, email=email, is_active=True)
            user.save()
            # messages.success(request, f'Account created for {username}. Please validate your email.')

            # request.session['username'] = username
            context = {
                "status": "OK",
            }
            # return render(request, 'ttt/index.html', context)
            return JsonResponse(context)

    # NEEDED?
    form = AddUserForm()
    # return render(request, 'ttt/index.html', { 'form': form })
    return JsonResponse({"status": "ERROR"})

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        form = LoginForm(data)
        print("hello", form.is_valid())
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            print(user)
            if user is not None:
                login(request, user)
                request.session['username'] = username
                print(request.session['username'])
                # messages.info(request, f"You are now logged in as {username}.")
                response = JsonResponse({"status": "OK"})
                return response
            else:
                # messages.error(request, "Invalid username or password.")
                return JsonResponse({"status": "ERROR"})
        else:
            # messages.error(request, "Invalid username or password.")
            return JsonResponse({"status": "ERROR"})
    else:
        context = {
            "form":AddUserForm(),
            "form2": LoginForm(),
        }
        return render(request, 'ttt/index.html', context)

@csrf_exempt
def logout_user(request):
    # try:
    #     del request.session['username']
    # except KeyError:
    #     return JsonResponse({"status": "ERROR"})
    logout(request)
    return JsonResponse({"status": "OK"})

@csrf_exempt
def list_games(request):
    if request.user.is_authenticated:
        response = {
            'status': 'OK',
            'games': []
        }
        
        query = list(Game.objects.filter(user=request.user).values('id'))
        for game in query:
            response['games'].append({
                'id': game['id'],
            })

        return JsonResponse(response)

    return JsonResponse({"status": "ERROR"})

@csrf_exempt
@require_http_methods(["POST"])
def get_game(request):
    response = {
        'status': 'OK',
        'grid': '',
        'winner': '',
    }
    data = json.loads(request.body.decode('utf-8'))
    query = list(Game.objects.filter(user=request.user, id=data).values('grid', 'winner'))

    game = query[0]
    response['grid'] = game['grid']
    response['winner'] = game['winner']

    return JsonResponse(response)

@csrf_exempt
@require_http_methods(["POST"])
def get_score(request):
    response = {
        'status': 'OK',
        'human': 0,
        'wopr': 0,
        'tie': 0
    }

    query = list(Game.objects.filter(user=request.user).values('winner'))

    for game in query:
        if game['winner'] == 'X':
            response['human'] += 1
        elif game['winner'] == 'O':
            response['wopr'] += 1
        else:
            response['tie'] += 1

    return JsonResponse(response)