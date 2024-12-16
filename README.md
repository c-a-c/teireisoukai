# teireisoukai
定例総会を円滑に行うためのDiscord botです。

## 主な機能
- 会議をスラッシュコマンドから登録し、内容をjsonで管理
- 会議登録後、連絡・再送を自動で行う
- 委任状提出をui.TextInputから受け取り、内容をjsonで管理
- 出席率を計算し、通知
- 未出席者にDMの送信
- 投票チャンネルのメッセージに自動的に✅❌のリアクションを追加

<div id="member"></div>

## 使用方法（部員側）
- 定例総会前<br>
   - C.A.C.サーバーに定例総会botが連絡してくれます

- 委任状<br>
   - 画像左下の「委任状を提出」から提出できます
<img width="500" alt="スクリーンショット 2024-04-25 16 27 53" src="https://github.com/c-a-c/teireisoukai/assets/111753731/5d81453b-0f4c-4169-9cd7-32b05ad026c6">

- 定例総会時<br>
   - 定例総会サーバーのVCに入りましょう<br>
   - 入っていない場合BotからDMが来ます
<img width="500" alt="スクリーンショット 2024-12-14 13 46 14" src="https://github.com/user-attachments/assets/012378e1-401a-47cf-9f6a-94cdee75fcde" />




## 使用方法（庶務側）

### 会議の作成
#### 1. テキストチャンネルで`/register`と入力して送信

<img width="500" alt="スクリーンショット 2024-04-25 16 41 21" src="https://github.com/c-a-c/teireisoukai/assets/111753731/783791cf-c8d5-47e7-b8f4-5d1fd2874347">

#### 2. 日時を設定
   - 「次の水曜日13:30-」、「次の水曜日13:30-」の場合はそのまま選択でOK
   -  それ以外の場合は `年/月/日/時/分`の形式で入力してください
   -  最後に議題登録へ移るを選択
<img width="500" alt="スクリーンショット 2024-12-14 14 56 16" src="https://github.com/user-attachments/assets/7ad2ad09-40a4-44ea-be6b-d8a073769ff3" />

#### 3. 議題を設定
   -  議題を入力します
   -  議題が2個以上ある場合は「、」で区切って入力します
<img width="500" alt="スクリーンショット 2024-12-14 15 01 03" src="https://github.com/user-attachments/assets/cdf54383-547a-4f93-953b-b1ad150f3d96" />


#### 4. 送信
   -  「この内容で送信する」を選択するとC.A.C.サーバーに送信されます
<img width="625" alt="スクリーンショット 2024-12-14 15 03 42" src="https://github.com/user-attachments/assets/751d6638-21d5-4c47-b5ee-f7e26f788835" />

#### 5. 場所を変更
   -  送信画面の下中央に「場所を変更する」ボタンがあります
   -  教室が変わったときはこちらから変更してください
<img width="432" alt="スクリーンショット 2024-12-14 15 04 17" src="https://github.com/user-attachments/assets/e04b05fb-256f-434a-b6c5-a95183432ef3" />

#### 6. その他
   - 「戻る」ボタンを押すと1つ前の動作に戻すことができます
   - 間違って会議を作成した場合`/delete_meeting`から削除を行えます

## 仕様
- 出席率 = (委任状提出者 + VCに入っている現役部員)　/ サーバーにいる現役部員
## 開発

### .env
```
# discord botのトークン
TOKEN=""

# CACサーバー関連のID
CAC_GUILD_ID=
CAC_CHANNEL_ID=
MEMBER_ROLE_ID=

# 定例総会サーバー関連のID
MEETING_GUILD_ID=
VOTE_CHANNEL_ID=
MEETING_VC_CHANNEL_ID=
MEETING_CHAT_CHANNEL_ID=
CURRENT_MEMBER_ROLE_ID=
```
