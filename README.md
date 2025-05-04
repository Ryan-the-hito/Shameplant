# 🌿Shameplant: Dynamically Hide Your Dock

![r0mCpLR](https://i.imgur.com/r0mCpLR.png)

Shameplant is a macOS menu bar app to hide dock when a window get close. You can also set the threshold. 

## To-do list

Be aware that the app now still has some bugs and remains in the early test stage right now.

- [ ] Automatic download and replacement
- [x] Automatic restart when screen switches (Done in v0.0.9. )
- [x] There are bugs if you use stage manager to switch windows (Done in v0.0.9. As there is no direct way from Apple since there is no open API about Stage Manager as far as I know, I created a workaround in v0.0.9 that after you switch the windows in Stage Manager, click the window in the front once or two, will bring Shameplant back to work again. And this clicking function was not supported in the previous versions.)
- [x] Add: when switching between different windows of the same app (Done in v0.0.9. Now you can just click the window once or twice to solve this problem)
- [ ] Add: Blacklist feature
- [ ] Add an easier way to enable accessibility 
- [ ] Add a button to restart the app
- [ ] Add a button to add an app to blacklist (Is window also supported?)