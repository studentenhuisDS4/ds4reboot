var CACHE_NAME = 'ds4-cache-v1';

self.addEventListener('install', function (e) {
    e.waitUntil(
        caches.open(CACHE_NAME).then(function (cache) {
            return cache.addAll([
                '/',
                '/static/favicon.ico',
                '/static/js/uikit.min.js',
                '/static/js/base.js',
                '/static/js/jquery.js',
                '/static/js/flipclock.min.js',
                '/static/js/components/notify.min.js',
                '/static/js/components/datepicker.min.js',
                '/static/js/components/tooltip.min.js',
                '/static/css/uikit.almost-flat.min.css',
                '/static/css/components/notify.almost-flat.min.css',
                '/static/css/components/datepicker.almost-flat.min.css',
                '/static/css/components/tooltip.almost-flat.min.css',
                '/static/css/base.css',
                '/static/css/lf19.css',
                '/static/css/background.css'

            ]).then(function () {
                self.skipWaiting();
            });
        })
    );
});

// when the browser fetches a url
self.addEventListener('fetch', function(event) {
  event.respondWith(
    caches.match(event.request)
      .then(function(response) {
        // Cache hit - return response
        if (response) {
          return response;
        }

        return fetch(event.request).then(
          function(response) {
            // Check if we received a valid response
            if(!response || response.status !== 200 || response.type !== 'basic') {
              return response;
            }

            // IMPORTANT: Clone the response. A response is a stream
            // and because we want the browser to consume the response
            // as well as the cache consuming the response, we need
            // to clone it so we have two streams.
            var responseToCache = response.clone();

            caches.open(CACHE_NAME)
              .then(function(cache) {
                cache.put(event.request, responseToCache);
              });

            return response;
          }
        );
      })
    );
});