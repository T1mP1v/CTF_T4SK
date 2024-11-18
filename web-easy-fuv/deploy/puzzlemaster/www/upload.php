<?php
session_start();
$target_dir = "uploads/";
$target_file = $target_dir . basename($_FILES["fileToUpload"]["name"]);
$uploadOk = 1;
$minFileSize = 2*1024;
$maxFileSize = 2*1024*1024;

if (isset($_POST["submit"])) {
    $uploadOk = 1;
    $response = ""; 

    // Проверка MIME-типа
    $check = getimagesize($_FILES["fileToUpload"]["tmp_name"]);
    if ($check === false) {
        $uploadOk = 0;
        $response = "Это не изображение.";
    }

    // Проверка размера файла
    if ($_FILES["fileToUpload"]["size"] > $maxFileSize) {
        $uploadOk = 0;
        $response = "Файл слишком большой. Максимальный размер — 2 МБ.";
    } elseif ($_FILES["fileToUpload"]["size"] < $minFileSize) {
        $uploadOk = 0;
        $response = "Файл слишком маленький. Минимальный размер — 10 КБ.";
    }

    if ($uploadOk == 1) {
        if (move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $target_file)) {
            echo "<script>
                    localStorage.clear();
                    localStorage.setItem('puzzleImageUrl', '" . $target_file . "');
                    window.location.href = 'index.php';
                  </script>";
            exit();
        } else {
            $response = "Ошибка при загрузке файла.";
        }
    }
   
    if ($response != "") {
        echo $response;
    }
}
?>
