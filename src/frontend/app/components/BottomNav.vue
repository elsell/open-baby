<template>
  <div class="h-20 flex flex-row items-center justify-center gap-3">
    <UButton v-for="page in pages" :key="page.slug" :to="page.slug" variant="ghost" :ui="{
      base: 'h-full aspect-square'
    }">
      <div class="flex flex-col items-center w-full">
        <UIcon :name="page.icon" class="text-2xl" />
        <span>{{ page.title }}</span>
      </div>
    </UButton>
    <ColorModeButton />
  </div>
</template>

<script lang="ts" setup>

const pages = [
  {
    slug: "/",
    title: "Log",
    icon: "i-ph-note"
  },
  {
    slug: "/history",
    title: "History",
    icon: "i-ph-clock-counter-clockwise"
  }
]

</script>

<style></style>