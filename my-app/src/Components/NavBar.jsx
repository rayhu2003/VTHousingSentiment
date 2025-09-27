import React from 'react';
import './OptionBar.css';

const OptionBar = () => {
    const handleOptionClick = (option) => {
        alert(`You clicked on ${option}`);
    }

    return (
        <div style={{ display: 'flex', gap: '10px', padding: '10px 0' }}>
            <button onClick={() => handleOptionClick('Option 1')}>Option 1</button>
            <button onClick={() => handleOptionClick('Option 2')}>Option 2</button>
            <button onClick={() => handleOptionClick('Option 3')}>Option 3</button>
        </div>
    );
};

export default OptionBar;