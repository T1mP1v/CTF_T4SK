<?php
session_start();

$target_dir = "uploads/";
$target_file = $target_dir . basename($_FILES["fileToUpload"]["name"]);
$uploadOk = 1;
$imageFileType = strtolower(pathinfo($target_file, PATHINFO_EXTENSION));

// Проверка, является ли файл изображением (проверка MIME-типа)
if(isset($_POST["submit"])) {
    $check = getimagesize($_FILES["fileToUpload"]["tmp_name"]);
    if($check !== false) {
        $uploadOk = 1;
    } else {
        $uploadOk = 0;
        $response = ["error" => "Файл не является изображением."];
    }
}

// Попытка загрузить файл, если проверки пройдены
if ($uploadOk == 1 && move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $target_file)) {
    $_SESSION['imageUrl'] = $target_file;
    header('Location: /index.php');
} else if ($uploadOk == 0 && !isset($response) && isset($_SESSION['imageUrl'])) {
    $response = ["error" => "Не удалось загрузить файл."];
    echo $responce;
}

?>
