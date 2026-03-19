<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex justify-center items-center p-6">
    <slot></slot>
  </div>
</template>

<script setup lang="ts">
const colorMode = useColorMode()
colorMode.preference = 'light'
</script>

<style scoped></style>