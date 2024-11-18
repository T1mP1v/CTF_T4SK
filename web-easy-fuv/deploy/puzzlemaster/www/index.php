<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>PuzzleMaster</title>
    <link rel="stylesheet" href="css/style.css"> 
    <link href="https://fonts.googleapis.com/css?family=Josefin+Sans" rel="stylesheet">
</head>
<body>
    <div class="container-fluid">
        <div class="background">
            <div class="puzzle-title">Собери пазл :)</div>
            <div class="puzzle-container">
                <div id="fifteen"></div>
                <form id="uploadForm" class="hidden" action="upload.php" method="post" enctype="multipart/form-data">
                    Выберите изображение для загрузки:
                    <input type="file" name="fileToUpload" id="fileToUpload">
                    <input type="submit" value="Загрузить изображение" name="submit">
                </form>
            </div>
        </div>
    </div>
    <script>
        var p = {
            "diff": "100",
            "size": [400, 400],
            "grid": [3, 3],
            "fill": false,
            "number": false,
            "art": {
                "url": localStorage.getItem('puzzleImageUrl') || "uploads/15-puzzle.svg.png", 
                "ratio": false
            },
            "keyBoard": true,
            "gamePad": true,
            "time": 0.1,
            "style": "background-color:#c4cebb;display:grid;justify-items:center;align-items:center;font-family:Arial;color:#fff;border-radius:17px;font-size:33px;"
        }, freeslot = [], size = [], m = [], o, f = document.getElementById("fifteen");
    </script>
    <script src="fifteen_puzzle.js"></script>
</body>
</html>
