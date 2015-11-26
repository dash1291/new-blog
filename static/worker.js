importScripts('/serviceworker-cache-polyfill.js');

self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open('dash1291.github.io.cache').then(function(cache) {
      return cache.addAll([
        '/',
        '/posts.html',
        '/about.html',
	'/2015/09/20/serviceworkers.html',
        '/2014/12/28/browserstack-infantry.html',
        '/2014/03/22/mozilla-summer.html',
        '/2012/11/9/crunch-in-network.html',
      ]);
    })
  );
});

self.addEventListener('fetch', function(event) {
  var request = event.request;
  fetch(request)
    .then(function(response) {
      return response;
    })
    .catch(function(response) {
      return caches.match(request.url);
    })
});
