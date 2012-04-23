Luckyfier :)
=======

This is a fun project what can run on Google App Engine.
It will improve the images on a webpage with the same effect
what you can get in Picasa with the "I'm feeling lucky" button.

Demo: [http://im-feeling-lucky.appspot.com/im-feeling-lucky/index.html](http://im-feeling-lucky.appspot.com/im-feeling-lucky/index.html)

I created it because I wanted to see if my family photos would
look better with this effect, but I was lazy to update dozens of
photos, so I decided to find or create a solution, where I can
easily preview my (otherwise online) gallery.

History of the development
--------------------------------

I saw that the [im\_feeling\_lucky](https://developers.google.com/appengine/docs/python/images/imageclass#Image_im_feeling_lucky)
effect is part of the Image API in Google App Engine, so it was
obvious that I can create a simple web service what can "luckify"
an image. I thought that
[im-feeling-lucky](http://im-feeling-lucky.appspot.com) is a funny
and free app name in the cloud, so I created this application.

When I was developing this luckify service, my laziness
overpowered me again, and wanted to
extend this service, so it can update HTML content as well: alter
&lt;img&gt; elements' src attribute, so I can view my gallery
without any modifications.
My plan was to download the HTTP content on the server, and modify
it with a simple string replace.

Well, HTTP parsing is not that easy in GAE Python, since I was facing
with issues about unicode and 8bit strings. Finally I was managed
to make it work, but of course the result was not very nice, since
the CSS and JS files were missing. And more importantly the links
were not working, since I didn't alter the href attributes. I was
upset and thought this bite it too big for me...

Then it hit me: the server can proxy all request to the target
server and simply return all content as-is, only modify the jpeg
images with the Lucky effect. All I need to do is to store the
target server's address in a session variable, so my app will know
which website I want to luckify.

That's what you can find here: the HTTP proxy-and-luckyfier :)

The solution was surprisingly easy: **less than 100 lines of python code**!

I'm thinking about future improvements:

-   create a border for the altered images (it is an easy-to-do image effect which makes
    photos nicer and more professional)
-   add other effects, such as negative
-   add transformations such as rotating or mirroring
