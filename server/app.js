const net = require('net');
var room = {}   //紀錄房主資訊

var server = net.createServer((client) => {
    console.log("New Connect "); 
    client.on("data", (dataBuffer) => {
        const msg = dataBuffer.toString();
        const data = JSON.parse(msg);   //將訊息轉換為json
        console.log('read: ' + msg);
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

function search(client, data) {     //查詢 查詢name房間是否存在
    const result = {
        type: "result",
        msg: typeof room[data['name']] === 'object'
    };
    write(client, result);
}

function join(client, data) {
    let server = room[data['name']];
    cmsg = {
            type: "join",
            name: data['name'],
            address: server['address']
        };
    smsg = {
            type: "join",
            name: data['name'],
            address: data['address'] 
        };
    write(client, cmsg);
    write(server['socket'], smsg);
}

function create(client, data) {
    room[data['name']] = {
        address: data['address'],
        socket: client
    };
    const msg = {
        'type': 'result',
        'msg':  true
    };
    write(client, msg);
}

function write(client, data) {
    const msg = JSON.stringify(data);
    console.log('write: ' + msg);
    client.write(msg);
}

