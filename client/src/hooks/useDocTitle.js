import { useEffect } from 'react';

const useDocTitle = (title) => {
    useEffect(() => {
        if (title) {
            document.title = `${title} - PurePro`;
        } else {
            document.title = 'PurePro | The Perfect Protein Store';
        }
    }, [title]);

    return null;
};

export default useDocTitle;
