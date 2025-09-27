import OptionBar from "./Components/NavBar";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import SentimentList from "./Components/Sentiment";

function Home() {
  return (
    <div>
      <h2>Home</h2>
      <SentimentList />
    </div>
  );

}

function Review() {
  return <h2>Submit a Review</h2>;
}

export default function MyApp() {
  return (
    <BrowserRouter>
      <OptionBar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/Review" element={<Review />} />
      </Routes>
    </BrowserRouter>
  );
}