const fs = require('fs');
const path = require('path');

// Задайте значение N в байтах
const N = 1024; // Пример: 1 килобайт

// Получаем текущую директорию
const currentDirectory = process.cwd();

// Читаем содержимое текущей директории
fs.readdir(currentDirectory, (err, files) => {
    if (err) {
        console.error('Произошла ошибка при чтении директории:', err);
        return;
    }

    // Фильтруем файлы по размеру
    const filteredFiles = files.filter((file) => {
        const filePath = path.join(currentDirectory, file);
        const stats = fs.statSync(filePath);
        return stats.isFile() && stats.size > N;
    });

    if (filteredFiles.length === 0) {
        console.log('Нет файлов, удовлетворяющих условию.');
    } else {
        console.log('Файлы, размер которых больше', N, 'байт:');
        filteredFiles.forEach((file) => {
            console.log(file);
        });
    }
});
