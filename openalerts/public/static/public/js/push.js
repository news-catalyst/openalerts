// Modified from https://raw.githubusercontent.com/safwanrahman/django-webpush/master/webpush/static/webpush/webpush.js

var isPushEnabled = false,
  subBtn,
  messageBox,
  registration;

var enableText = "Via Notifications";
var disableText = "Disable Notifications";

window.addEventListener('load', function() {
  subBtn = document.getElementById('webpush-subscribe-button');
  messageBox = document.getElementById('webpush-message');

  subBtn.addEventListener('click',
    function() {
      subBtn.disabled = true;
      if (isPushEnabled) {
        return unsubscribe()
      }

      if ('serviceWorker' in navigator) { 
        var serviceWorker = document.querySelector('meta[name="service-worker-js"]').content;
        navigator.serviceWorker.register(serviceWorker)
          .then(
            function(reg) {
              console.log(reg)
              subBtn.textContent = 'Loading...';
              registration = reg;
              initialiseState(reg);
            }
          ).catch(function (error) {
            console.log(error);
          });
      }
      else {  
        messageBox.textContent = 'Notifications are not supported for your browser.';
        messageBox.style.display = 'block'; 
      }
    }
  );

  function initialiseState(reg) {
    if (!(reg.showNotification)) {
        messageBox.textContent = 'Your browser does not support push notifications.';
        subBtn.textContent = enableText;
        messageBox.style.display = 'block';
        return;
    }

    if (Notification.permission === 'denied') {
      messageBox.textContent = 'You declined to receive push notifications.';
      subBtn.textContent = enableText;
      subBtn.disabled = false;
      messageBox.style.display = 'block';
      return;  
    }

    if (!('PushManager' in window)) {
      messageBox.textContent = 'Your browser does not support push notifications.';
      subBtn.textContent = enableText;
      subBtn.disabled = false;
      messageBox.style.display = 'block';
      return;  
    }

    subscribe(reg)
  }
}
);


function subscribe(reg) {
  getSubscription(reg).then(
      function(subscription) {
        postSubscribeObj('subscribe',subscription);
      }
    )
    .catch(
      function(error) {
        console.log('Subscription error: ', error);
        messageBox.textContent = 'Unable to subscribe you to push notifications';
        subBtn.textContent = enableText;
        subBtn.disabled = false;
        messageBox.style.display = 'block';
      }
    )
}

function urlB64ToUint8Array(base64String) {
  const padding = '='.repeat((4 - base64String.length % 4) % 4);
  const base64 = (base64String + padding)
    .replace(/\-/g, '+')
    .replace(/_/g, '/');

  const rawData = window.atob(base64);
  const outputArray = new Uint8Array(rawData.length);

  for (var i = 0; i < rawData.length; ++i) {
    outputArray[i] = rawData.charCodeAt(i);
  }
  return outputArray;
}

function getSubscription(reg) {
    return reg.pushManager.getSubscription().then(
        function(subscription) {
          var metaObj, applicationServerKey, options;
          // Check if Subscription is available
          if (subscription) {
            return subscription;
          }

          metaObj = document.querySelector('meta[name="django-webpush-vapid-key"]');
          applicationServerKey = metaObj.content;
          options = {
              userVisibleOnly: true
          };
          if (applicationServerKey){
              options.applicationServerKey = urlB64ToUint8Array(applicationServerKey)
          }
          return registration.pushManager.subscribe(options)
        }
      )
}

function unsubscribe() {
  registration.pushManager.getSubscription()
    .then(
      function(subscription) {

        if (!subscription) {
          subBtn.disabled = false;
          messageBox.textContent = 'We could not locate your notification subscription. Try reloading the page.';
          messageBox.style.display = 'block';
          return;
        }
        postSubscribeObj('unsubscribe', subscription);
      }
    )  
}

function postSubscribeObj(statusType, subscription) {  
  var browser = navigator.userAgent.match(/(firefox|msie|chrome|safari|trident)/ig)[0].toLowerCase(),
    data = {  status_type: statusType,
              subscription: subscription.toJSON(),
              browser: browser,
              group: subBtn.dataset.group
           };

  fetch(subBtn.dataset.url, {
    method: 'post',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(data),
    credentials: 'include'
  })
    .then(
      function(response) {
        if ((response.status == 201) && (statusType == 'subscribe')) {
          subBtn.textContent = disableText;
          subBtn.disabled = false;
          isPushEnabled = true;
          messageBox.textContent = 'Successfully subscribed to notifications.';
          messageBox.style.display = 'block';
        }

        if ((response.status == 202) && (statusType == 'unsubscribe')) {
          getSubscription(registration)
            .then(
              function(subscription) {
                subscription.unsubscribe()
                .then(
                  function(successful) {
                    subBtn.textContent = enableText;
                    messageBox.textContent = 'Successfully unsubscribed from notifications.';
                    messageBox.style.display = 'block';
                    isPushEnabled = false;
                    subBtn.disabled = false;
                  }
                )
              }
            )
            .catch(
              function(error) {
                subBtn.textContent = disableText;
                messageBox.textContent = 'Something went wrong while trying to disable notifications.';
                messageBox.style.display = 'block';
                subBtn.disabled = false;
              }
            );
        }
      }
    )
}