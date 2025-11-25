import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import UploadData from './pages/UploadData';
import OntologyList from './pages/OntologyList';
import VisualizeOntology from './pages/VisualizeOntology';
import ViewOntology from './pages/ViewOntology';
import './App.css';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/upload" element={<UploadData />} />
        <Route path="/list" element={<OntologyList />} />
        <Route path="/visualize" element={<VisualizeOntology />} />
        <Route path="/view" element={<ViewOntology />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
