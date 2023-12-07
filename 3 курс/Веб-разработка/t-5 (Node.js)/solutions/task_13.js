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

    // Создаем массив объектов с информацией о каждом каталоге
    const directoryInfo = [];

    // Функция для асинхронного подсчета файлов и каталогов в каждом каталоге
    function countFilesAndDirectories(dirName, callback) {
        const dirPath = path.join(currentDirectory, dirName);
        fs.readdir(dirPath, { withFileTypes: true }, (err, subFiles) => {
            if (err) {
                console.error(`Произошла ошибка при чтении каталога ${dirName}:`, err);
                callback(null, 0, 0);
            } else {
                const subDirectories = subFiles.filter((subFile) => subFile.isDirectory());
                callback(null, subFiles.length, subDirectories.length);
            }
        });
    }

    // Асинхронно получаем информацию о каждом каталоге
    let processedCount = 0;
    directories.forEach((dir) => {
        countFilesAndDirectories(dir.name, (err, fileCount, subDirectoryCount) => {
            if (!err) {
                directoryInfo.push({ name: dir.name, fileCount, subDirectoryCount });
            }
            processedCount++;

            // После обработки всех каталогов выводим результат
            if (processedCount === directories.length) {
                // Сортируем каталоги по числу файлов и каталогов
                directoryInfo.sort((a, b) => {
                    const aTotal = a.fileCount + a.subDirectoryCount;
                    const bTotal = b.fileCount + b.subDirectoryCount;
                    return bTotal - aTotal;
                });

                // Выводим имена каталогов и информацию
                console.log('Каталоги, упорядоченные по числу файлов и каталогов:');
                directoryInfo.forEach((info) => {
                    console.log(`Каталог: ${info.name}, Число файлов: ${info.fileCount}, Число подкаталогов: ${info.subDirectoryCount}`);
                });
            }
        });
    });

    if (directories.length === 0) {
        console.log('В текущей директории нет каталогов.');
    }
});
