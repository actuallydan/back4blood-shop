# back4blood-shop

Free add-ons for [b4bcoop](https://github.com/actuallydan/b4b-coop), the unofficial private co-op mod for Back 4
Blood: new outfits and weapon looks you can add from inside the game. This repository holds the signed add-on list
that b4bcoop's **Add-ons** tab shows, and the add-ons themselves (one GitHub release each).

Each add-on is listed with its license. Many are fan conversions marked "Private use": shared for free between friends, not for sale or redistribution.

## For players

You don't need to do anything here. In the game:

1. Press **`~`** (the key left of `1`) to open the b4bcoop window, and click the **Add-ons** tab. The list loads by
   itself the first time you reach Fort Hope after starting the game (**Refresh** gets it again).
2. Click **Add** next to an add-on. Most are ready at once, no restart needed.
3. **Wear** puts on an outfit (in Fort Hope it opens the game's customization screen with the outfit on; any survivor
   can wear it). **Use** puts a weapon look on your weapon, **Stop** takes it off.
4. **Update** gets a newer version, **Remove** takes an add-on out again.

Add-ons are only downloaded when you click **Add** or **Update**. Other players never learn which add-ons you have:
friends with the same add-on see your outfit, everyone else sees your normal survivor. This is b4bcoop 0.9.7 and newer;
0.8 to 0.9.6 have the shop in a **Browse** tab (**Get the add-on list** first). Update b4bcoop from the `~` window's
**Updates** tab.

The mod checks every list against the shop's signature (a key built into b4bcoop) and every download against the
size and SHA-256 in that list. A list or file that doesn't match is not used.

## For add-on makers: submitting an add-on

1. Build your add-on with the b4bcoop modkit (`b4bmod pack`). The result is one `.pak` file with a
   `b4bcoop-addoninfo.txt` inside (title, author, version, description).
2. Open a pull request that adds your entry to `entries.json`, plus an optional thumbnail in `thumbs/` (PNG or JPEG,
   at most 1 MB; shown small in the list and up to 320x320 when a player hovers it, so a square picture of at least
   320x320 looks best):
   ```json
   {"addons": [
     {"id": "casual_joe", "version": "1.0", "license": "CC0-1.0",
      "license_url": "https://creativecommons.org/publicdomain/zero/1.0/",
      "author": "Your name", "name": "Casual Joe", "description": "A relaxed outfit, for any survivor.",
      "thumb": "casual_joe.png", "min_b4bcoop": "0.8.0"}
   ]}
   ```
   - `id`: lowercase letters, digits, `_` and `-`, at most 32 characters. It becomes the file name `<id>.pak`.
   - `version` is required. `name`, `author` and `description` default to the pak's addoninfo.
   - `license`: an SPDX id from this list: `CC0-1.0`, `CC-BY-3.0`, `CC-BY-4.0`, `CC-BY-SA-3.0`, `CC-BY-SA-4.0`,
     `MIT`, `Apache-2.0`, `BSD-2-Clause`, `BSD-3-Clause`, `OFL-1.1`, `Unlicense`. Link it in `license_url`.
   - `min_b4bcoop` (optional): the oldest b4bcoop version your add-on works with.
3. In the pull request, link your `.pak` file (for example a release in your own repository) and say where every part
   of it comes from.
4. A maintainer reviews it. If it is accepted, the maintainer publishes a release `<id>-v<version>` in this repository
   with `<id>.pak` as its asset, then merges your pull request. The catalog workflow builds and signs the list, and
   the add-on shows up in the game's Add-ons tab.

Updating: bump `version` in a new pull request. The new file is published as a new release `<id>-v<version>`.

## License requirements (read before submitting)

- Submit only add-ons whose **every file** you have the right to share publicly under the license you state. If
  you didn't make something yourself, its license must allow redistribution and modification, and you must follow its
  terms (for example credit for CC-BY).
- **Add-ons built with the modkit contain copies of game material instances and skeleton data** from Back 4 Blood,
  because that's how a new look is hooked into the game. Whether you may share those copies is **your
  responsibility** as the submitter. This project gives no legal advice and no permission on anyone else's behalf.
- **Not accepted:** models, textures, sounds or other content ripped from other games, films or commercial
  products; paid or "personal use only" assets; content under non-commercial (NC) or no-derivatives (ND) licenses;
  anything whose origin or license you can't show.
- Add-ons that turn out to break these rules are removed from the list.
- Every add-on stays under its own license (the one in `entries.json`). Back 4 Blood and its content belong to their
  owners. This project is not affiliated with or endorsed by them.

## How the list is built

`.github/workflows/catalog.yml` runs when `entries.json` or `thumbs/` change, when a release is published, edited or
deleted, and when started by hand:

1. `scripts/fetch-paks.py` downloads each entry's `<id>.pak` from this repo's release `<id>-v<version>`.
2. b4b-coop's `tools/shop-catalog.py` (pinned commit) reads each pak and computes its size, SHA-256, content class
   (cosmetic or gameplay-affecting) and what it adds or replaces. It refuses bad ids and unknown licenses.
3. The list is signed with the shop key (ed25519, secret `SHOP_SIGNING_KEY`), checked against
   `shop-signing.pub.pem`, and `catalog.json` + `catalog.json.sig` are committed to `main`.

Check the list yourself: `openssl pkeyutl -verify -pubin -inkey shop-signing.pub.pem -rawin -in catalog.json -sigfile
catalog.json.sig`.

## License

The scripts and workflow in this repository are MIT licensed (see `LICENSE`). Add-ons are not covered by that
license: each one is under the license stated in its entry.
