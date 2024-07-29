import React from 'react';


const TSComponentTest: React.FC = () => {
    let myString: string = "This is ts indeed"
    return (
        <div>Hello from TypeScript: {myString}</div>
    );
};

export default TSComponentTest;
