------
"title": "Using ServiceWorkers for Offline Reading"
"layout": "post_sw"
------

*While I was playing with ServiceWorkers, I got a lot of ideas on how I could use this powerful feature. But making my blog accessible offline seemed to be the easiest and least useless of them.*

So ServiceWorkers is this new-ish browser feature, still under rapid development, that allows web developers take control of the networking part of the requests they make. Using this, one can write pieces of JavaScript code that can intercept all the requests that their web application makes and take further control of them. A ServiceWorker can essentially act like a proxy server. You can use them for caching your HTTP requests, provide offline experience, selectively routing HTTP requests, etc.

While ServiceWorkers allows you to intercept your HTTP requests, it also provides API for caching your requests. So, you can use these APIs, for populating the ServiceWorker cache, with whatever HTTP requests you want. Once your ServiceWorker intercepts an HTTP request, you can query its cache whether it has the response for that particular request. If you find it, you can return the cached response, otherwise you can propagate the request over the actual network. For creating an offline experience, you would do the same in reverse order: *intercept a request -> make the request over the network -> if it succeeds then return the response, else return the cached response*. In some network setups, it might take a while before you know the request has failed over the network and you should return the cached response. This might lead to long response times leading to bad user experience. In such cases, you can return a cached response while you send the request over the network and have in place some mechanism to update the content when you get it from the network.

Since I'm too lazy to do the latter, I decided to go for the simpler approach. This page initializes a ServiceWorker for this website. The ServiceWorker, once active, populates its cache with all the pages on this blog (Yes I'm sorry, it just did it or its doing it). For subsequent visits to the other pages, the ServiceWorker will intercept the HTTP request, try to fetch the content from the server. If it fails to do so, it will return the content stored in its cache as the response. Thats it. If you've read this far, and you're not on a dial-up connection, the ServiceWorker must have done its job, and my offline readable blog is your reward.

Wait a minute though. This would work only if you're on Chrome 40 or later. Might also work on Firefox nightly but I didn't check it. Let me know if it works for you there, or if it doesn't work if you expected it.

If you'd like to start playing with ServiceWorkers, this is a nice talk to watch - [https://www.youtube.com/watch?v=SmZ9XcTpMS4](https://www.youtube.com/watch?v=SmZ9XcTpMS4).

If you'd like to know the current status of ServiceWorkers, follow this link - [https://jakearchibald.github.io/isserviceworkerready/](https://jakearchibald.github.io/isserviceworkerready/)
