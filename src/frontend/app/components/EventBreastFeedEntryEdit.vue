<template>
  <UForm :schema="breastFeedSchema" :state="state" class="flex flex-col justify-between gap-10 h-full"
    @submit="onSubmit">
    <div class="h-full flex flex-col gap-5">

      <!-- Duration -->
      <div class="flex flex-col  gap-3">
        <div class="flex flex-row justify-between w-full">
          <label class="font-bold">Duration</label>
          <span class="opacity-80">{{ state.duration }} minutes</span>
        </div>

        <UFormField name="duration">
          <USlider v-model="state.duration" size="xl" :min="0" :max="60" />
        </UFormField>
      </div>

      <!-- Time -->
      <div class="flex flex-row gap-5">
        <UFormField name="date">
          <div class="flex flex-col gap-3">
            <label class="font-bold">Date</label>

            <UInput v-model="state.date" size="xl" type="date" />
          </div>
        </UFormField>
        <UFormField name="time">
          <div class="flex flex-col gap-3">
            <label class="font-bold">Time</label>

            <UInput v-model="state.time" size="xl" type="time" :default-value="state.time" />
          </div>
        </UFormField>
      </div>

      <!-- Side -->
      <UFormField name="side">

        <div class="flex flex-col gap-3">


          <label class="font-bold">Side</label>

          <URadioGroup v-model="state.side" size="xl" variant="card" :items="breastFeedSideItems"
            orientation="horizontal" indicator="hidden" :ui="{
              fieldset: 'flex flex-row items-center justify-between md:justify-start w-full',
              item: 'flex-grow'
            }">
            <template #label="{ item }">
              <div class="flex flex-row items-center gap-1">
                <UIcon v-if="item.icon" class="text-2xl" :name="item.icon" />
                <span>{{ item.label }}</span>
              </div>
            </template>
          </URadioGroup>

          <!-- Notes -->
          <UFormField name="notes">
            <div class="flex flex-col gap-3">
              <label class="font-bold">Notes</label>
              <UTextarea v-model="state.notes" placeholder="Add any additional notes here..." />
            </div>
          </UFormField>
        </div>
      </UFormField>
    </div>
    <UButton size="xl" block type="submit" :loading="isLoading">
      {{ isEdit ? 'Edit Breast Feed' : 'Log Breast Feed' }}
    </UButton>
    {{ state }}
  </UForm>
</template>

<script lang="ts" setup>
import type { IAPIBreastFeedEvent } from '~~/repository/modules/feed/types';
import * as v from 'valibot'
import type { RadioGroupItem } from '@nuxt/ui';
import { useEventForm } from '~/composables/useEventForm';
import { BreastFeedSide, toBreastFeedSide } from '~~/types/feed';

const emit = defineEmits<{
  submit: [],
  cancel: []
}>()

const props = withDefaults(defineProps<{
  event?: IAPIBreastFeedEvent
  isEdit?: boolean
}>(), {
  event: undefined
})

const { $api } = useNuxtApp()
const eventStore = useEventStore();

const breastFeedSchema = v.object({
  time: v.pipe(v.string()),
  date: v.pipe(v.string()),
  duration: (v.pipe(v.number())),
  side: v.pipe(v.enum(BreastFeedSide)),
  notes: v.nullish(v.pipe(v.string()))
})

type BreastFeedSchema = v.InferOutput<typeof breastFeedSchema>

const startingFeedData = props.event ? props.event : await eventStore.getDefaultBreastFeedEventData();

// The server only stores start/end times, not duration. So, we need
// to manually calculate the duration if there is an event passed
// in to us so that we can show it in the "edit" version of the component.
const breastFeedDurationInMinutes = startingFeedData.time_end ? (new Date(startingFeedData.time_end).getTime() - new Date(startingFeedData.time_start).getTime()) / 60000 : 0;

const initialState: BreastFeedSchema = {
  duration: breastFeedDurationInMinutes,
  side: toBreastFeedSide(startingFeedData.side),
  date: '', // Will be set by the composable
  time: '', // Will be set by the composable
  notes: props.isEdit ? startingFeedData.notes : undefined
};

const { state, onSubmit, isLoading } = useEventForm<typeof breastFeedSchema, IAPIBreastFeedEvent>({
  schema: breastFeedSchema,
  createEvent: (data) => $api.events.feed.createEventBreastFeed({
    ...data,
    name: 'feed_breast',
    side: data.side,
    // Here we need to convert from a duration to a time_end.
    time_end: state.duration ? new Date(new Date(data.time_start).getTime() + (state.duration * 60000)).toISOString() : undefined,
    description: '',
  }),
  updateEvent: (data) => $api.events.feed.updateEventBreastFeed({
    ...data,
    name: 'feed_breast',
    description: '',
    side: data.side,
    // Here we need to convert from a duration to a time_end.
    time_end: state.duration ? new Date(new Date(data.time_start).getTime() + (state.duration * 60000)).toISOString() : undefined,
  }),
  onSubmit: () => {
    emit('submit');
  },
  initialState,
  isEdit: props.isEdit,
  event: props.event,
});

const breastFeedSideItems = ref<RadioGroupItem[]>([
  {
    label: "Left",
    icon: "i-mdi-arrow-left",
    value: BreastFeedSide.Left,
  },
  {
    label: "Right",
    icon: "i-mdi-arrow-right",
    value: BreastFeedSide.Right,
  },
  {
    label: "Both",
    icon: "i-mdi-arrow-left-right",
    value: BreastFeedSide.Both,
  }
])

</script>

<style></style>