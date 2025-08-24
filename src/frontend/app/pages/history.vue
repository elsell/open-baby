<template>
  <div class="flex flex-col gap-1">
    <UTable :column-visibility="{ id: false }" :data="data?.events" :columns="columns" :loading="status === 'pending'"
      class="flex-1" />

    <span v-for="event in events.events" :key="event.id" class="flex flex-row gap-2 w-full justify-between">
      {{ event.name }}
      <NuxtTime :datetime="event.time_start" relative />
      (
      <NuxtTime :datetime="event.time_start" hour="2-digit" minute="2-digit" weekday="short" />)
      <UButton icon="i-ph-trash" color="error" @click="deleteEvent(event.id)" />
    </span>

    <ConfirmDialog :open="showDialog" title="Delete Event" description="This action cannot be undone."
      confirm-text="Delete" cancel-text="Cancel" confirm-color="error" confirm-variant="solid"
      @confirm="deleteEvent(eventIdToDelete, true)" @cancel="handleCancelDelete" :confirm-loading="confirmLoading">
      Are you sure you want to delete this event?
    </ConfirmDialog>

  </div>
</template>

<script lang="ts" setup>
import type { IAPIEvent } from '~~/repository/modules/events/types';
import { ConfirmDialog } from '#components';
import type { TableColumn } from '@nuxt/ui'
import type { Row } from '@tanstack/vue-table'
const { $api } = useNuxtApp()

const events = await $api.events.events.listEvents(10000)
const UButton = resolveComponent('UButton')
const UDropdownMenu = resolveComponent('UDropdownMenu')


const { data, status, error, refresh, clear } = await useAsyncData(
  'event-list',
  async () => await $api.events.events.listEvents(10000)
)

function getRowItems(row: Row<IAPIEvent>) {
  return [
    {
      type: 'label',
      label: 'Actions'
    },
    {
      label: 'Edit',
      onSelect() {
        // TODO
      }
    },
    {
      type: 'separator'
    },
    {
      label: 'Delete',
      onSelect() {
        deleteEvent(row.getValue("id"))
      }
    },

  ]
}

const columns: TableColumn<IAPIEvent>[] = [
  {
    accessorKey: 'id',
    header: 'Id',
    enableHiding: true
  },
  {
    accessorKey: 'name',
    header: 'Event Type'
  },
  {
    accessorKey: 'time_start',
    header: 'Time'
  },
  {
    id: 'actions',
    cell: ({ row }) => {
      return h(
        'div',
        { class: 'text-right' },
        h(
          UDropdownMenu,
          {
            content: {
              align: 'end'
            },
            items: getRowItems(row),
            'aria-label': 'Actions dropdown'
          },
          () =>
            h(UButton, {
              icon: 'i-lucide-ellipsis-vertical',
              color: 'neutral',
              variant: 'ghost',
              class: 'ml-auto',
              'aria-label': 'Actions dropdown'
            })
        )
      )
    }
  }
]


const eventIdToDelete: Ref<undefined | string> = ref()

const confirmLoading = ref(false)

const toast = useToast()

const showDialog = ref(false)


async function deleteEvent(eventId?: string, confirm: boolean = false) {
  if (!eventId) return

  if (!confirm) {
    eventIdToDelete.value = eventId
    showDialog.value = true
    return
  }

  try {
    confirmLoading.value = true
    await $api.events.events.deleteEvent(eventId)
    toast.add({
      title: "Event Deleted",
      color: "success"
    })
  } finally {
    confirmLoading.value = false
    showDialog.value = false
  }

}

function handleCancelDelete() {
  showDialog.value = false
  eventIdToDelete.value = undefined
}

</script>

<style></style>