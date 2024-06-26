# teireisoukai
定例総会を円滑に行うためのDiscord botです。

## 主な機能
- 会議をスラッシュコマンドから登録し、内容をjsonで管理
- 会議登録後、連絡・再送を自動で行う
- 委任状提出をui.TextInputから受け取り、内容をjsonで管理
- 出席率を計算し、通知
- 未出席者にDMの送信
- 投票チャンネルのメッセージに自動的に✅❌のリアクションを追加

## 使用方法（部員側）
定例総会前になるとC.A.C.サーバー連絡に定例総会botが連絡してくれます。
メッセージの下部には委任状に関するボタンがあるので、提出したい人はここから提出してください。
定例総会時にvcチャンネルにいないかつ委任状を提出していないとbotからDMが送信されるので注意してください。</br>

#### 連絡例

<img width="856" alt="スクリーンショット 2024-04-25 16 27 53" src="https://github.com/c-a-c/teireisoukai/assets/111753731/5d81453b-0f4c-4169-9cd7-32b05ad026c6">

## 使用方法（庶務側）

### 会議の作成

会議を作成するにはテキストチャンネルで`/register`と入力します。

<img width="851" alt="スクリーンショット 2024-04-25 16 41 21" src="https://github.com/c-a-c/teireisoukai/assets/111753731/783791cf-c8d5-47e7-b8f4-5d1fd2874347">

送信すると、登録メッセージが返信されるので入力を続けます。
最後に「この内容で送信」というボタンが表示されるので、そのボタンを押すと連絡に送信されます。
登録後は再送、出席率の確認を自動的に行うためこれ以上の操作の必要はありません。


### 会議の削除
`/register`で登録した会議は`/delete_meeting`で削除できます。
操作は`/register`と同様です。

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
