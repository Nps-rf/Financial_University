const fs = require('fs');
const path = require('path');

// Получаем текущую директорию
const currentDirectory = process.cwd();

// Задаем количество дней N (замените на желаемое число)
const N = 7; // Например, для последних 7 дней

// Вычисляем дату N дней назад от текущей даты
const dateNdaysAgo = new Date();
dateNdaysAgo.setDate(dateNdaysAgo.getDate() - N);

// Читаем содержимое текущей директории
fs.readdir(currentDirectory, { withFileTypes: true }, (err, files) => {
    if (err) {
        console.error('Произошла ошибка при чтении директории:', err);
        return;
    }

    // Фильтруем файлы, проверяя их дату модификации
    const recentFiles = files.filter((file) => {
        const filePath = path.join(currentDirectory, file.name);
        const stats = fs.statSync(filePath);
        return stats.mtime >= dateNdaysAgo;
    });

    if (recentFiles.length === 0) {
        console.log(`В текущей директории нет файлов или директорий, измененных за последние ${N} дней.`);
    } else {
        console.log(`Файлы и директории, измененные за последние ${N} дней в текущей директории:`);
        recentFiles.forEach((file) => {
            console.log(file.name);
        });
    }
});
