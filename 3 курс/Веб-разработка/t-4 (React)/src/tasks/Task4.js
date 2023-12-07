import React, { useState } from 'react';

import { PrismLight as SyntaxHighlighter } from 'react-syntax-highlighter';
import javascript from 'react-syntax-highlighter/dist/esm/languages/prism/javascript';
import darcula from 'react-syntax-highlighter/dist/esm/styles/prism/darcula';

SyntaxHighlighter.registerLanguage('javascript', javascript);

export function Task4() {
    const [code, ] = useState('import fs from \'fs\';\n' +
        'import path from \'path\';\n' +
        '\n' +
        '/**\n' +
        ' * Получает все файлы с заданным расширением из указанной директории.\n' +
        ' *\n' +
        ' * @param {string} dirPath - Путь к директории.\n' +
        ' * @param {string} ext - Расширение файлов для поиска (например, \'.js\').\n' +
        ' * @return {Array<string>} - Массив путей к файлам.\n' +
        ' */\n' +
        'function getFilesWithExtension(dirPath, ext) {\n' +
        '    let result = [];\n' +
        '    const files = fs.readdirSync(dirPath);\n' +
        '\n' +
        '    for (const file of files) {\n' +
        '        const filePath = path.join(dirPath, file);\n' +
        '        const stat = fs.statSync(filePath);\n' +
        '\n' +
        '        if (stat.isDirectory()) result = result.concat(getFilesWithExtension(filePath, ext));\n' +
        '        else if (path.extname(file) === ext) result.push(filePath);\n' +
        '    }\n' +
        '\n' +
        '    return result;\n' +
        '}\n' +
        '\n' +
        '// Пример использования\n' +
        'void function () {\n' +
        '    const dirPath = \'./\';\n' +
        '    const ext = \'.js\';\n' +
        '    const files = getFilesWithExtension(dirPath, ext);\n' +
        '    console.info(files);\n' +
        '}()\n'); // Initial code

    const runCode = () => {
        // Code to send 'code' to the server to run
        // For example, you might use the fetch API to POST the code to a server-side route
        fetch('/run-code', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ code })
        })
            .then(response => response.json())
            .then(data => {
                console.log('Server response:', data);
            });
    };

    const darkContainerStyle = {
        backgroundColor: 'rgba(60,81,93,0.6)', // Darcula-like background color
        color: 'white',
        padding: '20px',
        borderRadius: '8px'
    };

    return (
        <div className="container animate__animated animate__fadeIn" style={darkContainerStyle}>
            <div className="row mt-5">
                <div className="col-12">
                    <h2>Node.js Runtime</h2>
                </div>
            </div>

            <div className="row mt-3">
                <div className="col-12">
                    <SyntaxHighlighter language='javascript' style={darcula} showLineNumbers={true}>
                        {code}
                    </SyntaxHighlighter>
                </div>
            </div>

            <div className="row mt-3">
                <div className="col-12">
                    <button className="btn btn-primary" onClick={runCode}>
                        Run
                    </button>
                </div>
            </div>
        </div>
    );
}

export default Task4;
