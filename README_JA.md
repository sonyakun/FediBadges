# FediBadges
> [!TIP]
> [English Version](https://github.com/sonyakun/fedibadges/blob/master/README.md) is available.

ActivityPubを採用したマイクロブログ向けのバッジ生成用ツールです。

## 使い方
[Web上](https://fedibadges.sonyakun.com)で作成が可能です。

### Webで作成
usernameにMisskeyなどのアカウント名を入力します。 (例: `cocoa_vrc`)
> [!WARNING]
> アカウント名は、@の後に続くドメインを除く文字列のことを指します。

hostには、サーバーのドメインを入力します。 (例: `misskey.io`)

icon typeは以下の三種類が利用できます。
<p><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/f/f2/ActivityPub-logo-symbol.svg/130px-ActivityPub-logo-symbol.svg.png" height=25 width=25> ActivityPub</p>
<p><img src="https://assets.misskey-hub.net/public/icon.png" height=25 width=25> Misskey</p>
<p><img src="https://joinmastodon.org/logos/logo-purple.svg" height=25 width=25> Mastodon</p>

すべて入力したらGenerateをクリックすることで画像が生成されます。生成された画像の下にはURLとコピーボタンが表示されます。

## セルフホスト
> [!IMPORTANT]
> [既知の問題](https://github.com/vercel/vercel/issues/11545)の影響で、Vercelで利用する場合はNode.jsのバージョンを18に、Pythonのバージョンを3.9に設定する必要があります。

[![Vercelで展開](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fsonyakun%2Ffedibadges)

Vercelで動作確認済みです。

## 謝辞
* Misskey logo by [Misskey](https://misskey-hub.net/ja/brand-assets/)
* Mastodon lobo by [Mastodon](https://joinmastodon.org/ja/branding)
* ActivityPub logo by [WikiMedia Commons](https://commons.wikimedia.org/wiki/File:ActivityPub-logo-symbol.svg)