$(function () {

    var winner = ' ';
    var grid = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '];

    function showPage(page) {
        $('.page').hide()
        $('#' + page + "Page").show()
    }

    $('#signupButton').click(() => {
        showPage('signup');
    })

    $('#loginButton').click(() => {
        showPage('login');
    })

    $('.box').click(function () {
        play(this.id);
    });

    $('#signupForm').submit(function(event) {
        event.preventDefault();

        data = $(this).serializeArray().reduce((dict, field) => {
            dict[field.name] = field.value;
            return dict;
        }, {});
        
        fetch("/adduser", {
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
            
            if(response.status == "OK")
                showPage('play');
        })
    })

    $('#loginForm').submit(function(event) {
        event.preventDefault();

        data = $(this).serializeArray().reduce((dict, field) => {
            dict[field.name] = field.value;
            return dict;
        }, {});
        
        fetch("/login", {
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

            if(response.status == "OK")
                showPage('play');
        })
    })

    $('#logoutButton').click(function(event) {
        fetch("/logout", {
            method: "GET",
            mode: "cors",
            cache: "no-cache",
            credentials: "same-origin",
            headers: {
                "Content-Type": "application/json"
            },
            redirect: "follow",
            referrer: "no-referrer",
        })
        .then(response => {
            return response.json();
        })
        .then(response => {
            console.log(response);

            if(response.status == "OK")
                showPage('login');
        })
    })

    function fillGrid(grid) {
        for (var i = 0; i < grid.length; i++) {
            document.getElementById(i).innerHTML = grid[i];
        }    
    }

    function play(id) {
        
        var box = document.getElementById(id);
        
        // only if there isn't a winner AND box is empty
        if(winner == ' ' && box.innerHTML == ' ') {
            box.innerHTML = 'X';
            // grid[id] = 'X'

            data = {
                // "grid": grid,
                "move": id // parse int?
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