$(function () {

    var winner = ' ';
    var grid = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '];

    $('.box').click(function () {
        play(this.id);
    });

    function fillGrid(grid) {
        for (var i = 0; i < grid.length; i++) {
            // document.getElementById(i).innerHTML = grid[i] == ' ' ? '-' : grid[i];
            document.getElementById(i).innerHTML = grid[i];
        }    
    }

    function play(id) {
        
        var box = document.getElementById(id);
        
        if(winner == ' ' && box.innerHTML == ' ') {
            box.innerHTML = 'X';

            data = {
                "play": id,
                "grid": grid,
            }
            fetch("/ttt/play", {
                method: "POST",
                mode: "cors",
                cache: "no-cache",
                credentials: "same-origin",
                headers: {
                    "Content-Type": "application/json"
                },
                redirect: "follow",
                referrer: "no-referrer",
                body: JSON.stringify(data)
            })
            .then(response => {
                return response.json();
            })
            .then(response => {
                console.log(response);
                grid = response.grid;
                winner = response.winner;
                fillGrid(grid);
                if(winner != ' ' || !grid.includes(' '))
                    document.getElementById("winner").innerHTML = "The winner is " + (winner != ' ' ? winner : "no one") + "."
            })
        }

    }
    if(document.getElementById("grid"))
        fillGrid(grid);
  });