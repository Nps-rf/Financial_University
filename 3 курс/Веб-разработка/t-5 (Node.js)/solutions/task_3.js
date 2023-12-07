const fs = require('fs');
const path = require('path');

// Задайте значение N в днях
const N = 7; // Пример: 7 дней

// Получаем текущую директорию
const currentDirectory = process.cwd();

// Читаем содержимое текущей директории
fs.readdir(currentDirectory, (err, files) => {
    if (err) {
        console.error('Произошла ошибка при чтении директории:', err);
        return;
    }

    // Фильтруем файлы по дате корректировки
    const filteredFiles = files.filter((file) => {
        const filePath = path.join(currentDirectory, file);
        const stats = fs.statSync(filePath);
        const modificationDate = stats.mtime; // Дата корректировки файла

        // Рассчитываем разницу в днях между текущей датой и датой корректировки файла
        const currentDate = new Date();
        const daysDiff = Math.floor(
            (currentDate - modificationDate) / (24 * 60 * 60 * 1000)
        );

        return daysDiff <= N;
    });

    if (filteredFiles.length === 0) {
        console.log('Нет файлов, удовлетворяющих условию.');
    } else {
        console.log('Файлы, дата корректировки которых не позднее', N, 'дней назад:');
        filteredFiles.forEach((file) => {
            console.log(file);
        });
    }
});
