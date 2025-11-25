<template>
  <div class="flex flex-col gap-4">
    <DiaperStatsWidget :days="selectedWindow" />

    <!-- Events Section -->
    <div class="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-lg shadow-sm overflow-hidden">
      <!-- Section Header with Tabs -->
      <div class="px-4 py-3 border-b border-gray-200 dark:border-gray-800">
        <div class="flex flex-row items-center justify-between gap-3">
          <!-- Tab-style Date Selector -->
          <div class="flex flex-row gap-1">
            <button
              @click="selectedWindow = 7"
              :class="[
                'px-3 py-1.5 text-sm font-medium rounded-md transition-colors',
                selectedWindow === 7
                  ? 'bg-blue-500 text-white'
                  : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800'
              ]"
            >
              <span class="hidden sm:inline">Last 7 days</span>
              <span class="sm:hidden">7 days</span>
            </button>
            <button
              @click="selectedWindow = 30"
              :class="[
                'px-3 py-1.5 text-sm font-medium rounded-md transition-colors',
                selectedWindow === 30
                  ? 'bg-blue-500 text-white'
                  : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800'
              ]"
            >
              <span class="hidden sm:inline">Last 30 days</span>
              <span class="sm:hidden">30 days</span>
            </button>
            <button
              @click="selectedWindow = null"
              :class="[
                'px-3 py-1.5 text-sm font-medium rounded-md transition-colors',
                selectedWindow === null
                  ? 'bg-blue-500 text-white'
                  : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800'
              ]"
            >
              All time
            </button>
          </div>

          <!-- Event Count -->
          <div v-if="status !== 'pending' && data?.events" class="text-sm text-gray-500 dark:text-gray-400">
            <span v-if="data.events.length >= 10000" class="text-amber-600 dark:text-amber-500">
              Showing first 10,000 events
            </span>
            <span v-else>
              {{ data.events.length }} {{ data.events.length === 1 ? 'event' : 'events' }}
            </span>
          </div>
        </div>
      </div>

      <!-- Loading Skeleton -->
      <div v-if="status === 'pending'" class="p-8">
        <div class="animate-pulse space-y-4">
          <div class="h-12 bg-gray-200 dark:bg-gray-800 rounded"></div>
          <div class="h-12 bg-gray-200 dark:bg-gray-800 rounded"></div>
          <div class="h-12 bg-gray-200 dark:bg-gray-800 rounded"></div>
          <div class="h-12 bg-gray-200 dark:bg-gray-800 rounded"></div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else-if="!data?.events || data.events.length === 0" class="flex flex-col items-center justify-center py-16 px-4">
        <UIcon name="i-lucide-calendar-off" class="text-6xl text-gray-300 dark:text-gray-700 mb-4" />
        <h3 class="text-lg font-semibold text-gray-700 dark:text-gray-300 mb-2">No Events Found</h3>
        <p class="text-sm text-gray-500 dark:text-gray-400 text-center">
          <span v-if="selectedWindow">No events logged in the last {{ selectedWindow }} days.</span>
          <span v-else>No events have been logged yet.</span>
        </p>
      </div>

      <!-- Events Table -->
      <UTable v-else :column-visibility="{ id: false, metadata: false, time_end: false }" :data="data?.events" :columns="columns"
        @select="onSelect" :loading="status === 'pending'" class="transition-opacity duration-200"
        :class="{ 'opacity-50': status === 'pending' }" />
    </div>

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
const { $api } = useNuxtApp()

const UButton = resolveComponent('UButton')
const UDropdownMenu = resolveComponent('UDropdownMenu')

const eventStore = useEventStore()

// Date range selector state
const selectedWindow = ref<number | null>(30)

// Calculate date range based on selected window
const getDateRange = () => {
  if (selectedWindow.value === null) {
    return { start_time: undefined, end_time: undefined }
  }
  const endTime = new Date()
  const startTime = new Date()
  startTime.setDate(startTime.getDate() - selectedWindow.value)
  return { start_time: startTime.toISOString(), end_time: endTime.toISOString() }
}

const { data, status, refresh } = await useAsyncData(
  'event-list',
  async () => {
    const { start_time, end_time } = getDateRange()
    return await $api.events.events.listEvents(10000, 0, start_time, end_time)
  },
  {
    watch: [selectedWindow]
  }
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
  else if (eventType === 'pump') {
    const pumpEvent = await $api.events.pump.getEventPump(eventId)
    eventStore.selectedPumpEventToEdit = pumpEvent
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
      else if (eventType === 'pump') {
        displayName = 'Pump'

        const timeStart = row.getValue("time_start") as string
        const timeEnd = row.getValue("time_end") as string | undefined

        const durationMins =  ( (timeEnd ? (new Date(timeEnd).getTime()): (new Date().getTime())) - new Date(timeStart).getTime()) / 60000

        // Add icon
        const icon = 'i-healthicons-breast-pump'

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