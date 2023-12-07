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

    // Функция для изменения прав доступа к файлу
    function changeFilePermissions(file) {
        const filePath = path.join(currentDirectory, file.name);

        // Изменяем права доступа на чтение только для владельца
        fs.chmod(filePath, '444', (err) => {
            if (err) {
                console.error(`Ошибка при изменении прав доступа к файлу ${file.name}:`, err);
            } else {
                console.log(`Права доступа к файлу ${file.name} изменены: редакторы стали читателями.`);
            }
        });
    }

    // Применяем функцию изменения прав доступа к каждому файлу
    files.forEach((file) => {
        changeFilePermissions(file);
    });
});
