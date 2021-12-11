# PyPPUB
*Portable PUBlications for Python*

Contained in this repo is the spec for a format I made up one day for some reason called PPUB, or Portable PUBlication. I made it because I thought I wanted to blog but I was having one of those "hating the state of the modern web" weeks. PPUB is basically an archive with publication metadata baked in. It allows markdown files along with any embedded content to be wrapped up into a single compressed file.

PPIX is an indexing format which allows for searching through a library of PPUB files quickly and easily. A companion project called php-ppub can be configured to read PPIX files and expose a search functionality to visitors of your php-ppub blog site.

The idea was to make posts easily archivable, uploadable, and distribuitable. Maybe one day this format will still be useful when we abandon the concept that is the "modern web". Or life will go on and this will be abandoned. But hey, I'm sitting here right now publishing this to GitHub and actually putting in the effort to read the words you are reading right now, so who knows. I might even actually start blogging.

A [UI is available](https://github.com/Tilo15/PPublisher) in GTK3 which makes use of this library. Everything needs to be cleaned up and packaged at some point though.