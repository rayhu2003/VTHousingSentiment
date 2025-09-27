import OptionBar from "./Components/NavBar";
import { BrowserRouter, Routes, Route } from "react-router-dom";

function Home() {
  return <h2>Home Page</h2>;
}

function About() {
  return <h2>About Page</h2>;
}

function Contact() {
  return <h2>Contact Page</h2>;
}

export default function MyApp() {
  return (
    <BrowserRouter>
      <OptionBar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="/contact" element={<Contact />} />
      </Routes>
      <div>
        <h1>Welcome to My App</h1>
      </div>
    </BrowserRouter>
  );
}