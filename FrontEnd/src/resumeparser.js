import axios from "axios";
import React, { useState } from "react";

const ResumeParser = () => {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const parseResume = async () => {
    const formData = new FormData();
    formData.append("file", file);
    setLoading(true);
    try {
      const res = await axios.post("http://localhost:8000/parse-resume/", formData);
      setResult(res.data);
    } catch (err) {
      alert("Parsing failed");
    }
    setLoading(false);
  };

  return (
    <div>
      <input type="file" onChange={e => setFile(e.target.files[0])} />
      <button onClick={parseResume}>Parse</button>
      {loading && <p>Loading...</p>}
      {result && (
        <div>
          <h4>Parsed Data</h4>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

export default ResumeParser;
