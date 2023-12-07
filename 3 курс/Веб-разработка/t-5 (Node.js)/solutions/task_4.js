const fs = require('fs');

// Задайте суффикс файла, например, '.txt'
const suffix = '.js';

// Получаем текущую директорию
const currentDirectory = process.cwd();

// Читаем содержимое текущей директории
fs.readdir(currentDirectory, (err, files) => {
    if (err) {
        console.error('Произошла ошибка при чтении директории:', err);
        return;
    }

    // Фильтруем файлы по суффиксу
    const filteredFiles = files.filter((file) => file.endsWith(suffix));

    if (filteredFiles.length === 0) {
        console.log(`Нет файлов с суффиксом "${suffix}" в текущем каталоге.`);
    } else {
        console.log(`Файлы с суффиксом "${suffix}" в текущем каталоге:`);
        filteredFiles.forEach((file) => {
            console.log(file);
        });
    }
});
