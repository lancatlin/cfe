# 交換IP伺服器 README
## 用途
讓兩個客戶端透過相同的**room name**可以連結到彼此。
功能：
1. search 搜尋房間
2. create 建立房間
3. join 加入房間
4. close 關閉房間（建立房間者限定）

### [Github](https://github.com/lancatlin/cfe)
## 一、通訊接口
資料全部透過JSON傳遞，**JSON必須先格式化為字串再傳送**，有以下幾種Type:
### 一、search
查詢指令，查詢伺服器是否已經有某個房間。
格式：
``` json=
{
	"type": "search",
	"name": 房間名稱
}
```
伺服器回覆：
``` json=
{
	"type": "result",
	"msg":  搜尋結果（true/false）
}
```

### 二、create
建立指令，建立一個新的房間。
**注意，登記之Address將會是不同的socket，因此需要額外提供address參數**
客戶端格式：
```json=
{
	"type": "create",
	"name": 房間名稱,
	"address": 
	{
		"lan": LAN IP,
		"port": Server port (註1)
	}
```
// 註一： Server socket 跟連線到交換IP伺服器的socket是不相同的，此處提供的Address是要讓往後的客戶端連線進來的，因此建議在啟動伺服端後，再做create。

伺服器回覆：
``` json=
{
	"type": "result",
	"msg":  執行結果（true / false）
}
```
伺服器儲存內容：
```javascript=
(client, data) {
	name = data["name"]
	address = data["address"]
	room[name] = {
		"address": {
			"wan": client.remoteAddress,
			"lan": address["lan"],
			"port":  address["port"]
		},
		"socket": client
	}
}
```
伺服器在儲存時會自動加入其公網IP(socket.remoteAddress)，以及對應之客戶端socket，以供未來回覆新連線。

### 三、join
用於讓客戶端連線上一個room。
| 名稱 | 解釋 | 
| --- | --- |
| 交換IP Server | 負責交換IP的伺服器 |
|客戶端 A | 創建房間的socket |
|Game Server | 規則引擎 |
| 客戶端B | 即將取得房間地址的socket |
| A Game Client | A電腦連線到Game Server的socket|
| B Game Client | B電腦連線到Game Server的socket|
客戶端A, B是連接到 交換IP伺服器的socket。

此動作會使用到兩個客戶端，首先即將加入的客戶端B對 room 房間發起連線，伺服器收到後會回覆B 房間room的所有人的address，伺服器也會向房間 room 的建立者客戶端A，發送即將連線者的address，以供打洞。這邊注意，**是發送給 "客戶端A" 而非 "規則引擎"** ，由原本的建立者客戶端A來負責中介的工作。
客戶端B格式：
```json=
{
	"type": "join",
	"name": 房間名稱,
	"address": {
		"lan": LAN IP,
		"port": Game Client Port(註1)
	}
}
```
// 註1: 此處的port也非客戶端 B之port，而是即將連線到規則引擎的socket的port。

伺服器回覆B:
```json=
{
	"type": "join",
	"address": {
		"wan": Game Server 之 公網IP,
		"lan": Game Server 之 私網IP,
		"port": Game Server port
	}
}
```

伺服器回覆 A:
```json=
{
	"type": "join",
	"address": {
		"wan": B Game Client 之公網IP,
		"lan": B Game Client 之私網IP,
		"port": B Game Client port
	}
}
```

### 四、close
**//尚未實做**
移除指令，用於移除目前建立的房間。只有建立房間之socket有權使用此命令。
客戶端格式：
```json=
{
	"type": "close"
}
```

## 二、錯誤訊息
```jsonld=
{
    "type": "err",
    "msg": msg
}
```
以下將說明各個情況之msg
### 資料格式錯誤
無法解析為json: **fail data**  
name 無法被解析： **fail name**  
address 格式錯誤： **fail address**  
### create
無提供address: **address error**
房間已被建立: **room exist**
### join
如果房間不存在: **room not exist**
無提供address: **address error**
### close
如果並非房間擁有者： **not room owner**
找不到房間： **room not exist**

## 三、Python Wrapper
Connect class 可用來連接到Switch伺服器，並執行search, create, join, close操作。  
### __init__
創建Connect物件，提供伺服器位址。
參數： address
回傳值： 無
```python=
#example
import connect

address = ("lancatserver.ddns.net", 8122)
c = connect.Connect(address)
```

### search
查詢伺服器 name 房間是否存在
參數： name
回傳值： true / false
```python=
name = "room"
result = c.search(name)
```

### create
建立房間，並在有新連線時以callback函數取得資料。
參數： name, address, callback
回傳值： true / false
callback 參數： (ip, port)
```python=
c.create(name, ('127.0.0.1', 8888), lambda data: print(data))
```

### join
取得房間的位址。
參數： name, address
回傳值： (ip, port) / None
```python=
addr = c.join(name, ('127.0.0.1', 8899))
```

### close
關閉連線。
參數：無
回傳值：無
```python=
c.close()
```