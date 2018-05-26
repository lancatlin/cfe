const net = require('net');

var server = net.createServer((client) => {
    console.log("New Connect from " + client.address);
    client.on("data", (dataBuffer) => {
        data = JSON.stringify(dataBuffer);
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

function search(client, data) {
    result = {type: "result"};
    if(typeof room[data['name']] === 'object') {
        result['msg'] = 1;
        client.write(result);
    }else{
        result['msg'] = 0;
        client.write(result);
    }
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

