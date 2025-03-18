import { useEffect, useState } from "react";
import axios from "axios";

const API_URL = "http://127.0.0.1:8000/thoughts/";

function App() {
  const [thoughts, setThoughts] = useState([]);
  const [text, setText] = useState("");

  useEffect(() => {
    fetchThoughts();
  }, []);

  const fetchThoughts = async () => {
    try {
      const response = await axios.get(API_URL);
      setThoughts(response.data);
    } catch (error) {
      console.error("Error fetching thoughts:", error);
    }
  };

  const submitThought = async (e) => {
    e.preventDefault();
    if (!text.trim()) return;

    try {
      await axios.post(API_URL, { text });
      setText("");
      fetchThoughts();
    } catch (error) {
      console.error("Error posting thought:", error);
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white flex flex-col items-center p-6">
      <h1 className="text-3xl font-bold mb-4">💭 Share your thoughts</h1>

      <form
        onSubmit={submitThought}
        className="w-full max-w-md bg-gray-800 p-4 rounded-lg shadow-lg"
      >
        <textarea
          className="w-full p-2 bg-gray-700 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400"
          rows="3"
          placeholder="Share your thought..."
          value={text}
          onChange={(e) => setText(e.target.value)}
        />
        <button
          type="submit"
          className="w-full mt-2 bg-blue-500 hover:bg-blue-600 text-white py-2 rounded-md"
        >
          Share Thought
        </button>
      </form>

      <div className="w-full max-w-md mt-6 space-y-3">
        {thoughts.length === 0 ? (
          <p className="text-gray-400">No thoughts shared yet. Be the first!</p>
        ) : (
          thoughts.map((thought) => (
            <div
              key={thought.id}
              className="bg-gray-800 p-4 rounded-lg shadow-md"
            >
              <p className="text-gray-300">{thought.text}</p>
              <p className="text-gray-500 text-sm mt-2">
                Shared on {new Date(thought.timestamp).toLocaleString()}
              </p>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default App;
