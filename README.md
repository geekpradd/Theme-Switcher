##Theme Switcher 

This is a Sublime Text 3 Plugin to switch Themes directly from the GUI like how Color Schemes can be changed.

This Plugin is in BETA status currently. It has been tested and developed on Sublime Text 3065 Linux x64 on Ubuntu 14.04.

###Why Theme Switcher?

Sublime Text has many themes available for download from Package Control and many of them are very cool looking. But, there is a slight problem with the entire theme system on activating themes.

For example, let's say I am browsing for Themes on Package Control.

I searched for Themes and I found the "Flatland" theme. I installed it directly from Sublime Text and then I want to try the theme out.

Now the only way to do so, is to open my Preferences file, and modify it to activate Flatland.

So, in my prefernces file, I modified the `theme` key to become `Flatland.sublime-theme`. But the Theme did not activate.

Wait, why? Because the theme file is named `Flatland Dark.sublime-theme`. So to activate the Theme, I have to go to the Flatland GitHub page and then search for Instructions.

So, to just activate a Theme, I have to do a lot of work.

That's where Theme Switcher jumps in. Theme Switcher automatically adds your Themes to the Menu from which you can easily Activate your Themes. Theme Switcher also displays multiple variants of Themes so that you can use them all at ease. For example, all variants of the "Afterglow" Theme can be accessed and activated from the GUI itself.

###Usage

After Installing the plugin, Go to Preferences - Theme - Your Desired Theme. 

For example to activate the Flatland theme, after installation, Go to Preferences - Theme - Theme Flatland - and then click on Flatland Dark.

Note that you might have to reload Sublime Text (by closing and reopening) to get completely activate the Theme. This is native Sublime Text behaviour and cannot be changed.

###For Package Developers

If you are developing a Theme for Sublime Text, then your Package name (as given in the Package Control Repoistory) must have the word "Theme" (with a capital T ) in it so that Theme Switcher can recognise your Theme.

Also, the current version only supports ST3 and Themes installed by Package Control, although "User" themes support is coming too.

###About 

Created by Pradipta (geekpradd). Copyright 2015. MIT Licensed. 