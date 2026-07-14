import { motion } from "framer-motion";
import { useEffect } from "react";
import "../styles/splash.css";

import detective from "../assets/detective.png";

export default function SplashScreen({ onFinish }) {

  useEffect(() => {

    const timer = setTimeout(() => {

      if (onFinish) onFinish();

    }, 3500);

    return () => clearTimeout(timer);

  }, [onFinish]);



  return (

    <div className="splash-container">

      {/* Background Glow */}
      <div className="background-glow"></div>

      {/* Floating Particles */}

      <div className="particles">

        <span></span>
        <span></span>
        <span></span>
        <span></span>
        <span></span>
        <span></span>

      </div>

      {/* AI Detective */}

      <motion.img

        src={detective}

        className="detective"

        animate={{
          y: [0, -12, 0],
          rotate: [0, 1, 0, -1, 0]
        }}

        transition={{
          duration: 6,
          repeat: Infinity,
          ease: "easeInOut"
        }}

      />



      <motion.div

        className="content"

        initial={{
          opacity: 0,
          y: 30
        }}

        animate={{
          opacity: 1,
          y: 0
        }}

        transition={{
          duration: 1
        }}

      >

        <h1>

          INFLUENCER

          <br />

          <span>DETECTIVE</span>

        </h1>

        <p className="subtitle">

          AI POWERED CREATOR INTELLIGENCE

        </p>

        {/* Radar */}

        <div className="scanner">

          <div className="scan-line"></div>

        </div>

        {/* Loading */}

        <div className="loading-section">

          <p>Initializing Intelligence...</p>

          <div className="loading-bar">

            <div className="loading-fill"></div>

          </div>

        </div>

      </motion.div>

    </div>

  );

}
