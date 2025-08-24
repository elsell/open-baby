<template>
  <div data-vaul-drawer-wrapper class="h-full">
    <UDrawer v-model:open="showEventEntryDrawer" should-scale-background set-background-color-on-scale handle-only
      @close="eventStore.selectedEventToEdit = undefined">
      <template #content>
        <div class="min-h-[50vh] relative flex flex-col p-5">
          <EventFeedEntryEdit v-if="eventStore.selectedEventToEdit === 'feed_bottle'" :is-edit="isEdit"
            :feed-event="eventStore.selectedBottleFeedEventToEdit" class="flex-grow" @cancel="eventStore.clearEditState"
            @submit="onSubmit" />
        </div>
      </template>
    </UDrawer>
  </div>
</template>

<script lang="ts" setup>
defineProps<{
  isEdit?: boolean
}>()

const emit = defineEmits<{
  submit: []
}>()

const eventStore = useEventStore()

const showEventEntryDrawer: Ref<boolean> = ref(false)

watch(() => eventStore.selectedEventToEdit, (newVal) => {
  if (newVal !== undefined) showEventEntryDrawer.value = true
  else showEventEntryDrawer.value = false
})

function onSubmit() {
  showEventEntryDrawer.value = false
  emit('submit')
}

</script>

<style></style>