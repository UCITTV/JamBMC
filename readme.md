# JamBMC (Jamendo XBMC)#

![Add-on Icon](http://i.imgur.com/qNisZDi.png)

## What is JamBMC? ##
JamBMC is a XBMC music add-on to browse, search, stream and download Songs and Albums from Jamendo.com. It was developed to participate in [Jamendo's App-Contest](http://developer.jamendo.com/contest).

## What is Jamendo? ##
[Jemando.com](http://www.jamendo.com/) is a the worlds largest digital service for free music.

## What is XBMC? ##
[XBMC](http://xbmc.org/) is an open source media center software which can run on multiple platforms like Windows, Linux, OSX, iOS or Android.

## Screenshots ##
![Screenshot](http://i.imgur.com/NqkXR76l.png)
Add-on Info Screen.

![Screenshot](http://i.imgur.com/TWdsTtFl.png)
Root Menu in List-View.

![Screenshot](http://i.imgur.com/8ydB1B2l.png)
Root Menu in Thumbnail-View.

![Screenshot](http://i.imgur.com/WruUor3l.jpg)
Discover -> Songs. By default sorted by "popularity (month)". You can filter this view by multiple Tags or change the sort method. Switching Pages is also possible.

![Screenshot](http://i.imgur.com/YOnAqZol.png)
Context Menu on a Song.

![Screenshot](http://i.imgur.com/52WIzy7l.png)
Song Info with full meta-data integration.

![Screenshot](http://i.imgur.com/8o0EWDzl.png)
Tag Filtering, there are ~40 Tags available and you can filter any view by as much Tags as you want.

![Screenshot](http://i.imgur.com/78GBp8jl.png)
Sort method choosing. There are multiple different sort methods available - depending on the context.

![Screenshot](http://i.imgur.com/I8KapWtl.png)
Downloading. You can download single Songs or complete Albums - including Covers. Once downloaded Songs are always played local.

![Screenshot](http://i.imgur.com/xrINYkEl.png)
Discover -> Artists. Same here: You can sort or filter to find exactly what you are looking for.

![Screenshot](http://i.imgur.com/4MsFEbel.png)
Mixtape management is one of the most useful features: You can create as much different Mixtapes as you need and let XBMC play them. Just open the context menu on any song and choose the mixtape you want to add this Song to.


## Features ##

**Discover**

- Browse Songs, Albums, Artists, Playlists and Radios
- Show Artists near your location


**Search**

You can search for Songs, Albums, Artists and Playlists.

- Albums, Artists
	- Search name
- Songs
	- name
	- tags
	- genre
	- instruments
	- mood
	- artist
	- album


**Ordering**

In most views you have full control about the ordering depending on the context.
This allows views like "This weeks most popular Songs", "New Albums", "This month most downloaded Songs", "All time most popular Artists", ...

- Albums
    - releasedate (desc, asc),
    - popularity (total, month, week)
- Artists
    - name
    - joindate (desc, asc)
    - popularity (total, month, week)
- Songs
    - buzzrate
    - downloads (total, month, week)
    - listens (total, month, week)
    - popularity (total, month, week)
    - releasedate (desc, asc)


**Tag-Filtering**

In most views you can filter the items by Tags (Tags can be Genre or Instrument). You can select one or multiple Tags at once. This allows Views like "Show me all Songs which have the "Rock"-Genre and "Electric Guitar"-Instruments. And you can even combine that with custom sorting


**Context-Menus**

- Album Context-Menu
    - Show Album Info (does not work currently due to XBMC limitations)
    - Download this Album
    - Show Songs in this Album
    - Show Albums by this Artist
- Song Context-Menu
    - Show Song Info
    - Download this Song
    - Add/Del to Mixtape
    - Show Albums by this Artist
    - Show similar Songs
    - Show Songs in this Album
- Artist Context-Menu
    - Show Albums by this Artist


**Download**

- Downlod single Songs
- Download complete Albums
- Once downloaded Songs will be played automatically local (no matter if the song was downloaded single or as part of an album)
- Covers will also be downloaded and saved next to the audio files so that XBMC can import those to its music database
- Choose the download Format you like: MP3 (VBR good Quality), OGG or even the lossless format FLAC
- Downloading is possible to any XBMC supported path (local, SMB, NFS, ...)


**Mixtapes**

- You can create multiple own local Mixtapes (similar to Playlists)
- You can create as much Mixtapes and add as much Songs to each as you like
- Just open the context menu on any Song to add or delete this Song to any existing mixtape or to add it to a new mixtape


**Radio**

Listen to one of ten Jemando created Radio Streams (Electronic, Rock, Jazz, Jamendo Best of, ...)


**Playback History**

Every Song you play will be added to your Playback History. If any Song is finished XBMC will automatically play the next one from the view you started playback. With this Feature you are still able to find the Songs you were listening to.


**Your Jamendo.com User-Account**

After you entered your Jamendo.com Username you can access:

- Artists you are fan of
- Albums in your "My Albums"-list
- Songs you like, favourited or wrote an review
- Your public Playlists


**Technical Features**

- API-Request Cache, most API-Requests are cached for 24 hours to improve the plugin response time and reduce the load on Jamendo API.
- XBMC-Skin Image integration. This add-on uses multiple XBMC-Skin provided Images to automatically match your choosen XBMC-Skin's look.


**Settings**

- Set items-per-Page (max 100)
- Choose the Audio Format. Playback: MP3, OGG. Download: MP3, OGG, FLAC
- Set Cover Size (Big, Medium, Small)
- Enable Thumbnail-View forcing. If enabled the plugin will automatically switch to a thumbnail-like view (instead of tabular list view).
- Force HTTPS. If enabled all API Requests will be encrypted.