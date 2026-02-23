import React from 'react';

const Component = () => {
    const isActive = true;
    return (
        <div className={`container ${isActive ? 'active' : ''}`}>
            <span className="text-bold">Hello</span>
            <button className="btn btn-secondary">Action</button>
        </div>
    );
};

export default Component;
