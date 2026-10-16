/* Service worker mínimo do Mapa dos Astros: permite mostrar notificações (obrigatório no Android)
   e traz o app de volta ao tocar na notificação. Não guarda cache de propósito (evita versões velhas). */
self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", e => e.waitUntil(self.clients.claim()));
self.addEventListener("notificationclick", e => {
  e.notification.close();
  e.waitUntil(self.clients.matchAll({ type: "window", includeUncontrolled: true }).then(cs => cs.length ? cs[0].focus() : self.clients.openWindow("./")));
});
