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

    // Фильтруем только каталоги
    const directories = files.filter((file) => file.isDirectory());

    // Для каждого каталога, считаем количество файлов
    directories.forEach((dir) => {
        const dirPath = path.join(currentDirectory, dir.name);
        fs.readdir(dirPath, (err, subFiles) => {
            if (err) {
                console.error(`Произошла ошибка при чтении каталога ${dir.name}:`, err);
            } else {
                console.log(`Каталог: ${dir.name}, Количество файлов: ${subFiles.length}`);
            }
        });
    });

    if (directories.length === 0) {
        console.log('В текущей директории нет каталогов.');
    }
});
