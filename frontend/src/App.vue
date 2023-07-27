<script setup>
import TheHeader from "./components/TheHeader.vue";
import AppNotifications from "./components/AppNotifications.vue";

</script>

<template>
  <div>
    <TheHeader />
    <router-view class="" />
    <AppNotifications />
  </div>
</template>
