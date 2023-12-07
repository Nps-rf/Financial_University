const fs = require('fs');
const path = require('path');

// Имена подкаталогов для сравнения (замените на нужные)
const subdirectory1 = 'test_folder';
const subdirectory2 = 'folder_with_child';

// Получаем текущую директорию
const currentDirectory = process.cwd();

// Функция для получения списка файлов и каталогов в заданной директории
function getDirectoryContents(directory) {
    const directoryPath = path.join(currentDirectory, directory);
    try {
        return fs.readdirSync(directoryPath);
    } catch (err) {
        return [];
    }
}

// Получаем список файлов и каталогов в обоих подкаталогах
const contents1 = getDirectoryContents(subdirectory1);
const contents2 = getDirectoryContents(subdirectory2);

// Функция для сравнения списков и вывода несовпадающих элементов
function compareDirectoriesContents(list1, list2, directory1, directory2) {
    const differences = [];

    list1.forEach((item1) => {
        if (!list2.includes(item1)) {
            differences.push(path.join(directory1, item1));
        }
    });

    list2.forEach((item2) => {
        if (!list1.includes(item2)) {
            differences.push(path.join(directory2, item2));
        }
    });

    return differences;
}

// Сравниваем содержимое подкаталогов и выводим несовпадающие элементы
const differences = compareDirectoriesContents(contents1, contents2, subdirectory1, subdirectory2);

if (differences.length === 0) {
    console.log('Содержимое указанных подкаталогов идентично.');
} else {
    console.log('Несовпадающие элементы в указанных подкаталогах:');
    differences.forEach((difference) => {
        console.log(difference);
    });
}
