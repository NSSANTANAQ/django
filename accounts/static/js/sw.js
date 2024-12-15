// sw.js

function urlBase64ToUint8Array(base64String) {
    const padding = '='.repeat((4 - base64String.length % 4) % 4);
    const base64 = (base64String + padding)
        .replace(/\-/g, '+')
        .replace(/_/g, '/');
    const rawData = window.atob(base64);
    const outputArray = new Uint8Array(rawData.length);
    for (let i = 0; i < rawData.length; ++i) {
        outputArray[i] = rawData.charCodeAt(i);
    }
    return outputArray;
}

self.addEventListener('install', function(event) {
    event.waitUntil(self.skipWaiting());
});

self.addEventListener('activate', function(event) {
    event.waitUntil(self.clients.claim());
});

self.addEventListener('pushsubscriptionchange', function(event) {
    event.waitUntil(
        self.registration.pushManager.subscribe({
            userVisibleOnly: true,
            applicationServerKey: urlBase64ToUint8Array('BMrI6XUaOLp_m5xmE4vTGYvCBcMpZPvrzhFf0HMaGEmycCZ6Dcx8mzmZkc563GE7D28vo8oyTgBWupjRr6Mht5Q')
        }).then(function(newSubscription) {
            const uniqueEndpoint = `https://serviciosenlinea.epmapas.gob.ec/api/register-subscription/${btoa(JSON.stringify(newSubscription))}/`;
            return fetch('/api/register-subscription/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    endpoint: uniqueEndpoint,
                    keys: newSubscription.toJSON().keys
                })
            });
        })
    );
});

self.addEventListener('push', function(event) {
    const data = event.data ? event.data.text() : 'No data';
    const title = 'Nueva Notificación Push';
    const options = {
        body: data,
        icon: '/icon.png',
        badge: '/badge.png'
    };
    event.waitUntil(self.registration.showNotification(title, options));
});
