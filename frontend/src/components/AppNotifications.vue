<template>
  <div class="fixed right-0 top-20 flex flex-col gap-2">
    <transition-group name="notification">
      <div v-for="notification in notifications" :key="notification.id" :style="{borderColor: notification.type === 'error' ? 'red' : 'green'}" class="flex justify-between gap-8 border-l-4 border-blue-800 bg-white px-4 py-2">
        <p>{{ notification.message }}</p>
        <button @click="removeNotification(notification.id)">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="h-5 w-5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
    </transition-group>
  </div>
</template>

<script setup>
import useNotifications from "../composables/useNotifications";

const {notifications, removeNotification} = useNotifications();
</script>

<style>
.notification-enter-active,
.notification-leave-active {
  transition: all .5s ease
}

.notification-enter-from,
.notification-leave-to {
  opacity: 0;
  transform: translateX(100%);
}

.notification-move {
  transition: transform .5s ease
}

</style>
