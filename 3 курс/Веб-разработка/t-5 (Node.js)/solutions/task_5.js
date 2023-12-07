const fs = require('fs');

// Задайте шаблон для поиска файлов
const pattern = /.*fg.D/;

// Получаем текущую директорию
const currentDirectory = process.cwd();

// Читаем содержимое текущей директории
fs.readdir(currentDirectory, (err, files) => {
    if (err) {
        console.error('Произошла ошибка при чтении директории:', err);
        return;
    }

    // Фильтруем файлы по шаблону
    const filteredFiles = files.filter((file) => pattern.test(file));

    if (filteredFiles.length === 0) {
        console.log(`Нет файлов, удовлетворяющих шаблону "${pattern}".`);
    } else {
        console.log(`Файлы, удовлетворяющие шаблону "${pattern}" в текущей папке:`);
        filteredFiles.forEach((file) => {
            console.log(file);
        });
    }
});
