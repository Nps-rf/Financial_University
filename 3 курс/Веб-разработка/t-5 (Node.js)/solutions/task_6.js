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

    // Фильтруем папки
    const folders = files.filter((file) => file.isDirectory());

    // Проверяем, что каждая папка не содержит подпапок
    const topLevelFolders = [];
    folders.forEach((folder) => {
        const folderPath = path.join(currentDirectory, folder.name);
        const subFolders = fs.readdirSync(folderPath, { withFileTypes: true })
            .filter((subFolder) => subFolder.isDirectory());

        if (subFolders.length === 0) {
            topLevelFolders.push(folder.name);
        }
    });

    if (topLevelFolders.length === 0) {
        console.log('В текущей директории нет папок без подпапок.');
    } else {
        console.log('Папки без подпапок в текущей директории:');
        topLevelFolders.forEach((folder) => {
            console.log(folder);
        });
    }
});
