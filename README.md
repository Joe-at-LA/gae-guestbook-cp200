gae-guestbook-cp200
===================

Guestbook sample app on Google App Engine for the CP200 online course.

### Overview

This sample Guestbook application was developed based on Google App Engine platform using Python programming language, one of the supported languages of the service. This code submission is the last part of the CP200 online course in which once passed gives you access to the L300 presence based classes and further certification.

The application provides a Guestbook interface which users can write their own greetings and switch among different guestbooks. It supports both anonymous and logged-in users.

### GAE Services

GAE provides you many built-in services you can use on your application out-of-the-box. This abstraction layer GAE provides allows you to focus more on the application business than on server configuration issues. This sample uses the following services:

* [Datastore](https://developers.google.com/appengine/docs/python/datastore/) (Schemaless database used to store the greetings)
* [Memcache](https://developers.google.com/appengine/docs/python/memcache/) (Caching mechanism used to speed-up greeting retrieval and decrease Datastore load)
* [OAuth](https://developers.google.com/appengine/docs/python/oauth/) (users with Google account can authenticate on the app)


These services combined results in a scalable application managed by Google's infrastructure which can handle a big load by using this architecture.

Feel free to fork and learn with this sample app :)