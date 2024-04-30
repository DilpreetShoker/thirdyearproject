const mongoose = require("mongoose")

const VideoDetailsSchema = new mongoose.Schema(
    {
        video: String
    },
    {
    collection: "VideoDetails"
    }
);

mongoose.model("videoDetails",VideoDetailsSchema)