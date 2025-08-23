<template>
  <UApp>
    <NuxtLoadingIndicator />
    <NuxtLayout>
      <div class="flex flex-col h-full">
        <div class="overflow-auto flex-grow">
          <NuxtPage />
        </div>
        <BottomNav />
      </div>
    </NuxtLayout>
  </UApp>
</template>

<script setup lang="ts">

</script>

<style>
#__nuxt,
html,
body {
  @apply h-full;
}
</style>