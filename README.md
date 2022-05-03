# GroovyEasy
Spotify（音楽ストリーミングサービス）を複数人で共有して操作可能なWebアプリ  
- ドライブなどの時に、一つのスマートフォンを使いまわしたり、そのスマートフォンの操作をしている人に操作をお願いしなくて済む
- それぞれのスマートフォンから、音楽の停止・再生、次に再生への追加、検索などが可能
- Spotifyのプレミアムプランに契約している1人がログインするだけでよい。その他の人はSpotifyのアカウントを持っていなくてよい
- アプリログイン後、リンクを共有することで誰でもSpotifyを操作可能（Spotifyアカウントを持っていなくてもよい）

## App URL 
### **https://groovyeasy.herokuapp.com/**  

## Features　

### 1、 Login 
- 「Login Spotify」ボタンを押下 

![1](https://user-images.githubusercontent.com/88955673/166409750-81abf6bc-c956-4a15-9794-f60cb19d32e2.png) 
-  Spotifyにログイン 

![2](https://user-images.githubusercontent.com/88955673/166410066-16c8f4dc-c6a2-419d-b286-56fb668eedfc.png) 

### 2、 Home 
- ログインしたユーザー名が表示される 
- 「リンクをコピー」を押下しリンクを他の人に共有する 
- 「delete room」を押下することでサービス終了 

![4](https://user-images.githubusercontent.com/88955673/166410287-ca8707fe-54ab-4e66-a30b-6d29daafabdf.png)

### 3、 Now 
- 現在再生中の曲が表示される 
- 各ボタンを押下することで、一時停止・スキップ（前・後ろ）が可能 

![6](https://user-images.githubusercontent.com/88955673/166410819-8c2f660b-cfe1-4fed-88c2-452c917e3928.png)

### 4、 Search
- 検索バーに文字を入力することで曲を探すことが可能
- 最大10件表示される 

![8](https://user-images.githubusercontent.com/88955673/166411505-f63bbab6-fd66-405e-b169-36ddc27c0faf.png)

- 表示された曲を押下し、その後「OK」を押下することで[次に再生]に追加することができる

![10](https://user-images.githubusercontent.com/88955673/166411889-54db3c09-1c94-496d-8ffb-3377f8b20c27.png)

### 5、 Others
- Spotifyのプレミアムプランに契約していない人がログインした場合はサービスを利用できない
  * **ログインユーザのみがプレミアムに契約している必要があり、その他のユーザはSpotifyのアカウントはいらない**

![3](https://user-images.githubusercontent.com/88955673/166412225-968948c1-10b6-4e9f-a526-03c5013623f6.png)

- Home画面で「delete room」を押下した後にリンクにアクセスした場合はサービスを使用できない

![12](https://user-images.githubusercontent.com/88955673/166412046-0d146a73-5717-46ac-9647-4cefc96b6528.png)
