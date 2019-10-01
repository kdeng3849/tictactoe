from datetime import datetime
import json
import random

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .forms import AddUserForm, LoginForm
from .models import Game
from .tokens import account_activation_token

@csrf_exempt
def index(request):

    context = {
        "addUserForm": AddUserForm(),
        "loginForm": LoginForm(),
    }

    return render(request, 'ttt/index.html', context)

@csrf_exempt
def play(request):

    # check if logged in
    if not request.user.is_authenticated:
        return JsonResponse({"status": "ERROR"})

    data = json.loads(request.body.decode('utf-8'))
    move = data['move']

    if "grid" in request.session:
        grid = request.session['grid']
    else:
        grid = [' ']*9
        request.session['start_time'] = datetime.now().strftime("%m%d%y%H%M%S")
        new_game = Game(id=request.session['start_time'], user=request.user)
        new_game.save()
    
    if move is not None:
        move = int(move)
        grid[move] = 'X'
    else:
        return JsonResponse({"grid": grid})


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
            while grid[i] != ' ' and j < 9:
                i = random.randint(0, 8)
                j += 1
            grid[i] = 'O'

    winner = check_winner(grid)
    
    if winner == ' ':
        make_move(grid)
        winner = check_winner(grid)
        request.session['grid'] = grid

    # if there is a winner, or no more empty spaces (tie)
    if winner != ' ' or ' ' not in grid:
        start_time = request.session['start_time']
        try:
            game = Game.objects.get(id=start_time)
            game.grid = str(grid)
            game.winner = winner
            game.save()
        except Game.DoesNotExist:
            return JsonResponse({"status": "ERROR"})

        # start new game
        try:
            del request.session['start_time']
            del request.session['grid']
        except KeyError:
            pass

    return JsonResponse({"status": "OK", "grid": grid, "winner": winner})

@csrf_exempt
@require_http_methods(["POST"])
def add_user(request):

    data = json.loads(request.body.decode('utf-8'))
    form = AddUserForm(data)

    if form.is_valid():
        username, password, email = [form.cleaned_data.get('username'), form.cleaned_data.get('password'), form.cleaned_data.get('email')]

        # check if user already exists
        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            context = {
                "status": "ERROR",
            }
            return JsonResponse(context)

        # create user
        user = User.objects.create_user(username=username, password=password, email=email, is_active=False)
        user.save()

        current_site = get_current_site(request)
        mail_subject = 'Activate your ttt account.'
        # key = account_activation_token.make_token(user)
        message = render_to_string('ttt/email_verification.html', {
            'user': user,
            'domain': current_site.domain,
            'email': user.email,
            'key': 'abracadabra',
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()

        return JsonResponse({"status": "OK"})


@csrf_exempt
def verify(request):

    data = json.loads(request.body.decode('utf-8'))
    email = data['email']
    key = data['key']

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        user = None

    # if user is not None and account_activation_token.check_token(user, key):
    if user is not None and key == 'abracadabra':
        user.is_active = True
        user.save()

        return JsonResponse({"status": "OK"})

    return JsonResponse({"status": "ERROR"})

@csrf_exempt
@require_http_methods(["POST"])
def login_user(request):

    data = json.loads(request.body.decode('utf-8'))
    form = LoginForm(data)

    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            response = JsonResponse({"status": "OK"})
            login(request, user)
            request.session['username'] = username
            response.set_cookie('username', username)
            return response

    return JsonResponse({"status": "ERROR"})


@csrf_exempt
def logout_user(request):

    logout(request)
    response = JsonResponse({'status': 'OK'})
    response.delete_cookie('username')

    return response

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

    if request.user.is_authenticated:
        response = {
            'status': 'OK',
            'grid': '',
            'winner': '',
        }

        try:
            data = json.loads(request.body.decode('utf-8'))
            query = Game.objects.get(id=data['id'])
        except Game.DoesNotExist:
            return JsonResponse({"status": "ERROR"})

        response['grid'] = query.grid.replace('[', '').replace(']', '').replace("'", '').split(', ')
        response['winner'] = query.winner

        return JsonResponse(response)

    return JsonResponse({"status": "ERROR"})

@csrf_exempt
@require_http_methods(["POST"])
def get_score(request):

    if request.user.is_authenticated:
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

    return JsonResponse({"status": "ERROR"})
