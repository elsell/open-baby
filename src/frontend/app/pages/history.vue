<template>
  <div class="flex flex-col gap-1">
    <UTable :column-visibility="{ id: false, metadata: false, time_end: false }" :data="data?.events" :columns="columns"
      @select="onSelect" :loading="status === 'pending'" class="flex-1" />

    <ConfirmDialog :open="showDialog" title="Delete Event" description="This action cannot be undone."
      confirm-text="Delete" cancel-text="Cancel" confirm-color="error" confirm-variant="solid"
      @confirm="deleteEvent(eventIdToDelete, true)" @cancel="handleCancelDelete" :confirm-loading="confirmLoading">
      Are you sure you want to delete this event?
    </ConfirmDialog>

    <EventEditDrawer :is-edit="true" @submit="refresh" />
  </div>
</template>

<script lang="ts" setup>
import type { IAPIEvent, IAPIEventType } from '~~/repository/modules/events/types';
import { ConfirmDialog, NuxtTime, UIcon } from '#components';
import type { TableColumn, TableRow } from '@nuxt/ui'
import type { Row } from '@tanstack/vue-table'
import type { IAPIBreastFeedEvent } from '~~/repository/modules/feed/types';
const { $api } = useNuxtApp()

const UButton = resolveComponent('UButton')
const UDropdownMenu = resolveComponent('UDropdownMenu')

const eventStore = useEventStore()

const { data, status, refresh } = await useAsyncData(
  'event-list',
  async () => await $api.events.events.listEvents(10000)
)
async function onSelect(row: TableRow<IAPIEvent>, e?: Event) {
  const eventType: IAPIEventType = row.getValue('name')
  const eventId: string = row.getValue('id')

  eventStore.clearEditState()

  // Preload event data for editing
  if (eventType === 'feed_bottle') {
    const bottleFeedEvent = await $api.events.feed.getEventBottleFeed(eventId)
    eventStore.selectedBottleFeedEventToEdit = bottleFeedEvent
  }
  else if (eventType === 'diaper_change') {
    const diaperChangeEvent = await $api.events.diaper.getEventDiaper(eventId)
    eventStore.selectedDiaperChangeEventToEdit = diaperChangeEvent
  }
  else if (eventType === 'feed_breast') {
    const breastFeedEvent = await $api.events.feed.getEventBreastFeed(eventId)
    eventStore.selectedBreastFeedEventToEdit = breastFeedEvent
  }
  else {
    throw new Error("Unknown event type. Ensure you're implementing it in history.vue");
  }

  // Open the drawer
  eventStore.selectedEventToEdit = eventType
}


function getRowItems(row: Row<IAPIEvent>) {
  return [
    {
      type: 'label',
      label: 'Actions'
    },
    {
      label: 'Edit',
      async onSelect() {
        onSelect(row)
      }
    },
    {
      type: 'separator'
    },
    {
      label: 'Delete',
      async onSelect() {
        await deleteEvent(row.getValue("id"))
        await refresh()
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
    accessorKey: 'metadata',
    header: 'metadata',
    enableHiding: true
  },
  {
    accessorKey: 'name',
    header: 'Event Type',
    cell: ({ row }) => {
      const eventType: IAPIEventType = row.getValue('name')
      let displayName = eventType.replace(/_/g, ' ')
      displayName = displayName.charAt(0).toUpperCase() + displayName.slice(1)

      if (eventType === 'feed_bottle') {
        displayName = 'Bottle Feed'
        const metadata = row.getValue('metadata') as Record<string, string | number | boolean>

        // Add icon
        const icon = 'i-mdi-baby-bottle-outline'


        return h('div', { style: "display: flex; flex-direction: row; align-items: center; flex-gap: 8px;" }, [
          h(UIcon, { name: icon, class: 'text-2xl mr-2' }),
          h('div', [
            h('span', { style: 'text-transform: capitalize;' }, displayName),
            h('br'),
            h('span', { class: 'opacity-50 text-sm' }, `${metadata.amount_ml ?? 'N/A'}ml ${metadata.is_formula ? 'Formula' : 'Breast Milk'}`)
          ])
        ])
      }
      else if (eventType === 'diaper_change') {
        const metadata = row.getValue('metadata') as Record<string, string | number | boolean>
        let contents = ''
        if (metadata.diaper_contents_size) contents += `${metadata.diaper_contents_size} `
        if (metadata.diaper_contents_color) contents += `${metadata.diaper_contents_color} `
        if (metadata.diaper_contents_consistency) contents += `${metadata.diaper_contents_consistency} `
        if (contents === '') contents = 'No contents logged'

        const icon = "i-mdi-diaper-outline"

        return h('div', { style: "display: flex; flex-direction: row; align-items: center; flex-gap: 8px;" }, [
          h(UIcon, { name: icon, class: 'text-2xl mr-2' }),
          h('div', [
            h('span', { style: 'text-transform: capitalize;' }, displayName),
            h('br'),
            h('span', { class: 'opacity-50 text-sm text-transform: capitalize' }, contents)
          ])
        ])
      }
      else if (eventType === 'feed_breast') {
        displayName = 'Breast Feed'

        const timeStart = row.getValue("time_start") as string
        const timeEnd = row.getValue("time_end") as string | undefined

        const durationMins =  ( (timeEnd ? (new Date(timeEnd).getTime()): (new Date().getTime())) - new Date(timeStart).getTime()) / 60000

        // Add icon
        const icon = 'i-mdi-mother-nurse'

        return h('div', { style: "display: flex; flex-direction: row; align-items: center; flex-gap: 8px;" }, [
          h(UIcon, { name: icon, class: 'text-2xl mr-2' }),
          h('div', [
            h('span', { style: 'text-transform: capitalize;' }, displayName),
            h('br'),
            h('span', { class: 'opacity-50 text-sm' }, `${durationMins} mins`)
          ])
        ])
      }

      return h('span', { style: 'text-transform: capitalize;' }, displayName)
    }
  },
  {
    accessorKey: 'time_start',
    header: 'Time',
    cell: ({ row }) => {
      return h('div', [
        h(NuxtTime, {
          datetime: row.getValue('time_start'),
          relative: true
        }),
        h('br'),
        h(NuxtTime, {
          datetime: row.getValue('time_start'),
          hour: '2-digit',
          minute: '2-digit',
          day: 'numeric',
          month: 'short',
          weekday: 'short',
          class: 'opacity-50 text-sm'

        }),
      ])
    }
  },
  {
    accessorKey: "time_end",
    enableHiding: true
  },
  {
    id: 'actions',
    accessorKey: 'actions',
    header: "",
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
    await refresh()
    eventIdToDelete.value = undefined
  }

}

function handleCancelDelete() {
  showDialog.value = false
  eventIdToDelete.value = undefined
}

</script>

<style></style>