<template>
  <div>
    <header>
      <nav class="flex items-center justify-between p-6 lg:px-8" aria-label="Global">
        <div class="flex lg:flex-1">
          <router-link to="/" class="-m-1.5 p-1.5">
            <span class="font-bold text-blue-500">ETA SYSTEM</span>
          </router-link>
        </div>
        <div class="hidden lg:flex lg:gap-x-12">
          <router-link to="/active-etas" class="text-sm font-semibold leading-6 text-gray-900">
            Active ETAs
          </router-link>
          <router-link to="/" class="text-sm font-semibold leading-6 text-gray-900">
            Create ETA
          </router-link>
        </div>
        <div v-if="!username" class="flex flex-1 justify-end space-x-2">
          <router-link to="/login" class="rounded-md bg-gray-200 px-4 py-2 text-sm font-semibold leading-6 text-gray-900 hover:bg-gray-300">Sign in</router-link>
          <router-link to="/register" class="rounded-md bg-gray-200 px-4 py-2 text-sm font-semibold leading-6 text-gray-900 hover:bg-gray-300">Register</router-link>
        </div>
        <div v-else class="flex flex-1 items-center justify-end space-x-2">
          <span>{{ username }}</span>
          <button class="rounded-md bg-gray-200 px-4 py-2 text-sm font-semibold leading-6 text-gray-900 hover:bg-gray-300" @click="logOut">
            Log Out
          </button>
        </div>
      </nav>
    </header>
  </div>
</template>
<script setup>
import {ref, watch} from "vue";
import {useRoute} from "vue-router";
import router from "../router/index";

const route = useRoute();
const username = ref(localStorage.getItem("username"));

watch(route, () => username.value = localStorage.getItem("username")); // check user logged in state when route changes

const logOut = () => {
  // remove token and username from localstorage
  localStorage.removeItem("token");
  localStorage.removeItem("username");
  username.value = null;
  router.push("/login");
};
</script>
