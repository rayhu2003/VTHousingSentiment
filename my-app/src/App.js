import OptionBar from "./Components/NavBar";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import SentimentList from "./Components/Sentiment";

function Home() {
  return (
    <div>
      <SentimentList />
    </div>
  );

}

function AboutSentiment() {
  return (
    <>
      <h2 style={{ textAlign: "center", marginBottom: "40px" }}>How Sentiment Analysis Works</h2>
      <p style={{ maxWidth: "800px", margin: "0 auto", lineHeight: "1.6", padding: "0 20px", fontSize: "18px", textIndent: "40px" }}>
        Sentiment analysis is a natural language processing (NLP) technique used to determine the emotional tone behind a series of words. This is particularly useful in understanding customer feedback, social media conversations, and other forms of text data.
        To gather data we looked at top 10 posts on public forums such as Reddit and stored the texts of the post and their comments. We then used Gemini 
        in order to give a sentiment score from 1 to 10 where 5 is neutral, anything below 5 is negative, and anything above 5 is positive. We analyzed sentiments based on three categories: maintenance, distance, and environment. 
      </p>
    </>
  );
}

export default function MyApp() {
  return (
    <BrowserRouter>
      <OptionBar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/AboutSentiment" element={<AboutSentiment />} />
      </Routes>
    </BrowserRouter>
  );
}