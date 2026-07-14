import { useState } from "react";
import SplashScreen from "./components/SplashScreen";
import Home from "./pages/Home";

export default function App() {
  const [showSplash, setShowSplash] = useState(true);

  return showSplash ? (
    <SplashScreen onFinish={() => setShowSplash(false)} />
  ) : (
    <Home />
  );
}
