# Openroll

This project aims to create a `native` cruchyroll experience by embeding mpv
player into a QT window sprinkled with everything else you need from crunchyroll

# Disclaimer

I am not associated with crunchyroll in anyway. This app is defintly going to
cross some legal line because it is making use of the name/brand/IP, so I this
repo might disapear one day. But I really hope they see the good that this app
can do in giving there customers a better user experiance (no more buffering
mainly).

The above might change after I actually look at there offical documentation...
Which I still have not done.

## Tasks

### Humble beginnings

1. Place mpv in a QT window with a label
	1. label is hardcoded
	1. mpv is fed a hardcoded path to an opensource video
1. Play a video from crunchyroll leveraging yt-dlp
	1. url to video is hardcoded
1. Update label with stats from mpv
	1. At least elapsed seconds or something

### Usable app

1. Create login page to retrieve cookie from crunchyroll
	1. after successfull login display window with mpv player
	1. feed mpv the cookie
	1. hardcoded url to video should now point to premium video
1. Create watchlist window
	1. Should be list of videos from users actual watch list
	1. videos should be clickable and open the mpv window
	1. mpv window should play the video clicked
1. Video progress should be synced to crunchyroll
	1. no idea what the send interval should be :(
	1. video progress should be fetched from crunchyroll
	1. video should start based on what is recieved from crunchyroll
1. Add the following ep as the next video in mpv's playlist (auto play next ep)
	1. Hmmmmm... should we not just add all eps to the playlist? We can just
	set the current video to the correct video in the playlist. This needs
	investigation.
