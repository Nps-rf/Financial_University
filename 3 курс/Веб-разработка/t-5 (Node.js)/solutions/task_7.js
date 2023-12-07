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

    // Проверяем, что каждая папка содержит подпапки
    const foldersWithSubfolders = [];
    folders.forEach((folder) => {
        const folderPath = path.join(currentDirectory, folder.name);
        const subFolders = fs.readdirSync(folderPath, { withFileTypes: true })
            .filter((subFolder) => subFolder.isDirectory());

        if (subFolders.length > 0) {
            foldersWithSubfolders.push(folder.name);
        }
    });

    if (foldersWithSubfolders.length === 0) {
        console.log('В текущей директории нет папок, содержащих подпапки.');
    } else {
        console.log('Папки, содержащие подпапки в текущей директории:');
        foldersWithSubfolders.forEach((folder) => {
            console.log(folder);
        });
    }
});
