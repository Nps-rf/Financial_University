const fs = require('fs');
const path = require('path');

// Получаем текущую директорию
const currentDirectory = process.cwd();

// Читаем содержимое текущей директории
fs.readdir(currentDirectory, (err, files) => {
    if (err) {
        console.error('Произошла ошибка при чтении директории:', err);
        return;
    }

    // Фильтруем файлы, исключая каталоги
    const filesOnly = files.filter((file) => {
        const filePath = path.join(currentDirectory, file);
        return fs.statSync(filePath).isFile();
    });

    // Сортируем файлы в алфавитном порядке
    filesOnly.sort();

    // Выводим имена файлов
    console.log('Файлы в алфавитном порядке:');
    filesOnly.forEach((file) => {
        console.log(file);
    });
});
