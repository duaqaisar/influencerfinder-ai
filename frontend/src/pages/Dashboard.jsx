import "./../styles/dashboard.css";

export default function Dashboard(){

return(

<div className="dashboard">

<div className="navbar">

<div className="logo">

INFLUENCER <span>DETECTIVE</span>

</div>

<div className="nav-right">

<div className="icon">🔔</div>

<div className="icon">⚙️</div>

<div className="icon">👤</div>

</div>

</div>


<div className="hero">

<h1>

Find the Perfect Influencer

</h1>

<p>

AI Powered Creator Intelligence Platform

</p>

<div className="search-box">

<input
placeholder="Search influencers, brands, or topics..."
/>

<button>

Search

</button>

</div>

</div>


<div className="grid">

<div className="card">

<h2>

Influencer Results

</h2>

<div className="placeholder">

Results will appear here

</div>

</div>

<div className="card">

<h2>

AI Analysis

</h2>

<div className="placeholder">

AI insights will appear here

</div>

</div>

</div>

</div>

)

}
