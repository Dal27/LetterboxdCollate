import PropTypes from 'prop-types';

const UsernameInputForm = ({ username, onChange, onSubmit }) => {
    return (
        <form className="mt-4" onSubmit={onSubmit}>
            <label>
                Username:
                <input className="border-b-2 divide-x border-mocha focus:outline-hidden" type="text" value={username} onChange={onChange}/>
            </label>
           <button type="submit" className="inline-block rounded border border-bluey bg-pinky px-12 py-3 mx-8 text-sm 
           font-medium text-amber-700 hover:bg-transparent hover:text-greeny hover:font-bold focus:outline-none focus:ring">
            Submit</button>

        </form>
    );
};

UsernameInputForm.propTypes = {
    username: PropTypes.string.isRequired,
    onChange: PropTypes.func.isRequired,
    onSubmit: PropTypes.func.isRequired,
};

export default UsernameInputForm;