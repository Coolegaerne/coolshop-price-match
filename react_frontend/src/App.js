import React from 'react';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Form from './components/Form';
import Success from './components/Success';
import Error from './components/Error';
import AlreadyExist from './components/AlreadyExist';

export function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Form />}/>
        <Route path="/success" element={<Success />} />
        <Route path="/error" element={<Error />} />
        <Route path="/already_exist" element={<AlreadyExist />} />
      </Routes>
    </Router>
  );
}

export default App;
