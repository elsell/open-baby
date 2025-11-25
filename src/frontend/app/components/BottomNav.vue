<template>
  <div class="h-20 flex flex-row items-center justify-center gap-3 bg-white dark:bg-gray-900 border-t border-gray-200 dark:border-gray-800 shadow-[0_-1px_3px_rgba(0,0,0,0.05)]">
    <UButton v-for="page in pages" :key="page.slug" :to="page.slug" variant="ghost" :ui="{
      base: 'h-full aspect-square'
    }" :class="isActivePage(page.slug) ? 'text-blue-500 dark:text-blue-400' : 'text-gray-500 dark:text-gray-400'">
      <div class="flex flex-col items-center w-full">
        <UIcon :name="page.icon" class="text-2xl" />
        <span :class="isActivePage(page.slug) ? 'font-semibold' : 'font-normal'">{{ page.title }}</span>
      </div>
    </UButton>
    <ColorModeButton />
  </div>
</template>

<script lang="ts" setup>

const route = useRoute()

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
  },
  {
    slug: "/stats",
    title: "Stats",
    icon: "i-ph-chart-bar"
  }
]

const isActivePage = (slug: string) => {
  return route.path === slug
}

</script>

<style></style>