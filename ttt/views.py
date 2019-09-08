from datetime import date
import json, random

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

# from .forms import NameForm

# Create your views here.
@csrf_exempt
def index(request):

    if request.method == "POST":
        if request.POST.get('name') not in ['', None]:
            name = request.POST.get('name')
            context = {
                "name": name,
            }
            print("hello", name)
            return render(request, 'ttt/index.html', context)
    
    return render(request, 'ttt/index.html')

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

    return JsonResponse({"grid": grid, "winner": winner})