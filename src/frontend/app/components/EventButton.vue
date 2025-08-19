<template>
  <UButton class="h-full w-full cursor-pointer" style="text-transform: capitalize;" @click="$emit('click')">
      <div class="w-full h-full flex flex-col items-center justify-center gap-3 text-5xl">
        <UIcon class="text-9xl" :name="icon"/>
        <span class="opacity-80">{{ name }}</span>
      </div>
  </UButton>
</template>

<script lang="ts" setup>
defineProps<{
  name: string,
  icon: string
}>()

defineEmits<{
  click: []
}>()
</script>

<style></style>