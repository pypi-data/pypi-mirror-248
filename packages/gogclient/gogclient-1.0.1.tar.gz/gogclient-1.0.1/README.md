# gog-client

A python client to access your GOG.com account.

# Description

The platform GOG.com (formerly known as Good Old Games),
provides storage access to the games that the user has purchased.
Access to this content delivery network requires the user to log in by
posting username and password into an auth form.

This was enough until some time ago, GOG changed the interface which resulted in various projects like the
gogrepo scripts [1] to stop working. Unfortunately [1] seems also abandoned.

# Getting Started
- Install using the regular python options,
- Copy the gogrepo.toml to your home directory,
- Then change the entries manually to match your needs which means setting your base directory,
  language and OS. Entries follow what GOG uses in their JSON content. 
  There are fallbacks defined when a product has not your OS or language, fallback is windows 
  and English respectively.

This is my config that I use on an Odroid HC2.

```
[gogrepo]
repo-base-dir = "/wad/0/public/GOG"
prefered-languages = ["English", ]
prefered-manual-languages = ["English", "EN", ]
prefered-os = ["linux", ]
```

- Execute `gogrepo -c gogrepo.toml` in shell. The script is copied to your local .bin directory
  on installation for convenience.
- Regularly backup the gogrepo.db3 file in your repo.
- Be sure nobody has access to your home directory, and you are admin on your own machine, so don't use Android!
  Your GOG account credentials are stored there in a plain .pkl file which you need to delete when you change your
  password.

# Known Issues
- Is not capable to handle ReCaptcha.
- Only tested on linux, expect Issues on other OS.

# TODOs
- Needs Best Practice credential storage mechanism, it stores a .pkl file in your home directory.
- Needs manual USER-INPUT of two-step authentication, i.e. the four-digit code you get via e-mail unless you disabled it.

# Why this client?
GOG wants to sell their GOG Galaxy Client but does not provide any official documentation
of their api.
Additionally, GOG can no longer be trusted after they massively deployed geo-blocking and censorship [2].

So users should be able to automatically mirror what they own to their local file
storages.

There has also been a case where GOG proved to be unreliable basically killing all of their customers GOG Galaxy Clients
and Games recently and blaming it on their external storage provider [3].

# Discount Evaluation Script

There is a Work-In-Progress Script for checking discounts and warn you if GOG tries to pull something on you.
Execute `gogdiscounts` in a shell. It will take your bookmarks from Firefox, fetch the current discounts from GOG for
a given locale which is now de_DE and de_AT, for the purpose of proving that GOG does locale based geo-blocking.

# LICENSE
The license is GPL V3.0 based with the extension that any government employee is forbidden to use this software.

# Deprecation of PyPi Packages
Packages on PyPi are no longer updated due to attempts of the PyPi to enforce new rules and basically flush out 
developers who do not consent.
Recent packages can be installed directly from git, i.e. "pip install git+<LINK-TO-GIT-REPOSITORY>".

# References
[1] https://github.com/eddie3/gogrepo

[2] https://www.gog.com/forum/general/release_lust_from_beyond_m_edition_c7082

[3] https://www.gog.com/forum/general/update_on_technical_issues_affecting_downloading_and_updating_games_afa62
