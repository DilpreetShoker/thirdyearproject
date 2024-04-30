import cricketBall from './logo4.png';
import batCraft from './BatCraft.png'
import './App.css';
import { useState,useEffect } from 'react';
import axios from "axios";
import CircularProgressBar from './CircularProgressBar';
function App() {
  const [video,setVideo]=useState(null)
  const [filename, setFilename] = useState(null)
  const [playerMatched,setPlayerMatched] = useState();
  const [percentageMatched, setPercentageMatched] = useState();
  const [message, setMessage] = useState();
  const [feedback1, setfeedback1] = useState(null);
  const [feedback2, setfeedback2] = useState(null);
  const [feedback3, setfeedback3] = useState(null);
  const [classication, setClassification]= useState(null)
  const [currShot, setCurrShot] = useState('coverDrive');
  const [view, setView] = useState('home');


  useEffect(() =>{
    getMessage()
  })
  const[statusColor, setStatisColot] = useState("white")
  const sumbitVideo = async(e) =>{
    e.preventDefault();
    const formData = new FormData();
    formData.append("video",video);
    setView('loading');
    const result = await axios.post(
      "http://localhost:3000/upload-video",
      formData,
      {
        headers: {"content-Type": "multipart/form-data"}
      })
      if (result.data.Status === "ok") {
        const feedback = result.data.message.split(',');
        console.log(feedback)
        setPlayerMatched(feedback[0])
        setPercentageMatched(feedback[1])
        setfeedback1(feedback[2])
        setfeedback2(feedback[3])
        setfeedback3(feedback[4])
        setClassification(feedback[5])
        // Handle successful upload and message received from server
      } else {
        // Handle server response error
        console.error('Upload failed', result.data);
      }
      setView('results');

  }
  const onInputChange = (e) => {
    console.log(e.target.files[0].name);
    setVideo(e.target.files[0]);
    setFilename(e.target.files[0].name)
    setStatisColot("#001011")


  }

  const getMessage = async() => {
    try {
        const result = await axios.get("http://localhost:3000/get-message");
        console.log(result);  // Log the successful result
        setMessage(result);  // Set the message based on the result
    } catch (error) {
        console.error(error);  // Log the error if the request fails
        setMessage(null);  // Optionally set the message state to null or an error message
    }
}
  const navigateToAbout = () => setView('about');
  const returnToHome = () => setView('home');

  
  return (
    <>

<div className="content">
    <div className="black-box"></div>
    <div className="white-box"></div>
</div>
<div className="navbar">
    <img src={batCraft} alt="logo"></img>
    <div className='nav-buttons'>
      <button className="nav-btn" id ="home" onClick= {returnToHome}>Home</button>
      <button className="nav-btn" id = "about" onClick = {navigateToAbout}>About</button>
    </div>
    
</div>
<div className={`center-div ${view === 'home' ? '' : 'hidden'}`}>
    <div className="left-section">
      <div className="title">Welcome to Bat<span>Craft</span></div>
      <img src={cricketBall} alt="image" />
      <div className="instructions">
        <div className = "heading">How to use Bat<span>Craft</span>?</div>
        <div className = "step">
          <div className="num">1</div>
          <div className="msg">Click on select file</div>
        </div>
        <div className = "step">
          <div className="num">2</div>
          <div className="msg">Chose the file you want to select</div>
        </div>
        <div className = "step">
          <div className="num">3</div>
          <div className="msg">Click on upload file</div>
        </div>
        <div className = "step">
          <div className="num">4</div>
          <div className="msg">Let Bat<span>Craft</span> do its magic</div>
        </div>
      </div>
    </div>
    <div className="right-section">
      <form onSubmit = {sumbitVideo}>
        
      <div className="shot">
        <input id="coverDrive" name="tripple" type="radio" value="coverDrive" className="shot-input" defaultchecked />
        <label htmlFor="coverDrive" className="shot-label coverDrive" >Cover Drive</label>
        <input id="straightDrive" name="tripple" type="radio" value="straightDrive" className="shot-input"  />
        <label htmlFor="straightDrive" className="shot-label straightDrive">Straight Drive</label>
        <input id="pullShot" name="tripple" type="radio" value="pullShot" className="shot-input" />
        <label htmlFor="pullShot" className="shot-label pullShot">Pull Shot</label>
        <span className="shot-selector"></span>
      </div>
      <div className="statusText" style ={{'backgroundColor': statusColor}}>{filename ? filename :"No file chosen"}</div>
        <input type="file" accept= "video/*" onChange = {onInputChange} placeholder = "Select File"/>
       
        <button type = "submit">Upload</button>
      </form>
    </div>
</div>
<div className={`loading-div ${view === 'loading' ? '' : 'hidden'}`}>
  <div className='loading-text'>Analysing...</div>
</div>
<div className={`AboutUs-div ${view === 'about' ? '' : 'hidden'}`}>
  <h1>About us</h1>
  <p> This website is the front-end of a third year dissertation project. The project was developed by Dilpreet Singh
    with the help of project supervisor, Shan Raza.
  </p>
</div>
<div className={`results-div ${view === 'results' ? '' : 'hidden'}`}>
  <div className='left-section'>
  <h1>Results</h1>
  <div className="instructions">
        <div className = "heading">Things to Improve</div>
        <div className = "step">
          <div className="num">1</div>
          <div className="msg">{feedback1 ? feedback1: 'feedback 1'}</div>
        </div>
        <div className = "step">
          <div className="num">2</div>
          <div className="msg">{feedback2 ? feedback2: 'feedback 1'}</div>
        </div>
        <div className = "step">
          <div className="num">3</div>
          <div className="msg">{feedback3 ? feedback3: 'feedback 1'}</div>
        </div>
      </div>

  </div>
  <div className= 'right-section'>
    <div className='circle-bar'>
      <CircularProgressBar progress={percentageMatched} size={200} />
    </div>
    <p>Your technqiue is classified as <b>{classication ? classication : 'unknown'}</b>and resembles the most with <b>{playerMatched ? playerMatched: 'Not found'}</b>
    with a {percentageMatched ? percentageMatched: 'x'}% match</p>
    
  </div>
</div>
</>

  )};


export default App;
