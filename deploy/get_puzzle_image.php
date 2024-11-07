<?php
session_start();

// Проверьте, существует ли изображение, и выдайте его URL
$imagePath = $_SESSION['imageUrl']; // Замените на правильный путь к вашему изображению

if (file_exists($imagePath)) {
    echo '"'.$imagePath.'"';
} else {
    $imagePath = '"uploads/art.jpg"';
    echo $imagePath;
}
?>