<!DOCTYPE html>
<html>
<head>
<style>
 body{height:97vh;padding:0;display:grid;align-content:center;justify-content:center;}
</style>
</head>


 <form id="uploadForm" action="upload.php" method="post" enctype="multipart/form-data">
    Выберите изображение для загрузки:
    <input type="file" name="fileToUpload" id="fileToUpload">
    <input type="submit" value="Загрузить изображение" name="submit">
</form>
<body>
<div id='fifteen'></div>
<script>
    var p = {
        "diff": "100",
        "size": [
            400,
            400
        ],
        "grid": [
            3,
            3
        ],
        "fill": false,
        "number": false,
        "art": {
            "url": "", // обновится после fetch
            "ratio": false
        },
        "keyBoard": true,
        "gamePad": true,
        "time": 0.1,
        "style": "background-color:#c4cebb;display:grid;justify-items:center;align-items:center;font-family:Arial;color:#fff;border-radius:17px;font-size:33px;"
    }, freeslot = [], size = [], m = [], o, f = document.getElementById("fifteen");
    fetch('get_puzzle_image.php', { method: 'GET' })
    .then(response => response.text()) 
    .then(data => {
        //alert(data); 
        p.art.url = data // Устанавливаем URL изображения
    })
</script>
<script src="fifteen_puzzle.js"></script>
</body>
</html>
