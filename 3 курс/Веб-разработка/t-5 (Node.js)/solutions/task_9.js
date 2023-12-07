const fs = require('fs');
const path = require('path');

// Получаем текущую директорию
const currentDirectory = process.cwd();

// Читаем содержимое текущей директории
fs.readdir(currentDirectory, { withFileTypes: true }, (err, files) => {
    if (err) {
        console.error('Произошла ошибка при чтении директории:', err);
        return;
    }

    // Разделяем файлы и каталоги
    const directories = [];
    const filesOnly = [];

    files.forEach((file) => {
        const filePath = path.join(currentDirectory, file.name);
        const stats = fs.statSync(filePath);

        if (file.isDirectory()) {
            directories.push({ name: file.name, size: stats.size });
        } else {
            filesOnly.push({ name: file.name, size: stats.size });
        }
    });

    // Сортируем каталоги и файлы по размеру
    directories.sort((a, b) => a.size - b.size);
    filesOnly.sort((a, b) => a.size - b.size);

    // Выводим каталоги
    console.log('Каталоги:');
    directories.forEach((dir) => {
        console.log(dir.name);
    });

    // Выводим файлы
    console.log('Файлы:');
    filesOnly.forEach((file) => {
        console.log(file.name);
    });
});
