const fs = require('fs');
const path = require('path');

// Имя нового каталога
const newDirectoryName = 'НовыйКаталог';

// Количество файлов для копирования (замените на желаемое число)
const N = 5; // Например, скопировать 5 файлов

// Получаем текущую директорию (родительский каталог)
const parentDirectory = process.cwd();

// Создаем новый каталог
const newDirectoryPath = path.join(parentDirectory, newDirectoryName);
fs.mkdir(newDirectoryPath, (err) => {
    if (err) {
        console.error('Ошибка при создании нового каталога:', err);
        return;
    }

    // Читаем содержимое текущей директории (родительского каталога)
    fs.readdir(parentDirectory, { withFileTypes: true }, (err, files) => {
        if (err) {
            console.error('Произошла ошибка при чтении директории:', err);
            return;
        }

        // Фильтруем только файлы (не каталоги)
        const filesOnly = files.filter((file) => file.isFile());

        // Сортируем файлы по размеру в убывающем порядке
        filesOnly.sort((a, b) => {
            const fileAPath = path.join(parentDirectory, a.name);
            const fileBPath = path.join(parentDirectory, b.name);
            const statsA = fs.statSync(fileAPath);
            const statsB = fs.statSync(fileBPath);
            return statsB.size - statsA.size;
        });

        // Выбираем первые N файлов (с наибольшими размерами) для копирования
        const filesToCopy = filesOnly.slice(0, N);

        // Копируем выбранные файлы в новый каталог
        filesToCopy.forEach((file) => {
            const sourceFilePath = path.join(parentDirectory, file.name);
            const destinationFilePath = path.join(newDirectoryPath, file.name);

            fs.copyFile(sourceFilePath, destinationFilePath, (err) => {
                if (err) {
                    console.error(`Ошибка при копировании файла ${file.name}:`, err);
                } else {
                    console.log(`Скопирован файл ${file.name} в новый каталог.`);
                }
            });
        });
    });
});
