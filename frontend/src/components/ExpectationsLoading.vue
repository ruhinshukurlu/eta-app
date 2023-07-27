<template>
  <div class="flex w-full flex-col space-y-4">
    <div v-for="i in 8" :key="i" class="grid animate-pulse grid-cols-5 gap-5">
      <div class="h-8 w-full rounded-md bg-gray-300" />
      <div class="h-8 w-full rounded-md bg-gray-300" />
      <div class="h-8 w-full rounded-md bg-gray-300" />
      <div class="h-8 w-full rounded-md bg-gray-300" />
      <div class="h-8 w-full rounded-md bg-gray-300" />
    </div>
  </div>
</template>
