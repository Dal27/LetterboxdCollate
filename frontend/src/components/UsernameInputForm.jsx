import PropTypes from 'prop-types';

const UsernameInputForm = ({ username, onChange, onSubmit }) => {
    return (
        <form onSubmit={onSubmit}>
            <label>
                Username:
                <input type="text" value={username} onChange={onChange} />
            </label>
            <button type="submit">Submit</button>
        </form>
    );
};

UsernameInputForm.propTypes = {
    username: PropTypes.string.isRequired,
    onChange: PropTypes.func.isRequired,
    onSubmit: PropTypes.func.isRequired,
};

export default UsernameInputForm;