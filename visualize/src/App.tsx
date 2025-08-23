import { useEffect, useState } from 'react'
import './App.css'

type Language = 'en' | 'en_s' | 'de' | 'de_s' | 'fr' | 'fr_s' | 'it' | 'it_s'

const DEFAULT_LANGUAGE: Language = 'de'

type Description = {
    id: string,
    name: string,
    language: 'en' | 'en_s' | 'de' | 'de_s' | 'fr' | 'fr_s' | 'it' | 'it_s'
    text: string,
}

type AsyncAction = () => Promise<void>

const exampleDescription: Description = {
    id: 'asldkfasldkfj',
    name: 'Worb',
    language: 'en',
    text: 'This is the description of the Worb Dorf station...'
}

function App() {
    const [query, querySet] = useState('');
    const [language, setLanguage] = useState(DEFAULT_LANGUAGE);

    const [data, dataSet] = useState<Description[]>([])
    const [suggestedResults, suggestedResultsSet] = useState<Description[]>([])
    const [description, descriptionSet] = useState<Description | null>(null)
    const [error, errorSet] = useState<string | null>(null)

    const handleChange: React.ChangeEventHandler<HTMLInputElement> = (e) => {
        const value = e.target.value;
        querySet(value);
        if (value) {
            const filtered = data.filter((item) =>
                item.name.toLowerCase().includes(value.toLowerCase())
            );
            suggestedResultsSet(filtered);
        } else {
            suggestedResultsSet([]);
        }
    };

    const handleSuggestionClick = (item: Description) => {
        querySet(item.name);
        suggestedResultsSet([]);
    };

    const handleSearch = () => {
        console.log('X')
        const foundList = data.filter((item) =>
            item.name.toLowerCase().includes(query.toLowerCase())
        );

        if (foundList.length == 0) {
            errorSet('not found')
            suggestedResultsSet([])
            descriptionSet(null)
            querySet('')
        } else if (foundList.length > 1) {
            errorSet('more than one result')
            descriptionSet(null)
        } else {
            const found = foundList[0]
            errorSet(null)
            suggestedResultsSet([])
            querySet(found.name)
            descriptionSet(found);
        }
    };

    const onPageLoad: AsyncAction = async () => {
        // await fetch.apply...
        dataSet([exampleDescription])
        return Promise.resolve()
    }

    useEffect(() => {
        onPageLoad()
    }, [])

    const handleKeyDown: React.KeyboardEventHandler<HTMLInputElement> = (e) => {
        console.log('key down')
        if (e.key === "Enter") {
            console.log('enter')
            e.preventDefault();
            handleSearch();
        }
    };


    return (
        <>
            <div className='controls'>

                {/* choose language */}
                <select
                    value={language}
                    onChange={(e) => setLanguage(e.target.value as Language)}
                >
                    <option value='en'>English</option>
                    <option value='de'>Deutsch</option>
                    <option value='fr'>Français</option>
                    <option value='it'>Italiano</option>
                </select>

                {/* search */}
                <input
                    type='text'
                    value={query}
                    onChange={handleChange}
                    onKeyDown={handleKeyDown}
                    placeholder=''
                />
                <ul>
                    {suggestedResults.map((item, index) => (
                        <li
                            key={index}
                            onClick={() => handleSuggestionClick(item)}
                        >
                            {item.name}
                        </li>
                    ))}
                </ul>

                <button onClick={handleSearch}>Show</button>
            </div>
            <div className='problem'>
                {error ? <p>{error}</p> : <></>}
            </div>
            <div className='result'>
                {description ? <p>{description.text}</p> : <></>}
            </div>

        </>
    )
}

export default App
