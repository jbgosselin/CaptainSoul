CaptainSoul
=====

Netsoul client with python2.7, twisted, pygtk, pynotify and pywebkitgtk

for (re)installing use dump_script.sh

if you don't have notification install pynotify

and install a notification daemon like xfce4-notifyd

works directly on the dump

for archlinux do:
```sh
pacman -Sy twisted pygtk python2-notify pywebkitgtk
```

for the dump you can launch boot.sh in the xinitrc like that
```sh
xterm -e ./boot.sh
```

it will ask you for your sudo password in order to kill dump's netsoul and start cptsoul

Features:

- Always actif log
- Contact list
- Chat
- Notification
- File transfer

To do:

- Blacklist
- Tab/Window chat
