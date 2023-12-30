#! /usr/bin/env python

# LICENSE: AGPLv3. See LICENSE at root of repo

import json
import os
import re
import shutil
import unicodedata
from datetime import datetime
from pathlib import Path

import requests
import vdf

k_applist_fname = "applist.json"
re_remove_hyphen = re.compile(r"- ")
re_remove_subtitle = re.compile(r"\s*:.*")
re_remove_braces = re.compile(r"\s*\(.*\)")
re_remove_pc = re.compile(r"[ _](pc|for windows|windows)$")


def _strip_nonascii(text):
    """Remove non-ascii character to make for easier comparisons.

    _strip_nonascii(str) -> str
    """
    stripped = text.encode("ascii", "ignore")
    return stripped.decode().strip()


def _remove_accents(text):
    """Takes a unicode string and omits characters that would combine with the
    previous one (diacritics).
    See https://stackoverflow.com/a/517974/79125
    """
    nfkd_form = unicodedata.normalize("NFKD", text)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])


def _remove_punctuation(text):
    """Remove punctuation character to make for easier comparisons."""
    return re.sub(r"[:;,.=+?]", "", text)


class SteamAccount:
    """
    Data class to associate steamid and username
    """

    def __init__(self, steamid, username):
        self.steamid = steamid
        self.username = username

    def get_grid_folder(self, steam_folder):
        return f"{steam_folder}/userdata/{self.steamid}/config/grid"

    def get_user_folder(self, steam_folder):
        return f"{steam_folder}/userdata/{self.steamid}"

    def get_shortcut_filepath(self, steam_folder):
        return os.path.join(
            steam_folder, "userdata", self.steamid, "config/shortcuts.vdf"
        )


class SteamDatabase:

    """Database of steam information."""

    def __init__(self, steam_path, cache_folder, prefer_uri=False):
        """
        :steam_path: Path to folder containing steam.exe.
        :cache_folder: Where to store downloaded files.
        :prefer_uri: Use uris for GameDefinitions where possible.
        """
        self._steam_path = Path(steam_path)
        self._cache_folder = Path(cache_folder)
        self._apps = self._load_app_list()
        self._prefer_uri = prefer_uri

    def enumerate_steam_accounts(self):
        """
        Returns a list of SteamAccounts that have signed into steam on this machine

        enumerate_steam_accounts() -> list(SteamAccount)
        """
        accounts = list()
        with os.scandir(self._steam_path / "userdata") as childs:
            for child in childs:
                if not child.is_dir():
                    continue

                steamid = os.fsdecode(child.name)

                # we need to look inside this user's localconfig.vdf to figure out their
                # display name

                localconfig_file = os.path.join(child.path, "config/localconfig.vdf")
                if not os.path.exists(localconfig_file):
                    continue

                # here we just replace any malformed characters since we are only doing this to get the
                # display name
                with open(
                    localconfig_file, "r", encoding="utf-8", errors="replace"
                ) as localconfig:
                    cfg = vdf.load(localconfig)["UserLocalConfigStore"]
                    username = "(unknown username)"
                    # Some users have Friends, some have friends, and some are friendless
                    if "friends" in cfg:
                        username = cfg["friends"]["PersonaName"]
                    if "Friends" in cfg:
                        username = cfg["Friends"]["PersonaName"]
                    accounts.append(SteamAccount(steamid, username))

        return accounts

    def _make_gamename_comparable(self, name):
        """Convert a game name into something easier to compare. Does minimal
        transformations to ensure the best matches, but removes irrelevant
        details.

        _make_gamename_comparable(str) -> str
        """
        # Always remove hypen because it adds extra uncertainty.
        name = re_remove_hyphen.sub("", name)
        # Ignore 'the' vs 'The' differences (fixes Into The Breach)
        name = name.lower()
        return name

    def _load_app_list(self):
        """Load or download the app list.

        _load_app_list() -> dict
        """
        data = None
        now = datetime.utcnow()
        current_version = 3

        applist_file = self._cache_folder / k_applist_fname
        if applist_file.is_file():
            with applist_file.open("r", encoding="utf-8") as file:
                data = json.load(file)

            if data["version"] != current_version:
                data = None
            else:
                write_date = datetime.fromisoformat(data["download_timestamp"])
                delta = now - write_date
                if delta.days > 7:
                    # Stale applist. Trigger re-download.
                    data = None

        if not data:
            print("Downloading latest app list from Steam...")
            response = requests.get(
                "http://api.steampowered.com/ISteamApps/GetAppList/v2"
            )
            apps = response.json()["applist"]["apps"]
            name_to_id = {}
            stripped_to_id = {}
            for g in apps:
                name = g["name"]
                if not name:
                    continue
                name = self._make_gamename_comparable(name)
                name_to_id[name] = g["appid"]
                if " trial" not in name and " demo" not in name:
                    # Include a stripped set for better name guessing.
                    # Without accents (for ABZU):
                    stripped = _remove_accents(name)
                    if stripped not in name_to_id:
                        stripped_to_id[stripped] = g["appid"]
                    # Without punctuation (for Raji)
                    stripped = _remove_punctuation(name)
                    if stripped not in name_to_id:
                        stripped_to_id[stripped] = g["appid"]
                    # Without subtitle:
                    stripped = re_remove_subtitle.sub("", name, 1)
                    if stripped not in name_to_id:
                        stripped_to_id[stripped] = g["appid"]
            data = {
                "version": current_version,
                "download_timestamp": now.isoformat(),
                "name_to_id": name_to_id,
                "stripped_to_id": stripped_to_id,
            }
            applist_file.parent.mkdir(parents=True, exist_ok=True)
            with applist_file.open("w", encoding="utf-8") as file:
                file.write(json.dumps(data, indent=2))

        return data

    def guess_appid(self, name):
        """Guess the steam appid for a given game name.

        guess_appid(str) -> str
        """
        name_to_id = self._apps["name_to_id"]
        stripped_to_id = self._apps["stripped_to_id"]
        name = self._make_gamename_comparable(name)
        appid = name_to_id.get(name)

        if appid == 3970:
            # Assume Prey 2017 over Prey 2006 since the newer one has more art.
            appid = 480490

        if not appid:
            # For: "Control" -> "Control Ultimate Edition"
            for suffix in [" ultimate edition", " digital edition", " steam edition"]:
                long_name = name + suffix
                appid = name_to_id.get(long_name)
                if appid:
                    break
        if not appid:
            # For: "Death's Door Win10" -> "Death's Door"
            stripped = re.sub(r" win10\b", "", name, 1)
            appid = name_to_id.get(stripped)
        if not appid:
            # For: "Yakuza Kiwami (PC)" -> "Yakuza Kiwami"
            stripped = re_remove_braces.sub("", name, 1)
            appid = name_to_id.get(stripped)
        if not appid:
            # For: "Ghost of a Tale PC" -> "Ghost of a Tale"
            # For: "Genesis Noir for Windows" -> "Genesis Noir"
            stripped = re_remove_pc.sub("", name, 1)
            appid = name_to_id.get(stripped)
        if not appid:
            # For: "Grand Theft Auto V: Premium Edition" -> "Grand Theft Auto V"
            stripped = re_remove_subtitle.sub("", name, 1)
            appid = stripped_to_id.get(stripped)
        if not appid:
            # For: "Raji: An Ancient Epic" -> "Raji An Ancient Epic"
            stripped = _remove_punctuation(name)
            appid = name_to_id.get(stripped)
            if not appid:
                appid = stripped_to_id.get(stripped)
        if not appid:
            # For: "ABZÛ" -> "ABZU"
            name = _remove_accents(name)
            appid = name_to_id.get(name)
            if not appid:
                appid = stripped_to_id.get(name)
        if not appid:
            # For: "Rocket League®" -> "Rocket League"
            name = _strip_nonascii(name)
            appid = name_to_id.get(name)
        # Might return None.
        return appid

    def download_art_multiple(self, user, games, should_replace_existing):
        """Download art for a list of GameDefinitions

        download_art_multiple(SteamAccount, list[GameDefinition], bool) -> None
        """
        count = 0
        for game in games:
            success = self.download_art(user, game, should_replace_existing)
            if success:
                count += 1
        return count

    def _try_copy_art_to(self, art_fname, dest):
        """Duplicate downloaded art.
        Sometimes the best art is the same as some other art.

        _try_copy_art_to(Path, Path) -> None
        """
        dest = dest.with_suffix(art_fname.suffix)
        if not dest.is_file():
            try:
                # Steam works with symlinks if you can create them. Saves disk
                # space.
                os.symlink(art_fname, dest)
            except OSError:
                # Can only symlink as root. Copy instead.
                shutil.copy(art_fname, dest)

    def _is_supported_image(self, fname):
        """Does steam support using this type of image for grid art.

        _is_supported_image(str) -> bool
        """
        return not fname.endswith(".gif")

    def download_art(self, user, game, should_replace_existing):
        targets = self._get_grid_art_destinations(game, user)
        targets["boxart"].parent.mkdir(exist_ok=True, parents=True)
        appid = self.guess_appid(game.display_name)
        downloaded_art = False
        found_art = 0
        expected_art = len(targets)
        logs = []
        if appid:
            urls = self._get_art_urls(appid)

            for k, url in urls.items():
                did_download, fname, msg = self._try_download_image(
                    url, targets[k], should_replace_existing
                )
                downloaded_art |= did_download
                if fname:
                    found_art += 1
                else:
                    logs.append(msg)
        else:
            logs.append("Appid not found.")

        if (
            found_art < expected_art
            and game.art_url
            and self._is_supported_image(game.art_url)
        ):
            # Maybe not on steam. Fall back to other art.
            dest_fname = targets["logo"]
            did_download, fname, msg = self._try_download_image(
                game.art_url, dest_fname, should_replace_existing
            )
            downloaded_art |= did_download
            if fname:
                found_art += 3
                # Use the logo art for box art. Looks better than grey box.
                self._try_copy_art_to(fname, targets["boxart"])
                # Logo is closest to big picture's banner format.
                self._try_copy_art_to(fname, targets["10foot"])
                logs.append("Using fallback art. No hero available.")
            else:
                logs.append(msg)
        else:
            logs.append("No non-steam art found.")

        if found_art < expected_art:
            print(f"Found {found_art}/{expected_art} art for '{game.display_name}'")
            print(" ", "\n  ".join(logs))
        return downloaded_art

    def _get_art_urls(self, appid):
        """Get the hero, boxart, and logo art urls for the input appid.

        _get_art_urls(int) -> dict[str,str]
        """
        return {
            "boxart": f"https://steamcdn-a.akamaihd.net/steam/apps/{appid}/library_600x900_2x.jpg",
            "hero": f"https://steamcdn-a.akamaihd.net/steam/apps/{appid}/library_hero.jpg",
            "logo": f"https://steamcdn-a.akamaihd.net/steam/apps/{appid}/logo.png",
            "10foot": f"https://steamcdn-a.akamaihd.net/steam/apps/{appid}/header.jpg",
        }

    def _try_download_image(self, url, dest_fname, should_replace_existing):
        url_path = Path(url)
        fname = dest_fname.with_suffix(url_path.suffix)
        if not fname.is_file() or should_replace_existing:
            return self._download_image(url, fname)
        return False, fname, "Already exists"

    def _download_image(self, url, dest_fname):
        """Download an image to dest_fname.

        Returns:
        * did we download something
        * the image file on disk (if downloaded or already existed)
        * status message

        _download_image(str, Path) -> (bool,str,str)
        """
        page = requests.get(url)
        if page.status_code == 200:
            with dest_fname.open("wb") as f:
                f.write(page.content)
            return True, dest_fname, f"Downloaded '{url}' to '{dest_fname}'."
        return False, None, f"Error {page.status_code} for '{url}'."

    def _get_grid_art_destinations(self, game, user):
        """Get filepaths for the grid images for the input shortcut.

        _get_grid_art_destinations(GameDefinition, SteamAccount) -> dict[str,Path]
        """
        grid = Path(user.get_grid_folder(self._steam_path))
        exe, args = game.get_launcher(self._prefer_uri)
        # vdf stores signed, but filenames use unsigned.
        shortcut = game.get_shortcut_id_unsigned()
        return {
            "boxart": grid / f"{shortcut}p.jpg",
            "hero": grid / f"{shortcut}_hero.jpg",
            "logo": grid / f"{shortcut}_logo.png",
            "10foot": grid / f"{shortcut}_bigpicture.png",
        }


def _test():
    import pprint

    db = SteamDatabase(
        "C:/Program Files (x86)/Steam",
        os.path.expandvars("$TEMP/steamsync"),
        prefer_uri=False,
    )
    user = db.enumerate_steam_accounts()[0]
    pprint.pp([user.steamid, user.username])
    game_name = "Death's Door Win10"
    appid = db.guess_appid(game_name)
    print(game_name, appid)


if __name__ == "__main__":
    _test()
