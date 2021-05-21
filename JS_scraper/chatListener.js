require('dotenv').config(); 
const fetch = require('node-fetch');
const tmi = require("tmi.js");
utf8 = require('utf8')

const client = new tmi.Client({
	channels: [process.env.CURRENT_CHANNEL]
});

client.connect();

client.on('message', (channel, tags, message, self) => {
	
    data = {'timestamp': new Date().getTime(),
            'channel': channel,
            'tags': tags,
            'message': message};

    const options = {
        method: 'POST',
        mode: 'cors',
        Headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    }
    
    fetch('http://localhost:5001/writerinput',  options)
        .then (res => res.json())
        .then(resdata => {
             console.log(resdata)
        })
        .catch(err => {
            console.log("AN ERROR OCCURED:")
            console.log(err)
        })
});
