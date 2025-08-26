<template>
  <div class="h-full">
    <UApp :toaster="toaster">
      <NuxtLoadingIndicator />
      <NuxtLayout>
        <div class="flex flex-col h-full" data-vaul-drawer-wrapper>
          <div class="overflow-auto flex-grow">
            <NuxtPage />
          </div>
          <BottomNav />
        </div>
      </NuxtLayout>
    </UApp>
  </div>
</template>

<script setup lang="ts">
import type { ToasterProps } from '@nuxt/ui';

const toaster: ToasterProps = { position: 'top-center', duration: 2000 };
</script>

<style>
#__nuxt,
html,
body {
  @apply h-full;
}
</style>