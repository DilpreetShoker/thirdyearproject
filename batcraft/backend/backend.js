const express = require("express");
const app = express();
const spawn = require("child_process").spawn;
app.use(express.json());
const cors = require("cors");
app.use(cors());

var curr_filename = ''
var message = ''
var send_message = false;

app.get("/",async(_,res) => {
    res.send("Success!!");
})
// Open Server
app.listen(3000, () => {
    console.log("Server Started");
})

// Define multer and axios
const multer = require('multer');
const { default: axios } = require("axios");
// The following code is used to store the file in local
const storage = multer.diskStorage({
    destination: function (req, file, cb) {
      cb(null, "uploads/");
    },
    filename: function (req, file, cb) {
      const uniqueSuffix = Date.now();
      cb(null, uniqueSuffix + file.originalname);
      curr_filename = "uploads/"+ uniqueSuffix + file.originalname
    },
  });

// Multer is initialised
const upload = multer({storage: storage})
app.post("/upload-video", upload.single("video"), async (req,res) => {

    console.log(req.body);
    // backend.py is called upon with the filename of the video being analysed
    const backendPy = spawn('python', ['backend.py',curr_filename])
    backendPy.stdout.on('data', (data)=>{
        // filename is converted to string
        console.log(data.toString('utf8'))
        message = data.toString('utf8');
    })
    backendPy.on('close', (code) => {
        console.log(`child process exited with code ${code}`);

        res.send({ Status: "ok", message: message });
    });

})


app.post("/get-message", async (req,res) => {
    try{
        await send_message.then (() =>{
            
        })
    }catch(error){

    }
})
