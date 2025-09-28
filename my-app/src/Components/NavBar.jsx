import React from 'react';
import './OptionBar.css';
import { useNavigate} from 'react-router-dom';

export default function OptionBar() {
    const navigate = useNavigate();

    return (
        <nav>
            <button onClick={() => navigate('/')}>Home</button>
            <button onClick={() => navigate('/AboutSentiment')}>About Sentiment</button>
        </nav>
    );
}