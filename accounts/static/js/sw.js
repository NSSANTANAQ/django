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

// Evento de instalación
self.addEventListener('install', function(event) {
    event.waitUntil(self.skipWaiting());
});

// Evento de activación
self.addEventListener('activate', function(event) {
    event.waitUntil(self.clients.claim());
});

// Evento pushsubscriptionchange
self.addEventListener('pushsubscriptionchange', function(event) {
    event.waitUntil(
        self.registration.pushManager.subscribe({
            userVisibleOnly: true,
            applicationServerKey: urlBase64ToUint8Array('MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEKEElM7spZZ7D1TnCnY+h2J6vBUsFUDQGS2a3LljuNN+XUKrNXfjm2LgIeIKgDtsfBPK2DerAadgAVbcKcEOMxg==')
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
            }).catch(error => {
                console.error('Error al registrar la suscripción:', error);
            });
        })
    );
});

// Evento push
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