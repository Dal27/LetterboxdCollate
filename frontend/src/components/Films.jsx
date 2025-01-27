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
            <div className="relative grid max-h-screen grid-cols-[1fr_2.5rem_auto_2.5rem_1fr] grid-rows-[1fr_1px_auto_1px_1fr]">
                <div className="col-start-3 row-start-3 min-w-lg flex-col p-2 ">
                    <div className="rounded-xl md:h-full bg-white p-10 text-sm/7">  

                        <h1 className='text-bluey'>Welcome to Letterboxd Collate</h1>
                        <UsernameInputForm username={username} onChange={handleChange} onSubmit={handleSubmit} />
                        {username && <p>Username: {username}</p>}
                    </div>
                </div>
            </div>
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