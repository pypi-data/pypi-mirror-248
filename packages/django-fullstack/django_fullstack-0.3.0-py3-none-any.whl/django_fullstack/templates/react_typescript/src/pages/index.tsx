import { useState } from 'react';
import reactLogo from './assets/react.svg';
import viteLogo from '/vite.svg';

const App: React.FC = () => {
  const [count, setCount] = useState<number>(0);

  return (
    <div className="font-sans text-base leading-6 font-normal">
      <div>
        <a href="https://vitejs.dev" target="_blank" rel="noopener noreferrer">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank" rel="noopener noreferrer">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1 className="text-4xl leading-5 font-bold">Vite + React</h1>
      <div className="card">
        <button
          onClick={() => setCount((count) => count + 1)}
          className="rounded-lg border border-transparent px-3 py-2 font-medium bg-gray-800 text-white hover:border-purple-600 focus:border-purple-600 focus:outline-none focus:border-4"
        >
          count is {count}
        </button>
        <p>
          Edit <code className="font-mono">src/App.tsx</code> and save to test HMR
        </p>
      </div>
      <p className="text-gray-500">
        Click on the Vite and React logos to learn more
      </p>
    </div>
  );
};

export default App;
