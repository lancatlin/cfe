const net = require('net');
var room = {}   //紀錄房主資訊

var server = net.createServer((client) => {
    console.log("New Connect "); 
    client.on("data", (dataBuffer) => {
        var data;
        try{
            const msg = dataBuffer.toString();
            data = JSON.parse(msg);   //將訊息轉換為json
            console.log('read: ' + msg);
        }catch (err) {
            console.log(err);
            client.write('Fail data');
            return;
        }
        switch(data["type"]) {          //依據type類型決定執行函數
            case "search":
                search(client, data);
                break;

            case "create":
                create(client, data);
                break; 
            case "join":
                join(client, data);
                break;
            default:
                console.log("error of data type");
                client.write("type undefind");
        }
    });
});
server.listen({
    host: 'localhost',
    port: 8122
});

function search(client, data) {     //查詢 查詢name房間是否存在
    if ( typeof data['name'] === 'string') {
        const result = {
            type: "result",
            msg: typeof room[data['name']] === 'object'
        };
        write(client, result);
    }else{
        client.write('Fail search');
    }
}

function join(client, data) {       //加入現有的房間
    let server = room[data['name']];
    data['address']['wan'] = client.remoteAddress;
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

function create(client, data) {     //建立房間
    if ( typeof data['address'] !== 'object') {
        client.write("Can't find address");
        return;
    }
    addr = data['address'];
    if (typeof addr['port'] === 'number' && typeof addr['lan'] === 'string'){
        data['address']['wan'] = client.remoteAddress;
        room[data['name']] = {
            address: data['address'],
            socket: client      //將socket儲存作為通訊管道
        };
        const msg = {
            'type': 'result',
            'msg':  true
        };
        write(client, msg);
    }else{
        client.write("Fail address type");
    }
}

function write(client, data) {
    const msg = JSON.stringify(data);
    console.log('write: ' + msg);
    client.write(msg);
}

