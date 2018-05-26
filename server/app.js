const net = require('net');
var room = {}

var server = net.createServer((client) => {
    console.log("New Connect "); 
    client.on("data", (dataBuffer) => {
        console.log(dataBuffer.toString());
        data = JSON.parse(dataBuffer.toString());
        console.log(data);
        switch(data["type"]) {
            case "search":
                search(client, data);
                break;

            case "create":
                create(client, data);
                break;

            case "join":
                join(client, data);
                break;
        }
    });
});
server.listen({
    host: 'localhost',
    port: 8122
});

function search(client, data) {
    result = {type: "result"};
    if(typeof room[data['name']] === 'object') {
        result['msg'] = 1;
    }else{
        result['msg'] = 0;
    }
    msg = JSON.stringify(result);
    console.log(msg);
    client.write(msg);
}

function join(client, data) {
    let server = room[data['name']];
    client.write({
            type: "join",
            name: data['name'],
            socket: server
        });
    server.write({
            type: "join",
            name: data['name'],
            socket: client
        });
}

function create(client, data) {
    room[data['name']] = client;
}

