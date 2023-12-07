const fs = require('fs');
// Получаем текущую директорию
const currentDirectory = process.cwd();

// Читаем содержимое текущей директории
fs.readdir(currentDirectory, { withFileTypes: true }, (err, files) => {
    if (err) {
        console.error('Произошла ошибка при чтении директории:', err);
        return;
    }

    let folderCount = 0;

    // Перебираем элементы в текущей директории
    files.forEach((file) => {
        if (file.isDirectory()) {
            folderCount++;
            console.log(`Имя папки: ${file.name}`);
        }
    });

    console.log(`Всего папок в текущей директории: ${folderCount}`);
});
