var net = require("net");

var socket = new net.Socket()
socket.connect(8080, "127.0.0.1", function(){
    console.log("Connection from", socket.address());    
});
socket.on('error', function(error){
    console.error("Error:", error)
});
socket.on('data', function(data){
    console.log("Received data", data.toString("utf-8"));
    //socket.destroy()
});



