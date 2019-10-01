$(function () {

    var winner = ' ';
    var grid = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '];

    function showPage(page) {
        $('.page').hide()
        $('#' + page).show()
    }

    $('#test').click(() => {
        var data = {
            "id": "093019215306"
        }
        
        fetch("/getgame", {
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
        })
    })

    $('button.signup').click(() => {
        showPage('signup');
    })

    $('button.login').click(() => {
        showPage('login');
    })

    $('button.reset').click(() => {
        resetGame();
    })

    $('.box').click(function () {
        play(this.id);
    });

    $('#signupForm').submit(function(event) {
        event.preventDefault();

        var data = $(this).serializeArray().reduce((dict, field) => {
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
                renderView();
        })
    })

    $('#loginForm').submit(function(event) {
        event.preventDefault();

        var data = $(this).serializeArray().reduce((dict, field) => {
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
                renderView();
                resetGame();
        })
    })

    $('button.logout').click(function(event) {
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
                renderView();
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

            var data = {
                "move": id
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
                if(winner != ' ' || !grid.includes(' ')) {
                    document.getElementById("winner").innerHTML = (winner != ' ' ? winner : "No one") + " won.";
                    $("button.reset").show()
                }
            })
        }
    }

    function getCookie(cname) {
        var name = cname + "=";
        var ca = document.cookie.split(';');
        for(var i = 0; i < ca.length; i++) {
            var c = ca[i];
            while (c.charAt(0) == ' ') {
                c = c.substring(1);
            }
            if (c.indexOf(name) == 0) {
                return c.substring(name.length, c.length);
            }
        }
        return "";
    }

    function resetGame() {
        winner = ' ';
        grid = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '];
        fillGrid(grid);
        document.getElementById("winner").innerHTML = "";
        $("button.reset").hide();
    }

    function renderView() {
        if(getCookie("username")) {
            showPage("play")
            $("button.signup").hide()
            $("button.login").hide()
            $("button.logout").show() 
        }
        else {
            showPage("login")
            $("button.signup").show()
            $("button.login").show()
            $("button.logout").hide()
        }
    }

    function initializeView() {
        fillGrid(grid);
        renderView();
        $("button.reset").hide();
    }

    initializeView();

  });