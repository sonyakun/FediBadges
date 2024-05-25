# FediBadges
> [!TIP]
> [日本語版](https://github.com/sonyakun/fedibadges/blob/master/README_JA.md)もあります。

Tools for badge generation for ActivityPub implemented microblogs.

## How To use
It can be created on the [Web](https://fedibadges.sonyakun.com).

### Make on Web
> [!WARNING]
> [fedibadges.sonyakun.com](https://fedibadges.sonyakun.com) is hosted on Vercel's Hobby Plan. Please consider [self-hosting](#self-hosting) when generating a large number of badges, for example.

Enter an account name such as Misskey in the username field. (Example: `cocoa_vrc`)
> [!WARNING]
> The account name is the string of characters following @, excluding the domain.

For host, enter the domain of the server. (Example: `misskey.io`)

The following three icon types are available:
<p><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/f/f2/ActivityPub-logo-symbol.svg/130px-ActivityPub-logo-symbol.svg.png" height=25 width=25> ActivityPub</p>
<p><img src="https://assets.misskey-hub.net/public/icon.png" height=25 width=25> Misskey</p>
<p><img src="https://joinmastodon.org/logos/logo-purple.svg" height=25 width=25> Mastodon</p>

Once everything is entered, click Generate to generate the image. The URL and copy button will appear below the generated image.

## self-hosting
> [!IMPORTANT]
> Due to a [known issue](https://github.com/vercel/vercel/issues/11545), the Node.js version must be set to 18 and the Python version to 3.9 when used with Vercel.

[![Deploy With Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fsonyakun%2Ffedibadges)

tested on Vercel.

### How to build
Install pipenv.

After that, change the python_version in the Pipfile to 3.12 (if you are using 3.12).

Run `pipenv install` in the fedbadges directory and run `pipenv run serve` after completion to start it.

## Thanks
* GitHub Corners by [@tholman](https://github.com/tholman)

* Misskey logo by [Misskey](https://misskey-hub.net/brand-assets/)
* Mastodon lobo by [Mastodon](https://joinmastodon.org/branding)
* ActivityPub logo by [WikiMedia Commons](https://commons.wikimedia.org/wiki/File:ActivityPub-logo-symbol.svg)