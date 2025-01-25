import { useState } from 'react';
import UsernameInputForm from './UsernameInputForm';
import api from '../api';

const Films = () => {
    const [username, setUsername] = useState('');
    const [recommendations, setRecommendations] = useState([]);

    const handleChange = (e) => {
        setUsername(e.target.value);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await api.post('/scrape_and_recommend', { username });
            setRecommendations(response.data);
        } catch (error) {
            console.error('Error fetching recommendations:', error);
        }
    };

    return (
        <div>
            <h1>Welcome to Letterboxd Collate</h1>
            <UsernameInputForm username={username} onChange={handleChange} onSubmit={handleSubmit} />
            {username && <p>Username: {username}</p>}
            <div>
                <h2>Recommendations</h2>
                <ul>
                    {recommendations.map((rec, index) => (
                        <li key={index}>{rec.title} ({rec.tmdb})</li>
                    ))}
                </ul>
            </div>
        </div>
    );
};

export default Films;