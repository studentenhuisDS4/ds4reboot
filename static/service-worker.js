var asset_base = '../';
self.addEventListener('install', function (e) {
    e.waitUntil(
        caches.open('ds4App').then(function (cache) {
            return cache.addAll([
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
self.addEventListener('fetch', function (event) {
    // either respond with the cached object or go ahead and fetch the actual url
    event.respondWith(
        caches.match(event.request).then(function (response) {
            if (response) {
                // retrieve from cache
                return response;
            }
            // fetch as normal
            return fetch(event.request);
        })
    );
});