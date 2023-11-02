// noinspection JSCheckFunctionSignatures

import React, {useState, useEffect, useRef} from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'animate.css';
import Task4 from "./tasks/Task4";

function App() {

    const [tasks, ] = useState([
        ['Задание 1', () => setActiveSolution(<div className={`alert alert-primary animate__animated ${animationClass}`}>React.js поднят</div>)],
        ['Задание 2', () => {
            setActiveSolution(<TaskLocalStorage />,
                'animate__fadeOut'
            );
        }],
        ['Задание 3', () => setActiveSolution(<TableExample />, 'animate__fadeIn')],
        ['Задание 4', () => setActiveSolution(<Task4 />, 'animate__zoomIn')],
        ['Задание 5', () => setActiveSolution(<div className={`alert alert-danger ${animationClass}`}><b>Задание находится в разработке</b></div>,
            'animate__zoomOut')],
    ]);

    const [activeTask, setActiveTask] = useState(null);
    const [activeSolution, setActiveSolution] = useState(null);
    const [animationClass] = useState('animate__zoomIn');

    const solutionRef = useRef(null); // Create a ref

    const handleTaskClick = (index, invoke) => {
        setActiveTask(index);

        const el = solutionRef.current;

        // Add the 'zoomOut' class and remove it after animation
        el.classList.add('animate__zoomOut');
        setTimeout(() => el.classList.remove('animate__zoomOut'), 500);

        // Wait for the zoom-out animation to complete before zooming in
        setTimeout(() => {
            // Invoke the function to set the new activeSolution
            invoke();

            // Add the 'zoomIn' class and remove it after animation
            el.classList.add('animate__zoomIn');

        }, 500);
    };

    const TaskLocalStorage = () => {

        const [storageData, setStorageData] = useState(Object.entries(localStorage));

        // Re-read localStorage when component mounts
        useEffect(() => {
            setStorageData(Object.entries(localStorage));
        }, []);

        const updateLocalStorage = () => {
            const key = document.getElementById('key').value;
            const value = document.getElementById('value').value;
            localStorage.setItem(key, value);
            // Update state to force re-render
            setStorageData(Object.entries(localStorage));

            document.getElementById('key').value = '';
            document.getElementById('value').value = '';
        };

        return (
            <div className={`animate__animated ${animationClass}`} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '10px' }}>

                <div style={{ width: '50%', marginBottom: '10px' }}>
                    <label>Ключ</label>
                    <input
                        type="text"
                        className="form-control"
                        id="key"
                    />
                </div>

                <div style={{ width: '50%', marginBottom: '10px' }}>
                    <label>Значение</label>
                    <input
                        type="text"
                        className="form-control"
                        id="value"
                    />
                </div>

                <button
                    type="button"
                    className="btn btn-primary"
                    onClick={() => updateLocalStorage()}
                >
                    Обновить данные
                </button>

                <div style={{ marginTop: '10px' }}>
                    <strong>Текущие данные:</strong>
                    <table className="table table-dark table-hover table-striped table-bordered">
                        <thead>
                        <tr>
                            <th>Ключ</th>
                            <th>Значение</th>
                        </tr>
                        </thead>
                        <tbody>
                        {storageData.map(([key, value]) => (
                            <tr key={key}>
                                <td>{key}</td>
                                <td>{value}</td>
                            </tr>
                        ))}
                        </tbody>
                    </table>
                </div>
                <button className="btn btn-danger" onClick={() => {
                    localStorage.clear();
                    setStorageData(Object.entries(localStorage));
                }}>Очистить</button>
            </div>
        )
    }

    const TableExample = () => {
        const [rows, setRows] = useState([1, 2, 3]);

        const addRow = () => setRows([...rows, rows.length + 1]);
        const removeRow = () => setRows(rows.slice(0, -1));

        return (
            <div className={`container animate__animated ${animationClass}`}>
                <button className="btn btn-success m-2" onClick={addRow}>Добавить строку</button>
                <button className="btn btn-danger m-2" onClick={removeRow}>Удалить строку</button>
                <table className="table table-dark">
                    <thead>
                    <tr>
                        <th>Строка</th>
                    </tr>
                    </thead>
                    <tbody>
                    {rows.map((row, index) => (
                        <tr key={index}>
                            <td>{row}</td>
                        </tr>
                    ))}
                    </tbody>
                </table>
            </div>
        );
    };

    return (
        <div className="App vh-100 bg-dark text-white">
            <div className="position-fixed top-0 start-50 translate-middle-x">
                <h1 className="text-center text-white mb-5 h2-responsive animate__animated animate__fadeIn">Задания</h1>

                <div className="d-flex flex-wrap justify-content-center mb-5 animate__animated animate__fadeInDown">
                    {tasks.map(([name, invoke], index) => (
                        <div
                            className={`btn btn-primary m-3 p-3 ${activeTask === index ? 'bg-success animate__animated animate__tada' : 'bg-secondary'} text-white shadow-lg`}
                            key={index}
                            onClick={() => handleTaskClick(index, invoke)}
                        >
                            {name}
                        </div>
                    ))}
                </div>
            </div>

            <div className="d-flex flex-column align-items-center justify-content-center h-100">
                <div ref={solutionRef}  className={`text-center mt-5 animate__animated ${activeSolution ? 'animate__fadeIn' : 'animate__fadeOutUp'}`}>
                    {activeSolution}
                </div>
            </div>
        </div>
    );
}

export default App;

