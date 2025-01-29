import { useState } from 'react';
import UsernameInputForm from './UsernameInputForm';
import api from '../api';
import StatusUpdate from './StatusUpdate';

const Films = () => {
    const [username, setUsername] = useState('');
    const [recommendations, setRecommendations] = useState([]);
    const [loading, setLoading] = useState(0);

    const handleChange = (e) => {
        setUsername(e.target.value);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(1); // Validating profile
        try {
            setLoading(2); // Gathering and generating movies
            const response = await api.post('/scrape_and_recommend', { username });
            setRecommendations(response.data);
            setLoading(3); // Done
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
                        <UsernameInputForm username={username} onChange={handleChange} onSubmit={handleSubmit}/>
                        <StatusUpdate loading={loading} username={username} />
                    </div>
                </div>
            </div>
            <div>
                <h2>Recommendations</h2>
                <div className="overflow-y-auto h-96 mt-6">
                    <ul className="grid grid-cols-3 gap-2">
                        {recommendations.map((rec, index) => (
                            <li key={index} className="text-center">
                                <a href={`https://www.themoviedb.org/movie/${rec.tmdb}`} target="_blank" rel="noopener noreferrer">
                                    <img src={rec.poster} alt={`Poster for ${rec.title}`} className="w-24 h-24 mx-auto" />
                                </a>
                                <p>{rec.title}</p>
                            </li>
                        ))}
                    </ul>
                </div>
            </div>
        </div>
    );
};

export default Films;