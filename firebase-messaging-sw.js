importScripts('https://www.gstatic.com/firebasejs/9.6.10/firebase-app-compat.js');
importScripts('https://www.gstatic.com/firebasejs/9.6.10/firebase-messaging-compat.js');

// Ваша конфигурация Firebase
const firebaseConfig = {
    apiKey: "AIzaSyCeGqvBeSJhsC-8Eye6rH47W7wA7hIvcOY",
    authDomain: "django-app-69d0f.firebaseapp.com",
    projectId: "django-app-69d0f",
    storageBucket: "django-app-69d0f.appspot.com",
    messagingSenderId: "782742220512",
    appId: "1:782742220512:web:e072e191f35cb4e4692a85"
};

// Инициализация Firebase в Service Worker
firebase.initializeApp(firebaseConfig);

const messaging = firebase.messaging();

// Обработка фоновых сообщений (background notifications)
messaging.onBackgroundMessage((payload) => {
    console.log('[firebase-messaging-sw.js] Received background message ', payload);

    // Настройки уведомления
    const notificationTitle = payload.notification.title;
    const notificationOptions = {
        body: payload.notification.body,
        icon: '/firebase-logo.png'  // Иконка уведомления (можете указать свою)
    };

    self.registration.showNotification(notificationTitle, notificationOptions);
});
